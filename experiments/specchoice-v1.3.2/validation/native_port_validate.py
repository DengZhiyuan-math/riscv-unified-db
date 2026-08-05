# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Independent, fail-closed validation for Darwin source-port outputs."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import stat
import struct
import subprocess
import sys
from pathlib import Path
from typing import Any

SANDBOX_EXEC = Path("/usr/bin/sandbox-exec")
SECTIONS = (("__TEXT", "__text"), ("__TEXT", "__stubs"))
ROOT_PREDECESSOR_SHA256 = "7f6d0761ccdb775ddb62e13ca641dd389819e587acaf29ca4f805f0ab502a1fd"
ROOT_PREDECESSOR_STATE = "failed_closed"
ROOT_PREDECESSOR_DIAGNOSTIC = "ORACLE_EXECUTION_NOT_IMPLEMENTED"


class ValidationError(ValueError):
    """A validation boundary was violated."""


def native_network_deny_profile() -> str:
    return "(version 1)\n(allow default)\n(deny network*)\n"


def native_oracle_profile() -> str:
    cache_roots = (Path.home() / ".cache", Path.home() / "Library" / "Caches")
    lines = native_network_deny_profile().splitlines()
    lines.extend(f"(deny file-write* (subpath \"{path}\"))" for path in cache_roots)
    return "\n".join(lines) + "\n"


def _canonical(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _load_object(path: Path, *, diagnostic: str) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ValidationError(diagnostic)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(diagnostic) from error
    if not isinstance(value, dict):
        raise ValidationError(diagnostic)
    return value


def read_root_predecessor(path: Path) -> tuple[dict[str, Any], str]:
    """Read the immutable failed-closed root without changing it."""
    if path.is_absolute():
        raise ValidationError("PREDECESSOR_PATH_NOT_RELATIVE")
    digest = _sha256(path)
    if digest != ROOT_PREDECESSOR_SHA256:
        raise ValidationError("PREDECESSOR_DIGEST_MISMATCH")
    payload = _load_object(path, diagnostic="PREDECESSOR_PARSE_FAILED")
    if (
        payload.get("state") != ROOT_PREDECESSOR_STATE
        or payload.get("diagnostic") != ROOT_PREDECESSOR_DIAGNOSTIC
    ):
        raise ValidationError("PREDECESSOR_STATE_MISMATCH")
    return payload, digest


def read_original_diagnostic(path: Path) -> str:
    """Admit only the immutable original whole-binary mismatch custody."""
    if path.is_absolute():
        raise ValidationError("ORIGINAL_DIAGNOSTIC_PATH_NOT_RELATIVE")
    payload = _load_object(path, diagnostic="ORIGINAL_DIAGNOSTIC_INVALID")
    left, right, cmp_l = payload.get("left"), payload.get("right"), payload.get("cmp_l")
    if not isinstance(left, dict) or not isinstance(right, dict) or not isinstance(cmp_l, dict):
        raise ValidationError("ORIGINAL_DIAGNOSTIC_INVALID")
    expected = (
        payload.get("diagnostic_id") == "FWD-05-08-PORT-20260805-original-whole-binary-mismatch"
        and payload.get("status") == "immutable_failed_diagnostic"
        and left.get("length") == 297208
        and right.get("length") == 297208
        and left.get("sha256") == "545a788e0e6dde0dc268d0575649a1335e9c67cd881df584d149cdbb567996c3"
        and right.get("sha256") == "6ee19c6136897c3b9ea8403d89339946eb3fec5cb563e27e67654078affd1485"
        and cmp_l.get("difference_count") == 544
        and cmp_l.get("stdout_sha256") == "2f236895ef71c74cd9194eecb140abf7b1fb915c0a19ac8aff6b5d329d564726"
    )
    if not expected:
        raise ValidationError("ORIGINAL_DIAGNOSTIC_MISMATCH")
    return _sha256(path)


def load_oracle(path: Path, *, generate: bool = False) -> dict[str, Any]:
    if generate:
        raise ValidationError("ORACLE_GENERATION_FORBIDDEN")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError("ORACLE_PARSE_FAILED") from error
    if not isinstance(payload, dict) or not isinstance(payload.get("cases"), list):
        raise ValidationError("ORACLE_INVALID")
    return payload


def create_record(path: Path, payload: dict[str, Any]) -> None:
    if path.exists() or path.is_symlink():
        raise ValidationError("RECORD_EXISTS")
    if payload.get("state") not in {"tracer_validated", "all_tools_validated_cache_unpublished", "validation_complete", "failed_closed"}:
        raise ValidationError("RECORD_STATE_INVALID")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        try:
            file_descriptor = os.open(path.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=descriptor)
        except FileExistsError as error:
            raise ValidationError("RECORD_EXISTS") from error
        with os.fdopen(file_descriptor, "wb") as handle:
            handle.write(_canonical(payload))
    finally:
        os.close(descriptor)


def fail_closed_record(path: Path, *, expected_sha256: str, stage: str, diagnostic: str) -> None:
    """Advance only the exact current non-authoritative handoff to failed custody."""
    original = path.read_bytes()
    if _sha256_bytes(original) != expected_sha256:
        raise ValidationError("RECORD_DIGEST_MISMATCH")
    try:
        prior = json.loads(original)
    except json.JSONDecodeError as error:
        raise ValidationError("RECORD_PARSE_FAILED") from error
    if not isinstance(prior, dict) or prior.get("state") not in {"tracer_validated", "all_tools_validated_cache_unpublished"}:
        raise ValidationError("RECORD_TRANSITION_INVALID")
    payload = {
        "completion_authorized": False,
        "diagnostic": diagnostic,
        "failed_stage": stage,
        "non_authoritative": True,
        "prior_record": prior,
        "prior_record_sha256": expected_sha256,
        "state": "failed_closed",
    }
    temporary = path.with_name(f".{path.name}.{expected_sha256[:12]}.failed")
    if temporary.exists():
        raise ValidationError("RECORD_TEMP_EXISTS")
    with open(temporary, "xb") as handle:
        handle.write(_canonical(payload))
        handle.flush()
        os.fsync(handle.fileno())
    if _sha256(path) != expected_sha256:
        temporary.unlink()
        raise ValidationError("RECORD_DIGEST_MISMATCH")
    os.replace(temporary, path)


def publish_cache(staged: dict[str, Path], cache_root: Path, *, mode: str, transaction_id: str) -> None:
    if mode == "deny":
        raise ValidationError("CACHE_WRITE_DENIED")
    if mode != "publish-no-replace" or not transaction_id:
        raise ValidationError("CACHE_MODE_INVALID")
    if not staged:
        raise ValidationError("CACHE_STAGED_EMPTY")
    cache_root.mkdir(parents=True, exist_ok=True)
    for name, source in staged.items():
        if not source.is_file() or source.is_symlink():
            raise ValidationError("CACHE_SOURCE_UNSAFE")
        target = cache_root / name
        if target.exists() or target.is_symlink():
            raise ValidationError("CACHE_COLLISION")
        os.link(source, target)


def _read_sections(path: Path) -> dict[tuple[str, str], tuple[int, int, int, bytes]]:
    raw = path.read_bytes()
    if len(raw) < 32 or raw[:4] != b"\xcf\xfa\xed\xfe":
        raise ValidationError("MACHO_REQUIRED")
    _, _, _, _, command_count, _, _, _ = struct.unpack_from("<IiiIIIII", raw, 0)
    cursor = 32
    found: dict[tuple[str, str], tuple[int, int, int, bytes]] = {}
    for _ in range(command_count):
        command, size = struct.unpack_from("<II", raw, cursor)
        if size < 8 or cursor + size > len(raw):
            raise ValidationError("MACHO_LOAD_COMMAND_INVALID")
        if command == 0x19:
            _, _, _, _, _, _, _, _, _, section_count, _ = struct.unpack_from("<II16sQQQQiiII", raw, cursor)
            section_cursor = cursor + 72
            for section_number in range(section_count):
                base = section_cursor + section_number * 80
                section_name, section_segment, _, length, offset, _, _, _, flags, _, _, _ = struct.unpack_from("<16s16sQQIIIIIIII", raw, base)
                key = (section_segment.split(b"\0", 1)[0].decode("ascii"), section_name.split(b"\0", 1)[0].decode("ascii"))
                if key in SECTIONS:
                    if key in found or offset + length > len(raw):
                        raise ValidationError("SECTION_LAYOUT_INVALID")
                    found[key] = (offset, length, flags, raw[offset : offset + length])
        cursor += size
    if tuple(found) != SECTIONS:
        raise ValidationError("SECTION_ORDER_OR_SET_INVALID")
    return found


def compare_executables(left: Path, right: Path) -> dict[str, Any]:
    for candidate in (left, right):
        mode = candidate.lstat().st_mode
        if not stat.S_ISREG(mode) or candidate.is_symlink():
            raise ValidationError("EXECUTABLE_NOT_REGULAR")
        result = subprocess.run(["/usr/bin/lipo", "-archs", str(candidate)], capture_output=True, check=False)
        if result.returncode or result.stdout.strip() != b"arm64":
            raise ValidationError("EXECUTABLE_NOT_ARM64")
    left_raw, right_raw = left.read_bytes(), right.read_bytes()
    if len(left_raw) != len(right_raw):
        raise ValidationError("EXECUTABLE_LENGTH_MISMATCH")
    left_sections, right_sections = _read_sections(left), _read_sections(right)
    projection: list[dict[str, Any]] = []
    for key in SECTIONS:
        lhs, rhs = left_sections[key], right_sections[key]
        if lhs[:3] != rhs[:3] or lhs[3] != rhs[3]:
            raise ValidationError("SECTION_PROJECTION_MISMATCH")
        projection.append({"segment": key[0], "section": key[1], "offset": lhs[0], "length": lhs[1], "flags": lhs[2], "sha256": _sha256_bytes(lhs[3])})
    differences = [{"offset": index, "left": left_raw[index], "right": right_raw[index]} for index in range(len(left_raw)) if left_raw[index] != right_raw[index]]
    return {"length": len(left_raw), "left_sha256": _sha256(left), "right_sha256": _sha256(right), "differences": differences, "sections": projection, "projection_sha256": _sha256_bytes(_canonical(projection))}


def _oracle_bytes(case: dict[str, Any], field: str) -> bytes:
    value = case.get(field, "")
    if not isinstance(value, str):
        raise ValidationError("ORACLE_FIELD_INVALID")
    try:
        return base64.b64decode(value, validate=True)
    except ValueError as error:
        raise ValidationError("ORACLE_ENCODING_INVALID") from error


def validate_oracles(
    operational_root: Path,
    oracle: dict[str, Any],
    tools: list[str],
    *,
    repetitions: int,
    runner: Any = subprocess.run,
) -> list[dict[str, Any]]:
    """Execute the committed fixture exactly twice through the fixed native guard."""
    if repetitions != 2 or not SANDBOX_EXEC.is_absolute() or str(SANDBOX_EXEC) != "/usr/bin/sandbox-exec":
        raise ValidationError("NATIVE_GUARD_REQUIRED")
    results: list[dict[str, Any]] = []
    for tool in tools:
        cases = [case for case in oracle["cases"] if isinstance(case, dict) and case.get("tool") == tool]
        if len(cases) < 2:
            raise ValidationError("ORACLE_CASES_INCOMPLETE")
        for build in (0, 1):
            candidate = operational_root / "staged" / f"{tool}-{build}"
            if not candidate.is_file() or candidate.is_symlink():
                raise ValidationError("ORACLE_CANDIDATE_INVALID")
            for repetition in range(repetitions):
                for case in cases:
                    argv = case.get("argv")
                    if not isinstance(argv, list) or not argv or not all(isinstance(item, str) for item in argv):
                        raise ValidationError("ORACLE_ARGV_INVALID")
                    if "__OUTPUT__" in argv:
                        raise ValidationError("ORACLE_OUTPUT_WRITE_FORBIDDEN")
                    result = runner(
                        [str(SANDBOX_EXEC), "-p", native_oracle_profile(), str(candidate), *argv],
                        input=_oracle_bytes(case, "stdin_base64"),
                        capture_output=True,
                        check=False,
                    )
                    if (
                        result.returncode != case.get("returncode")
                        or result.stdout != _oracle_bytes(case, "stdout_base64")
                        or result.stderr != _oracle_bytes(case, "stderr_base64")
                    ):
                        raise ValidationError("ORACLE_OUTPUT_MISMATCH")
                    results.append({"tool": tool, "build": build, "repetition": repetition, "argv": argv})
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--contract", type=Path, required=True)
    validate.add_argument("--oracle", type=Path, required=True)
    validate.add_argument("--operational-root", type=Path, required=True)
    validate.add_argument("--tools", nargs="+", required=True)
    validate.add_argument("--record", type=Path, required=True)
    validate.add_argument("--predecessor-record", type=Path)
    validate.add_argument("--record-mode")
    validate.add_argument("--create-stage")
    validate.add_argument("--advance-stage")
    validate.add_argument("--oracle-repetitions", type=int, required=True)
    validate.add_argument("--reproducibility-predicate", required=True)
    validate.add_argument("--full-binary-differences", required=True)
    validate.add_argument("--require-native-network-denial", action="store_true")
    validate.add_argument("--cache-mode", required=True)
    validate.add_argument("--original-diagnostic", type=Path)
    failed = subparsers.add_parser("fail-closed")
    failed.add_argument("--record", type=Path, required=True)
    failed.add_argument("--expected-sha256", required=True)
    failed.add_argument("--stage", required=True)
    failed.add_argument("--diagnostic", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "fail-closed":
            fail_closed_record(
                args.record,
                expected_sha256=args.expected_sha256,
                stage=args.stage,
                diagnostic=args.diagnostic,
            )
            return 0
        oracle = load_oracle(args.oracle)
        if (
            args.oracle_repetitions != 2
            or args.cache_mode != "deny"
            or not args.require_native_network_denial
            or args.reproducibility_predicate != "named-executable-sections-and-oracle"
            or args.full_binary_differences != "record-all"
            or args.record_mode != "create-only"
            or args.tools != ["espresso"]
            or args.create_stage != "tracer_validated"
            or args.advance_stage is not None
            or args.predecessor_record is None
            or args.original_diagnostic is None
        ):
            raise ValidationError("VALIDATION_ARGUMENTS_INVALID")
        _, predecessor_digest = read_root_predecessor(args.predecessor_record)
        original_diagnostic_digest = read_original_diagnostic(args.original_diagnostic)
        if args.record.exists() or args.record.is_symlink():
            raise ValidationError("RECORD_EXISTS")
        outputs = {name: compare_executables(args.operational_root / "staged" / f"{name}-0", args.operational_root / "staged" / f"{name}-1") for name in args.tools}
        oracle_results = validate_oracles(args.operational_root, oracle, args.tools, repetitions=args.oracle_repetitions)
        state = args.create_stage or args.advance_stage
        if state is None:
            raise ValidationError("RECORD_STAGE_REQUIRED")
        if _sha256(args.predecessor_record) != predecessor_digest:
            raise ValidationError("PREDECESSOR_DRIFT")
        payload = {
            "all_tools_admitted": False,
            "cache_publication": "not_run",
            "completion_authorized": False,
            "executables": outputs,
            "formal_execution": "not_run",
            "non_authoritative": True,
            "oracle_runs": oracle_results,
            "oracle_sha256": _sha256(args.oracle),
            "original_diagnostic_path": args.original_diagnostic.as_posix(),
            "original_diagnostic_sha256": original_diagnostic_digest,
            "predecessor_diagnostic": ROOT_PREDECESSOR_DIAGNOSTIC,
            "predecessor_record_path": args.predecessor_record.as_posix(),
            "predecessor_record_sha256": predecessor_digest,
            "predecessor_state": ROOT_PREDECESSOR_STATE,
            "regression": "not_run",
            "state": state,
        }
        create_record(args.record, payload)
        if _sha256(args.predecessor_record) != predecessor_digest:
            raise ValidationError("PREDECESSOR_DRIFT")
    except ValidationError as error:
        print(str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

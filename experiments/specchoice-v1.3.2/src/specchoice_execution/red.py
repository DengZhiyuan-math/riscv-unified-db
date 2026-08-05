# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Descriptor-bound, Red-only no-call evidence construction."""

from __future__ import annotations

import ast
import base64
import contextlib
import socket
from collections.abc import Callable, Iterator, Mapping
from pathlib import Path
from unittest.mock import patch

from specchoice_evidence.canonical import canonical_json_bytes, sha256_bytes
from specchoice_evidence.filesystem import (
    FilesystemPolicyError,
    enumerate_authoritative_files,
    read_authoritative_file,
    require_relative_posix_path,
    write_exact_descriptor_files,
)
from specchoice_evidence.runtime_closure import (
    build_runtime_closure,
    verify_runtime_closure,
)
from specchoice_measurement.diagnostics import ordered_diagnostics
from specchoice_measurement.strict_json import decode_strict_json
from specchoice_treatments.h3 import (
    H3ValidationError,
    build_h3_red_readiness_v6,
    build_h3_red_review_packet_v6,
    load_phase4_freeze_inputs_v6,
    validate_h3_red_authority_v6,
)


class RedExecutionError(ValueError):
    """Stable fail-closed error for the Phase 5 Red-only contract."""

    def __init__(self, code: str, *, failed_attempt: dict[str, object] | None = None) -> None:
        super().__init__(code)
        self.failed_attempt = failed_attempt


_POLICY_PATH = "config/execution/red-execution-policy-v1.json"
_AUTHORITY_PATHS = (
    "phase4/branch-authority-v6.json",
    "reports/h3/h3-red-review-v6/review-packet.json",
    "receipts/h3-branch-readiness-v6.json",
    "reviews/h3-branch-decision-v6.json",
)
_RAW_EVIDENCE_PATHS = ("phase3/data-authority-v1.json", *_AUTHORITY_PATHS)
_RESULT_PATH = "runs/red-execution-v1/manifest.json"
_OUTPUT_PATHS = (
    "runs/red-execution-v1/attempt-chain.json",
    "runs/red-execution-v1/evidence-span-audit.json",
    _RESULT_PATH,
    "runs/red-execution-v1/model-call-ledger.json",
    "runs/red-execution-v1/ordered-diagnostics.json",
    "runs/red-execution-v1/parsed-evidence.json",
    "runs/red-execution-v1/raw-evidence.json",
    "runs/red-execution-v1/runtime-audit.json",
    "runs/red-execution-v1/structural-audit.json",
    "runs/red-execution-v1/terminal-receipt.json",
    "runs/red-execution-v1/zero-cell-matrix.json",
)
_FORBIDDEN_IMPORT_ROOTS = frozenset({"boto3", "http", "importlib", "openai", "requests", "subprocess", "urllib"})
_FORBIDDEN_CALLS = frozenset({"__import__", "eval", "exec"})


def _is_integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _load_canonical(root: Path, path: str) -> tuple[dict[str, object], bytes]:
    try:
        _, raw = read_authoritative_file(root, path)
        value = decode_strict_json(raw)
    except (FilesystemPolicyError, UnicodeError, ValueError) as error:
        raise RedExecutionError("RED_AUTHORITATIVE_INPUT_INVALID") from error
    if not isinstance(value, dict) or canonical_json_bytes(value) != raw:
        raise RedExecutionError("RED_AUTHORITATIVE_INPUT_INVALID")
    return value, raw


def validate_red_execution_policy_v1(value: object) -> dict[str, object]:
    """Accept only the one closed canonical policy and exact Red zero boundary."""
    required = {
        "allowed_cli_commands", "authority_inputs", "branch", "closure_paths",
        "forbidden_surface_roots", "matrix", "output_paths", "requirements",
        "schema_version", "successor_required_on_byte_change",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise RedExecutionError("RED_POLICY_INVALID")
    if value["schema_version"] != "red-execution-policy-v1" or value["branch"] != "red":
        raise RedExecutionError("RED_POLICY_INVALID")
    matrix = value["matrix"]
    if (
        not isinstance(matrix, dict)
        or set(matrix) != {"N_strict", "expected_cells", "formula", "repeat_count"}
        or any(not _is_integer(matrix[key]) for key in ("N_strict", "expected_cells", "repeat_count"))
        or matrix != {"N_strict": 0, "expected_cells": 0, "formula": "0*3*0=0", "repeat_count": 0}
    ):
        raise RedExecutionError("RED_INTEGER_CONTRACT_INVALID")
    for key in ("closure_paths", "output_paths"):
        paths = value[key]
        if not isinstance(paths, list) or paths != sorted(paths) or len(paths) != len(set(paths)):
            raise RedExecutionError("RED_POLICY_INVALID")
        try:
            [require_relative_posix_path(path) for path in paths]
        except (FilesystemPolicyError, TypeError) as error:
            raise RedExecutionError("RED_POLICY_PATH_INVALID") from error
    if value["output_paths"] != list(_OUTPUT_PATHS):
        raise RedExecutionError("RED_POLICY_INVALID")
    requirements = value["requirements"]
    if requirements != {
        "TS-11": "conditional_not_applicable_red_pending_phase7",
        "TS-12": "conditional_not_applicable_red_pending_phase7",
    }:
        raise RedExecutionError("RED_POLICY_INVALID")
    if value["allowed_cli_commands"] != ["execute-red-temporary"] or value["successor_required_on_byte_change"] is not True:
        raise RedExecutionError("RED_POLICY_INVALID")
    return value


def _policy(root: Path) -> dict[str, object]:
    value, _ = _load_canonical(root, _POLICY_PATH)
    return validate_red_execution_policy_v1(value)


def validate_red_authority_v1(root: Path, policy: Mapping[str, object] | None = None) -> dict[str, object]:
    """Validate only descriptor-held v6 authority bytes before any writer opens."""
    policy = _policy(root) if policy is None else policy
    values: dict[str, dict[str, object]] = {}
    raws: dict[str, bytes] = {}
    for path in _AUTHORITY_PATHS:
        value, raw = _load_canonical(root, path)
        values[path], raws[path] = value, raw
    expected = policy.get("authority_inputs")
    if not isinstance(expected, dict):
        raise RedExecutionError("RED_POLICY_INVALID")
    for path, raw in raws.items():
        repository_path = f"experiments/specchoice-v1.3.2/{path}"
        if expected.get(repository_path) != sha256_bytes(raw):
            raise RedExecutionError("RED_AUTHORITY_SUBSTITUTION")
    try:
        freeze_inputs = load_phase4_freeze_inputs_v6(experiment_root=root)
        packet = build_h3_red_review_packet_v6(freeze_inputs)
        readiness = build_h3_red_readiness_v6(packet)
        authority = validate_h3_red_authority_v6(
            authority=values[_AUTHORITY_PATHS[0]],
            freeze_inputs=freeze_inputs,
            packet=packet,
            readiness=readiness,
            decision_raw=raws[_AUTHORITY_PATHS[3]],
        )
    except H3ValidationError as error:
        raise RedExecutionError("RED_AUTHORITY_SUBSTITUTION") from error
    if (
        authority.get("branch") != "red"
        or authority.get("N_strict") != 0
        or authority.get("repeat_count") != 0
        or authority.get("h4_required") is not False
        or any(authority.get(key) is not False for key in (
            "external_calls_authorized", "model_execution_authorized",
            "production_retrieval_authorized", "provider_config_present",
        ))
    ):
        raise RedExecutionError("RED_AUTHORITY_SUBSTITUTION")
    return authority


def audit_red_execution_surface_v1(root: Path, policy: Mapping[str, object] | None = None) -> dict[str, object]:
    """Bind and scan the current finite source/config/test closure fail-closed."""
    policy = _policy(root) if policy is None else policy
    paths = policy.get("closure_paths")
    if not isinstance(paths, list):
        raise RedExecutionError("RED_POLICY_INVALID")
    try:
        closure = build_runtime_closure(root, paths)
        verify_runtime_closure(closure, root)
    except (FilesystemPolicyError, ValueError) as error:
        raise RedExecutionError("RED_CLOSURE_DRIFT") from error
    findings: list[dict[str, object]] = []
    for path in ("src/specchoice_execution/red.py", "src/specchoice_execution/cli.py"):
        try:
            _, raw = read_authoritative_file(root, path)
            tree = ast.parse(raw.decode("utf-8"), filename=path)
        except (FilesystemPolicyError, SyntaxError, UnicodeError) as error:
            raise RedExecutionError("RED_FORBIDDEN_SURFACE") from error
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [item.name for item in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                names = [node.module]
            for name in names:
                if name.split(".", 1)[0] in _FORBIDDEN_IMPORT_ROOTS:
                    findings.append({"kind": "forbidden_import", "path": path, "value": name})
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in _FORBIDDEN_CALLS:
                findings.append({"kind": "forbidden_dynamic_call", "path": path, "value": node.func.id})
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "os" and node.func.attr in {"getenv", "popen", "system"}:
                    findings.append({"kind": "forbidden_os_call", "path": path, "value": f"os.{node.func.attr}"})
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "importlib":
                    findings.append({"kind": "forbidden_dynamic_import", "path": path, "value": node.func.attr})
    if findings:
        raise RedExecutionError("RED_FORBIDDEN_SURFACE")
    return {"closure": closure, "forbidden_findings": [], "schema_version": "red-structural-audit-v1"}


@contextlib.contextmanager
def deny_all_sockets_v1(security_events: list[dict[str, object]]) -> Iterator[None]:
    """Deny every supported socket constructor before it reaches the OS."""
    def denied(constructor: str) -> Callable[..., object]:
        def fail(*_args: object, **_kwargs: object) -> object:
            security_events.append({"code": "RED_SOCKET_DENIED", "constructor": constructor, "event": "socket_operation"})
            raise RedExecutionError("RED_SOCKET_DENIED")

        return fail

    with contextlib.ExitStack() as stack:
        for name in ("socket", "create_connection", "create_server", "socketpair", "fromfd"):
            stack.enter_context(patch.object(socket, name, denied(name)))
        yield


def _component(value: object) -> dict[str, object]:
    raw = canonical_json_bytes(value)
    return {"byte_length": len(raw), "sha256": sha256_bytes(raw)}


def _build_result(root: Path, policy: Mapping[str, object], authority: Mapping[str, object]) -> tuple[dict[str, object], dict[str, bytes]]:
    raw_evidence = []
    for path in _RAW_EVIDENCE_PATHS:
        evidence, raw = read_authoritative_file(root, path)
        raw_evidence.append({
            "base64": base64.b64encode(raw).decode("ascii"),
            "byte_length": evidence.byte_length,
            "path": path,
            "sha256": evidence.sha256,
        })
    raw_evidence.sort(key=lambda item: str(item["path"]))
    parsed_evidence = {"empty_set": "explicit_empty_set", "findings": [], "schema_version": "red-parsed-evidence-v1"}
    diagnostics = [item.as_dict() for item in ordered_diagnostics(())]
    evidence_span_audit = {"findings": [], "schema_version": "red-evidence-span-audit-v1"}
    structural_audit = audit_red_execution_surface_v1(root, policy)
    runtime_audit = {"schema_version": "red-runtime-audit-v1", "security_events": []}
    ledger = {"calls": [], "schema_version": "red-model-call-ledger-v1"}
    partitions = {name: {"attempted": 0, "completed": 0, "expected": 0, "failed": 0, "retried": 0} for name in ("A", "B", "C")}
    matrix = {"N_strict": 0, "actual_cells": 0, "branch": "red", "cells": [], "expected_cells": 0, "formula": "0*3*0=0", "partitions": partitions, "repeat_count": 0, "schema_version": "red-zero-cell-matrix-v1"}
    components = {
        "evidence_span_audit": evidence_span_audit,
        "model_call_ledger": ledger,
        "ordered_diagnostics": diagnostics,
        "parsed_evidence": parsed_evidence,
        "raw_evidence": raw_evidence,
        "runtime_audit": runtime_audit,
        "structural_audit": structural_audit,
        "zero_cell_matrix": matrix,
    }
    terminal_receipt = {
        "authority_sha256": authority["authority_sha256"],
        "components": {name: _component(value) for name, value in sorted(components.items())},
        "schema_version": "red-terminal-receipt-v1",
        "status": "completed",
    }
    terminal_receipt["receipt_sha256"] = sha256_bytes(canonical_json_bytes(terminal_receipt))
    attempt_chain = {"attempts": [{"attempt_id": "red-execution-v1-attempt-001", "model_call_ledger_sha256": _component(ledger)["sha256"], "receipt_sha256": terminal_receipt["receipt_sha256"], "status": "completed"}], "schema_version": "red-attempt-chain-v1"}
    result = {
        "attempt_chain": attempt_chain,
        "evidence_span_audit": evidence_span_audit,
        "matrix": matrix,
        "model_call_ledger": ledger,
        "ordered_diagnostics": diagnostics,
        "parsed_evidence": parsed_evidence,
        "permissions": {"granted_downstream_permissions": ["phase6_red_evidence_evaluation", "phase7_red_evidence_evaluation"], "model_execution_authorized": False},
        "policy_sha256": sha256_bytes(canonical_json_bytes(policy)),
        "raw_evidence": raw_evidence,
        "requirements": dict(policy["requirements"]),
        "runtime_audit": runtime_audit,
        "schema_version": "red-execution-evidence-v1",
        "status": "completed",
        "structural_audit": structural_audit,
        "terminal_receipt": terminal_receipt,
    }
    values = {
        "runs/red-execution-v1/attempt-chain.json": attempt_chain,
        "runs/red-execution-v1/evidence-span-audit.json": evidence_span_audit,
        _RESULT_PATH: result,
        "runs/red-execution-v1/model-call-ledger.json": ledger,
        "runs/red-execution-v1/ordered-diagnostics.json": diagnostics,
        "runs/red-execution-v1/parsed-evidence.json": parsed_evidence,
        "runs/red-execution-v1/raw-evidence.json": raw_evidence,
        "runs/red-execution-v1/runtime-audit.json": runtime_audit,
        "runs/red-execution-v1/structural-audit.json": structural_audit,
        "runs/red-execution-v1/terminal-receipt.json": terminal_receipt,
        "runs/red-execution-v1/zero-cell-matrix.json": matrix,
    }
    return result, {path: canonical_json_bytes(value) for path, value in values.items()}


def validate_red_evidence_v1(*, root: Path | None = None, value: object | None = None) -> dict[str, object]:
    """Validate the completed no-call contract from its manifest or a supplied value."""
    if (root is None) == (value is None):
        raise RedExecutionError("RED_EVIDENCE_INPUT_INVALID")
    if root is not None:
        value, _ = _load_canonical(root, _RESULT_PATH)
    if not isinstance(value, dict) or value.get("schema_version") != "red-execution-evidence-v1":
        raise RedExecutionError("RED_EVIDENCE_INVALID")
    ledger, matrix, parsed, spans = (value.get("model_call_ledger"), value.get("matrix"), value.get("parsed_evidence"), value.get("evidence_span_audit"))
    if ledger != {"calls": [], "schema_version": "red-model-call-ledger-v1"}:
        raise RedExecutionError("RED_CALL_LEDGER_INVALID")
    if not isinstance(matrix, dict) or matrix.get("cells") != [] or matrix.get("formula") != "0*3*0=0" or matrix.get("expected_cells") != 0:
        raise RedExecutionError("RED_MATRIX_INVALID")
    if not isinstance(parsed, dict) or parsed.get("findings") != [] or parsed.get("empty_set") != "explicit_empty_set":
        raise RedExecutionError("RED_EMPTY_SET_INVALID")
    if not isinstance(spans, dict) or not isinstance(spans.get("findings"), list):
        raise RedExecutionError("RED_EVIDENCE_INVALID")
    for finding in spans["findings"]:
        if not isinstance(finding, dict) or not finding.get("spans"):
            raise RedExecutionError("RED_SURFACED_EMPTY_SPAN")
    requirements = value.get("requirements")
    if requirements != {"TS-11": "conditional_not_applicable_red_pending_phase7", "TS-12": "conditional_not_applicable_red_pending_phase7"}:
        raise RedExecutionError("RED_REQUIREMENT_STATE_INVALID")
    if root is not None:
        expected_values = {
            "runs/red-execution-v1/attempt-chain.json": value["attempt_chain"],
            "runs/red-execution-v1/evidence-span-audit.json": value["evidence_span_audit"],
            "runs/red-execution-v1/model-call-ledger.json": value["model_call_ledger"],
            "runs/red-execution-v1/ordered-diagnostics.json": value["ordered_diagnostics"],
            "runs/red-execution-v1/parsed-evidence.json": value["parsed_evidence"],
            "runs/red-execution-v1/raw-evidence.json": value["raw_evidence"],
            "runs/red-execution-v1/runtime-audit.json": value["runtime_audit"],
            "runs/red-execution-v1/structural-audit.json": value["structural_audit"],
            "runs/red-execution-v1/terminal-receipt.json": value["terminal_receipt"],
            "runs/red-execution-v1/zero-cell-matrix.json": value["matrix"],
        }
        if enumerate_authoritative_files(root) != set(_OUTPUT_PATHS):
            raise RedExecutionError("RED_UNREGISTERED_ARTIFACT")
        for path, expected in expected_values.items():
            _, raw = read_authoritative_file(root, path)
            if raw != canonical_json_bytes(expected):
                raise RedExecutionError("RED_EXACT_RESUME_MISMATCH")
    return value


def build_red_evidence_v1(
    *,
    root: Path,
    output_root: Path,
    write_observer: Callable[[], None] | None = None,
    socket_probe: Callable[[], object] | None = None,
) -> dict[str, object]:
    """Build, validate, and atomically publish one disposable Red package."""
    policy = _policy(root)
    authority = validate_red_authority_v1(root, policy)
    security_events: list[dict[str, object]] = []
    try:
        with deny_all_sockets_v1(security_events):
            if socket_probe is not None:
                socket_probe()
            result, payloads = _build_result(root, policy, authority)
    except RedExecutionError as error:
        if str(error) != "RED_SOCKET_DENIED":
            raise
        raise RedExecutionError(
            "RED_SOCKET_DENIED",
            failed_attempt={
                "authoritative": False,
                "metrics_emitted": False,
                "model_call_ledger": {"calls": [], "schema_version": "red-model-call-ledger-v1"},
                "security_events": security_events,
                "status": "failed",
            },
        ) from error
    validate_red_evidence_v1(value=result)
    if (_RESULT_PATH in enumerate_authoritative_files(output_root)):
        existing = validate_red_evidence_v1(root=output_root)
        if existing != result:
            raise RedExecutionError("RED_EXACT_RESUME_MISMATCH")
        return existing
    if enumerate_authoritative_files(output_root):
        raise RedExecutionError("RED_OUTPUT_PARTIAL_OR_OCCUPIED")
    if write_observer is not None:
        write_observer()
    try:
        write_exact_descriptor_files(output_root, payloads)
    except (FilesystemPolicyError, OSError) as error:
        raise RedExecutionError("RED_OUTPUT_PARTIAL_OR_OCCUPIED") from error
    published = validate_red_evidence_v1(root=output_root)
    if published != result:
        raise RedExecutionError("RED_EXACT_RESUME_MISMATCH")
    return published

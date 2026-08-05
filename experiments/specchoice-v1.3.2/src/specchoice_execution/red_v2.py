# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Forward-only, descriptor-bound Red v2 evidence contract.

This module deliberately has no provider, retrieval, credential, process, or
network capability.  Its only successful result is a zero-call Red package.
"""

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
    read_authoritative_file,
    require_relative_posix_path,
    write_exact_descriptor_files,
)
from specchoice_evidence.runtime_closure import build_runtime_closure, verify_runtime_closure
from specchoice_measurement.diagnostics import ordered_diagnostics
from specchoice_measurement.strict_json import decode_strict_json
from specchoice_treatments.h3 import (
    H3ValidationError,
    build_h3_red_readiness_v6,
    build_h3_red_review_packet_v6,
    load_phase4_freeze_inputs_v6,
    validate_h3_red_authority_v6,
)


class RedExecutionV2Error(ValueError):
    """Stable, fail-closed diagnostic for the successor contract."""


_POLICY_PATH = "config/execution/red-execution-policy-v2.json"
_AUTHORITY_PATHS = (
    "phase4/branch-authority-v6.json",
    "reports/h3/h3-red-review-v6/review-packet.json",
    "receipts/h3-branch-readiness-v6.json",
    "reviews/h3-branch-decision-v6.json",
)
_RAW_PATHS = ("phase3/data-authority-v1.json", *_AUTHORITY_PATHS)
_FORMAL = (
    "runs/red-execution-v2/attempt-chain.json",
    "runs/red-execution-v2/evidence-span-audit.json",
    "runs/red-execution-v2/matrix-manifest.json",
    "runs/red-execution-v2/model-call-ledger.json",
    "runs/red-execution-v2/no-call-runtime-audit.json",
    "runs/red-execution-v2/no-call-structural-audit.json",
    "runs/red-execution-v2/ordered-diagnostics.json",
    "runs/red-execution-v2/parsed-evidence.json",
    "runs/red-execution-v2/raw-evidence.json",
    "runs/red-execution-v2/red-trigger-evidence.json",
)
_RECEIPT = "receipts/red-execution-v2.json"
_REPORT = "reports/red-execution/red-execution-v2.md"
_FORBIDDEN_IMPORTS = frozenset({"boto3", "http", "importlib", "openai", "requests", "subprocess", "urllib"})
_FORBIDDEN_CALLS = frozenset({"__import__", "eval", "exec"})


def _load_canonical(root: Path, path: str) -> tuple[dict[str, object], bytes]:
    try:
        _evidence, raw = read_authoritative_file(root, path)
        value = decode_strict_json(raw)
    except (FilesystemPolicyError, UnicodeError, ValueError) as error:
        raise RedExecutionV2Error("RED_AUTHORITATIVE_INPUT_INVALID") from error
    if not isinstance(value, dict) or canonical_json_bytes(value) != raw:
        raise RedExecutionV2Error("RED_AUTHORITATIVE_INPUT_INVALID")
    return value, raw


def _paths(value: object) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(path, str) for path in value):
        raise RedExecutionV2Error("RED_POLICY_INVALID")
    if value != sorted(value) or len(value) != len(set(value)):
        raise RedExecutionV2Error("RED_POLICY_NONCANONICAL")
    try:
        [require_relative_posix_path(path) for path in value]
    except (FilesystemPolicyError, TypeError) as error:
        raise RedExecutionV2Error("RED_POLICY_PATH_INVALID") from error
    return value


def validate_red_execution_policy_v2(value: object) -> dict[str, object]:
    """Validate the raw policy without permitting self-identity recursion."""
    if not isinstance(value, dict):
        raise RedExecutionV2Error("RED_POLICY_INVALID")
    if any(key in value for key in ("policy_sha256", "policy_byte_length", "runtime_closure_sha256", "gate_a_projection_sha256")):
        raise RedExecutionV2Error("RED_POLICY_SELF_REFERENCE")
    required = {
        "allowed_cli_commands", "argument_schema", "authority_inputs", "branch", "closure_paths",
        "forbidden_surface_roots", "formal_output_paths", "matrix", "output_targets", "policy_path",
        "requirements", "schema_version", "successor_required_on_byte_change",
    }
    if set(value) != required or value.get("schema_version") != "red-execution-policy-v2":
        raise RedExecutionV2Error("RED_POLICY_INVALID")
    if value.get("policy_path") != _POLICY_PATH or value.get("branch") != "red":
        raise RedExecutionV2Error("RED_POLICY_INVALID")
    closure = _paths(value["closure_paths"])
    formal = _paths(value["formal_output_paths"])
    if _POLICY_PATH in closure or set(closure) & set(formal):
        raise RedExecutionV2Error("RED_POLICY_SELF_REFERENCE")
    if formal != list(_FORMAL):
        raise RedExecutionV2Error("RED_POLICY_INVALID")
    if value.get("allowed_cli_commands") != ["execute-red"]:
        raise RedExecutionV2Error("RED_POLICY_INVALID")
    expected_arguments = ["--repo-root", "--policy", "--authority", "--packet", "--readiness", "--decision", "--attempt-root", "--formal-root", "--receipt", "--report"]
    if value.get("argument_schema") != expected_arguments:
        raise RedExecutionV2Error("RED_POLICY_INVALID")
    if value.get("matrix") != {"N_strict": 0, "actual_cells": 0, "expected_cells": 0, "formula": "0*3*0=0", "repeat_count": 0}:
        raise RedExecutionV2Error("RED_INTEGER_CONTRACT_INVALID")
    if value.get("requirements") != {"TS-11": "conditional_not_applicable_red_pending_phase7", "TS-12": "conditional_not_applicable_red_pending_phase7"}:
        raise RedExecutionV2Error("RED_REQUIREMENT_STATE_INVALID")
    targets = value.get("output_targets")
    if targets != {"attempt_root": "runs/red-attempts-v2", "formal_root": "runs/red-execution-v2", "receipt": _RECEIPT, "report": _REPORT}:
        raise RedExecutionV2Error("RED_POLICY_INVALID")
    if value.get("successor_required_on_byte_change") is not True:
        raise RedExecutionV2Error("RED_POLICY_INVALID")
    authorities = value.get("authority_inputs")
    if not isinstance(authorities, dict) or sorted(authorities) != list(authorities) or set(authorities) != set(_RAW_PATHS):
        raise RedExecutionV2Error("RED_POLICY_INVALID")
    for path, digest in authorities.items():
        try:
            require_relative_posix_path(path)
        except (FilesystemPolicyError, TypeError) as error:
            raise RedExecutionV2Error("RED_POLICY_PATH_INVALID") from error
        if not isinstance(digest, str) or len(digest) != 64:
            raise RedExecutionV2Error("RED_POLICY_INVALID")
    return value


def _policy(root: Path) -> tuple[dict[str, object], bytes]:
    value, raw = _load_canonical(root, _POLICY_PATH)
    return validate_red_execution_policy_v2(value), raw


def validate_red_authority_v2(root: Path, policy: Mapping[str, object] | None = None) -> dict[str, object]:
    """Rebuild, rather than trust, the Phase 4 v6 Red authority."""
    policy = _policy(root)[0] if policy is None else policy
    raws: dict[str, bytes] = {}
    values: dict[str, dict[str, object]] = {}
    for path in _AUTHORITY_PATHS:
        values[path], raws[path] = _load_canonical(root, path)
    for path in _RAW_PATHS:
        _value, raw = _load_canonical(root, path)
        if policy["authority_inputs"].get(path) != sha256_bytes(raw):
            raise RedExecutionV2Error("RED_AUTHORITY_SUBSTITUTION")
    try:
        freeze = load_phase4_freeze_inputs_v6(experiment_root=root)
        packet = build_h3_red_review_packet_v6(freeze)
        readiness = build_h3_red_readiness_v6(packet)
        authority = validate_h3_red_authority_v6(
            authority=values[_AUTHORITY_PATHS[0]], freeze_inputs=freeze, packet=packet,
            readiness=readiness, decision_raw=raws[_AUTHORITY_PATHS[3]],
        )
    except H3ValidationError as error:
        raise RedExecutionV2Error("RED_AUTHORITY_SUBSTITUTION") from error
    if authority.get("branch") != "red" or authority.get("N_strict") != 0 or authority.get("repeat_count") != 0:
        raise RedExecutionV2Error("RED_AUTHORITY_SUBSTITUTION")
    if any(authority.get(key) is not False for key in ("external_calls_authorized", "model_execution_authorized", "production_retrieval_authorized", "provider_config_present")):
        raise RedExecutionV2Error("RED_AUTHORITY_SUBSTITUTION")
    return authority


def audit_red_execution_surface_v2(root: Path, policy: Mapping[str, object] | None = None) -> dict[str, object]:
    """Bind the finite v2 closure and reject dynamic or external capability."""
    policy = _policy(root)[0] if policy is None else policy
    try:
        closure = build_runtime_closure(root, list(policy["closure_paths"]))
        verify_runtime_closure(closure, root)
    except (FilesystemPolicyError, ValueError) as error:
        raise RedExecutionV2Error("RED_CLOSURE_DRIFT") from error
    findings: list[dict[str, object]] = []
    for path in ("src/specchoice_execution/red_v2.py", "src/specchoice_execution/cli_v2.py", "tests/test_authorized_execution_v2.py"):
        try:
            _evidence, raw = read_authoritative_file(root, path)
            tree = ast.parse(raw.decode("utf-8"), filename=path)
        except (FilesystemPolicyError, SyntaxError, UnicodeError) as error:
            raise RedExecutionV2Error("RED_FORBIDDEN_SURFACE") from error
        for node in ast.walk(tree):
            names = [item.name for item in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) and node.module else []
            if any(name.split(".", 1)[0] in _FORBIDDEN_IMPORTS for name in names):
                findings.append({"path": path, "kind": "forbidden_import"})
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in _FORBIDDEN_CALLS:
                findings.append({"path": path, "kind": "forbidden_call"})
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "os" and node.func.attr in {"environ", "getenv", "popen", "system"}:
                findings.append({"path": path, "kind": "forbidden_os"})
    if findings:
        raise RedExecutionV2Error("RED_FORBIDDEN_SURFACE")
    return {"closure": closure, "forbidden_findings": [], "schema_version": "red-no-call-structural-audit-v2"}


@contextlib.contextmanager
def deny_all_sockets_v2(security_events: list[dict[str, object]]) -> Iterator[None]:
    """Install the all-socket tripwire before admission or filesystem output."""
    def denied(name: str) -> Callable[..., object]:
        def fail(*_args: object, **_kwargs: object) -> object:
            security_events.append({"code": "RED_SOCKET_DENIED", "constructor": name, "event": "socket_operation"})
            raise RedExecutionV2Error("RED_SOCKET_DENIED")
        return fail
    with contextlib.ExitStack() as stack:
        for name in ("socket", "create_connection", "create_server", "socketpair", "fromfd"):
            stack.enter_context(patch.object(socket, name, denied(name)))
        yield


def build_gate_a_projection_v2(root: Path) -> dict[str, object]:
    """Return the external, non-persisted Gate-A projection and its external hash."""
    policy, policy_raw = _policy(root)
    entries: list[dict[str, object]] = []
    for path in sorted({*policy["closure_paths"], *_RAW_PATHS}):
        _evidence, raw = read_authoritative_file(root, path)
        entries.append({"path": path, "byte_length": len(raw), "sha256": sha256_bytes(raw)})
    basis = {
        "schema_version": "red-execution-runtime-closure-basis-v2",
        "policy": {"path": _POLICY_PATH, "byte_length": len(policy_raw), "sha256": sha256_bytes(policy_raw)},
        "entries": entries,
    }
    runtime_hash = sha256_bytes(canonical_json_bytes(basis))
    projection: dict[str, object] = {
        "schema_version": "red-execution-gate-a-projection-v2",
        "policy_entry": basis["policy"],
        "runtime_closure_basis": basis,
        "runtime_closure_sha256": runtime_hash,
        "allowed_cli_commands": policy["allowed_cli_commands"],
        "argument_schema": policy["argument_schema"],
        "authority_inputs": policy["authority_inputs"],
        "formal_output_paths": policy["formal_output_paths"],
        "output_targets": policy["output_targets"],
        "requirements": policy["requirements"],
        "red_matrix": policy["matrix"],
        "forbidden_surface_roots": policy["forbidden_surface_roots"],
    }
    projection["gate_a_projection_sha256"] = sha256_bytes(canonical_json_bytes(projection))
    return projection


def _component(value: object) -> dict[str, object]:
    raw = canonical_json_bytes(value)
    return {"byte_length": len(raw), "sha256": sha256_bytes(raw)}


def _build_payloads(root: Path, policy: Mapping[str, object], authority: Mapping[str, object]) -> tuple[dict[str, object], dict[str, bytes]]:
    projection = build_gate_a_projection_v2(root)
    structural = audit_red_execution_surface_v2(root, policy)
    runtime = {"schema_version": "red-no-call-runtime-audit-v2", "security_events": []}
    ledger = {"calls": [], "schema_version": "red-model-call-ledger-v2"}
    raw = []
    for path in _RAW_PATHS:
        evidence, bytes_ = read_authoritative_file(root, path)
        raw.append({"path": path, "base64": base64.b64encode(bytes_).decode("ascii"), "byte_length": evidence.byte_length, "sha256": evidence.sha256})
    raw.sort(key=lambda item: str(item["path"]))
    parsed = {"empty_set": "explicit_empty_set", "findings": [], "schema_version": "red-parsed-evidence-v2"}
    diagnostics = [item.as_dict() for item in ordered_diagnostics(())]
    spans = {"findings": [], "schema_version": "red-evidence-span-audit-v2"}
    partitions = {name: {"attempted": 0, "completed": 0, "expected": 0, "failed": 0, "retried": 0} for name in ("A", "B", "C")}
    matrix = {"N_strict": 0, "actual_cells": 0, "branch": "red", "cells": [], "expected_cells": 0, "formula": "0*3*0=0", "partitions": partitions, "repeat_count": 0, "schema_version": "red-zero-cell-matrix-v2"}
    trigger = {"authority_sha256": authority["authority_sha256"], "branch": "red", "N_strict": 0, "repeat_count": 0, "schema_version": "red-trigger-evidence-v2"}
    components = {"evidence_span_audit": spans, "matrix_manifest": matrix, "model_call_ledger": ledger, "no_call_runtime_audit": runtime, "no_call_structural_audit": structural, "ordered_diagnostics": diagnostics, "parsed_evidence": parsed, "raw_evidence": raw, "red_trigger_evidence": trigger}
    receipt = {"authority_sha256": authority["authority_sha256"], "components": {name: _component(value) for name, value in sorted(components.items())}, "gate_a_projection_sha256": projection["gate_a_projection_sha256"], "policy_sha256": projection["policy_entry"]["sha256"], "runtime_closure_sha256": projection["runtime_closure_sha256"], "schema_version": "red-execution-receipt-v2", "status": "completed"}
    receipt["receipt_sha256"] = sha256_bytes(canonical_json_bytes(receipt))
    attempt = {"attempts": [{"attempt_id": "red-execution-v2-attempt-001", "model_call_ledger_sha256": _component(ledger)["sha256"], "receipt_sha256": receipt["receipt_sha256"], "status": "completed"}], "schema_version": "red-attempt-chain-v2"}
    values = { _FORMAL[0]: attempt, _FORMAL[1]: spans, _FORMAL[2]: matrix, _FORMAL[3]: ledger, _FORMAL[4]: runtime, _FORMAL[5]: structural, _FORMAL[6]: diagnostics, _FORMAL[7]: parsed, _FORMAL[8]: raw, _FORMAL[9]: trigger, _RECEIPT: receipt }
    report = "# Red execution v2\n\nRed no-call evidence only; TS-11 and TS-12 remain conditional pending Phase 7.\n"
    payloads = {path: canonical_json_bytes(value) for path, value in values.items()}
    payloads[_REPORT] = report.encode("utf-8")
    return receipt, payloads


def validate_red_evidence_v2(*, root: Path, value: object | None = None) -> dict[str, object]:
    """Validate only the complete fixed v2 evidence set and its three hashes."""
    receipt = value
    if receipt is None:
        receipt, _raw = _load_canonical(root, _RECEIPT)
    if not isinstance(receipt, dict) or receipt.get("schema_version") != "red-execution-receipt-v2" or receipt.get("status") != "completed":
        raise RedExecutionV2Error("RED_EVIDENCE_INVALID")
    if not all(isinstance(receipt.get(key), str) and len(receipt[key]) == 64 for key in ("policy_sha256", "runtime_closure_sha256", "gate_a_projection_sha256")):
        raise RedExecutionV2Error("RED_EVIDENCE_INVALID")
    ledger, _raw = _load_canonical(root, _FORMAL[3])
    matrix, _raw = _load_canonical(root, _FORMAL[2])
    parsed, _raw = _load_canonical(root, _FORMAL[7])
    if ledger != {"calls": [], "schema_version": "red-model-call-ledger-v2"} or matrix.get("cells") != [] or matrix.get("expected_cells") != 0 or parsed.get("findings") != []:
        raise RedExecutionV2Error("RED_EVIDENCE_INVALID")
    return receipt


def execute_red_v2(*, root: Path, supplied_paths: Mapping[str, str]) -> dict[str, object]:
    """Publish one complete v2 set or exactly resume it; never repair a mismatch."""
    policy, _policy_raw = _policy(root)
    expected = {"policy": _POLICY_PATH, "authority": _AUTHORITY_PATHS[0], "packet": _AUTHORITY_PATHS[1], "readiness": _AUTHORITY_PATHS[2], "decision": _AUTHORITY_PATHS[3], **policy["output_targets"]}
    if dict(supplied_paths) != expected:
        raise RedExecutionV2Error("RED_ARGUMENT_MISMATCH")
    try:
        [require_relative_posix_path(path) for path in supplied_paths.values()]
    except (FilesystemPolicyError, TypeError) as error:
        raise RedExecutionV2Error("RED_ARGUMENT_MISMATCH") from error
    security_events: list[dict[str, object]] = []
    with deny_all_sockets_v2(security_events):
        authority = validate_red_authority_v2(root, policy)
        receipt, payloads = _build_payloads(root, policy, authority)
        existing = [path for path in payloads if (root / path).exists() or (root / path).is_symlink()]
        if existing:
            if len(existing) != len(payloads):
                raise RedExecutionV2Error("RED_OUTPUT_PARTIAL_OR_OCCUPIED")
            try:
                if all(read_authoritative_file(root, path)[1] == raw for path, raw in payloads.items()):
                    return validate_red_evidence_v2(root=root)
            except FilesystemPolicyError as error:
                raise RedExecutionV2Error("RED_OUTPUT_PARTIAL_OR_OCCUPIED") from error
            raise RedExecutionV2Error("RED_OUTPUT_PARTIAL_OR_OCCUPIED")
        try:
            write_exact_descriptor_files(root, payloads)
        except FilesystemPolicyError as error:
            raise RedExecutionV2Error("RED_OUTPUT_PARTIAL_OR_OCCUPIED") from error
        return validate_red_evidence_v2(root=root, value=receipt)

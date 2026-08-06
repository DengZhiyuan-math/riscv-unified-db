# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Decision-free, create-only reviewer projections for a validated Red evaluation."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

from specchoice_evidence.canonical import (
    canonical_json_bytes,
    require_sha256,
    sha256_bytes,
)
from specchoice_evidence.filesystem import (
    FilesystemPolicyError,
    read_authoritative_files,
    write_exact_descriptor_files,
)

from .core import (
    METRIC_IDS,
    RESULT_STATES,
    EvaluationBundle,
    EvaluationError,
    build_construction_feasibility,
    build_red_evaluation,
)

_POLICY_SCHEMA = "partition-evaluation-policy-v2"
_LEGACY_POLICY_SCHEMA = "partition-evaluation-policy-v1"
_PACKET_SCHEMA = "partition-evaluation-red-packet-v2"
_READINESS_SCHEMA = "partition-evaluation-red-readiness-v2"
_OUTPUT_KEYS = ("packet", "markdown", "readiness")
_DECISION_SCHEMA = "partition-evaluation-review-decision-v1"
_RESPONSE_VALUES = frozenset(("approved", "disputed", "incomplete"))
_DECISION_LIMITS = {
    "external_publication_authorized": False,
    "final_narrative_authorized": False,
    "h5_interpretation_authorized": False,
    "h6_communication_authorized": False,
    "model_authorized": False,
    "network_authorized": False,
    "provider_authorized": False,
    "retrieval_authorized": False,
    "subprocess_authorized": False,
}
EXPECTED_COMPONENT_IDS = (
    "applicability",
    "atomic_rows",
    "construction",
    "deterministic_measurement",
    "failures",
    "metrics",
    "populations",
    "red_execution_evidence",
    "warnings",
)


@dataclass(frozen=True)
class ReviewDecision:
    """Closed human review record, bound to one decision-free package."""

    schema_version: str
    generation_id: str
    packet_sha256: str
    readiness_sha256: str
    reviewer_id: str
    disposition: str
    domain_responses: dict[str, str]
    item_responses: dict[str, str]
    disputes: list[dict[str, object]]
    conclusion_ready: bool
    phase7_interpretation_authorized: bool
    authority_limits: dict[str, bool]
    d16_acknowledgement: bool
    decision_sha256: str


def _error(code: str) -> None:
    raise EvaluationError(code)


def _canonical_object(value: object, code: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping) or canonical_json_bytes(value) != canonical_json_bytes(dict(value)):
        _error(code)
    return value


def _self_hash(value: Mapping[str, object], field: str, code: str) -> str:
    try:
        observed = require_sha256(value.get(field))
    except ValueError as error:
        raise EvaluationError(code) from error
    basis = dict(value)
    basis.pop(field, None)
    if observed != sha256_bytes(canonical_json_bytes(basis)):
        _error(code)
    return observed


def _component_hashes(packet: Mapping[str, object]) -> dict[str, str]:
    components = packet.get("components")
    if not isinstance(components, Mapping):
        _error("EVALUATION_PACKET_COMPONENTS_INVALID")
    return {str(name): sha256_bytes(canonical_json_bytes(value)) for name, value in sorted(components.items())}


def _decision_free_projection(value: object) -> object:
    """Rename deterministic classification labels that would imply a human grant."""
    if isinstance(value, str):
        return value.replace("disposition", "classification_outcome")
    if isinstance(value, list):
        return [_decision_free_projection(item) for item in value]
    if isinstance(value, Mapping):
        return {
            str(_decision_free_projection(key)): _decision_free_projection(item)
            for key, item in value.items()
        }
    return value


_PACKET_METRIC_IDS = tuple(
    "classification_outcome" if metric_id == "disposition" else metric_id
    for metric_id in METRIC_IDS
)


def _input_digest(inputs: Sequence[Mapping[str, object]]) -> str:
    return sha256_bytes(canonical_json_bytes([
        {"path": item["path"], "sha256": item["sha256"]}
        for item in sorted(inputs, key=lambda item: str(item["path"]))
    ]))


def validate_evaluation_policy(experiment_root: Path, project_root: Path, policy: Mapping[str, object]) -> None:
    """Validate the non-circular, complete local package generation policy."""
    if policy.get("schema_version") == _LEGACY_POLICY_SCHEMA:
        _error("EVALUATION_POLICY_LEGACY_GENERATION")
    if policy.get("schema_version") != _POLICY_SCHEMA:
        _error("EVALUATION_POLICY_INVALID")
    if not isinstance(policy.get("generation_id"), str) or not policy["generation_id"]:
        _error("EVALUATION_POLICY_INVALID")
    if policy.get("branch") != "red" or policy.get("n_strict") != 0 or policy.get("repeat_count") != 0:
        _error("EVALUATION_POLICY_INVALID")
    _self_hash(policy, "policy_sha256", "EVALUATION_POLICY_HASH_INVALID")
    outputs = policy.get("outputs")
    if not isinstance(outputs, Mapping) or set(outputs) != set(_OUTPUT_KEYS):
        _error("EVALUATION_POLICY_OUTPUTS_INVALID")
    if any(not isinstance(outputs[key], str) or not outputs[key] for key in _OUTPUT_KEYS):
        _error("EVALUATION_POLICY_OUTPUTS_INVALID")
    if len({str(outputs[key]) for key in _OUTPUT_KEYS}) != len(_OUTPUT_KEYS):
        _error("EVALUATION_POLICY_OUTPUTS_INVALID")
    if tuple(policy.get("metric_ids", ())) != _PACKET_METRIC_IDS:
        _error("EVALUATION_POLICY_METRICS_INVALID")
    component_ids = policy.get("component_ids")
    if not isinstance(component_ids, list) or tuple(component_ids) != EXPECTED_COMPONENT_IDS:
        _error("EVALUATION_POLICY_COMPONENTS_INVALID")
    runtime = policy.get("runtime_closure")
    if not isinstance(runtime, Mapping) or runtime.get("path") != "receipts/runtime-executable-closure-v4.json":
        _error("EVALUATION_POLICY_RUNTIME_INVALID")
    try:
        require_sha256(runtime.get("sha256"))
    except ValueError as error:
        raise EvaluationError("EVALUATION_POLICY_RUNTIME_INVALID") from error
    limits = policy.get("authority_limits")
    expected_limits = {
        "external_publication_authorized": False,
        "model_authorized": False,
        "network_authorized": False,
        "provider_authorized": False,
        "retrieval_authorized": False,
        "subprocess_authorized": False,
    }
    if limits != expected_limits:
        _error("EVALUATION_POLICY_AUTHORITY_INVALID")
    inputs = policy.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        _error("EVALUATION_POLICY_INPUTS_INVALID")
    normalized: list[dict[str, object]] = []
    for item in inputs:
        if not isinstance(item, Mapping) or set(item) != {"path", "sha256"} or not isinstance(item["path"], str):
            _error("EVALUATION_POLICY_INPUTS_INVALID")
        try:
            require_sha256(item["sha256"])
        except ValueError as error:
            raise EvaluationError("EVALUATION_POLICY_INPUTS_INVALID") from error
        normalized.append({"path": item["path"], "sha256": item["sha256"]})
    paths = [str(item["path"]) for item in normalized]
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        _error("EVALUATION_POLICY_INPUTS_INVALID")
    try:
        files = read_authoritative_files(experiment_root, paths)
    except (FilesystemPolicyError, OSError, ValueError) as error:
        raise EvaluationError("EVALUATION_POLICY_INPUTS_INVALID") from error
    for item in normalized:
        if sha256_bytes(files[str(item["path"])][1]) != item["sha256"]:
            _error("EVALUATION_POLICY_INPUT_SUBSTITUTED")
    matching_runtime_inputs = [item for item in normalized if item["path"] == runtime["path"]]
    if len(matching_runtime_inputs) != 1 or matching_runtime_inputs[0]["sha256"] != runtime["sha256"]:
        _error("EVALUATION_POLICY_RUNTIME_INVALID")
    if sha256_bytes(files[str(runtime["path"])][1]) != runtime["sha256"]:
        _error("EVALUATION_POLICY_RUNTIME_INVALID")
    build_construction_feasibility(experiment_root, project_root, policy.get("construction_inputs", ()))


def build_evaluation_packet(
    bundle: EvaluationBundle, *, policy: Mapping[str, object] | None = None,
    construction_attempts: Sequence[object] = (),
) -> dict[str, object]:
    """Bind all machine evidence while leaving a human disposition outside the packet."""
    payload = _decision_free_projection(bundle.as_dict())
    assert isinstance(payload, dict)
    payload.update({
        "packet_kind": _PACKET_SCHEMA,
        "generation_id": None if policy is None else policy["generation_id"],
        "policy_sha256": None if policy is None else policy["policy_sha256"],
        "atomic_rows": payload["rows"],
        "case_rows": payload["rows"],
        "closed_joins": [],
        "construction_feasibility": [asdict(item) for item in construction_attempts],
        "failures": [],
        "warnings": [],
        "complete": True,
        "conclusion_ready": False,
    })
    components = {
        "applicability": payload["applicability_matrix"],
        "atomic_rows": payload["atomic_rows"],
        "construction": payload["construction_feasibility"],
        "deterministic_measurement": payload["deterministic_measurement"],
        "failures": payload["failures"],
        "metrics": payload["metrics"],
        "populations": payload["populations"],
        "red_execution_evidence": payload["red_execution_evidence"],
        "warnings": payload["warnings"],
    }
    payload["components"] = components
    component_hashes = _component_hashes(payload)
    payload["component_sha256"] = component_hashes
    payload["component_set_sha256"] = sha256_bytes(canonical_json_bytes(component_hashes))
    payload["input_sha256"] = sha256_bytes(canonical_json_bytes({
        "deterministic_measurement": payload["deterministic_measurement"],
        "red_execution_evidence": payload["red_execution_evidence"],
    }))
    payload["packet_sha256"] = sha256_bytes(canonical_json_bytes(payload))
    return payload


def validate_evaluation_packet(
    experiment_root: Path, project_root: Path, policy: Mapping[str, object], packet: Mapping[str, object],
) -> None:
    """Recompute packet identities, applicability, denominators, and authority boundaries."""
    validate_evaluation_policy(experiment_root, project_root, policy)
    if packet.get("packet_kind") != _PACKET_SCHEMA or packet.get("generation_id") != policy["generation_id"]:
        _error("EVALUATION_PACKET_INVALID")
    if packet.get("policy_sha256") != policy["policy_sha256"] or packet.get("branch") != "red":
        _error("EVALUATION_PACKET_POLICY_INVALID")
    if packet.get("n_strict") != 0 or packet.get("repeat_count") != 0 or packet.get("no_model_calls") is not True:
        _error("EVALUATION_PACKET_BRANCH_INVALID")
    if packet.get("conclusion_ready") is not False or packet.get("complete") is not True:
        _error("EVALUATION_PACKET_AUTHORITY_INVALID")
    _self_hash(packet, "packet_sha256", "EVALUATION_PACKET_HASH_INVALID")
    components = packet.get("components")
    if not isinstance(components, Mapping) or tuple(sorted(components)) != EXPECTED_COMPONENT_IDS:
        _error("EVALUATION_PACKET_COMPONENTS_INVALID")
    component_hashes = packet.get("component_sha256")
    if (
        not isinstance(component_hashes, Mapping)
        or tuple(sorted(component_hashes)) != EXPECTED_COMPONENT_IDS
        or dict(component_hashes) != _component_hashes(packet)
    ):
        _error("EVALUATION_PACKET_COMPONENTS_INVALID")
    if packet.get("component_set_sha256") != sha256_bytes(canonical_json_bytes(component_hashes)):
        _error("EVALUATION_PACKET_COMPONENTS_INVALID")
    metrics = packet.get("metrics")
    applicability = packet.get("applicability_matrix")
    populations = packet.get("populations")
    if not isinstance(metrics, list) or not isinstance(applicability, list) or not isinstance(populations, list):
        _error("EVALUATION_PACKET_CONTENT_INVALID")
    if metrics != applicability or tuple(item.get("metric_id") for item in metrics if isinstance(item, Mapping)) != _PACKET_METRIC_IDS:
        _error("EVALUATION_PACKET_METRICS_INVALID")
    denominators = {item.get("population_id"): item.get("denominator") for item in populations if isinstance(item, Mapping)}
    for metric in metrics:
        if not isinstance(metric, Mapping) or metric.get("state") not in RESULT_STATES:
            _error("EVALUATION_PACKET_METRICS_INVALID")
        if metric["state"] == "measured" and denominators.get(metric.get("population_id")) != metric.get("denominator"):
            _error("EVALUATION_PACKET_DENOMINATOR_INVALID")
        if metric["state"] == "not_applicable_red" and any(key in metric for key in ("numerator", "denominator", "score")):
            _error("EVALUATION_PACKET_APPLICABILITY_INVALID")
    for warning in packet.get("warnings", []):
        if not isinstance(warning, Mapping) or warning.get("effect") != "report_only":
            _error("EVALUATION_PACKET_WARNING_INVALID")
    if packet.get("failures") != []:
        _error("EVALUATION_PACKET_BLOCKING_DOMAIN")
    expected = build_evaluation_packet(
        build_red_evaluation(experiment_root),
        policy=policy,
        construction_attempts=build_construction_feasibility(
            experiment_root, project_root, policy["construction_inputs"],
        ),
    )
    if canonical_json_bytes(packet) != canonical_json_bytes(expected):
        _error("EVALUATION_PACKET_DERIVATION_INVALID")


def render_evaluation_markdown(packet: Mapping[str, object]) -> bytes:
    """Render a deterministic Red-first projection without adding conclusions."""
    authority = packet["red_execution_evidence"]
    assert isinstance(authority, Mapping)
    sections = (
        ("Applicability matrix", packet["applicability_matrix"]),
        ("Case rows", packet["case_rows"]),
        ("Metrics", packet["metrics"]),
        ("Warnings", packet["warnings"]),
        ("Failures", packet["failures"]),
        ("Construction feasibility", packet["construction_feasibility"]),
    )
    body = (
        "# Red authority\n\n"
        f"- Branch: `{packet['branch']}`\n"
        f"- N_strict: `{packet['n_strict']}`\n"
        f"- repeat_count: `{packet['repeat_count']}`\n"
        f"- verified_no_model_calls: `{packet['no_model_calls']}`\n"
        f"- Red evidence authority: `{authority['source_sha256']}`\n"
    )
    for title, value in sections:
        body += f"\n# {title}\n\n```json\n"
        body += canonical_json_bytes(value).decode("utf-8")
        body += "```\n"
    return body.encode("utf-8")


def build_readiness(
    packet: Mapping[str, object], *, policy: Mapping[str, object] | None = None, markdown: bytes | None = None,
) -> dict[str, object]:
    """Return a bounded machine identity; it cannot grant any human outcome."""
    packet_sha256 = packet.get("packet_sha256")
    if not isinstance(packet_sha256, str):
        raise TypeError("EVALUATION_PACKET_HASH_INVALID")
    if policy is None:
        payload = {"packet_sha256": packet_sha256, "schema_version": _READINESS_SCHEMA, "status": "ready_for_human_review"}
    else:
        if markdown is None:
            _error("EVALUATION_MARKDOWN_REQUIRED")
        payload = {
            "authority_limits": policy["authority_limits"],
            "blocking_domains": [],
            "component_sha256": packet["component_set_sha256"],
            "conclusion_ready": False,
            "generation_id": policy["generation_id"],
            "input_sha256": packet["input_sha256"],
            "markdown_sha256": sha256_bytes(markdown),
            "packet_sha256": packet_sha256,
            "policy_sha256": policy["policy_sha256"],
            "ready_for_human_review": True,
            "runtime_closure_sha256": policy["runtime_closure"]["sha256"],
            "schema_version": _READINESS_SCHEMA,
        }
    return {**payload, "readiness_sha256": sha256_bytes(canonical_json_bytes(payload))}


def validate_readiness(
    experiment_root: Path, project_root: Path, policy: Mapping[str, object], packet: Mapping[str, object], markdown: bytes,
    readiness: Mapping[str, object],
) -> None:
    """Require readiness to bind exact machine material while preserving the human boundary."""
    validate_evaluation_packet(experiment_root, project_root, policy, packet)
    if readiness.get("schema_version") != _READINESS_SCHEMA or readiness.get("generation_id") != policy["generation_id"]:
        _error("EVALUATION_READINESS_INVALID")
    expected = build_readiness(packet, policy=policy, markdown=markdown)
    if dict(readiness) != expected:
        _error("EVALUATION_READINESS_HASH_INVALID")
    if readiness.get("blocking_domains") != [] or readiness.get("ready_for_human_review") is not True or readiness.get("conclusion_ready") is not False:
        _error("EVALUATION_READINESS_AUTHORITY_INVALID")
    if readiness.get("authority_limits") != policy["authority_limits"]:
        _error("EVALUATION_READINESS_AUTHORITY_INVALID")


def _outputs_occupied(root: Path, outputs: Mapping[str, object]) -> tuple[bool, bool]:
    states = []
    for key in _OUTPUT_KEYS:
        target = root / str(outputs[key])
        try:
            os.lstat(target)
            states.append(True)
        except FileNotFoundError:
            states.append(False)
    return any(states), all(states)


def publish_evaluation_package(
    experiment_root: Path, project_root: Path, policy: Mapping[str, object],
) -> tuple[dict[str, object], bytes, dict[str, object]]:
    """Create the exact three-file packet or validate a zero-write exact resume."""
    validate_evaluation_policy(experiment_root, project_root, policy)
    outputs = policy["outputs"]
    assert isinstance(outputs, Mapping)
    occupied, complete = _outputs_occupied(experiment_root, outputs)
    if occupied and not complete:
        _error("EVALUATION_OUTPUT_PARTIAL_OR_OCCUPIED")
    bundle = build_red_evaluation(experiment_root)
    packet = build_evaluation_packet(
        bundle, policy=policy,
        construction_attempts=build_construction_feasibility(experiment_root, project_root, policy["construction_inputs"]),
    )
    validate_evaluation_packet(experiment_root, project_root, policy, packet)
    markdown = render_evaluation_markdown(packet)
    readiness = build_readiness(packet, policy=policy, markdown=markdown)
    validate_readiness(experiment_root, project_root, policy, packet, markdown, readiness)
    payloads = {
        str(outputs["packet"]): canonical_json_bytes(packet),
        str(outputs["markdown"]): markdown,
        str(outputs["readiness"]): canonical_json_bytes(readiness),
    }
    try:
        write_exact_descriptor_files(experiment_root, payloads)
    except FilesystemPolicyError as error:
        raise EvaluationError("EVALUATION_OUTPUT_PARTIAL_OR_OCCUPIED") from error
    return packet, markdown, readiness


def _response_map(value: object, expected: set[str], code: str) -> dict[str, str]:
    if not isinstance(value, Mapping) or set(value) != expected:
        _error(code)
    result = {str(key): item for key, item in value.items()}
    if any(not isinstance(item, str) or item not in _RESPONSE_VALUES for item in result.values()):
        _error(code)
    return result


def _validate_disputes(value: object, domain_ids: set[str], item_ids: set[str]) -> list[dict[str, object]]:
    if not isinstance(value, list):
        _error("REVIEW_DECISION_DISPUTES_INVALID")
    normalized: list[dict[str, object]] = []
    for dispute in value:
        if not isinstance(dispute, Mapping) or set(dispute) != {"blocking", "reason", "response", "target_id", "target_type"}:
            _error("REVIEW_DECISION_DISPUTES_INVALID")
        target_type, target_id = dispute.get("target_type"), dispute.get("target_id")
        valid_target = (target_type == "domain" and target_id in domain_ids) or (target_type == "item" and target_id in item_ids)
        if not valid_target or not isinstance(dispute.get("blocking"), bool) or dispute.get("response") not in {"disputed", "incomplete"}:
            _error("REVIEW_DECISION_DISPUTES_INVALID")
        if not isinstance(dispute.get("reason"), str) or not dispute["reason"].strip():
            _error("REVIEW_DECISION_DISPUTES_INVALID")
        normalized.append(dict(dispute))
    return normalized


def _review_targets(packet: Mapping[str, object]) -> tuple[set[str], set[str]]:
    rows = packet.get("case_rows")
    if not isinstance(rows, list):
        _error("REVIEW_DECISION_TARGETS_INVALID")
    domain_ids = {row.get("authority_domain") for row in rows if isinstance(row, Mapping)}
    item_ids = {row.get("outcome_id") for row in rows if isinstance(row, Mapping)}
    if not domain_ids or not item_ids or not all(isinstance(value, str) for value in domain_ids | item_ids):
        _error("REVIEW_DECISION_TARGETS_INVALID")
    return domain_ids, item_ids


def _decision_payload(
    *, packet: Mapping[str, object], readiness: Mapping[str, object], reviewer_id: str,
    disposition: str, domain_responses: Mapping[str, str], item_responses: Mapping[str, str],
    disputes: Sequence[Mapping[str, object]], d16_acknowledgement: bool,
    mutation_requests: Sequence[object] = (),
) -> dict[str, object]:
    if mutation_requests:
        _error("SUCCESSOR_REQUIRED_SAME_VERSION_MUTATION")
    if not isinstance(reviewer_id, str) or not reviewer_id.strip() or disposition not in _RESPONSE_VALUES:
        _error("REVIEW_DECISION_INVALID")
    if d16_acknowledgement is not True:
        _error("REVIEW_DECISION_D16_ACK_REQUIRED")
    domains, items = _review_targets(packet)
    checked_domains = _response_map(domain_responses, domains, "REVIEW_DECISION_DOMAIN_RESPONSES_INVALID")
    checked_items = _response_map(item_responses, items, "REVIEW_DECISION_ITEM_RESPONSES_INVALID")
    checked_disputes = _validate_disputes(list(disputes), domains, items)
    response_values = set(checked_domains.values()) | set(checked_items.values())
    if disposition == "approved" and (response_values != {"approved"} or checked_disputes):
        _error("REVIEW_DECISION_APPROVAL_INVALID")
    if disposition != "approved" and not checked_disputes:
        _error("REVIEW_DECISION_DISPUTES_REQUIRED")
    blocking = any(bool(entry["blocking"]) for entry in checked_disputes)
    ready = disposition == "approved" and not blocking
    return {
        "schema_version": _DECISION_SCHEMA,
        "generation_id": packet["generation_id"],
        "packet_sha256": packet["packet_sha256"],
        "readiness_sha256": readiness["readiness_sha256"],
        "reviewer_id": reviewer_id,
        "disposition": disposition,
        "domain_responses": checked_domains,
        "item_responses": checked_items,
        "disputes": checked_disputes,
        "conclusion_ready": ready,
        "phase7_interpretation_authorized": ready,
        "authority_limits": dict(_DECISION_LIMITS),
        "d16_acknowledgement": True,
    }


def build_review_decision(
    experiment_root: Path, project_root: Path, policy: Mapping[str, object], *, reviewer_id: str, disposition: str,
    domain_responses: Mapping[str, str], item_responses: Mapping[str, str],
    disputes: Sequence[Mapping[str, object]], d16_acknowledgement: bool,
    mutation_requests: Sequence[object] = (),
) -> ReviewDecision:
    """Build a closed decision from a human response and the validated package only."""
    outputs = policy.get("outputs")
    if not isinstance(outputs, Mapping):
        _error("EVALUATION_POLICY_OUTPUTS_INVALID")
    try:
        packet = json.loads((experiment_root / str(outputs["packet"])).read_text(encoding="utf-8"))
        markdown = (experiment_root / str(outputs["markdown"])).read_bytes()
        readiness = json.loads((experiment_root / str(outputs["readiness"])).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise EvaluationError("EVALUATION_OUTPUT_PARTIAL_OR_OCCUPIED") from error
    validate_readiness(experiment_root, project_root, policy, packet, markdown, readiness)
    payload = _decision_payload(
        packet=packet, readiness=readiness, reviewer_id=reviewer_id, disposition=disposition,
        domain_responses=domain_responses, item_responses=item_responses, disputes=disputes,
        d16_acknowledgement=d16_acknowledgement, mutation_requests=mutation_requests,
    )
    payload["decision_sha256"] = sha256_bytes(canonical_json_bytes(payload))
    return ReviewDecision(**payload)


def validate_review_decision(
    experiment_root: Path, project_root: Path, policy: Mapping[str, object], decision: Mapping[str, object],
) -> ReviewDecision:
    """Revalidate both upstream identities and the complete closed response record."""
    if not isinstance(decision, Mapping) or decision.get("schema_version") != _DECISION_SCHEMA:
        _error("REVIEW_DECISION_INVALID")
    _self_hash(decision, "decision_sha256", "REVIEW_DECISION_HASH_INVALID")
    payload = build_review_decision(
        experiment_root, project_root, policy, reviewer_id=decision.get("reviewer_id", ""), disposition=decision.get("disposition", ""),
        domain_responses=decision.get("domain_responses", {}), item_responses=decision.get("item_responses", {}),
        disputes=decision.get("disputes", []), d16_acknowledgement=decision.get("d16_acknowledgement", False),
    )
    if dict(decision) != asdict(payload):
        _error("REVIEW_DECISION_INVALID")
    return payload


def publish_review_decision(
    experiment_root: Path, project_root: Path, policy: Mapping[str, object], decision: ReviewDecision, path: str,
) -> ReviewDecision:
    """Publish exactly one canonical decision, allowing only byte-identical resume."""
    validate_review_decision(experiment_root, project_root, policy, asdict(decision))
    try:
        write_exact_descriptor_files(experiment_root, {path: canonical_json_bytes(asdict(decision))})
    except FilesystemPolicyError as error:
        raise EvaluationError("REVIEW_DECISION_PARTIAL_OR_OCCUPIED") from error
    return decision

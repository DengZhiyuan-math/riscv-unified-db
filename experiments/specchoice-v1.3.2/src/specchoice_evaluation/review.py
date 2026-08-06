# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Decision-free reviewer projections for a validated Red evaluation."""

from __future__ import annotations

from collections.abc import Mapping

from specchoice_evidence.canonical import canonical_json_bytes, sha256_bytes

from .core import EvaluationBundle


def build_evaluation_packet(bundle: EvaluationBundle) -> dict[str, object]:
    """Bind a packet identity without selecting a human disposition."""
    payload = bundle.as_dict()
    payload["packet_kind"] = "partition-evaluation-red-review-packet-v1"
    payload["packet_sha256"] = sha256_bytes(canonical_json_bytes(payload))
    return payload


def render_evaluation_markdown(packet: Mapping[str, object]) -> bytes:
    """Render a deterministic, non-authoritative Red-first reviewer view."""
    authority = packet["red_execution_evidence"]
    assert isinstance(authority, Mapping)
    body = (
        "# Red authority\n\n"
        f"- Branch: `{packet['branch']}`\n"
        f"- N_strict: `{packet['n_strict']}`\n"
        f"- repeat_count: `{packet['repeat_count']}`\n"
        f"- verified_no_model_calls: `{packet['no_model_calls']}`\n"
        f"- Red evidence authority: `{authority['source_sha256']}`\n\n"
        "# Applicability matrix\n\n"
        "```json\n"
    )
    return body.encode("utf-8") + canonical_json_bytes(packet["applicability_matrix"]) + b"```\n"


def build_readiness(packet: Mapping[str, object]) -> dict[str, object]:
    """Return a machine readiness identity only; it is never approval."""
    packet_sha256 = packet.get("packet_sha256")
    if not isinstance(packet_sha256, str):
        raise TypeError("EVALUATION_PACKET_HASH_INVALID")
    payload = {
        "packet_sha256": packet_sha256,
        "schema_version": "partition-evaluation-red-readiness-v1",
        "status": "ready_for_human_review",
    }
    return {**payload, "readiness_sha256": sha256_bytes(canonical_json_bytes(payload))}

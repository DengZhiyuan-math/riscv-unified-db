# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Strict local entry point for the decision-free Red evaluator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from specchoice_evidence.canonical import canonical_json_bytes

from .core import EvaluationError, build_red_evaluation
from .review import (
    build_evaluation_packet,
    build_readiness,
    publish_evaluation_package,
    validate_evaluation_policy,
    validate_readiness,
    validate_review_decision,
)


class _NoAbbrevParser(argparse.ArgumentParser):
    def __init__(self, *args: object, **kwargs: object) -> None:
        kwargs["allow_abbrev"] = False
        super().__init__(*args, **kwargs)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="specchoice-evaluation", allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=_NoAbbrevParser)
    for name, handler in (("build-red", _build_red), ("verify-red-package", _verify_red_package)):
        command = commands.add_parser(name)
        command.add_argument("--repo-root", required=True)
        command.add_argument("--policy", required=True)
        command.set_defaults(handler=handler)
    decision = commands.add_parser("validate-decision")
    decision.add_argument("--repo-root", required=True)
    decision.add_argument("--policy", required=True)
    decision.add_argument("--decision", required=True)
    decision.set_defaults(handler=_validate_decision)
    return parser


def _load_policy(path: str) -> dict[str, object]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise EvaluationError("EVALUATION_POLICY_INVALID") from error
    if not isinstance(value, dict) or value.get("schema_version") != "partition-evaluation-policy-v1":
        raise EvaluationError("EVALUATION_POLICY_INVALID")
    return value


def _build_red(args: argparse.Namespace) -> int:
    root, policy = Path(args.repo_root).resolve(), _load_policy(args.policy)
    # Preserve the pre-publication diagnostic surface used by the earlier Phase 6 contract.
    if set(policy) == {"schema_version"}:
        bundle = build_red_evaluation(root)
        packet = build_evaluation_packet(bundle)
        readiness = build_readiness(packet)
        print(canonical_json_bytes({"branch": bundle.branch, "packet": packet, "readiness": readiness}).decode("utf-8"), end="")
        return 0
    packet, _markdown, readiness = publish_evaluation_package(root, policy)
    print(canonical_json_bytes({
        "branch": packet["branch"], "markdown_sha256": readiness["markdown_sha256"],
        "packet_sha256": packet["packet_sha256"], "readiness_sha256": readiness["readiness_sha256"],
    }).decode("utf-8"), end="")
    return 0


def _verify_red_package(args: argparse.Namespace) -> int:
    root, policy = Path(args.repo_root).resolve(), _load_policy(args.policy)
    validate_evaluation_policy(root, policy)
    outputs = policy["outputs"]
    assert isinstance(outputs, dict)
    try:
        packet = json.loads((root / str(outputs["packet"])).read_text(encoding="utf-8"))
        markdown = (root / str(outputs["markdown"])).read_bytes()
        readiness = json.loads((root / str(outputs["readiness"])).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise EvaluationError("EVALUATION_OUTPUT_PARTIAL_OR_OCCUPIED") from error
    validate_readiness(root, policy, packet, markdown, readiness)
    print(canonical_json_bytes({"packet_sha256": packet["packet_sha256"], "readiness_sha256": readiness["readiness_sha256"]}).decode("utf-8"), end="")
    return 0


def _validate_decision(args: argparse.Namespace) -> int:
    root, policy = Path(args.repo_root).resolve(), _load_policy(args.policy)
    try:
        decision = json.loads((root / args.decision).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise EvaluationError("REVIEW_DECISION_INVALID") from error
    validated = validate_review_decision(root, policy, decision)
    print(canonical_json_bytes({
        "conclusion_ready": validated.conclusion_ready,
        "decision_sha256": validated.decision_sha256,
        "phase7_interpretation_authorized": validated.phase7_interpretation_authorized,
    }).decode("utf-8"), end="")
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        return int(args.handler(args))
    except (EvaluationError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

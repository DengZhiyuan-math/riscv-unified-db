# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Strict local entry point for the decision-free Red evaluator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from specchoice_evidence.canonical import canonical_json_bytes

from .core import EvaluationError, build_red_evaluation
from .review import build_evaluation_packet, build_readiness


class _NoAbbrevParser(argparse.ArgumentParser):
    def __init__(self, *args: object, **kwargs: object) -> None:
        kwargs["allow_abbrev"] = False
        super().__init__(*args, **kwargs)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="specchoice-evaluation", allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=_NoAbbrevParser)
    command = commands.add_parser("build-red")
    command.add_argument("--repo-root", required=True)
    command.add_argument("--policy", required=True)
    command.set_defaults(handler=_build_red)
    return parser


def _build_red(args: argparse.Namespace) -> int:
    policy = Path(args.policy)
    try:
        value = json.loads(policy.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise EvaluationError("EVALUATION_POLICY_INVALID") from error
    if not isinstance(value, dict) or value.get("schema_version") != "partition-evaluation-policy-v1":
        raise EvaluationError("EVALUATION_POLICY_INVALID")
    bundle = build_red_evaluation(Path(args.repo_root))
    packet = build_evaluation_packet(bundle)
    readiness = build_readiness(packet)
    print(canonical_json_bytes({"branch": bundle.branch, "packet": packet, "readiness": readiness}).decode("utf-8"), end="")
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

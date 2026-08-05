# SPDX-License-Identifier: BSD-3-Clause-Clear
"""The sole closed production entry point for the Red v2 contract."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from specchoice_evidence.canonical import canonical_json_bytes

from .red_v2 import RedExecutionV2Error, execute_red_v2


class _NoAbbrevParser(argparse.ArgumentParser):
    def __init__(self, *args: object, **kwargs: object) -> None:
        kwargs["allow_abbrev"] = False
        super().__init__(*args, **kwargs)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="specchoice-execution-v2", allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=_NoAbbrevParser)
    command = commands.add_parser("execute-red")
    for name in ("repo-root", "policy", "authority", "packet", "readiness", "decision", "attempt-root", "formal-root", "receipt", "report"):
        command.add_argument(f"--{name}", required=True)
    command.set_defaults(handler=_execute_red)
    return parser


def _execute_red(args: argparse.Namespace) -> int:
    if args.repo_root != ".":
        raise RedExecutionV2Error("RED_ARGUMENT_MISMATCH")
    supplied = {"policy": args.policy, "authority": args.authority, "packet": args.packet, "readiness": args.readiness, "decision": args.decision, "attempt_root": args.attempt_root, "formal_root": args.formal_root, "receipt": args.receipt, "report": args.report}
    receipt = execute_red_v2(root=Path("."), supplied_paths=supplied)
    print(canonical_json_bytes(receipt).decode("utf-8"), end="")
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        return int(args.handler(args))
    except (RedExecutionV2Error, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

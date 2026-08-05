# SPDX-License-Identifier: BSD-3-Clause-Clear
"""The intentionally closed temporary Red-execution CLI."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from specchoice_evidence.canonical import canonical_json_bytes
from specchoice_evidence.filesystem import (
    FilesystemPolicyError,
    require_relative_posix_path,
)

from .red import RedExecutionError, build_red_evidence_v1

_EXPERIMENT_ROOT = Path(__file__).resolve().parents[2]


def _execute_red_temporary(args: argparse.Namespace) -> int:
    relative = require_relative_posix_path(args.target)
    result = build_red_evidence_v1(root=_EXPERIMENT_ROOT, output_root=_EXPERIMENT_ROOT / relative)
    sys.stdout.buffer.write(canonical_json_bytes(result))
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Expose exactly one no-provider/no-model command with no abbreviation."""
    parser = argparse.ArgumentParser(prog="specchoice-execution", allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("execute-red-temporary", allow_abbrev=False)
    command.add_argument("--target", required=True)
    command.set_defaults(handler=_execute_red_temporary)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Write canonical stdout only for a validated result; errors use exit 2."""
    try:
        args = build_parser().parse_args(argv)
        return int(args.handler(args))
    except (FilesystemPolicyError, RedExecutionError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    except SystemExit as error:
        return int(error.code)


if __name__ == "__main__":
    raise SystemExit(main())

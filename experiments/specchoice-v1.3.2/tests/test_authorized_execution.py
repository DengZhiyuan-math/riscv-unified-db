# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Red-only execution closure tests."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from specchoice_evidence.canonical import canonical_json_bytes
from specchoice_execution.red import (
    RedExecutionError,
    build_red_evidence_v1,
    validate_red_evidence_v1,
)


class AuthorizedExecutionTests(unittest.TestCase):
    """Exercise the complete no-call path only in disposable roots."""

    maxDiff = None

    def setUp(self) -> None:
        self.experiment = Path(__file__).parents[1]

    def _copy_experiment(self, directory: str) -> Path:
        destination = Path(directory) / "experiment"
        shutil.copytree(
            self.experiment,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"),
        )
        return destination

    def test_exact_v6_tracer_publishes_complete_temporary_red_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            target = Path(directory) / "temporary-evidence"
            target.mkdir()
            result = build_red_evidence_v1(root=root, output_root=target)

            self.assertEqual("completed", result["status"])
            self.assertEqual("red", result["matrix"]["branch"])
            self.assertEqual([], result["model_call_ledger"]["calls"])
            self.assertFalse(result["permissions"]["model_execution_authorized"])
            self.assertEqual(
                ["phase6_red_evidence_evaluation", "phase7_red_evidence_evaluation"],
                result["permissions"]["granted_downstream_permissions"],
            )
            self.assertEqual(result, validate_red_evidence_v1(root=target))
            self.assertTrue((target / "runs/red-execution-v1/terminal-receipt.json").is_file())
            self.assertFalse((self.experiment / "runs/red-execution-v1").exists())

    def test_ts07_distinct_nonempty_spans_and_explicit_empty_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            target = Path(directory) / "target"
            target.mkdir()
            result = build_red_evidence_v1(root=root, output_root=target)
            self.assertEqual([], result["parsed_evidence"]["findings"])
            self.assertEqual("explicit_empty_set", result["parsed_evidence"]["empty_set"])
            self.assertEqual([], result["evidence_span_audit"]["findings"])

            invalid = dict(result)
            invalid["evidence_span_audit"] = {
                "findings": [{"finding_id": "F-1", "spans": []}],
                "schema_version": "red-evidence-span-audit-v1",
            }
            with self.assertRaisesRegex(RedExecutionError, "RED_SURFACED_EMPTY_SPAN"):
                validate_red_evidence_v1(value=invalid)

    def test_zero_matrix_and_conditional_requirement_states(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            target.mkdir()
            result = build_red_evidence_v1(root=self._copy_experiment(directory), output_root=target)
            matrix = result["matrix"]
            self.assertEqual(0, matrix["expected_cells"])
            self.assertEqual("0*3*0=0", matrix["formula"])
            self.assertEqual([], matrix["cells"])
            for treatment in ("A", "B", "C"):
                self.assertEqual(
                    {"attempted": 0, "completed": 0, "expected": 0, "failed": 0, "retried": 0},
                    matrix["partitions"][treatment],
                )
            self.assertEqual(
                "conditional_not_applicable_red_pending_phase7",
                result["requirements"]["TS-11"],
            )
            self.assertEqual(
                "conditional_not_applicable_red_pending_phase7",
                result["requirements"]["TS-12"],
            )

    def test_identical_temporary_resume_is_zero_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            target = Path(directory) / "target"
            target.mkdir()
            first = build_red_evidence_v1(root=root, output_root=target)
            writes = 0

            def observe_write() -> None:
                nonlocal writes
                writes += 1

            second = build_red_evidence_v1(
                root=root, output_root=target, write_observer=observe_write
            )
            self.assertEqual(first, second)
            self.assertEqual(0, writes)
            self.assertEqual(
                canonical_json_bytes(first), canonical_json_bytes(second)
            )


if __name__ == "__main__":
    unittest.main()

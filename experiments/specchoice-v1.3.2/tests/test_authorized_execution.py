# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Red-only execution closure tests."""

from __future__ import annotations

import shutil
import socket
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from specchoice_evidence.canonical import canonical_json_bytes
from specchoice_execution.red import (
    RedExecutionError,
    audit_red_execution_surface_v1,
    build_red_evidence_v1,
    deny_all_sockets_v1,
    execute_red_with_attempt_custody_v1,
    validate_red_evidence_v1,
)
from specchoice_measurement.strict_json import decode_strict_json


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

    def test_all_socket_constructors_and_address_classes_fail_closed(self) -> None:
        constructors = (
            lambda: socket.socket(),
            lambda: socket.create_connection(("127.0.0.1", 1)),
            lambda: socket.create_server(("192.168.1.2", 0)),
            lambda: socket.socketpair(),
            lambda: socket.fromfd(0, socket.AF_INET, socket.SOCK_STREAM),
        )
        events: list[dict[str, object]] = []
        with deny_all_sockets_v1(events):
            for constructor in constructors:
                with self.assertRaisesRegex(RedExecutionError, "RED_SOCKET_DENIED"):
                    constructor()
        self.assertEqual(5, len(events))
        self.assertTrue(all(event["code"] == "RED_SOCKET_DENIED" for event in events))

    def test_blocked_operations_are_security_events_not_calls(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            target = Path(directory) / "target"
            target.mkdir()
            with self.assertRaisesRegex(RedExecutionError, "RED_SOCKET_DENIED") as caught:
                build_red_evidence_v1(
                    root=root,
                    output_root=target,
                    socket_probe=lambda: socket.create_connection(("203.0.113.1", 443)),
                )
            failed_attempt = caught.exception.failed_attempt
            self.assertEqual([], failed_attempt["model_call_ledger"]["calls"])
            self.assertEqual(False, failed_attempt["authoritative"])
            self.assertEqual(False, failed_attempt["metrics_emitted"])
            self.assertEqual("RED_SOCKET_DENIED", failed_attempt["security_events"][0]["code"])
            self.assertEqual(set(), set(target.iterdir()))

    def test_phase5_structural_scan_covers_cli_config_dependencies_and_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            audit = audit_red_execution_surface_v1(root)
            self.assertEqual([], audit["forbidden_findings"])
            source = root / "src/specchoice_execution/cli.py"
            source.write_text(source.read_text(encoding="utf-8") + "\nimport requests\n", encoding="utf-8")
            with self.assertRaisesRegex(RedExecutionError, "RED_FORBIDDEN_SURFACE"):
                audit_red_execution_surface_v1(root)

    def test_checkpoint_inventory_matches_policy_and_no_formal_target_exists(self) -> None:
        policy = decode_strict_json(
            (self.experiment / "config/execution/red-execution-policy-v1.json").read_bytes()
        )
        self.assertIsInstance(policy, dict)
        assert isinstance(policy, dict)
        self.assertEqual(
            sorted(policy["output_paths"]),
            policy["output_paths"],
        )
        for path in policy["output_paths"]:
            self.assertFalse((self.experiment / path).exists(), path)
        self.assertFalse((self.experiment / "receipts/red-execution-v1.json").exists())
        self.assertFalse((self.experiment / "reports/red-execution").exists())

    def test_every_failure_has_immutable_non_authoritative_custody(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            formal = Path(directory) / "formal"
            formal.mkdir()
            with self.assertRaisesRegex(RedExecutionError, "RED_SOCKET_DENIED") as caught:
                execute_red_with_attempt_custody_v1(
                    root=root,
                    output_root=formal,
                    socket_probe=lambda: socket.socket(),
                )
            failed = caught.exception.failed_attempt
            assert failed is not None
            self.assertEqual("attempt-000001", failed["attempt_id"])
            self.assertFalse(failed["authoritative"])
            self.assertFalse(failed["metrics_emitted"])
            self.assertEqual([], failed["model_call_ledger"]["calls"])
            self.assertEqual("RED_SOCKET_DENIED", failed["security_events"][0]["code"])
            attempt = root / "runs/red-attempts/attempt-000001"
            self.assertEqual(
                {
                    "attempt.json", "frozen-inputs.json", "model-call-ledger.json",
                    "observed-differences.json", "ordered-diagnostics.json",
                    "raw-custody.json", "security-events.json",
                },
                {path.name for path in attempt.iterdir()},
            )
            before = {path.name: path.read_bytes() for path in attempt.iterdir()}
            with self.assertRaisesRegex(RedExecutionError, "RED_SOCKET_DENIED"):
                execute_red_with_attempt_custody_v1(
                    root=root,
                    output_root=formal,
                    socket_probe=lambda: socket.socket(),
                )
            self.assertEqual(before, {path.name: path.read_bytes() for path in attempt.iterdir()})
            self.assertTrue((root / "runs/red-attempts/attempt-000002").is_dir())
            self.assertFalse((formal / "runs/red-execution-v1").exists())

    def test_retries_are_contiguous_append_only_and_input_identical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            formal = Path(directory) / "formal"
            formal.mkdir()
            for _ in range(2):
                with self.assertRaisesRegex(RedExecutionError, "RED_SOCKET_DENIED"):
                    execute_red_with_attempt_custody_v1(
                        root=root, output_root=formal, socket_probe=lambda: socket.socket()
                    )
            attempt_root = root / "runs/red-attempts"
            first = attempt_root / "attempt-000001/attempt.json"
            first.write_bytes(canonical_json_bytes({"tampered": True}))
            with self.assertRaisesRegex(RedExecutionError, "RED_ATTEMPT_CHAIN_INVALID"):
                execute_red_with_attempt_custody_v1(
                    root=root, output_root=formal, socket_probe=lambda: socket.socket()
                )

    def test_drift_builds_decision_free_successor_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            formal = Path(directory) / "formal"
            formal.mkdir()
            expected = execute_red_with_attempt_custody_v1(
                root=root, output_root=Path(directory) / "temporary"
            )["frozen_inputs"]
            changed = deepcopy(expected)
            changed["policy_sha256"] = "0" * 64
            with self.assertRaisesRegex(RedExecutionError, "RED_FROZEN_INPUT_DRIFT"):
                execute_red_with_attempt_custody_v1(
                    root=root,
                    output_root=formal,
                    expected_frozen_inputs=changed,
                )
            successor = root / "runs/red-successors/successor-001"
            self.assertEqual(
                {"candidate-closure.json", "observed-differences.json", "readiness.json"},
                {path.name for path in successor.iterdir()},
            )
            readiness = decode_strict_json((successor / "readiness.json").read_bytes())
            self.assertEqual(False, readiness["authoritative"])
            self.assertEqual(False, readiness["metrics_emitted"])
            self.assertNotIn("authority", readiness)
            self.assertFalse((formal / "runs/red-execution-v1").exists())

    def test_clean_success_leaves_conditional_namespaces_absent_and_roles_confined(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            formal = Path(directory) / "formal"
            formal.mkdir()
            result = execute_red_with_attempt_custody_v1(root=root, output_root=formal)
            self.assertEqual("completed", result["status"])
            self.assertFalse((root / "runs/red-attempts").exists())
            self.assertFalse((root / "runs/red-successors").exists())
            self.assertEqual([], result["attempt_chain"]["attempts"])

    def test_occupied_partial_symlink_interrupted_and_concurrent_targets_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            formal = Path(directory) / "formal"
            formal.mkdir()
            partial = formal / "runs/red-execution-v1"
            partial.mkdir(parents=True)
            (partial / "manifest.json").write_bytes(b"{}\n")
            with self.assertRaisesRegex(RedExecutionError, "RED_OUTPUT_PARTIAL_OR_OCCUPIED"):
                execute_red_with_attempt_custody_v1(root=root, output_root=formal)
            self.assertTrue((root / "runs/red-attempts/attempt-000001").is_dir())
            self.assertEqual(b"{}\n", (partial / "manifest.json").read_bytes())


if __name__ == "__main__":
    unittest.main()

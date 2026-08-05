# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Copied-root contracts for the forward-only Red v2 executor."""

from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import socket
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from specchoice_evidence.canonical import canonical_json_bytes, sha256_bytes
from specchoice_execution.red_v2 import (
    RedExecutionV2Error,
    audit_red_execution_surface_v2,
    build_gate_a_projection_v2,
    deny_all_sockets_v2,
)


EXPERIMENT = Path(__file__).resolve().parents[1]
POLICY = "config/execution/red-execution-policy-v2.json"
AUTHORITY = "phase4/branch-authority-v6.json"
PACKET = "reports/h3/h3-red-review-v6/review-packet.json"
READINESS = "receipts/h3-branch-readiness-v6.json"
DECISION = "reviews/h3-branch-decision-v6.json"
ATTEMPTS = "runs/red-attempts-v2"
FORMAL = "runs/red-execution-v2"
RECEIPT = "receipts/red-execution-v2.json"
REPORT = "reports/red-execution/red-execution-v2.md"


class AuthorizedExecutionV2Tests(unittest.TestCase):
    def _copy_experiment(self, directory: str) -> Path:
        root = Path(directory) / "experiment"
        shutil.copytree(EXPERIMENT, root, ignore=shutil.ignore_patterns("__pycache__"))
        return root

    def _argv(self) -> list[str]:
        return [
            "execute-red", "--repo-root", ".", "--policy", POLICY,
            "--authority", AUTHORITY, "--packet", PACKET, "--readiness", READINESS,
            "--decision", DECISION, "--attempt-root", ATTEMPTS, "--formal-root", FORMAL,
            "--receipt", RECEIPT, "--report", REPORT,
        ]

    def _run(self, root: Path, argv: list[str] | None = None) -> tuple[int, str, str]:
        from specchoice_execution.cli_v2 import main

        stdout, stderr = io.StringIO(), io.StringIO()
        previous = Path.cwd()
        try:
            os.chdir(root)
            with redirect_stdout(stdout), redirect_stderr(stderr):
                return main(argv or self._argv()), stdout.getvalue(), stderr.getvalue()
        finally:
            os.chdir(previous)

    def test_exact_execute_red_contract_publishes_complete_v2_set_in_copy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            code, stdout, stderr = self._run(root)
            self.assertEqual(0, code, stderr)
            receipt = canonical_json_bytes(json.loads(stdout))
            self.assertEqual(receipt, (root / RECEIPT).read_bytes())
            expected = {
                "attempt-chain.json", "evidence-span-audit.json", "matrix-manifest.json",
                "model-call-ledger.json", "no-call-runtime-audit.json", "no-call-structural-audit.json",
                "ordered-diagnostics.json", "parsed-evidence.json", "raw-evidence.json", "red-trigger-evidence.json",
            }
            self.assertEqual(expected, {path.name for path in (root / FORMAL).iterdir()})
            self.assertTrue((root / REPORT).is_file())
            self.assertEqual("completed", json.loads(stdout)["status"])
            for protected in ("runs/red-execution-v1", "runs/red-attempts", "runs/red-successors"):
                self.assertFalse((root / protected).exists())
            for actual in (FORMAL, ATTEMPTS, RECEIPT, REPORT):
                self.assertFalse((EXPERIMENT / actual).exists())

    def test_gate_a_projection_recomputes_non_circular_policy_and_closure_hashes(self) -> None:
        projection = build_gate_a_projection_v2(EXPERIMENT)
        raw = (EXPERIMENT / POLICY).read_bytes()
        self.assertEqual(sha256_bytes(raw), projection["policy_entry"]["sha256"])
        self.assertEqual(len(raw), projection["policy_entry"]["byte_length"])
        entries = projection["runtime_closure_basis"]["entries"]
        self.assertEqual(sorted(item["path"] for item in entries), [item["path"] for item in entries])
        self.assertNotIn(POLICY, [item["path"] for item in entries])
        self.assertEqual(
            sha256_bytes(canonical_json_bytes(projection["runtime_closure_basis"])),
            projection["runtime_closure_sha256"],
        )
        basis = dict(projection)
        observed = basis.pop("gate_a_projection_sha256")
        self.assertEqual(sha256_bytes(canonical_json_bytes(basis)), observed)

    def test_policy_self_reference_and_projection_recursion_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            value = json.loads((root / POLICY).read_text())
            value["policy_sha256"] = "0" * 64
            (root / POLICY).write_bytes(canonical_json_bytes(value))
            with self.assertRaisesRegex(RedExecutionV2Error, "RED_POLICY_SELF_REFERENCE"):
                build_gate_a_projection_v2(root)
            self.assertFalse((root / FORMAL).exists())

    def test_input_and_target_mismatch_fails_before_writer_or_socket(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            argv = self._argv()
            argv[argv.index("--report") + 1] = "reports/redirect.md"
            code, _stdout, stderr = self._run(root, argv)
            self.assertEqual(2, code)
            self.assertIn("RED_ARGUMENT_MISMATCH", stderr)
            self.assertFalse((root / FORMAL).exists())

    def test_v1_bytes_and_namespaces_are_unchanged(self) -> None:
        before = {
            path: hashlib.sha256((EXPERIMENT / path).read_bytes()).hexdigest()
            for path in (
                "config/execution/red-execution-policy-v1.json", "src/specchoice_execution/red.py",
                "src/specchoice_execution/cli.py", "src/specchoice_execution/__init__.py",
                "tests/test_authorized_execution.py",
            )
        }
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            self.assertEqual(0, self._run(root)[0])
        after = {path: hashlib.sha256((EXPERIMENT / path).read_bytes()).hexdigest() for path in before}
        self.assertEqual(before, after)

    def test_exact_replay_is_byte_identical_and_zero_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            self.assertEqual(0, self._run(root)[0])
            paths = [root / FORMAL / name for name in sorted(path.name for path in (root / FORMAL).iterdir())]
            paths.extend([root / RECEIPT, root / REPORT])
            before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in paths}
            self.assertEqual(0, self._run(root)[0])
            self.assertEqual(before, {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in paths})

    def test_partial_symlink_and_traversal_targets_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            partial = root / FORMAL
            partial.mkdir(parents=True)
            (partial / "attempt-chain.json").write_bytes(b"{}\n")
            self.assertEqual(2, self._run(root)[0])
            self.assertEqual(b"{}\n", (partial / "attempt-chain.json").read_bytes())
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            (root / "runs").mkdir(exist_ok=True)
            os.symlink("/tmp", root / FORMAL)
            self.assertEqual(2, self._run(root)[0])
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            argv = self._argv()
            argv[argv.index("--formal-root") + 1] = "runs/../escape"
            self.assertEqual(2, self._run(root, argv)[0])

    def test_all_socket_constructors_are_denied_without_real_calls(self) -> None:
        for name, call in (
            ("socket", lambda: socket.socket()),
            ("create_connection", lambda: socket.create_connection(("127.0.0.1", 1))),
            ("create_server", lambda: socket.create_server(("127.0.0.1", 0))),
            ("socketpair", socket.socketpair),
            ("fromfd", lambda: socket.fromfd(0, socket.AF_INET, socket.SOCK_STREAM)),
        ):
            events: list[dict[str, object]] = []
            with self.assertRaisesRegex(RedExecutionV2Error, "RED_SOCKET_DENIED"), deny_all_sockets_v2(events):
                call()
            self.assertEqual([{"code": "RED_SOCKET_DENIED", "constructor": name, "event": "socket_operation"}], events)

    def test_forbidden_surface_and_future_output_policy_membership_fail_before_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            cli = root / "src/specchoice_execution/cli_v2.py"
            cli.write_text(cli.read_text() + "\nimport openai\n")
            with self.assertRaisesRegex(RedExecutionV2Error, "RED_FORBIDDEN_SURFACE"):
                audit_red_execution_surface_v2(root)
            self.assertFalse((root / FORMAL).exists())
        with tempfile.TemporaryDirectory() as directory:
            root = self._copy_experiment(directory)
            value = json.loads((root / POLICY).read_text())
            value["closure_paths"].append("runs/red-execution-v2/attempt-chain.json")
            value["closure_paths"].sort()
            (root / POLICY).write_bytes(canonical_json_bytes(value))
            with self.assertRaisesRegex(RedExecutionV2Error, "RED_POLICY_SELF_REFERENCE"):
                build_gate_a_projection_v2(root)


if __name__ == "__main__":
    unittest.main()

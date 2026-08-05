# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Contract tests for the validation-only native guarded regression harness."""

from __future__ import annotations

import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

from validation import guarded_regress


class GuardedRegressTests(unittest.TestCase):
    def _root(self, directory: str) -> Path:
        root = Path(directory) / "repo"
        formal = root / "experiments/specchoice-v1.3.2/runs/red-execution-v2"
        formal.mkdir(parents=True)
        for filename in guarded_regress.FORMAL_FILENAMES:
            (formal / filename).write_text(f"{filename}\n")
        receipt = root / "experiments/specchoice-v1.3.2/receipts/red-execution-v2.json"
        report = root / "experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v2.md"
        receipt.parent.mkdir(parents=True)
        report.parent.mkdir(parents=True)
        receipt.write_text("{}\n")
        report.write_text("# Red\n")
        return root

    @staticmethod
    def _result(argv: list[str], code: int = 0) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(argv, code, stdout="out", stderr="err")

    def _guard_runner(
        self, *, harmless_code: int = 0, child_code: int = 0, network_code: int = 1, write_code: int = 1
    ):
        def run(argv: list[str], _cwd: Path, _env: dict[str, str]) -> subprocess.CompletedProcess[str]:
            command = argv[3:]
            if command == ["/usr/bin/true"]:
                return self._result(argv, harmless_code)
            if command[:2] == ["/usr/bin/python3", "-c"] and "socket.socket" in command[2]:
                return self._result(argv, network_code)
            if command[:2] == ["/usr/bin/python3", "-c"]:
                return self._result(argv, write_code)
            return self._result(argv, child_code)

        return run

    def test_unavailable_guard_fails_before_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._root(directory)
            with self.assertRaisesRegex(guarded_regress.GuardedRegressError, "NATIVE_GUARD_UNAVAILABLE"):
                guarded_regress.run_guarded_command(
                    root, runner=self._guard_runner(), guard_path=Path("/missing/sandbox-exec")
                )

    def test_bad_or_nonfunctional_profile_fails_before_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._root(directory)
            with self.assertRaisesRegex(guarded_regress.GuardedRegressError, "NATIVE_GUARD_NONFUNCTIONAL"):
                guarded_regress.run_guarded_command(root, runner=self._guard_runner(harmless_code=1))
            with self.assertRaisesRegex(guarded_regress.GuardedRegressError, "NETWORK_PROBE_NOT_DENIED"):
                guarded_regress.run_guarded_command(root, runner=self._guard_runner(network_code=0))
            with self.assertRaisesRegex(guarded_regress.GuardedRegressError, "WRITE_PROBE_NOT_DENIED"):
                guarded_regress.run_guarded_command(root, runner=self._guard_runner(write_code=0))

    def test_prohibited_child_result_is_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._root(directory)
            with self.assertRaisesRegex(guarded_regress.GuardedRegressError, "CHILD_FAILED returncode=-9"):
                guarded_regress.run_guarded_command(root, runner=self._guard_runner(child_code=-9))

    def test_evidence_change_addition_and_removal_fail(self) -> None:
        for mutation in ("change", "addition", "removal"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = self._root(directory)

                def runner_for(case: str):
                    def run(argv: list[str], cwd: Path, _env: dict[str, str]) -> subprocess.CompletedProcess[str]:
                        command = argv[3:]
                        if command == ["/usr/bin/true"]:
                            return self._result(argv)
                        if command[:2] == ["/usr/bin/python3", "-c"]:
                            return self._result(argv, 1)
                        formal = cwd / "experiments/specchoice-v1.3.2/runs/red-execution-v2"
                        if case == "change":
                            (formal / guarded_regress.FORMAL_FILENAMES[0]).write_text("changed\n")
                        elif case == "addition":
                            (formal / "extra.json").write_text("extra\n")
                        else:
                            (formal / guarded_regress.FORMAL_FILENAMES[0]).unlink()
                        return self._result(argv)

                    return run

                with self.assertRaisesRegex(guarded_regress.GuardedRegressError, "EVIDENCE_MUTATED"):
                    guarded_regress.run_guarded_command(root, runner=runner_for(mutation))

    def test_unchanged_fake_local_command_succeeds_without_network(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._root(directory)
            fake = root / "bin/regress"
            fake.parent.mkdir()
            fake.write_text("#!/bin/sh\nexit 0\n")
            fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
            original = guarded_regress._SANDBOX_EXEC
            self.addCleanup(setattr, guarded_regress, "_SANDBOX_EXEC", original)
            guarded_regress._SANDBOX_EXEC = Path("/usr/bin/sandbox-exec")
            record = guarded_regress.run_guarded_command(root, runner=self._guard_runner())
            self.assertEqual(("./bin/regress", "--all"), record.argv)
            self.assertEqual(0, record.returncode)


if __name__ == "__main__":
    unittest.main()

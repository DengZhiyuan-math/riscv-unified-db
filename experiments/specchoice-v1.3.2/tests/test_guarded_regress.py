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
    _NETWORK_DENIED_STDOUT = "GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno=1 diagnostic=Operation not permitted\n"

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
        config = root / ".mise.toml"
        config.write_text("[tools]\n")
        self._mise_path = root / "fixed-cache/mise/mise-2026.7.5"
        self._mise_path.parent.mkdir(parents=True)
        self._mise_path.write_text("#!/bin/sh\nexit 0\n")
        self._mise_path.chmod(self._mise_path.stat().st_mode | stat.S_IXUSR)
        original_mise_path = guarded_regress._default_mise_path
        self.addCleanup(setattr, guarded_regress, "_default_mise_path", original_mise_path)
        guarded_regress._default_mise_path = lambda: self._mise_path
        return root

    @staticmethod
    def _result(
        argv: list[str], code: int = 0, *, stdout: str = "out", stderr: str = "err"
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(argv, code, stdout=stdout, stderr=stderr)

    def _guard_runner(
        self,
        *,
        harmless_code: int = 0,
        child_code: int = 0,
        mise_code: int = 0,
        network_code: int = 77,
        network_stdout: str = _NETWORK_DENIED_STDOUT,
        network_stderr: str = "",
        write_code: int = 1,
    ):
        def run(argv: list[str], _cwd: Path, _env: dict[str, str]) -> subprocess.CompletedProcess[str]:
            command = argv[3:]
            if command == ["/usr/bin/true"]:
                return self._result(argv, harmless_code)
            if command[:2] == ["/usr/bin/python3", "-c"] and "socket.socket" in command[2]:
                return self._result(argv, network_code, stdout=network_stdout, stderr=network_stderr)
            if command == [str(self._mise_path), "exec", "--", "bundle", "--version"]:
                return self._result(argv, mise_code)
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

    def test_network_preflight_requires_connect_to_fixed_loopback_port_zero(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._root(directory)
            observed: list[list[str]] = []
            default_runner = self._guard_runner()

            def runner(argv: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
                command = argv[3:]
                if command[:2] == ["/usr/bin/python3", "-c"] and "socket.socket" in command[2]:
                    observed.append(command)
                return default_runner(argv, cwd, env)

            guarded_regress.run_guarded_command(root, runner=runner)

            self.assertEqual(1, len(observed))
            probe = observed[0][2]
            self.assertIn("socket.socket(socket.AF_INET, socket.SOCK_STREAM)", probe)
            self.assertIn('s.connect(("127.0.0.1", 0))', probe)

    def test_network_preflight_accepts_only_calibrated_eperm_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._root(directory)
            guarded_regress.run_guarded_command(root, runner=self._guard_runner())

            for code, stdout, stderr in (
                (77, "GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno=1 diagnostic=Permission denied\n", ""),
                (77, self._NETWORK_DENIED_STDOUT, "unexpected\n"),
                (78, self._NETWORK_DENIED_STDOUT, ""),
            ):
                with self.subTest(code=code, stdout=stdout, stderr=stderr), self.assertRaisesRegex(
                    guarded_regress.GuardedRegressError, "NETWORK_PROBE_NOT_DENIED"
                ):
                    guarded_regress.run_guarded_command(
                        root,
                        runner=self._guard_runner(network_code=code, network_stdout=stdout, network_stderr=stderr),
                    )

    def test_network_preflight_rejects_connect_success_and_ambiguous_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._root(directory)
            for code, stdout in (
                (0, "GUARDED_REGRESS_NETWORK_CONNECT_SUCCEEDED\n"),
                (78, "GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno=111 diagnostic=Connection refused\n"),
                (-9, ""),
            ):
                with self.subTest(code=code, stdout=stdout), self.assertRaisesRegex(
                    guarded_regress.GuardedRegressError, "NETWORK_PROBE_NOT_DENIED"
                ):
                    guarded_regress.run_guarded_command(
                        root, runner=self._guard_runner(network_code=code, network_stdout=stdout)
                    )

    def test_missing_mise_fails_before_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._root(directory)
            missing_mise = root / "missing-cache/mise/mise-2026.7.5"
            with self.assertRaisesRegex(guarded_regress.GuardedRegressError, "MISE_TOOLCHAIN_UNAVAILABLE"):
                guarded_regress.run_guarded_command(
                    root, runner=self._guard_runner(), mise_path=missing_mise
                )

    def test_mise_preflight_pins_existing_executable_and_project_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._root(directory)
            observed: list[tuple[list[str], dict[str, str]]] = []
            default_runner = self._guard_runner()

            def runner(argv: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
                command = argv[3:]
                if command == [str(self._mise_path), "exec", "--", "bundle", "--version"]:
                    observed.append((command, env))
                return default_runner(argv, cwd, env)

            guarded_regress.run_guarded_command(root, runner=runner)

            self.assertEqual(1, len(observed))
            command, environment = observed[0]
            resolved_root = root.resolve()
            self.assertEqual([str(self._mise_path), "exec", "--", "bundle", "--version"], command)
            self.assertEqual(str(self._mise_path.parent.parent), environment["XDG_CACHE_HOME"])
            self.assertEqual(str(resolved_root / ".mise.toml"), environment["MISE_CONFIG_FILE"])
            self.assertEqual(str(resolved_root), environment["MISE_PROJECT_ROOT"])

    def test_unavailable_mise_toolchain_fails_before_regression_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self._root(directory)
            with self.assertRaisesRegex(guarded_regress.GuardedRegressError, "MISE_TOOLCHAIN_UNAVAILABLE"):
                guarded_regress.run_guarded_command(root, runner=self._guard_runner(mise_code=1))

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
                        if command[:2] == ["/usr/bin/python3", "-c"] and "socket.socket" in command[2]:
                            return self._result(
                                argv, 77, stdout=self._NETWORK_DENIED_STDOUT, stderr=""
                            )
                        if command == [str(self._mise_path), "exec", "--", "bundle", "--version"]:
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

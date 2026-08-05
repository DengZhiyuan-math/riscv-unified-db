# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Contract coverage for the Darwin arm64 source-port validator."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from validation import native_port_build, native_port_validate


class NativePortContractTests(unittest.TestCase):
    def _write_contract(self, directory: Path, *, tools: dict | None = None) -> Path:
        contract = {
            "contract_id": "darwin-arm64-source-port-20260805",
            "schema_version": 1,
            "tools": tools
            or {
                "espresso": {
                    "source_url": "https://github.com/psksvp/espresso-ab-1.0.git",
                    "source_commit": "18f59c723545f11bcb46d9e38e936531c990e5cf",
                    "patches": [],
                    "executable": "espresso",
                    "cache_version": "espresso-18f59c7",
                    "build_commands": [["./configure", "--prefix=__STAGING__"], ["/usr/bin/make"]],
                }
            },
            "environment_allowlist": ["CC", "CXX", "LC_ALL", "PATH"],
        }
        path = directory / "contract.json"
        path.write_text(json.dumps(contract, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def test_exact_full_source_identities(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_contract(Path(directory))
            loaded = native_port_build.load_contract(path)
            native_port_build.validate_contract(loaded, tracer_tool="espresso")
            loaded["tools"]["espresso"]["source_commit"] = "18f59c7"
            with self.assertRaisesRegex(native_port_build.ContractError, "SOURCE_COMMIT_NOT_FULL"):
                native_port_build.validate_contract(loaded, tracer_tool="espresso")

    def test_espresso_tracer_rejects_unbound_all_tools(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            loaded = native_port_build.load_contract(self._write_contract(Path(directory)))
            with self.assertRaisesRegex(native_port_build.ContractError, "ALL_TOOLS_PATCHES_UNBOUND"):
                native_port_build.validate_contract(loaded, tracer_tool=None)

    def test_builder_and_validator_are_independent(self) -> None:
        source = Path(native_port_validate.__file__).read_text(encoding="utf-8")
        self.assertNotIn("native_port_build", source)

    def test_validator_uses_native_no_network_profile(self) -> None:
        profile = native_port_validate.native_network_deny_profile()
        self.assertEqual("(version 1)\n(allow default)\n(deny network*)\n", profile)
        self.assertEqual("/usr/bin/sandbox-exec", str(native_port_validate.SANDBOX_EXEC))
        self.assertIn("(deny file-write*", native_port_validate.native_oracle_profile())

    def test_candidate_cannot_generate_oracle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            oracle = Path(directory) / "oracle.json"
            oracle.write_text('{"cases": []}\n', encoding="utf-8")
            with self.assertRaisesRegex(native_port_validate.ValidationError, "ORACLE_GENERATION_FORBIDDEN"):
                native_port_validate.load_oracle(oracle, generate=True)

    def test_tracer_cannot_write_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            staged = root / "espresso"
            staged.write_bytes(b"candidate")
            with self.assertRaisesRegex(native_port_validate.ValidationError, "CACHE_WRITE_DENIED"):
                native_port_validate.publish_cache(
                    {"espresso": staged}, root / "cache", mode="deny", transaction_id="test"
                )

    def test_tracer_handoff_is_create_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "record.json"
            payload = {"state": "tracer_validated", "non_authoritative": True}
            native_port_validate.create_record(record, payload)
            with self.assertRaisesRegex(native_port_validate.ValidationError, "RECORD_EXISTS"):
                native_port_validate.create_record(record, payload)

    def test_successor_admits_the_exact_required_predecessor_stage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            try:
                os.chdir(directory)
                record = Path("attempt-02.json")
                native_port_validate.create_record(record, {"state": "tracer_validated", "non_authoritative": True})
                _, digest = native_port_validate.read_successor_predecessor(record, "tracer_validated")
                self.assertEqual(hashlib.sha256(record.read_bytes()).hexdigest(), digest)
                with self.assertRaisesRegex(native_port_validate.ValidationError, "PREDECESSOR_STATE_MISMATCH"):
                    native_port_validate.read_successor_predecessor(record, "all_tools_validated_cache_unpublished")
            finally:
                os.chdir(previous)

    def test_oracles_use_fixed_native_guard_and_repeat_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            staged = root / "staged"
            staged.mkdir()
            for build in (0, 1):
                (staged / f"espresso-{build}").write_bytes(b"candidate")
            oracle = {
                "cases": [
                    {"tool": "espresso", "argv": ["-efast"], "stdin_base64": "", "returncode": 0, "stdout_base64": "", "stderr_base64": ""},
                    {"tool": "espresso", "argv": ["-Dsignature"], "stdin_base64": "", "returncode": 0, "stdout_base64": "", "stderr_base64": ""},
                ]
            }
            calls: list[list[str]] = []

            def runner(argv: list[str], **_: object) -> subprocess.CompletedProcess[bytes]:
                calls.append(argv)
                return subprocess.CompletedProcess(argv, 0, b"", b"")

            results = native_port_validate.validate_oracles(root, oracle, ["espresso"], repetitions=2, runner=runner)
            self.assertEqual(8, len(results))
            self.assertTrue(all(call[:2] == ["/usr/bin/sandbox-exec", "-p"] for call in calls))

    def test_oracle_mismatch_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            staged = root / "staged"
            staged.mkdir()
            for build in (0, 1):
                (staged / f"espresso-{build}").write_bytes(b"candidate")
            oracle = {"cases": [{"tool": "espresso", "argv": ["-efast"], "stdin_base64": "", "returncode": 0, "stdout_base64": "eA==", "stderr_base64": ""}, {"tool": "espresso", "argv": ["-Dsignature"], "stdin_base64": "", "returncode": 0, "stdout_base64": "", "stderr_base64": ""}]}
            with self.assertRaisesRegex(native_port_validate.ValidationError, "ORACLE_OUTPUT_MISMATCH"):
                native_port_validate.validate_oracles(root, oracle, ["espresso"], repetitions=2, runner=lambda argv, **_: subprocess.CompletedProcess(argv, 0, b"", b""))

    def test_oracle_supports_committed_input_and_output_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            staged = root / "staged"
            staged.mkdir()
            for build in (0, 1):
                (staged / f"must-{build}").write_bytes(b"candidate")
            oracle = {
                "cases": [
                    {
                        "tool": "must",
                        "argv": ["-o", "__OUTPUT__", "__INPUT__"],
                        "input_files": {"__INPUT__": "Y2YgMSAxCjEgMAo="},
                        "output_files": {"__OUTPUT__": "bXVzLXJlc3VsdAo="},
                        "stdin_base64": "",
                        "returncode": 0,
                        "stdout_base64": "",
                        "stderr_base64": "",
                    },
                    {
                        "tool": "must",
                        "argv": ["-o", "__OUTPUT__", "__INPUT__"],
                        "input_files": {"__INPUT__": "Y2YgMSAxCjEgMAo="},
                        "output_files": {"__OUTPUT__": "bXVzLXJlc3VsdAo="},
                        "stdin_base64": "",
                        "returncode": 0,
                        "stdout_base64": "",
                        "stderr_base64": "",
                    },
                ]
            }

            def runner(argv: list[str], **_: object) -> subprocess.CompletedProcess[bytes]:
                Path(argv[-2]).write_bytes(b"mus-result\n")
                self.assertTrue(Path(argv[-1]).is_file())
                return subprocess.CompletedProcess(argv, 0, b"", b"")

            results = native_port_validate.validate_oracles(root, oracle, ["must"], repetitions=2, runner=runner)
            self.assertEqual(8, len(results))

    def test_changed_patch_bytes_and_extra_patch_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            patch = root / "allowed.patch"
            patch.write_text("diff --git a/a b/a\n", encoding="utf-8")
            digest = hashlib.sha256(patch.read_bytes()).hexdigest()
            native_port_build.validate_patch_set(root, [{"path": "allowed.patch", "sha256": digest}])
            patch.write_text("changed\n", encoding="utf-8")
            with self.assertRaisesRegex(native_port_build.ContractError, "PATCH_SHA256_MISMATCH"):
                native_port_build.validate_patch_set(root, [{"path": "allowed.patch", "sha256": digest}])
            patch.write_text("diff --git a/a b/a\n", encoding="utf-8")
            (root / "extra.patch").write_text("diff --git a/b b/b\n", encoding="utf-8")
            with self.assertRaisesRegex(native_port_build.ContractError, "UNDECLARED_PATCH"):
                native_port_build.validate_patch_set(root, [{"path": "allowed.patch", "sha256": digest}])

    def test_patch_manifest_accepts_only_declared_nested_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            patch = root / "mustool" / "0001-port.patch"
            patch.parent.mkdir()
            patch.write_text("diff --git a/a b/a\n", encoding="utf-8")
            digest = hashlib.sha256(patch.read_bytes()).hexdigest()
            native_port_build.validate_patch_set(root, [{"path": "mustool/0001-port.patch", "sha256": digest}])

    def test_staged_candidate_preserves_execute_permission(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            destination = root / "destination"
            source.write_bytes(b"candidate")
            source.chmod(0o755)
            native_port_build.stage_executable(source, destination)
            self.assertTrue(os.access(destination, os.X_OK))


if __name__ == "__main__":
    unittest.main()

# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Fail-closed native confinement for the fixed repository regression command.

This module is validation-only: it is deliberately outside the Red evidence
closure and is not imported by the formal executor.  Its only child command is
the literal repository regression argv declared in ``FIXED_REGRESSION_ARGV``.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import stat
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

_EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
_EXPERIMENT_SOURCE = _EXPERIMENT_ROOT / "src"
if str(_EXPERIMENT_SOURCE) not in sys.path:
    sys.path.insert(0, str(_EXPERIMENT_SOURCE))

from specchoice_evidence.filesystem import (
    FilesystemPolicyError,
    enumerate_authoritative_files,
    read_authoritative_files,
)

FORMAL_FILENAMES = (
    "attempt-chain.json",
    "evidence-span-audit.json",
    "matrix-manifest.json",
    "model-call-ledger.json",
    "no-call-runtime-audit.json",
    "no-call-structural-audit.json",
    "ordered-diagnostics.json",
    "parsed-evidence.json",
    "raw-evidence.json",
    "red-trigger-evidence.json",
)
_FORMAL_ROOT = Path("experiments/specchoice-v1.3.2/runs/red-execution-v2")
_RECEIPT = Path("experiments/specchoice-v1.3.2/receipts/red-execution-v2.json")
_REPORT = Path("experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v2.md")
_SANDBOX_EXEC = Path("/usr/bin/sandbox-exec")
_FIXED_REGRESSION_ARGV = ("./bin/regress", "--all")
_PREFLIGHT_TRUE = ("/usr/bin/true",)
_PREFLIGHT_NETWORK = (
    "/usr/bin/python3",
    "-c",
    (
        "import errno, os, socket, sys\n"
        "s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
        "s.settimeout(1.0)\n"
        "try:\n"
        ' s.connect(("127.0.0.1", 0))\n'
        "except OSError as error:\n"
        " diagnostic=error.strerror or os.strerror(error.errno)\n"
        ' print(f"GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno={error.errno} diagnostic={diagnostic}")\n'
        " sys.exit(77 if error.errno == errno.EPERM and diagnostic == os.strerror(errno.EPERM) else 78)\n"
        "else:\n"
        ' print("GUARDED_REGRESS_NETWORK_CONNECT_SUCCEEDED")\n'
        " sys.exit(79)\n"
        "finally:\n"
        " s.close()"
    ),
)
_PREFLIGHT_NETWORK_RETURN_CODE = 77
_PREFLIGHT_NETWORK_STDOUT = "GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno=1 diagnostic=Operation not permitted\n"
_MISE_EXECUTABLE_NAME = "mise-2026.7.5"
_MISE_CONFIG = Path(".mise.toml")
_PREFLIGHT_WRITE = (
    "/usr/bin/python3",
    "-c",
    "import pathlib, sys; pathlib.Path(sys.argv[1]).write_bytes(b'x')",
)


class GuardedRegressError(RuntimeError):
    """A stable fail-closed admission or guarded-run failure."""


@dataclass(frozen=True)
class GuardedRun:
    """Non-authoritative record returned to the caller for its own reporting."""

    argv: tuple[str, ...]
    returncode: int
    stdout_sha256: str
    stderr_sha256: str


Runner = Callable[[Sequence[str], Path, dict[str, str]], subprocess.CompletedProcess[str]]


def _run_process(argv: Sequence[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(argv), cwd=cwd, env=env, capture_output=True, text=True, check=False)


def _absolute_repo_root(repo_root: Path) -> Path:
    if repo_root.is_symlink():
        raise GuardedRegressError("GUARDED_REGRESS_INVALID_REPO_ROOT")
    root = repo_root.resolve(strict=True)
    if not root.is_dir():
        raise GuardedRegressError("GUARDED_REGRESS_INVALID_REPO_ROOT")
    return root


def snapshot_v2_evidence(repo_root: Path) -> tuple[tuple[str, int, str], ...]:
    """Return the exact twelve-leaf v2 inventory from regular no-follow leaves."""
    root = _absolute_repo_root(repo_root)
    try:
        observed = enumerate_authoritative_files(root / _FORMAL_ROOT)
    except FilesystemPolicyError as error:
        raise GuardedRegressError("GUARDED_REGRESS_FORMAL_ROOT_MISSING") from error
    if observed != set(FORMAL_FILENAMES):
        raise GuardedRegressError("GUARDED_REGRESS_FORMAL_INVENTORY_MISMATCH")
    relatives = [(_FORMAL_ROOT / filename) for filename in FORMAL_FILENAMES]
    relatives.extend((_RECEIPT, _REPORT))
    names = [relative.as_posix() for relative in sorted(relatives, key=lambda value: value.as_posix())]
    try:
        evidence = read_authoritative_files(root, names)
    except FilesystemPolicyError as error:
        raise GuardedRegressError("GUARDED_REGRESS_EVIDENCE_LEAF_UNSAFE") from error
    return tuple((name, item.byte_length or 0, item.sha256 or "") for name, (item, _) in evidence.items())


def _sandbox_quote(path: Path) -> str:
    return '"' + str(path).replace("\\", "\\\\").replace('"', '\\"') + '"'


def _protected_paths(repo_root: Path, probe_root: Path | None) -> tuple[Path, ...]:
    home = Path.home()
    paths = [
        repo_root / _FORMAL_ROOT,
        repo_root / _RECEIPT,
        repo_root / _REPORT,
        repo_root / ".venv",
        repo_root / ".mise",
        repo_root / "node_modules",
        repo_root / "vendor" / "bundle",
        repo_root / ".bundle",
        repo_root / ".mise.toml",
        repo_root / "pyproject.toml",
        repo_root / "uv.lock",
        repo_root / "Gemfile",
        repo_root / "Gemfile.lock",
        repo_root / "package-lock.json",
        home / ".local" / "share" / "mise",
        home / ".cache",
        home / "Library" / "Caches",
        home / ".npm",
        home / ".gem",
        home / ".cargo",
        home / ".rustup",
        Path("/opt/homebrew"),
        Path("/usr/local"),
        Path("/Library"),
    ]
    if probe_root is not None:
        paths.append(probe_root)
    return tuple(sorted((path.resolve(strict=False) for path in paths), key=str))


def build_sandbox_profile(repo_root: Path, probe_root: Path | None = None) -> str:
    """Build the deterministic native profile used for every guarded process."""
    root = _absolute_repo_root(repo_root)
    lines = ["(version 1)", "(allow default)", "(deny network*)"]
    for path in _protected_paths(root, probe_root):
        lines.append(f"(deny file-write* (subpath {_sandbox_quote(path)}))")
    return "\n".join(lines) + "\n"


def _offline_environment() -> dict[str, str]:
    environment = dict(os.environ)
    environment.update(
        {
            "MISE_OFFLINE": "1",
            "UV_OFFLINE": "1",
            "PIP_NO_INDEX": "1",
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            "BUNDLE_FROZEN": "true",
            "BUNDLE_DEPLOYMENT": "true",
            "npm_config_offline": "true",
            "npm_config_update_notifier": "false",
            "CARGO_NET_OFFLINE": "true",
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return environment


def _default_mise_path() -> Path:
    return Path.home() / ".cache" / "mise" / _MISE_EXECUTABLE_NAME


def _require_mise_toolchain(repo_root: Path, mise_path: Path | None) -> tuple[Path, Path]:
    mise = _default_mise_path() if mise_path is None else mise_path
    config = repo_root / _MISE_CONFIG
    try:
        mise_mode = os.stat(mise).st_mode
        config_mode = os.stat(config).st_mode
    except FileNotFoundError as error:
        raise GuardedRegressError("GUARDED_REGRESS_MISE_TOOLCHAIN_UNAVAILABLE") from error
    if (
        mise.is_symlink()
        or config.is_symlink()
        or not stat.S_ISREG(mise_mode)
        or not stat.S_ISREG(config_mode)
        or not os.access(mise, os.X_OK)
    ):
        raise GuardedRegressError("GUARDED_REGRESS_MISE_TOOLCHAIN_UNAVAILABLE")
    return mise, config


def _mise_environment(repo_root: Path, mise: Path, config: Path) -> dict[str, str]:
    environment = _offline_environment()
    environment.update(
        {
            "XDG_CACHE_HOME": str(mise.parent.parent),
            "MISE_CONFIG_FILE": str(config),
            "MISE_PROJECT_ROOT": str(repo_root),
        }
    )
    return environment


def _require_exact_guard(guard_path: Path) -> Path:
    if guard_path != _SANDBOX_EXEC:
        raise GuardedRegressError("GUARDED_REGRESS_NATIVE_GUARD_UNAVAILABLE")
    try:
        mode = os.stat(guard_path).st_mode
    except FileNotFoundError as error:
        raise GuardedRegressError("GUARDED_REGRESS_NATIVE_GUARD_UNAVAILABLE") from error
    if not stat.S_ISREG(mode) or not os.access(guard_path, os.X_OK):
        raise GuardedRegressError("GUARDED_REGRESS_NATIVE_GUARD_UNAVAILABLE")
    return guard_path


def _guard_argv(guard_path: Path, profile: str, command: Sequence[str]) -> list[str]:
    return [str(guard_path), "-p", profile, *command]


def preflight_native_guard(
    repo_root: Path,
    *,
    runner: Runner = _run_process,
    guard_path: Path = _SANDBOX_EXEC,
    mise_path: Path | None = None,
) -> str:
    """Require a working native guard plus enforced network and write denials."""
    root = _absolute_repo_root(repo_root)
    guard = _require_exact_guard(guard_path)
    mise, config = _require_mise_toolchain(root, mise_path)
    environment = _mise_environment(root, mise, config)
    with tempfile.TemporaryDirectory(prefix="guarded-regress-") as directory:
        probe_root = Path(directory)
        profile = build_sandbox_profile(root, probe_root)
        harmless = runner(_guard_argv(guard, profile, _PREFLIGHT_TRUE), root, environment)
        if harmless.returncode != 0:
            raise GuardedRegressError("GUARDED_REGRESS_NATIVE_GUARD_NONFUNCTIONAL")
        network = runner(_guard_argv(guard, profile, _PREFLIGHT_NETWORK), root, environment)
        if (
            network.returncode != _PREFLIGHT_NETWORK_RETURN_CODE
            or network.stdout != _PREFLIGHT_NETWORK_STDOUT
            or network.stderr != ""
        ):
            raise GuardedRegressError("GUARDED_REGRESS_NETWORK_PROBE_NOT_DENIED")
        toolchain = runner(
            _guard_argv(guard, profile, (str(mise), "exec", "--", "bundle", "--version")), root, environment
        )
        if toolchain.returncode != 0:
            raise GuardedRegressError("GUARDED_REGRESS_MISE_TOOLCHAIN_UNAVAILABLE")
        sentinel = probe_root / "protected-sentinel"
        write = runner(_guard_argv(guard, profile, (*_PREFLIGHT_WRITE, str(sentinel))), root, environment)
        if write.returncode == 0 or sentinel.exists():
            raise GuardedRegressError("GUARDED_REGRESS_WRITE_PROBE_NOT_DENIED")
    return profile


def run_guarded_command(
    repo_root: Path,
    *,
    runner: Runner = _run_process,
    guard_path: Path = _SANDBOX_EXEC,
    mise_path: Path | None = None,
) -> GuardedRun:
    """Run only the fixed regression argv after admission, then compare snapshots."""
    root = _absolute_repo_root(repo_root)
    before = snapshot_v2_evidence(root)
    profile = preflight_native_guard(root, runner=runner, guard_path=guard_path, mise_path=mise_path)
    mise, config = _require_mise_toolchain(root, mise_path)
    result = runner(
        _guard_argv(_require_exact_guard(guard_path), profile, _FIXED_REGRESSION_ARGV),
        root,
        _mise_environment(root, mise, config),
    )
    record = GuardedRun(
        argv=_FIXED_REGRESSION_ARGV,
        returncode=result.returncode,
        stdout_sha256=hashlib.sha256(result.stdout.encode("utf-8")).hexdigest(),
        stderr_sha256=hashlib.sha256(result.stderr.encode("utf-8")).hexdigest(),
    )
    if result.returncode != 0:
        raise GuardedRegressError(
            f"GUARDED_REGRESS_CHILD_FAILED returncode={record.returncode} "
            f"stdout_sha256={record.stdout_sha256} stderr_sha256={record.stderr_sha256}"
        )
    try:
        after = snapshot_v2_evidence(root)
    except GuardedRegressError as error:
        raise GuardedRegressError("GUARDED_REGRESS_EVIDENCE_MUTATED") from error
    if after != before:
        raise GuardedRegressError("GUARDED_REGRESS_EVIDENCE_MUTATED")
    return record


def _validate_toolchain(repo_root: Path) -> None:
    expected = "952e015ef06176e1bdcce1c5634b4ff26c67b7ec7e226499d07a8138c9c02351"
    pyproject = repo_root / "pyproject.toml"
    if hashlib.sha256(pyproject.read_bytes()).hexdigest() != expected:
        raise GuardedRegressError("GUARDED_REGRESS_TOOLCHAIN_DRIFT")
    python = repo_root / ".venv" / "bin" / "python"
    ruff = repo_root / ".venv" / "bin" / "ruff"
    if not python.is_file() or not ruff.is_file():
        raise GuardedRegressError("GUARDED_REGRESS_TOOLCHAIN_UNAVAILABLE")
    if sys.version_info[:3] != (3, 12, 13):
        raise GuardedRegressError("GUARDED_REGRESS_PYTHON_VERSION_MISMATCH")
    version = subprocess.run([str(ruff), "--version"], capture_output=True, text=True, check=False)
    if version.returncode != 0 or version.stdout.strip() != "ruff 0.16.0":
        raise GuardedRegressError("GUARDED_REGRESS_RUFF_VERSION_MISMATCH")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    arguments = parser.parse_args(argv)
    try:
        root = _absolute_repo_root(Path(arguments.repo_root))
        _validate_toolchain(root)
        record = run_guarded_command(root)
    except GuardedRegressError as error:
        print(str(error), file=sys.stderr)
        return 2
    print(
        "GUARDED_REGRESS_OK "
        f"argv={' '.join(record.argv)} stdout_sha256={record.stdout_sha256} stderr_sha256={record.stderr_sha256}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

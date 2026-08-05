# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Closed, source-only build admission for the Darwin native-port contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


class ContractError(ValueError):
    """A closed source-port contract was not satisfied."""


FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
PATCH_SUFFIX = ".patch"
FORBIDDEN_TOKENS = {"docker", "brew", "pip", "gem", "npm", "install", "strip", "codesign"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_contract(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ContractError("CONTRACT_PARSE_FAILED") from error
    if not isinstance(value, dict):
        raise ContractError("CONTRACT_NOT_OBJECT")
    return value


def _require_full_commit(tool: dict[str, Any]) -> None:
    commit = tool.get("source_commit")
    if not isinstance(commit, str) or not FULL_SHA.fullmatch(commit):
        raise ContractError("SOURCE_COMMIT_NOT_FULL")
    source_url = tool.get("source_url")
    if not isinstance(source_url, str) or not source_url.startswith("https://github.com/"):
        raise ContractError("SOURCE_URL_NOT_CANONICAL")


def _check_commands(commands: Any) -> None:
    if not isinstance(commands, list) or not commands:
        raise ContractError("BUILD_COMMANDS_MISSING")
    for argv in commands:
        if not isinstance(argv, list) or not argv or not all(isinstance(item, str) for item in argv):
            raise ContractError("BUILD_COMMAND_NOT_ARGV")
        if any(token in FORBIDDEN_TOKENS for token in argv):
            raise ContractError("FORBIDDEN_BUILD_COMMAND")
        if any(any(marker in arg for marker in ("$", "`", ";", "|", "&&")) for arg in argv):
            raise ContractError("SHELL_INTERPOLATION_FORBIDDEN")


def validate_contract(contract: dict[str, Any], *, tracer_tool: str | None) -> None:
    tools = contract.get("tools")
    if not isinstance(tools, dict) or not tools:
        raise ContractError("TOOLS_MISSING")
    required = {"eqntott", "must", "espresso"}
    if tracer_tool is None and set(tools) != required:
        raise ContractError("ALL_TOOLS_PATCHES_UNBOUND")
    if tracer_tool is not None and tracer_tool not in tools:
        raise ContractError("TRACER_TOOL_UNKNOWN")
    for name, tool in tools.items():
        if not isinstance(name, str) or not isinstance(tool, dict):
            raise ContractError("TOOL_INVALID")
        _require_full_commit(tool)
        _check_commands(tool.get("build_commands"))
        patches = tool.get("patches")
        if not isinstance(patches, list):
            raise ContractError("PATCH_LIST_INVALID")
        for patch in patches:
            if not isinstance(patch, dict) or not isinstance(patch.get("path"), str) or not isinstance(patch.get("sha256"), str) or not SHA256.fullmatch(patch["sha256"]):
                raise ContractError("PATCH_MANIFEST_INVALID")
        if name == "espresso" and patches:
            raise ContractError("ESPRESSO_PATCH_FORBIDDEN")
        if tracer_tool is None and name != "espresso" and not patches:
            raise ContractError("ALL_TOOLS_PATCHES_UNBOUND")


def validate_patch_set(root: Path, manifest: list[dict[str, str]]) -> None:
    declared: set[Path] = set()
    for item in manifest:
        relative = item.get("path")
        expected = item.get("sha256")
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise ContractError("PATCH_MANIFEST_INVALID")
        relative_path = Path(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ContractError("PATCH_PATH_INVALID")
        path = root / relative_path
        if path.suffix != PATCH_SUFFIX or path.is_symlink() or not path.is_file():
            raise ContractError("PATCH_PATH_INVALID")
        if _sha256(path) != expected:
            raise ContractError("PATCH_SHA256_MISMATCH")
        declared.add(path)
    actual = {path for path in root.rglob(f"*{PATCH_SUFFIX}") if path.is_file() or path.is_symlink()}
    if actual != declared:
        raise ContractError("UNDECLARED_PATCH")


def _run(argv: list[str], *, cwd: Path, environment: dict[str, str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(argv, cwd=cwd, env=environment, capture_output=True, check=False)


def _clean_git_checkout(tool: dict[str, Any], root: Path) -> Path:
    source = root / "pristine" / tool["name"]
    source.parent.mkdir(parents=True, exist_ok=True)
    result = _run(["/usr/bin/git", "clone", "--no-checkout", tool["source_url"], str(source)], cwd=root, environment=os.environ.copy())
    if result.returncode:
        raise ContractError("SOURCE_CLONE_FAILED")
    for argv in (["/usr/bin/git", "checkout", "--detach", tool["source_commit"]], ["/usr/bin/git", "submodule", "status"], ["/usr/bin/git", "status", "--porcelain"]):
        result = _run(argv, cwd=source, environment=os.environ.copy())
        if result.returncode:
            raise ContractError("SOURCE_IDENTITY_FAILED")
        if (argv[-1] == "--porcelain" or argv[-1] == "status") and result.stdout:
            raise ContractError("SOURCE_DIRTY")
    return source


def _apply_patches(work: Path, patch_root: Path, patches: list[dict[str, str]]) -> None:
    for patch in patches:
        path = patch_root / patch["path"]
        for argv in (["/usr/bin/git", "apply", "--check", "--whitespace=error", str(path)], ["/usr/bin/git", "apply", "--whitespace=error", str(path)]):
            result = _run(argv, cwd=work, environment=os.environ.copy())
            if result.returncode:
                raise ContractError("PATCH_APPLICATION_FAILED")


def _build_one(tool: dict[str, Any], root: Path, number: int, patch_root: Path | None) -> Path:
    pristine = _clean_git_checkout(tool, root / f"build-{number}")
    work = root / f"build-{number}" / "work" / tool["name"]
    shutil.copytree(pristine, work, symlinks=True)
    patches = tool["patches"]
    if patches:
        if patch_root is None:
            raise ContractError("PATCH_ROOT_MISSING")
        _apply_patches(work, patch_root, patches)
    staged = root / "staged" / f"{tool['name']}-{number}"
    staged.parent.mkdir(parents=True, exist_ok=True)
    environment = {key: os.environ[key] for key in ("PATH", "LC_ALL", "CC", "CXX") if key in os.environ}
    environment.setdefault("LC_ALL", "C")
    for command in tool["build_commands"]:
        argv = [argument.replace("__STAGING__", str(root / "install" / str(number))) for argument in command]
        result = _run(argv, cwd=work, environment=environment)
        if result.returncode:
            raise ContractError("SOURCE_BUILD_FAILED")
    executable = work / tool["executable"]
    if not executable.is_file():
        candidates = list(work.rglob(tool["executable"]))
        if len(candidates) != 1:
            raise ContractError("EXECUTABLE_MISSING")
        executable = candidates[0]
    stage_executable(executable, staged)
    return staged


def stage_executable(source: Path, destination: Path) -> None:
    mode = source.stat().st_mode
    if not stat.S_ISREG(mode) or not mode & stat.S_IXUSR:
        raise ContractError("EXECUTABLE_NOT_EXECUTABLE")
    shutil.copy2(source, destination)
    destination.chmod(stat.S_IMODE(mode))


def build(contract: dict[str, Any], root: Path, tools: list[str], clean_builds: int, patch_root: Path | None = None) -> None:
    validate_contract(contract, tracer_tool=tools[0] if len(tools) == 1 else None)
    if clean_builds != 2:
        raise ContractError("CLEAN_BUILD_COUNT_INVALID")
    patches = [patch for name in tools for patch in contract["tools"][name]["patches"]]
    if patches:
        if patch_root is None:
            raise ContractError("PATCH_ROOT_MISSING")
        patch_root = patch_root.resolve()
        validate_patch_set(patch_root, patches)
    for name in tools:
        tool = dict(contract["tools"][name])
        tool["name"] = name
        for number in range(clean_builds):
            _build_one(tool, root, number, patch_root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("tracer", "build-all"):
        item = subparsers.add_parser(command)
        item.add_argument("--contract", type=Path, required=True)
        item.add_argument("--oracle", type=Path, required=True)
        item.add_argument("--operational-root", type=Path, required=True)
        item.add_argument("--patch-root", type=Path)
        item.add_argument("--tool")
        item.add_argument("--clean-builds", type=int, required=True)
    args = parser.parse_args(argv)
    try:
        contract = load_contract(args.contract)
        tools = [args.tool] if args.command == "tracer" else ["eqntott", "must", "espresso"]
        if not args.oracle.is_file():
            raise ContractError("ORACLE_MISSING")
        build(contract, args.operational_root, tools, args.clean_builds, args.patch_root)
    except ContractError as error:
        print(str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

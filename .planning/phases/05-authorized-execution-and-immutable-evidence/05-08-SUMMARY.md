---
phase: 05-authorized-execution-and-immutable-evidence
plan: 08
subsystem: Darwin arm64 native dependency port validation
tags: [darwin, arm64, native-port, cache, fail-closed]
status: complete
completed: 2026-08-05
---

# Phase 05 Plan 08: Darwin Native-Port Validation Summary

The versioned v3 successor completed a local, non-authoritative Darwin arm64 source-port validation without changing formal Red evidence or granting model/publication authority.

## Result

- Preserved the original v2 failure custody and completed the v3 all-tools successor chain.
- Published the three validated native executables and their three SHA-256 checksum leaves through one no-replace local cache transaction.
- Replayed the completed Red formal root byte-identically with zero writes.
- Ran the fixed guarded full regression twice, with both invocations passing under the existing native deny harness.
- Created only `attempt-04/contract-validation.json` in `validation_complete`; its SHA-256 is `3bf0c8fcee446111ea1dd93a3cc6cf6f6dedb630f55bb93c8852cfd3707d3f15`.

## Validation

Passed:

```text
cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_native_port_contract tests.test_guarded_regress -q
../../.venv/bin/ruff check --isolated validation/native_port_build.py validation/native_port_validate.py validation/guarded_regress.py tests/test_native_port_contract.py tests/test_guarded_regress.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root .
```

The formal `execute-red` replay retained the exact twelve formal/receipt/report leaves. The cache and source-port records remain operational validation custody only; they do not alter the Gate-A/Gate-B Red evidence closure.

## Scope

No source rebuild, oracle generation, dependency install, network use, external publication, model call, or formal evidence mutation occurred during the terminal gate. Unrelated worktree changes remain untouched.

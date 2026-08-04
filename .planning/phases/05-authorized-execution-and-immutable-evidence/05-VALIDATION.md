---
phase: 05
slug: authorized-execution-and-immutable-evidence
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-04
---

# Phase 05 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python standard-library `unittest`; project contract Python `>=3.12` |
| **Config file** | `pyproject.toml` for Ruff; `unittest` uses `PYTHONPATH=src` |
| **Quick run command** | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_authorized_execution tests.test_treatments_h3 tests.test_canonical tests.test_filesystem_boundary -q` |
| **Full suite command** | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_data_admission tests.test_data_splits tests.test_data_relevance tests.test_data_h2 tests.test_treatments_frame tests.test_treatments_prompts tests.test_treatments_retrieval tests.test_treatments_h3 tests.test_authorized_execution tests.test_canonical tests.test_filesystem_boundary -q && ruff check --isolated src/specchoice_execution tests/test_authorized_execution.py && git diff --check` |
| **Estimated runtime** | Target under 30 seconds for quick sampling; measure and record the actual runtime before execution authority is claimed |

The ambient shell observed during research exposes Python 3.11.14 and Ruff 0.12.0, below the declared Python `>=3.12` and Ruff 0.16.0 contract. Restoring the repository-pinned local toolchain is a blocking execution prerequisite; validation must not weaken the declared versions or perform network installation inside the formal Red evidence run.

---

## Sampling Rate

- **After every task commit:** Run the quick test command above.
- **After every plan wave:** Run the full suite command above under the pinned local toolchain.
- **Before `$gsd-verify-work`:** Full suite, pinned Ruff, `git diff --check`, exact-resume/no-write checks, and the no-network adversarial suite must be green.
- **Max feedback latency:** 30 seconds for the quick suite; split focused modules if the measured runtime exceeds this bound.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | TS-07, TS-11, TS-12 | T-05-01 | Only the exact persisted v6 Red authority and frozen execution closure pass admission before any evidence write. | unit/integration | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_authorized_execution -q` | ❌ W0 | ⬜ pending |
| 05-01-02 | 01 | 1 | TS-12 | T-05-02 | Structural scanning rejects provider, model, credential, production-retrieval, process-spawn, and network surfaces; every socket path fails closed. | security/adversarial | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_authorized_execution -q` | ❌ W0 | ⬜ pending |
| 05-02-01 | 02 | 2 | TS-07, TS-11, TS-12 | T-05-03 | A valid Red run publishes a zero-entry call ledger, zero-cell A/B/C manifest, separate evidence leaves, and one bound terminal receipt with no metrics. | integration | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_authorized_execution tests.test_treatments_h3 -q` | ❌ W0 | ⬜ pending |
| 05-02-02 | 02 | 2 | TS-12 | T-05-04 | Drift, socket attempts, occupied targets, and interrupted publication produce immutable non-authoritative failed attempts and never partial formal evidence. | fault injection | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_authorized_execution tests.test_filesystem_boundary -q` | ❌ W0 | ⬜ pending |
| 05-03-01 | 03 | 3 | TS-07, TS-11, TS-12 | T-05-05 | Exact rerun is byte-identical and zero-write; the final receipt binds the complete ordered attempt history and no unregistered run/raw-response leaf exists. | audit/replay | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_authorized_execution tests.test_canonical tests.test_filesystem_boundary -q` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `experiments/specchoice-v1.3.2/tests/test_authorized_execution.py` — authority/closure admission, ledger and matrix schemas, all-socket tripwire, immutable failed custody, ordered retries, drift, and exact-resume coverage.
- [ ] Freeze the final Phase 5 module, schema, CLI, and evidence paths into the execution closure before the first formal attempt.
- [ ] Restore and record the repository-pinned Python `>=3.12` and Ruff 0.16.0 local toolchain without adding a Phase 5 runtime dependency or using network access inside formal execution.
- [ ] Measure quick/full validation runtimes and keep the quick feedback loop below 30 seconds.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| A changed frozen closure cannot inherit the v6 authority automatically. | TS-11, TS-12 | Human approval is the authority source for any successor chain. | Inspect the successor candidate/readiness diff, confirm no new authority leaf exists without an explicit human decision, and verify the unchanged v6 authority remains historical for changed bytes. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verification or Wave 0 dependencies.
- [ ] Sampling continuity: no three consecutive tasks without automated verification.
- [ ] Wave 0 covers all missing test and toolchain references.
- [ ] No watch-mode flags.
- [ ] Quick feedback latency is below 30 seconds.
- [ ] Pinned Python/Ruff versions are recorded and used.
- [ ] `nyquist_compliant: true` set in frontmatter after validation.

**Approval:** pending

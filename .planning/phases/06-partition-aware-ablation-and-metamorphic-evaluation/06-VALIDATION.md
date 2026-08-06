---
phase: 06
slug: partition-aware-ablation-and-metamorphic-evaluation
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-06
---

# Phase 06 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python `unittest` under the repository-local CPython environment |
| **Config file** | none — focused modules run with `PYTHONPATH=src` |
| **Quick run command** | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation -q` |
| **Full suite command** | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation tests.test_measurement_scoring tests.test_data_relevance tests.test_authorized_execution_v2 -q` |
| **Estimated runtime** | under 60 seconds for the focused suite |

---

## Sampling Rate

- **After every task commit:** Run the Phase 6 quick command plus isolated Ruff on changed Python files.
- **After every plan wave:** Run the full focused suite above.
- **Before `$gsd-verify-work`:** Run the full focused suite, isolated Ruff, `git diff --check`, exact-resume checks, tamper checks, and the separate human review decision gate.
- **Max feedback latency:** 60 seconds for the focused suite.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 06-01-01 | 01 | 0 | TS-06 | T-06-01 | Red metric identities preserve applicability and independent denominators without a blended score | unit + frozen-artifact integration | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_red_metrics_preserve_applicability_and_separate_denominators -q` | ❌ W0 | ⬜ pending |
| 06-01-02 | 01 | 0 | TS-13 | T-06-02 | All four frozen metamorphic directions remain complete, unavailable, and unscored on Red | unit + frozen-artifact integration | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_red_metamorphic_registry_is_complete_and_unscored -q` | ❌ W0 | ⬜ pending |
| 06-02-01 | 02 | 1 | H1-02 | T-06-03 | Closed pair joins reject missing, duplicate, extra, or cross-partition rows | unit + tamper | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_pair_join_rejects_missing_duplicate_and_cross_partition_rows -q` | ❌ W0 | ⬜ pending |
| 06-02-02 | 02 | 1 | H1-03 | Advisory frame warnings are report-only and cannot alter metrics or eligibility | unit | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_frame_warning_is_report_only -q` | ❌ W0 | ⬜ pending |
| 06-03-01 | 03 | 2 | H1-04 | T-06-04 | Frozen family and metamorphic identity drift withholds every dependent domain | unit + tamper | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_frozen_binding_drift_withholds_dependent_domain -q` | ❌ W0 | ⬜ pending |
| 06-03-02 | 03 | 2 | H2-03 | PairHit derives only from preregistered eligible IDs and never ratio-scores an empty Red population | unit + frozen-artifact integration | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_pairhit_uses_only_frozen_eligible_ids -q` | ❌ W0 | ⬜ pending |
| 06-03-03 | 03 | 2 | H2-04 | C-minus-B and B-minus-A populations retain independent identities and denominators | unit | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_c_minus_b_population_is_independent -q` | ❌ W0 | ⬜ pending |
| 06-04-01 | 04 | 3 | TS-06, TS-13 | T-06-05 | Exact-resume publication is create-only; substituted inputs, occupied targets, or unresolved blocking domains fail closed | integration + tamper | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation -q` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py` — result-state, population, closed-join, authority-boundary, warning, packet/readiness/decision, exact-resume, and tamper contracts for all Phase 6 requirements.
- [ ] `experiments/specchoice-v1.3.2/src/specchoice_evaluation/` — narrow standard-library composition package exercised by the Wave 0 tests.
- [ ] No framework installation — reuse Python `unittest`, canonical JSON, structured diagnostics, descriptor-bound reads, and no-replace publication.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Human review decision is bound to the exact decision-free packet and readiness hashes | TS-06, TS-13, H1-02, H1-03, H1-04, H2-03, H2-04 | Machine readiness cannot grant review authority | Inspect branch declaration, applicability matrix, case joins, populations, warnings, failure ledger, and construction-feasibility ordering; approve, dispute, or mark incomplete without relabeling frozen same-version evidence. |

---

## Validation Sign-Off

- [ ] All tasks have automated verification or an explicit Wave 0 dependency.
- [ ] Sampling continuity: no three consecutive tasks without automated verification.
- [ ] Wave 0 covers every missing Phase 6 test reference.
- [ ] No watch-mode flags.
- [ ] Focused feedback latency remains under 60 seconds.
- [ ] Human review packet and decision remain separate content-bound artifacts.
- [ ] `nyquist_compliant: true` is set only after the planned test map is executable.

**Approval:** pending

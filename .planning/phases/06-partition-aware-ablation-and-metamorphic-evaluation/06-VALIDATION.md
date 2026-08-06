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
- **Before `$gsd-verify-work`:** Complete the five-plan topology through Wave 4, including the blocking Plan 05 human decision gate, then run the full focused suite, isolated Ruff, `git diff --check`, exact-resume checks, tamper checks, and hash-bound decision validation.
- **Max feedback latency:** 60 seconds for the focused suite.

## Execution Topology

- **Plans:** 5 (`06-01` through `06-05`), with one plan in each of Waves 0 through 4.
- **Automated task coverage:** 11/11 planned tasks have an automated command; `06-05-01` additionally requires a blocking human decision.
- **Current execution status:** 0/11 task rows are green; the Plan 05 human decision has not been recorded.
- **Closure rule:** Machine readiness does not imply approval. Phase 6 closes only after an exact-hash `approved` decision with complete responses and no blocking dispute; `disputed` or `incomplete` preserves evidence while keeping Phase 6 open and `conclusion_ready=false`.

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
| 06-04-02 | 04 | 3 | TS-06, TS-13, H1-02, H1-03, H1-04, H2-03, H2-04 | T-06-19, T-06-20, T-06-21, T-06-22, T-06-23, T-06-24 | The canonical packet, Markdown, and readiness publish as one create-only complete file set, validate exact component and upstream hashes, and exact-resume without repair, rewrite, pooled metrics, or decision/conclusion authority | integration + publication + exact resume | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_evaluation.cli build-red --repo-root . --policy config/evaluation/partition-evaluation-red-generation-001.json && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_evaluation.cli verify-red-package --repo-root . --policy config/evaluation/partition-evaluation-red-generation-001.json && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation -q` | ❌ W0 | ⬜ pending |
| 06-05-01 | 05 | 4 | TS-06, TS-13, H1-02, H1-03, H1-04, H2-03, H2-04 | T-06-25, T-06-26, T-06-27, T-06-28, T-06-29, T-06-30 | D-13 through D-16 remain human-controlled: the reviewer chooses only `approved`, `disputed`, or `incomplete` for the exact decision-free packet/readiness hashes, with complete per-domain/per-item responses and no semantic relabeling or authority expansion | integration + hash binding + blocking human decision | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_evaluation.cli verify-red-package --repo-root . --policy config/evaluation/partition-evaluation-red-generation-001.json && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_packet_readiness_are_decision_free_and_hash_bound -q` | ❌ W0 | ⬜ pending — blocking human |
| 06-05-02 | 05 | 4 | TS-06, TS-13, H1-02, H1-03, H1-04, H2-03, H2-04 | T-06-25, T-06-26, T-06-27, T-06-28, T-06-29, T-06-30, T-06-31 | The separate canonical decision revalidates exact packet/readiness hashes, closed responses, disposition, self-hash, successor-only mutation boundaries, derived conclusion readiness, limited Phase 7 interpretation authority, and create-only exact resume | integration + tamper + exact resume | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_evaluation.cli validate-decision --repo-root . --policy config/evaluation/partition-evaluation-red-generation-001.json --decision reviews/partition-evaluation-red-generation-001-decision.json && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_review_decision_requires_exact_hashes_and_closed_responses -q && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation -q && ../../.venv/bin/ruff check --isolated src/specchoice_evaluation/review.py src/specchoice_evaluation/cli.py tests/test_partition_evaluation.py` | ❌ W0 | ⬜ pending |

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
| Task `06-05-01`: blocking human review decision is bound to the exact decision-free packet and readiness hashes per D-13 through D-16 | TS-06, TS-13, H1-02, H1-03, H1-04, H2-03, H2-04 | Machine readiness cannot grant review authority, select a disposition, or acknowledge the bounded authority grant | After the automated `verify-red-package` and packet/readiness hash-binding test pass, inspect the exact packet/readiness hashes, Red declaration, applicability matrix, case joins, populations and denominators, warnings, failure ledger, four metamorphic directions, PairHit/repeat populations, and construction-feasibility ordering. Return exactly `approved`, `disputed`, or `incomplete` with reviewer identity, complete per-domain/per-item responses, and stable IDs, blocking flags, and non-empty reasons where applicable. Confirm no same-version evidence is relabeled and explicitly acknowledge that approval grants only Phase 7 interpretation of the exact reviewed package—not a narrative, model/provider/retrieval/network/publication, H5, or H6 authority. |

---

## Validation Sign-Off

- [ ] All 11 tasks across Plans 01-05 have automated verification or an explicit Wave 0 dependency.
- [ ] Sampling continuity: no three consecutive tasks without automated verification.
- [ ] Wave 0 covers every missing Phase 6 test reference, including the Plan 05 packet/readiness and decision-validation tests consumed in Wave 4.
- [ ] No watch-mode flags.
- [ ] Focused feedback latency remains under 60 seconds.
- [ ] The blocking `06-05-01` human decision gate completed against the exact packet/readiness hashes with one allowed disposition, reviewer identity, complete per-domain/per-item responses, and explicit D-16 acknowledgement.
- [ ] `06-05-02` revalidated the packet/readiness and decision self-hash, rejected stale/substituted/authority-expanding inputs, and derived `conclusion_ready` without accepting it from human input.
- [ ] Human review packet, machine readiness, and human decision remain separate content-bound artifacts per D-13; D-14 through D-16 disposition, successor, and authority boundaries remain enforced.
- [ ] Five-plan execution reached Wave 4; Phase 6 closure is recorded only for `approved` with no blocking dispute, while `disputed` or `incomplete` remains valid evidence but not phase sign-off.
- [ ] `nyquist_compliant: true` is set only after the planned test map is executable.

**Approval:** pending

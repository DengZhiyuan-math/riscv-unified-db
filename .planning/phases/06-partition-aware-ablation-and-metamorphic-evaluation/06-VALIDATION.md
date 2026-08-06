---
phase: 06
slug: partition-aware-ablation-and-metamorphic-evaluation
status: recovery-current
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-06
---

# Phase 06 — Recovery Validation Strategy

## Test Infrastructure

| Property | Value |
| --- | --- |
| Framework | Python `unittest` with repository-local CPython |
| Focused suite | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation -q` |
| Lint | `cd experiments/specchoice-v1.3.2 && ../../.venv/bin/ruff check --isolated tests/test_partition_evaluation.py` |
| Expected feedback | under 60 seconds |

## Preserved and Superseded History

`06-01` through `06-07` are completed immutable history. `06-08` is partial `incomplete_execution_failed_closed` history: Task 01 published the exact generation-002 packet/report/readiness; Task 02 lacked the required fully-qualified preservation test and its frozen output-absence assertion conflicts with the occupied output set. The exact 002 policy, frozen test, packet, report, and readiness are bound by `partition-evaluation-red-generation-002-incomplete.json`; its decision path is absent. `06-09` and `06-10` are superseded unexecuted history.

Generation-002 receives no review gate, decision, repair, deletion, or approval. The sole active topology is `06-11` through `06-14` in Waves 10 through 13.

## Active Recovery Verification Map

| Task | Wave | Status | Automated command |
| --- | --- | --- | --- |
| 06-11-01 | 10 | pending — preserve 002, write status records | `cd experiments/specchoice-v1.3.2 && test "$(shasum -a 256 config/evaluation/partition-evaluation-red-generation-002.json \| awk '{print $1}')" = 872c1ef7278d06b55f89f1a00bb3555cce5cec3b987a3971a9226a79cb2684c7 && test "$(shasum -a 256 tests/test_partition_evaluation.py \| awk '{print $1}')" = 894bdd6d3690ab4a66f506c8907bf0ae48c21d3138618dcb39583cbe6dfa27e7 && test ! -e reviews/partition-evaluation-red-generation-002-decision.json && PYTHONDONTWRITEBYTECODE=1 ../../.venv/bin/python -m json.tool receipts/partition-evaluation-red-generation-002-incomplete.json >/dev/null` |
| 06-11-02 | 10 | pending — RED before policy freeze | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -c 'import subprocess; names=["tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_003_policy_freezes_test_and_incomplete_predecessor","tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_003_exact_resume_and_adversarial_rejection","tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_003_decision_exact_resume_and_authority_limits"]; result=subprocess.run(["../../.venv/bin/python","-m","unittest",*names,"-q"],capture_output=True,text=True); raise SystemExit(0 if result.returncode != 0 and "partition-evaluation-red-generation-003.json" in result.stdout+result.stderr else 1)'` |
| 06-11-03 | 10 | pending — freeze 003 policy | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_002_package_is_preserved_as_incomplete_predecessor tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_003_policy_freezes_test_and_incomplete_predecessor tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_003_exact_resume_and_adversarial_rejection tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_003_decision_exact_resume_and_authority_limits -q && ../../.venv/bin/ruff check --isolated tests/test_partition_evaluation.py` |
| 06-12-01 | 11 | pending — create/verify decision-free package | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_evaluation.cli build-red --experiment-root . --project-root ../.. --policy config/evaluation/partition-evaluation-red-generation-003.json && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_evaluation.cli verify-red-package --experiment-root . --project-root ../.. --policy config/evaluation/partition-evaluation-red-generation-003.json && test ! -e reviews/partition-evaluation-red-generation-003-decision.json` |
| 06-12-02 | 11 | pending — zero-write resume and attack matrix | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_002_package_is_preserved_as_incomplete_predecessor tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_003_policy_freezes_test_and_incomplete_predecessor tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_003_exact_resume_and_adversarial_rejection -q && ../../.venv/bin/ruff check --isolated tests/test_partition_evaluation.py` |
| 06-13-01 | 12 | pending — blocking human response | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_evaluation.cli verify-red-package --experiment-root . --project-root ../.. --policy config/evaluation/partition-evaluation-red-generation-003.json && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_002_package_is_preserved_as_incomplete_predecessor tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_003_exact_resume_and_adversarial_rejection tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_003_decision_exact_resume_and_authority_limits -q && test ! -e reviews/partition-evaluation-red-generation-002-decision.json && test ! -e reviews/partition-evaluation-red-generation-003-decision.json` |
| 06-14-01 | 13 | pending — create-only 003 decision | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_evaluation.cli validate-decision --experiment-root . --project-root ../.. --policy config/evaluation/partition-evaluation-red-generation-003.json --decision reviews/partition-evaluation-red-generation-003-decision.json && test ! -e reviews/partition-evaluation-red-generation-002-decision.json` |
| 06-14-02 | 13 | pending — decision exact resume | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_002_package_is_preserved_as_incomplete_predecessor tests.test_partition_evaluation.PartitionEvaluationTests.test_generation_003_decision_exact_resume_and_authority_limits -q && test ! -e reviews/partition-evaluation-red-generation-002-decision.json` |

The frozen recovery regressions are `test_generation_002_package_is_preserved_as_incomplete_predecessor`, `test_generation_003_policy_freezes_test_and_incomplete_predecessor`, `test_generation_003_exact_resume_and_adversarial_rejection`, and `test_generation_003_decision_exact_resume_and_authority_limits`. The package regression covers forged/rehashed packets, each construction source, missing or extra components, malformed runtime, bare/substituted joins, and missing/equal/treatment-inconsistent interventions.

## Manual-Only Verification

`06-13-01` is the sole human gate. After validation of the exact generation-003 packet and readiness hashes, the reviewer supplies `reviewer_id`, one disposition (`approved`, `disputed`, or `incomplete`), complete domain and item responses, every dispute with target/response/reason/blocking flag, `d16_acknowledgement=true`, and a non-empty hash-bound rationale. The reviewer confirms that the exact Red applicability, provenance, joins, populations, interventions, warnings, construction history, and authority limits were inspected.

Machine readiness, the 06-13 response, and a disputed or incomplete decision cannot close the phase. Closure requires 06-14-01 to publish and validate the canonical `partition-evaluation-red-generation-003-decision.json`, followed by 06-14-02 exact resume, with `approved` disposition, every domain/item response approved, no disputes, `conclusion_ready=true`, `phase7_interpretation_authorized=true`, all broader authorities false, and the generation-002 decision still absent.

## Sign-Off

- [ ] All recovery rows are executable and green only after their own work completes.
- [ ] Generation-002 remains `incomplete_execution_failed_closed` and decision-free.
- [ ] Generation-003 policy is frozen only after the four regressions exist and the RED absence-path test passes.
- [ ] D-01 through D-16 retain Red-only, no-call, no-publication, and bounded-human-authority limits.
- [ ] Only the clean canonical generation-003 decision predicate can close Phase 6.

**Approval:** pending

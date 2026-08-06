---
phase: 06-partition-aware-ablation-and-metamorphic-evaluation
plan: 02
subsystem: evaluation
tags: [python, unittest, canonical-json, closed-join, pairwise-ablation, red-path]
requires:
  - phase: 06-01
    provides: Red-only result states, atomic rows, population manifests, and independent authority admissions
provides:
  - Closed D-08 artifact joins with exact atomic composite identities
  - Independent B-minus-A and C-minus-B pairwise contracts without shared populations
  - Advisory-only warning and blocking-failure ledgers with scoped dependency propagation
affects: [06-03, 06-04, 06-05, phase-07]
actuals:
  tokens: 6487
  tasks: 2
  commits: 5
tech-stack:
  added: []
  patterns: [closed artifact binding, exact control projection, report-only warning ledger, acyclic blocker propagation]
key-files:
  created: []
  modified:
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py
    - experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py
key-decisions:
  - "Represent Red pairwise comparisons as visible contracts with no rows, ratio, numerator, or denominator."
  - "Keep FRAME_COMBINATION_REQUIRES_REVIEW in a separately ordered advisory ledger that cannot enter scoring."
  - "Withhold only the declared dependency closure of a blocking failure so independent namespaces remain auditable."
patterns-established:
  - "Applicable artifact joins require one exact role set; all missing, extra, duplicate, or cross-partition inputs become invalid_withheld."
  - "Pairwise treatments compare exact control projections and derive separate population identities for each intervention."
requirements-completed: [H1-02, H1-03, H1-04, H2-04]
coverage:
  - id: D1
    description: Closed joins and B-minus-A/C-minus-B contracts fail closed on malformed or confounded inputs while Red stays row-free.
    requirement: H1-02
    verification:
      - kind: unit
        ref: tests/test_partition_evaluation.py#PartitionEvaluationTests.test_pair_join_rejects_missing_duplicate_and_cross_partition_rows
        status: pass
      - kind: unit
        ref: tests/test_partition_evaluation.py#PartitionEvaluationTests.test_c_minus_b_population_is_independent
        status: pass
    human_judgment: false
  - id: D2
    description: Frame warnings remain advisory-only and exact frozen-binding drift withholds only dependent frame results.
    requirement: H1-03
    verification:
      - kind: unit
        ref: tests/test_partition_evaluation.py#PartitionEvaluationTests.test_frame_warning_is_report_only
        status: pass
      - kind: unit
        ref: tests/test_partition_evaluation.py#PartitionEvaluationTests.test_frozen_binding_drift_withholds_dependent_domain
        status: pass
    human_judgment: false
duration: 24m
completed: 2026-08-06
status: complete
---

# Phase 06 Plan 02: Closed Join and Pairwise Evaluation Summary

**Closed case joins, independent ablation populations, and report-only frame warnings now preserve the Red branch's zero-row boundary without manufacturing experimental evidence.**

## Performance

- **Duration:** 24m
- **Started:** 2026-08-06T09:29:00Z
- **Completed:** 2026-08-06T09:53:10Z
- **Tasks:** 2/2
- **Files modified:** 2

## Accomplishments

- Added explicit applicable/inapplicable artifact bindings and D-08 closed-join manifests that reject incomplete, extra, duplicate, or cross-partition atomic inputs before a pair can score.
- Built separately identified B-minus-A and C-minus-B comparisons with exact permitted control differences; the frozen Red branch exposes both contracts without A/B/C rows or ratio fields.
- Added deterministic advisory-warning and failure ledgers plus scoped blocker propagation, preserving independent audit namespaces while withholding only declared dependents.

## Task Commits

1. **Task 1: Close atomic joins and isolate B-minus-A from C-minus-B** - `b116bd7e` (test), `549bf91a` (test), `79d5e5f0` (feat)
2. **Task 2: Separate frame warnings from failures and propagate only blocking authority** - `f88d53b6` (test), `4ffd34a2` (feat)

## Files Created/Modified

- `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py` - closed artifact joins, pairwise controls, Red comparison contracts, warning/failure ledgers, and dependency propagation.
- `experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py` - closure tamper, independent-population, Red no-row, advisory-invariance, and frozen-binding tests.

## Decisions Made

- Red inapplicability is represented by an explicit pairwise contract rather than fabricated A/B/C treatment rows or numeric zeroes.
- Advisory diagnostics may be reported and ordered but cannot change correctness, eligibility, identity, population, denominator, or score.
- Frozen-binding failures produce typed authority failures and only invalidate their dependency-graph closure.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Restored isolated Ruff import ordering after extending the test contract**
- **Found during:** Task 1
- **Issue:** The added core/test imports violated the repository's isolated Ruff gate.
- **Fix:** Applied Ruff's deterministic import ordering to the touched files.
- **Files modified:** `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py`, `experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py`
- **Verification:** isolated Ruff passed after the correction.
- **Committed in:** `549bf91a`

**Total deviations:** 1 auto-fixed Rule 1 issue.
**Impact on plan:** Formatting-only correction; no scope or authority expansion.

## Issues Encountered

The full module takes about 93 seconds because its existing integration checks rebuild isolated frozen trees. It completed successfully without retries or external access.

## Known Stubs

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plans 06-03 through 06-05 can consume closed joins, independent pairwise identities, report-only warning records, and scoped invalid-withheld propagation without reopening the Red-only authority boundary.

## Self-Check: PASSED

Both modified files exist and all five task commits are present in repository history.

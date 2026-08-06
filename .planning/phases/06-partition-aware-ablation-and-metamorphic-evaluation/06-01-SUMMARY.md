---
phase: 06-partition-aware-ablation-and-metamorphic-evaluation
plan: 01
subsystem: evaluation
tags: [python, unittest, canonical-json, red-path, metamorphic-registry]
requires:
  - phase: 02-deterministic-measurement-spine
    provides: frozen formal case outcomes and independently denominated metrics
  - phase: 05-authorized-execution-and-immutable-evidence
    provides: validated Red no-call evidence root
provides:
  - Red-only evaluator with independent deterministic and Red-evidence admissions
  - Four-state metric contract with canonical population manifests
  - Complete, unscored frozen metamorphic direction projection
affects: [06-02, 06-03, 06-04, 06-05, phase-07]
actuals:
  tokens: 9429
  tasks: 2
  commits: 4
tech-stack:
  added: []
  patterns: [descriptor-bound reads, canonical JSON, four-state result union, Red-first review packet]
key-files:
  created:
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/__init__.py
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/cli.py
    - experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py
  modified: []
key-decisions:
  - "Preserve deterministic measurement and Red execution evidence as independent admitted namespaces."
  - "Represent every Green/Yellow-only Red metric as not_applicable_red without a numerator, denominator, or score."
  - "Bind metamorphic directions to the Phase 3 authority registry while emitting no Red observation."
requirements-completed: [TS-06, TS-13]
coverage:
  - id: D1
    description: Red evaluation preserves authority-separated metrics, population denominators, and result-state legality.
    requirement: TS-06
    verification:
      - kind: integration
        ref: tests/test_partition_evaluation.py#PartitionEvaluationTests.test_red_metrics_preserve_applicability_and_separate_denominators
        status: pass
    human_judgment: false
  - id: D2
    description: The four frozen metamorphic directions are complete, unavailable, and unscored on Red.
    requirement: TS-13
    verification:
      - kind: integration
        ref: tests/test_partition_evaluation.py#PartitionEvaluationTests.test_red_metamorphic_registry_is_complete_and_unscored
        status: pass
    human_judgment: false
duration: 11m 26s
completed: 2026-08-06
status: complete
---

# Phase 06 Plan 01: Red Evaluation Tracer Summary

**A strict local evaluator now independently admits frozen Phase 2 measurement and Phase 5 no-call evidence, then emits a Red-first, decision-free packet with population-bound metrics and unscored metamorphic applicability.**

## Performance

- **Duration:** 11m 26s
- **Started:** 2026-08-06T09:28:52Z
- **Completed:** 2026-08-06T09:40:18Z
- **Tasks:** 2/2
- **Files modified:** 5

## Accomplishments

- Added a standard-library-only `specchoice_evaluation` package with descriptor-bound authority admission, canonical serialisation, and no model/provider/retrieval/network/subprocess surface.
- Preserved distinct `measured`, `empty_population`, `not_applicable_red`, and `invalid_withheld` result contracts; every measured denominator is rebuilt from a canonical eligible-ID manifest.
- Projected all four Phase 3 metamorphic direction IDs as registry-bound, unavailable, non-counting Red records without synthetic cases, metrics, or observations.

## Task Commits

1. **Task 1: Trace one frozen Red evaluation from authority roots to reviewer packet** - `345ce63f` (test), `be5b02af` (feat)
2. **Task 2: Project the complete frozen metamorphic registry without Red observations** - `bc08a63c` (feat)
3. **Verification correction:** `498c89f2` (fix)

## Files Created

- `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py` - authority admissions, locked result union, population manifests, Red metrics, and metamorphic projection.
- `experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py` - decision-free canonical packet, Red-first Markdown, and readiness identity.
- `experiments/specchoice-v1.3.2/src/specchoice_evaluation/cli.py` - exact `build-red` local entry point with required repository and policy arguments.
- `experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py` - frozen-root, four-state, canonical-order, CLI-surface, and metamorphic-drift coverage.

## Decisions Made

- Admission identities hash their descriptor-bound raw source set; authority self-hashes remain semantic bindings and are never substituted for raw-file hashes.
- The evaluator is decision-free: readiness is an identity only and cannot grant review, execution, retrieval, or publication authority.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Kept Red authority self-hash distinct from raw-file identity**
- **Found during:** Task 2
- **Issue:** Comparing `authority_sha256` to the raw authority-file digest incorrectly withheld the valid Red evidence namespace.
- **Fix:** Validate the receipt against the authority self-hash while preserving the descriptor-bound raw set hash in the admission record.
- **Files modified:** `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py`
- **Verification:** frozen Red integration and metamorphic registry tests pass.
- **Committed in:** `bc08a63c`

**2. [Rule 1 - Bug] Corrected isolated Ruff failures**
- **Found during:** Plan-level verification
- **Issue:** Import ordering, one unused binding, and exception type did not satisfy the repository's isolated Ruff gate.
- **Fix:** Applied the minimal lint-compliant edits without changing evaluation behavior.
- **Files modified:** `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py`, `review.py`, `tests/test_partition_evaluation.py`
- **Verification:** focused suite and isolated Ruff pass.
- **Committed in:** `498c89f2`

**Total deviations:** 2 auto-fixed Rule 1 issues.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation tests.test_measurement_scoring tests.test_data_relevance tests.test_authorized_execution_v2 -q` — pass
- `../../.venv/bin/ruff check --isolated src/specchoice_evaluation tests/test_partition_evaluation.py` — pass
- `git diff --check` — pass

## Known Stubs

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plans 06-02 through 06-05 can extend the locked Red evaluator without pooling its authority namespaces or converting Red inapplicability into an experimental zero.

## Self-Check: PASSED

All five implementation/test files and all four task commits are present in the repository history.

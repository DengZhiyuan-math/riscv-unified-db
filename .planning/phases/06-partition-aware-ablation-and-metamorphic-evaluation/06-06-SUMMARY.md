---
phase: 06-partition-aware-ablation-and-metamorphic-evaluation
plan: 06
subsystem: evaluation evidence provenance
tags: [python, unittest, canonical-json, sha256, red-only, provenance, runtime-closure]
requires:
  - phase: 06-05
    provides: Immutable generation-001 package and hash-bound human decision
provides:
  - Root-derived generation-002 policy, packet, readiness, and decision validation
  - Exact policy-bound construction source inventory under an explicit project root
  - Exact evaluation component inventory and stable malformed-runtime diagnostics
affects: [06-07, phase-6-verification, phase-7-interpretation]
actuals:
  tokens: 8886
  tasks: 2
  commits: 4
tech-stack:
  added: []
  patterns:
    - Explicit experiment-root and project-root authority boundaries
    - Canonical expected-packet rebuild before package, readiness, or decision acceptance
    - Ordered path/status/hash construction declaration contract
key-files:
  created: []
  modified:
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/cli.py
    - experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py
key-decisions:
  - "Generation-001 remains byte-identical historical evidence; only a generation-002 policy schema can satisfy the repaired derivation contract."
  - "Construction feasibility admits exactly nineteen ordered project-relative path/status/hash declarations and never infers repository authority from path depth."
  - "One exact component tuple governs policy declarations, packet components, and component hashes; malformed runtime entries fail with a controlled diagnostic."
patterns-established:
  - "Validate admitted inputs, rebuild canonical expected bytes, then compare the caller-supplied packet before downstream identities are trusted."
  - "Validate runtime membership and digest against the declared input inventory before descriptor-read lookup."
requirements-completed: [TS-06, H1-03]
coverage:
  - id: D1
    description: Rehashed forged packets and all declared construction-source mutations fail before generation-002 output publication.
    requirement: TS-06
    verification:
      - kind: unit
        ref: tests/test_partition_evaluation.py#PartitionEvaluationTests.test_forged_rehashed_packet_is_rejected_by_root_derivation
        status: pass
      - kind: unit
        ref: tests/test_partition_evaluation.py#PartitionEvaluationTests.test_each_declared_construction_source_is_policy_bound
        status: pass
    human_judgment: false
  - id: D2
    description: Exact component inventories and malformed runtime declarations fail closed through a stable non-traceback CLI error.
    requirement: H1-03
    verification:
      - kind: unit
        ref: tests/test_partition_evaluation.py#PartitionEvaluationTests.test_component_inventory_is_exact_and_live
        status: pass
      - kind: unit
        ref: tests/test_partition_evaluation.py#PartitionEvaluationTests.test_runtime_policy_error_is_stable_and_traceback_free
        status: pass
    human_judgment: false
duration: 5m
completed: 2026-08-06
status: complete
---

# Phase 06 Plan 06: Evaluation Provenance Gap Closure Summary

**Generation-002-only validation now rebuilds Red evaluation bytes from explicit admitted roots, freezes every construction source, and rejects incomplete component or runtime declarations without mutating generation-001 evidence.**

## Performance

- **Duration:** 5m
- **Started:** 2026-08-06T14:24:28+02:00
- **Completed:** 2026-08-06T14:28:40+02:00
- **Tasks:** 2/2
- **Files modified:** 4

## Accomplishments

- Rebuilt the expected Red packet from validated experiment/project roots and required canonical equality before readiness or review-decision validation.
- Bound construction feasibility to the complete ordered nineteen-file policy declaration, rejecting any source, status, order, duplicate, or digest drift before output creation.
- Enforced one exact component inventory and converted undeclared runtime closure input faults to `EVALUATION_POLICY_RUNTIME_INVALID` with exit code 2 and no traceback.
- Preserved every generation-001 policy, packet, Markdown, readiness, and decision byte exactly; no generation-002 policy, package, or decision was published.

## Task Commits

1. **Task 1: Trace policy-admitted roots through canonical derivation validation** — `97055400` (RED tests), `16716694` (implementation)
2. **Task 2: Enforce exact components and stable runtime diagnostics** — `0f11c6f3` (RED tests), `3d74bc93` (implementation)

## Files Created/Modified

- `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py` — explicit-root declared construction evidence contract.
- `experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py` — successor-only derived packet validation, exact component checks, and runtime declaration guard.
- `experiments/specchoice-v1.3.2/src/specchoice_evaluation/cli.py` — strict explicit experiment/project root command boundary.
- `experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py` — forged-package, construction-inventory, generation-history, component, and CLI runtime regressions.

## Validation

- Focused provenance and construction tests passed.
- Focused component and runtime-diagnostic tests passed.
- `tests.test_partition_evaluation`, `tests.test_measurement_scoring`, `tests.test_data_relevance`, and `tests.test_authorized_execution_v2` passed.
- Isolated Ruff and `git diff --check` passed.
- Current and pre-plan SHA-256 values match for all five generation-001 evidence artifacts; no `generation-002` path exists in the repository.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Restored isolated Ruff compliance after replacing the legacy CLI path**
- **Found during:** Task 1
- **Issue:** The new explicit-root CLI made three former imports unused and required canonical import formatting.
- **Fix:** Removed only the stale imports and applied the formatter's import layout.
- **Files modified:** `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py`, `experiments/specchoice-v1.3.2/src/specchoice_evaluation/cli.py`
- **Verification:** Isolated Ruff passed.
- **Committed in:** `16716694`

**Total deviations:** 1 auto-fixed Rule 1 issue.
**Impact on plan:** Formatting and unused-import correction only; no authority or dependency surface changed.

## Known Stubs

None. The empty mappings and lists found in Red-only evaluation code and tests represent explicit empty Red populations or test inputs, not UI-facing placeholders.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 06-07 can construct and publish a new generation only from a separately approved generation-002 policy. Generation-001 remains preserved history and cannot be reused as current derivation authority.

## Self-Check: PASSED

- All four plan files exist.
- Commits `97055400`, `16716694`, `0f11c6f3`, and `3d74bc93` are present in history.
- Generation-001 policy, packet, Markdown, readiness, and decision SHA-256 values match their pre-plan bytes.

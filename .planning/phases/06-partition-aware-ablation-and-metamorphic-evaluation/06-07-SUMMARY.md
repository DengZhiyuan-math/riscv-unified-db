---
phase: 06-partition-aware-ablation-and-metamorphic-evaluation
plan: 07
subsystem: evaluation evidence integrity
tags: [python, unittest, canonical-json, sha256, pairwise, provenance, red-only]
requires:
  - phase: 06-06
    provides: Root-derived policy validation, exact construction inventory, and runtime closure admission
provides:
  - Verified closed-join references for all pairwise scoring members
  - Immutable frozen A/B and B/C intervention contracts with exact-control validation
  - Generation-002 policy bound to fixed evaluator, test, construction, runtime, and predecessor bytes
affects: [phase-6-verification, phase-7-interpretation]
actuals:
  tokens: 10220
  tasks: 3
  commits: 5
tech-stack:
  added: []
  patterns:
    - Closed join references must carry one exact atomic row and an expected join hash
    - Pairwise attribution validates a treatment-specific frozen intervention before any denominator exists
    - Successor policies preserve predecessor evidence as non-authorizing derivation history
key-files:
  created:
    - experiments/specchoice-v1.3.2/config/evaluation/partition-evaluation-red-generation-002.json
  modified:
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py
    - experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py
key-decisions:
  - "Bare atomic rows cannot enter pairwise scoring; each member requires a closed manifest containing its exact identity once and the expected policy-bound join hash."
  - "A/B DelegationFrame and B/C complete-pair selection use immutable canonical treatment identities; equal, absent, swapped, ambient, or control-mismatched projections are invalid_withheld."
  - "Generation-001 remains byte-identical superseded derivation history; generation-002 is the sole policy successor and creates no package or human decision."
requirements-completed: [H1-02, H1-04, H2-04]
coverage:
  - id: D1
    description: Closed join references reject bare, missing, duplicated, cross-boundary, and hash-substituted pairwise members.
    requirement: H1-02
    verification:
      - kind: unit
        ref: tests/test_partition_evaluation.py#test_pairwise_requires_closed_verified_join
        status: pass
      - kind: unit
        ref: tests/test_partition_evaluation.py#test_substituted_closed_join_hash_cannot_measure
        status: pass
    human_judgment: false
  - id: D2
    description: Frozen treatment identities prove the named A/B or B/C intervention changed while all other controls stay equal.
    requirement: H2-04
    verification:
      - kind: unit
        ref: tests/test_partition_evaluation.py#test_pairwise_requires_real_named_intervention
        status: pass
      - kind: unit
        ref: tests/test_partition_evaluation.py#test_pairwise_rejects_missing_or_treatment_inconsistent_intervention
        status: pass
    human_judgment: false
  - id: D3
    description: Generation-002 freezes final inputs and preserved generation-001 predecessor identities without creating successor outputs.
    requirement: H1-04
    verification:
      - kind: unit
        ref: tests/test_partition_evaluation.py#test_generation_002_policy_freezes_fixed_code_construction_and_predecessor
        status: pass
    human_judgment: false
duration: 14min
completed: 2026-08-06
status: complete
---

# Phase 06 Plan 07: Pairwise Integrity and Generation-002 Policy Summary

**Closed-manifest pairwise admission, frozen treatment-difference contracts, and a non-publishing generation-002 Red policy successor**

## Performance

- **Duration:** 14 min
- **Started:** 2026-08-06T12:32:59Z
- **Completed:** 2026-08-06T12:46:54Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

- Replaced bare-row pairwise admission with immutable `VerifiedJoinReference` validation, including closed status, exact one-row membership, self identity, and policy-bound join hash.
- Bound the two named intervention comparisons to exact frozen treatment identities and withheld all unchanged, missing, swapped, unknown, or otherwise control-mismatched candidates.
- Added a forward-only generation-002 policy that binds final source/test bytes, construction and runtime inputs, and generation-001 predecessor hashes without creating successor outputs.

## Task Commits

1. **Task 1 RED: closed join regressions** - `c5fcb4a1` (test)
2. **Task 1 GREEN: verified closed joins** - `dc4e732f` (feat)
3. **Task 2 RED: named intervention regressions** - `f4da9009` (test)
4. **Task 2 GREEN: frozen pairwise interventions** - `724662d0` (feat)
5. **Task 3: generation-002 policy** - `69013e72` (feat)

## Files Created/Modified

- `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py` - Enforces closed joins, frozen intervention values, and exact construction declaration hashes.
- `experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py` - Adversarial pairwise and generation-002 policy coverage.
- `experiments/specchoice-v1.3.2/config/evaluation/partition-evaluation-red-generation-002.json` - Canonical forward-only successor policy.

## Decisions Made

- The paired metric remains wholly invalid when any supplied reference is bare, incomplete, duplicate, cross-boundary, or bound to an unexpected join hash; valid members never salvage a partial denominator.
- Construction declarations and on-disk source custody receive distinct stable diagnostics so a forged policy cannot be confused with a changed immutable source.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Restored the construction declaration's stable diagnostic boundary**
- **Found during:** Task 3
- **Issue:** The 06-06 exact-declaration regression expected `CONSTRUCTION_SOURCE_CONTRACT_INVALID` for a substituted declared hash, but the evaluator classified it as an artifact substitution.
- **Fix:** Added the immutable ordered construction SHA-256 contract. Declared-hash drift now fails as a contract error; physical source-byte drift still fails as `CONSTRUCTION_ARTIFACT_SUBSTITUTED`.
- **Files modified:** `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py`, `experiments/specchoice-v1.3.2/config/evaluation/partition-evaluation-red-generation-002.json`
- **Verification:** Full `tests.test_partition_evaluation` suite and isolated Ruff.
- **Committed in:** `69013e72` (part of Task 3)

**Total deviations:** 1 auto-fixed (Rule 1)

## Issues Encountered

Shared direct-main index locking prevented executor-side commits. The parent executor committed each exact prepared scope; no lock was removed or bypassed.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Generation-002 is immutable policy material only. A separate create-only successor may publish its packet, report, and readiness material; any human decision remains outside this plan.

## Self-Check: PASSED

- All three task artifacts exist at their recorded paths.
- All five task commits are present in Git history.
- Generation-001 policy, packet, report, readiness, and approved decision are unchanged; generation-002 packet, report, readiness, and decision remain absent.

---
*Phase: 06-partition-aware-ablation-and-metamorphic-evaluation*
*Completed: 2026-08-06*

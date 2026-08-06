---
phase: 06-partition-aware-ablation-and-metamorphic-evaluation
plan: 03
subsystem: evaluation
tags: [red-only, canonical-json, sha256, pairhit, metamorphic, construction-feasibility]
requires:
  - phase: 06-02
    provides: Closed joins, independent pairwise identities, and scoped blocker propagation
  - phase: 05-authorized-execution-and-immutable-evidence
    provides: Immutable Red execution and construction lifecycle evidence
provides:
  - Registry-bound Red metamorphic, repeat, shortcut-family, and PairHit result builders
  - A non-experimental immutable construction-feasibility audit track
affects: [06-04, 06-05, evaluation-packet, verifier]
actuals:
  tokens: 6246
  tasks: 3
  commits: 4
tech-stack:
  added: []
  patterns:
    - Canonical frozen-registry admission before result construction
    - Separate empty, inapplicable, and construction-evidence namespaces
key-files:
  created: []
  modified:
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py
    - experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py
key-decisions:
  - "PairHit@2 derives solely from strict_pairhit_eligible_case_ids and has no Red ratio."
  - "Construction lifecycle records remain immutable audit evidence outside rows, populations, and metrics."
  - "All four frozen metamorphic direction IDs are emitted in canonical order and retain unavailable Red status."
patterns-established:
  - "Fail closed on frozen family, split, relevance, or metamorphic binding drift while preserving independent deterministic evidence."
  - "Use SHA-256-bound population manifests for empty as well as measurable populations."
requirements-completed: [TS-13, H1-04, H2-03, H2-04]
coverage:
  - id: D1
    description: Frozen metamorphic directions and empty repeat/shortcut-family Red tracks remain visible without observations or scores.
    requirement: TS-13
    verification:
      - kind: unit
        ref: experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py#test_red_metamorphic_registry_is_complete_and_unscored
        status: pass
    human_judgment: false
  - id: D2
    description: PairHit@2 is bound to the exact frozen strict eligible collection and exposes no ratio for Red's empty population.
    requirement: H2-03
    verification:
      - kind: unit
        ref: experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py#test_pairhit_uses_only_frozen_eligible_ids
        status: pass
    human_judgment: false
  - id: D3
    description: Construction feasibility preserves Phase 5 predecessor/successor history outside experimental result namespaces.
    requirement: H2-04
    verification:
      - kind: unit
        ref: experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py#test_construction_feasibility_preserves_attempt_order_and_namespace
        status: pass
    human_judgment: false
duration: 25min
completed: 2026-08-06
status: complete
---

# Phase 06 Plan 03: Non-Pair Evaluation Tracks Summary

**Canonical registry-bound PairHit, metamorphic, repeat, shortcut-family, and construction-feasibility tracks that preserve Red absence without creating experimental observations or ratios.**

## Performance

- **Duration:** 25 min
- **Started:** 2026-08-06T10:46:00Z
- **Completed:** 2026-08-06T11:11:32Z
- **Tasks:** 3
- **Files modified:** 2

## Accomplishments

- Bound all four frozen metamorphic direction records, repeat emptiness, and shortcut-family results to canonical frozen registry identities.
- Added PairHit@2 eligibility enforcement with a distinct hashed empty Red population and no numerator, denominator, score, or retrieved rows.
- Added an immutable construction-feasibility audit for the Phase 5 lifecycle that cannot become an atomic result row, population, denominator, ratio, score, or correctness outcome.

## Task Commits

1. **Task 1: Bind metamorphic, repeat, and shortcut-family results** — `ed48493e` (RED test), `988339bc` (feat)
2. **Task 2: Calculate PairHit only over preregistered eligible population** — `19471c31` (feat)
3. **Task 3: Preserve C-minus-B independence and Phase 5 construction history** — `ea4c3b60` (feat)

## Files Created/Modified

- `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py` — Registry admission, Red non-pair result builders, PairHit eligibility, and construction-history audit types.
- `experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py` — Frozen-registry, empty PairHit, repeat, and construction namespace contracts.

## Decisions Made

- PairHit input keys must exactly equal the frozen strict eligible case collection; no ambient relevance or pooled denominator is accepted.
- Repeat observations and repeat comparisons are distinct immutable records; the Red branch has neither while still exposing a hashed empty repeat population.
- Construction evidence is path/hash/status-bound in a separate type and retains its predecessor/successor order rather than producing a success rate.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Removed a duplicate metamorphic test definition and restored isolated Ruff ordering.**
- **Found during:** Task 1
- **Issue:** The new contract test shadowed an existing same-named Red metamorphic test, which would have disabled the original regression assertions.
- **Fix:** Retained the established integration test, removed the duplicate, and applied Ruff's import ordering.
- **Files modified:** `experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py`, `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py`
- **Verification:** Focused unit tests and isolated Ruff passed.
- **Committed in:** `988339bc`

**2. [Rule 1 - Bug] Corrected the construction test's repository-relative source-path assertion.**
- **Found during:** Task 3
- **Issue:** The test omitted the valid `experiments/` prefix used by repository-relative construction evidence paths.
- **Fix:** Accepted only `.planning/` and `experiments/` repository-relative sources.
- **Files modified:** `experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py`
- **Verification:** Focused construction test, full module, and isolated Ruff passed.
- **Committed in:** `ea4c3b60`

**Total deviations:** 2 auto-fixed Rule 1 issues.

## Issues Encountered

The shared-worktree commit handoff placed the PairHit RED test in the Task 1 feature commit. Its failing behavior was nevertheless directly verified before Task 2 implementation, and the Task 2 production code remains isolated in `19471c31`.

## Known Stubs

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plans 06-04 and 06-05 can consume independent Red-only non-pair result identities and the immutable construction audit without reopening model, retrieval, network, credential, subprocess, or publication authority.

## Self-Check: PASSED

Both modified implementation/test files exist, and `ed48493e`, `988339bc`, `19471c31`, and `ea4c3b60` are present in repository history.

---
*Phase: 06-partition-aware-ablation-and-metamorphic-evaluation*
*Completed: 2026-08-06*

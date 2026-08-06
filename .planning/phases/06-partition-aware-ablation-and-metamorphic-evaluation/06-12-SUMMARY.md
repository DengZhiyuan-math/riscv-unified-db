---
phase: 06-partition-aware-ablation-and-metamorphic-evaluation
plan: 12
subsystem: immutable evaluation evidence
tags: [python, canonical-json, sha256, red-only, exact-resume, immutable-custody]
requires:
  - phase: 06-11
    provides: Frozen generation-003 policy, generation-002 incomplete-predecessor custody, and pre-publication attack regressions
provides:
  - Root-derived, decision-free generation-003 Red packet, reviewer projection, and readiness receipt
  - Byte- and nanosecond-mtime-identical zero-write replay of the complete package
  - Passing frozen adversarial rejection matrix while preserving generation-002 history
affects: [06-13, 06-14, phase-6-verification, phase-7-interpretation]
actuals:
  tokens: 36366
  tasks: 2
  commits: 1
tech-stack:
  added: []
  patterns:
    - Descriptor-bound create-only package publication permits only byte-identical exact resume
    - Readiness proves machine validation without creating review or Phase 7 authority
key-files:
  created:
    - experiments/specchoice-v1.3.2/runs/partition-evaluation-red-generation-003/evaluation-packet.json
    - experiments/specchoice-v1.3.2/runs/partition-evaluation-red-generation-003/evaluation-report.md
    - experiments/specchoice-v1.3.2/receipts/partition-evaluation-red-generation-003-readiness.json
  modified: []
key-decisions:
  - "Generation-003 remains a decision-free Red readiness artifact; human approval and Phase 7 interpretation are outside this plan."
requirements-completed: [TS-06, TS-13, H1-02, H1-03, H1-04, H2-03, H2-04]
coverage:
  - id: D1
    description: Root-derived generation-003 packet, report, and readiness receipt are published with all Red authority limits intact.
    requirement: TS-06
    verification:
      - kind: integration
        ref: specchoice_evaluation.cli build-red and verify-red-package for partition-evaluation-red-generation-003
        status: pass
    human_judgment: false
  - id: D2
    description: Generation-003 exact resume is zero-write and the pre-frozen adversarial probes reject substituted, partial, and unsafe output states.
    requirement: TS-13
    verification:
      - kind: unit
        ref: tests/test_partition_evaluation.py#test_generation_003_exact_resume_and_adversarial_rejection
        status: pass
      - kind: other
        ref: ruff check --isolated tests/test_partition_evaluation.py
        status: pass
    human_judgment: false
duration: 16min
completed: 2026-08-06
status: complete
---

# Phase 06 Plan 12: Generation-003 Publication Summary

**Immutable Red-only generation-003 evaluation packet, reviewer report, and readiness receipt with byte- and nanosecond-mtime-identical exact resume**

## Performance

- **Duration:** 16 min
- **Started:** 2026-08-06T16:01:33Z
- **Completed:** 2026-08-06T16:17:32Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- Published the only permitted generation-003 evidence set from the frozen policy and admitted roots: a canonical packet, deterministic reviewer report, and readiness receipt.
- Verified the package is `complete=true` while remaining Red-only and non-conclusive: `N_strict=0`, `repeat_count=0`, no model-call authority, and no generation-003 decision file.
- Replayed the same builder without any output-byte or nanosecond-mtime change, then passed the generation-002 custody, generation-003 freeze, exact-resume/adversarial, and isolated Ruff checks.

## Task Commits

1. **Task 1: Publish and verify one generation-003 Red path** - `a755dfe1` (feat)
2. **Task 2: Prove zero-write resume and the frozen attack matrix** - verification-only; no repository changes to commit

## Files Created/Modified

- `experiments/specchoice-v1.3.2/runs/partition-evaluation-red-generation-003/evaluation-packet.json` - Canonical, root-derived Red packet; embedded packet SHA-256 is `a97c6d744f4ca960b0efbbc115f5b80fb1bbc2169b9c98b5a266fc46aab78a62`.
- `experiments/specchoice-v1.3.2/runs/partition-evaluation-red-generation-003/evaluation-report.md` - Deterministic reviewer-facing projection of the packet.
- `experiments/specchoice-v1.3.2/receipts/partition-evaluation-red-generation-003-readiness.json` - Decision-free readiness; embedded readiness SHA-256 is `837775e9a413b46e5cc69c841cf1dde31775b3cea1fe6249d9267555ddf324d0`.

## Decisions Made

None - followed the frozen generation-003 policy exactly. The generated readiness is not a human decision and grants no Phase 7, model, provider, network, retrieval, subprocess, or publication authority.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Generation-003 is available for the separate human-review path in 06-13. It remains decision-free; 06-14 is the only later plan that may publish a decision after the explicit human response and its own exact-resume checks.

## Self-Check: PASSED

- Confirmed all three generation-003 package files exist.
- Confirmed task commit `a755dfe1` is present in Git history.

---
*Phase: 06-partition-aware-ablation-and-metamorphic-evaluation*
*Completed: 2026-08-06*

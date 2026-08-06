---
phase: 05-authorized-execution-and-immutable-evidence
plan: 09
subsystem: evidence-custody
tags: [git-archive, canonical-json, immutable-custody, red-evidence]
requires:
  - phase: 05-08
    provides: projection-v3 attempt-03/04 custody and native-port validation records
provides:
  - Git-tracked immutable projection-v2 failed-closed root
  - Canonical custody-only v2-to-v3 path-substitution receipt
  - Clean-export proof for independent Phase 5 re-verification
affects: [phase-05-reverification, phase-06]
actuals:
  tokens: 9118
  tasks: 2
  commits: 2
tech-stack:
  added: []
  patterns: [create-only canonical custody receipt, git-archive clean-tree validation]
key-files:
  created:
    - experiments/specchoice-v1.3.2/receipts/native-port-projection-v2-to-v3-custody-successor-v1.json
    - experiments/specchoice-v1.3.2/runs/native-port-darwin-arm64-projection-v2-20260805/contract-validation.json
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-09-SUMMARY.md
  modified: []
key-decisions:
  - "Preserved the root byte-for-byte and used a canonical forward-only receipt instead of rewriting v2 or v3 history."
  - "Kept the receipt non-authoritative: no model, provider, credential, retrieval, Green/Yellow, network, publication, metric, requirement-status, or conclusion authority is granted."
patterns-established:
  - "A clean git archive, rather than a dirty worktree, is the reproducibility boundary for custody closure."
requirements-completed: [TS-07, TS-11, TS-12]
coverage:
  - id: D1
    description: "Tracked projection-v2 root and six-entry canonical v2-to-v3 custody mapping."
    requirement: TS-07
    verification:
      - kind: integration
        ref: "git archive HEAD clean-export digest, predecessor-chain, mapping, and canonical-byte assertion"
        status: pass
    human_judgment: false
  - id: D2
    description: "Red no-call controls and exact predecessor admission rechecked without construction or publication."
    requirement: TS-11
    verification:
      - kind: unit
        ref: "tests.test_authorized_execution_v2, tests.test_native_port_contract, tests.test_guarded_regress focused command"
        status: pass
    human_judgment: false
status: complete
---

# Phase 05 Plan 09: Immutable Custody Gap Closure Summary

**The original failed-closed projection-v2 root is now Git-tracked unchanged, with a canonical non-authoritative receipt mapping every declared v2 custody location to its committed v3 successor.**

## Performance

- **Duration:** ~15 minutes
- **Completed:** 2026-08-06
- **Tasks:** 2/2
- **Files created:** 3

## Accomplishments

- Preserved the root at SHA-256 `7f6d0761ccdb775ddb62e13ca641dd389819e587acaf29ca4f805f0ab502a1fd`, Git blob `b32fc236bda37245529421bb9891f506d722db88`, state `failed_closed`, and diagnostic `ORACLE_EXECUTION_NOT_IMPLEMENTED`.
- Published `native-port-projection-v2-to-v3-custody-successor-v1` as canonical UTF-8/LF JSON, binding the `05-VERIFICATION.md` `gaps_found` identity and all six declared-to-actual substitutions.
- Reproduced root → attempt-02 → attempt-03 → attempt-04 from `git archive ff8c62e3fa8785f00252f2998f76b9e682a48a3c`, without consulting dirty or untracked worktree data.

## Task Commits

1. **Task 1: Make the unchanged v2 root durable and publish the path-mapping successor** — `ff8c62e3` (`fix`)
2. **Task 2: Prove the mapped chain from a clean Git export and hand off re-verification** — `f0cb15a0` (`docs`)

## Evidence Verified

| Artifact | SHA-256 / state | Introducing commit |
| --- | --- | --- |
| Projection-v2 root | `7f6d0761…502a1fd`; `failed_closed` | This plan, unchanged blob `b32fc236…722db88` |
| Projection-v2 attempt-02 | `84feca91…48bbf32`; `tracer_validated` | `d61c2b60…a5dc0f9a` |
| Projection-v3 attempt-03 | `3907ba6e…225d5391`; `all_tools_validated_cache_unpublished` | `b0c3926c…2cc81aa2` |
| Projection-v3 attempt-04 | `3bf0c8fc…3707d3f15`; `validation_complete` | `1d83a6cc…cf1f209f` |
| Projection-v3 contract / fixture | `34bd9634…577f3d97` / `74cf1def…ba52138e` | `b0c3926c…2cc81aa2` |
| Projection-v3 eqntott / mustool patches | `8f44de60…d12d4b49` / `b858cd29…09651200e` | `b0c3926c…2cc81aa2` |
| Custody successor receipt | `9ad56226…55dd4168ce` | `ff8c62e3…682a48a3c` |

The clean export recomputed every listed file digest, all predecessor path/SHA/state bindings, the six substitution entries and their introducing commits, and exact canonical receipt bytes. It also confirmed that all authority-limit booleans remain false except `non_authoritative=true`.

## Validation

- `git archive HEAD` into a new temporary directory: passed canonical-byte, digest, state, predecessor-chain, six-mapping, and authority-limit assertions.
- Confirmed every root/attempt/config/fixture/patch input required by the receipt is Git-tracked and that preserved v2/v3 artifacts have no worktree divergence from `HEAD`.
- Passed the plan-specified focused command (4 tests): exact Red zero-write replay, all-socket denial, exact predecessor-stage admission, and unchanged guarded local command without network.

## Authority Boundary

This is custody-only evidence. It neither rewrites `05-VERIFICATION.md` nor declares Phase 5 re-verified. It adds no model, provider, credential, retrieval, Green/Yellow execution, network, external-publication, metric, requirement-status, or final-conclusion authority.

## Deviations from Plan

None — plan executed exactly as written.

## Known Stubs

None.

## Next Phase Readiness

Request an independent Phase 5 re-verification against the unchanged `05-VERIFICATION.md`. Closure still requires a `passed` report with score `4/4`; Phase 6 remains blocked until that verifier, not this executor, records it.

## Self-Check: PASSED

- Task 1 commit `ff8c62e3` exists and contains the immutable root plus custody successor.
- The clean `git archive` proof and all four focused tests passed.

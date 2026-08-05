---
phase: 05-authorized-execution-and-immutable-evidence
plan: 01
subsystem: execution-evidence-boundary
tags: [red-path, no-call, immutable-evidence, descriptor-bound, socket-denial]
requires:
  - phase: 04-offline-treatments-retrieval-and-branch-freeze
    provides: exact v6 approved_red no-model authority
  - phase: 05-authorized-execution-and-immutable-evidence
    provides: pinned local Python and Ruff preflight from Plan 05-00
provides:
  - Temporary-root-only Red evidence construction with exact v6 admission and zero-write resume
  - Closed source/config/CLI surface audit and all-socket denial proof
  - Explicit human approval for the reviewed one-way Red evidence and publication contract
affects: [05-02, red-execution, immutable-evidence, phase-7-evaluation]
actuals:
  tokens: 7967
  tasks: 3
  commits: 5
tech-stack:
  added: []
  patterns: [canonical-json, descriptor-bound-no-replace, temporary-root-tracer, all-socket-tripwire]
key-files:
  created:
    - experiments/specchoice-v1.3.2/src/specchoice_execution/__init__.py
    - experiments/specchoice-v1.3.2/src/specchoice_execution/red.py
    - experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py
    - experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json
    - experiments/specchoice-v1.3.2/tests/test_authorized_execution.py
  modified: []
key-decisions:
  - "The explicit approve-exact-contract decision covers only the reviewed Red contract bound to policy c48b5c607aa3a6be532ca0accb7f9bfd685b1eab60f82dc2b4b4c4ce97285d15 and v6 authority 363cf85c4088f5f268692f8319b70b50f7ed717f7145ed84a6923499ae992518."
  - "Red remains branch=red with N_strict=0 and repeat_count=0; TS-11 and TS-12 remain conditional_not_applicable_red_pending_phase7."
  - "Any policy, closure, CLI, source, test, or evidence-byte drift requires a versioned successor and a new blocking human gate; the v6 authority cannot be reused."
requirements-completed: [TS-07, TS-11, TS-12]
coverage:
  - id: D1
    description: Exact persisted v6 authority admits a complete temporary Red evidence package only under the closed no-model contract.
    requirement: TS-07
    verification:
      - kind: integration
        ref: tests/test_authorized_execution.py#test_exact_v6_tracer_publishes_complete_temporary_red_evidence
        status: pass
    human_judgment: false
  - id: D2
    description: The policy inventory keeps all formal, failed-attempt, and successor targets absent at the approval boundary.
    requirement: TS-11
    verification:
      - kind: unit
        ref: tests/test_authorized_execution.py#test_checkpoint_inventory_matches_policy_and_no_formal_target_exists
        status: pass
    human_judgment: false
  - id: D3
    description: Every named socket constructor and address class fails closed without becoming a real-call ledger row.
    requirement: TS-12
    verification:
      - kind: unit
        ref: tests/test_authorized_execution.py#test_all_socket_constructors_and_address_classes_fail_closed
        status: pass
    human_judgment: false
duration: 3min
completed: 2026-08-05
status: complete
---

# Phase 05 Plan 01: Red Evidence Contract Summary

**A temporary-root-only, descriptor-bound Red evidence path now admits only the exact v6 no-model authority, proves zero-call closure, and has the explicitly approved one-way publication contract.**

## Performance

- **Duration:** 3min
- **Started:** 2026-08-05T08:04:41Z
- **Completed:** 2026-08-05T08:07:14Z
- **Tasks:** 3/3
- **Files modified:** 5

## Accomplishments

- Implemented and tested a standard-library Red execution package that accepts only the persisted v6 `approved_red` authority in a temporary experiment root.
- Bound an empty real-call ledger, structural closure audit, runtime socket-denial audit, zero-cell A/B/C matrix, and separate raw/parsed/diagnostic evidence leaves under one validated temporary package.
- Confirmed the explicit `approve-exact-contract` decision for the exact policy and authority hashes without creating any repository formal, failed-attempt, or successor target.

## Task Commits

1. **Task 1: Prove one complete Red no-call evidence path in a temporary root** — `f788911d` (test), `71a12f08` (feat)
2. **Task 2: Close structural and runtime call reachability** — `5b24d808` (test), `80c9f7a4` (feat), `ccbe582b` (test)
3. **Task 3: Approve the one-way evidence-schema and publication boundary** — no source commit; the explicit user decision is recorded in this plan summary and sequential state metadata.

## Files Created/Modified

- `experiments/specchoice-v1.3.2/src/specchoice_execution/red.py` — strict v6 admission, evidence validation, closure audit, and all-socket guard.
- `experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py` — closed temporary-only `execute-red` command surface.
- `experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json` — canonical zero-call policy and formal output inventory.
- `experiments/specchoice-v1.3.2/tests/test_authorized_execution.py` — temporary-root, exact-resume, policy-inventory, and adversarial socket coverage.

## Decisions Made

- User explicitly selected `approve-exact-contract`, authorizing only later implementation/publication of the reviewed Red evidence contract.
- The approval is bound to the canonical policy SHA-256 `c48b5c607aa3a6be532ca0accb7f9bfd685b1eab60f82dc2b4b4c4ce97285d15` and v6 authority SHA-256 `363cf85c4088f5f268692f8319b70b50f7ed717f7145ed84a6923499ae992518`.
- The approval grants no model, provider, credential, retrieval, network, metric, feasibility, external-publication, or Phase-7-closing authority. Formal Red evidence publication remains Plan 05-02 work.

## Verification

- Passed the exact checkpoint suite: three targeted authority, temporary-evidence, and all-socket tests under Python 3.12.13.
- Passed `tests.test_authorized_execution`, the Phase 5 focused regression (`authorized_execution`, `treatments_h3`, `canonical`, and `filesystem_boundary`), Ruff 0.16.0, and `git diff --check`.
- Reconfirmed that `runs/red-execution-v1`, `receipts/red-execution-v1.json`, `reports/red-execution/red-execution-v1.md`, `runs/red-attempts`, and `runs/red-successors` are absent.

## Deviations from Plan

None - plan executed exactly as written. The continuation honored the already approved blocking-human decision and wrote no formal evidence target.

## Known Stubs

None.

## Next Phase Readiness

Plan 05-02 may implement immutable failed-attempt/retry/successor custody and later return to its own final-closure human gate. It must retain the approved policy bytes and formal target boundary until that plan's authorized publication step.

## Self-Check: PASSED

- All five execution source/config/test files and this summary exist.
- Task commits `f788911d`, `71a12f08`, `5b24d808`, `80c9f7a4`, and `ccbe582b` exist in Git history.

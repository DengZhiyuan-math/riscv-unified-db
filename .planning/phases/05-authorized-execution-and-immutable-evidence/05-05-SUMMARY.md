---
phase: 05-authorized-execution-and-immutable-evidence
plan: 05
subsystem: immutable Red no-call evidence publication
tags: [red, no-call, immutable-evidence, gate-b, exact-resume]
requires:
  - phase: 05-authorized-execution-and-immutable-evidence
    provides: Gate-A-approved successor contract and explicit Gate-B final-closure confirmation
provides:
  - Completed fixed successor Red formal root with an empty real-call ledger
  - Terminal receipt and deterministic Markdown projection bound to the approved non-circular closure
  - Verified zero-write exact-resume behavior for the published successor evidence
affects: [05-06, phase-06, phase-07]
actuals:
  tokens: 15000
  tasks: 3
  commits: 2
tech-stack:
  added: []
  patterns: [descriptor-bound fixed-set publication, exact-resume zero-write verification, non-circular closure binding]
key-files:
  created:
    - experiments/specchoice-v1.3.2/runs/red-execution-v2/
    - experiments/specchoice-v1.3.2/receipts/red-execution-v2.json
    - experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v2.md
  modified:
    - .planning/STATE.md
key-decisions:
  - "Gate B confirmed the unchanged Gate-A projection 18e4a9a7ec40e881ff6d3994db4554a3907298a01511c566769177b51d40bdec for exactly one successor Red no-call publication and its exact-resume verification."
  - "Completed Red evidence authorizes only downstream Red-evidence evaluation; it authorizes no model, provider, credential, retrieval, network, external publication, metric, or final-conclusion action."
patterns-established:
  - "Existing complete formal evidence is validated and resumed with zero writes; a non-exact state must fail closed rather than repair published bytes."
requirements-completed: [TS-07, TS-11, TS-12]
coverage:
  - id: D1
    description: "The successor Red evidence set is complete, bound to the approved v2 closure, and records a completed zero-call result."
    requirement: TS-07
    verification:
      - kind: integration
        ref: "python -m specchoice_execution.cli_v2 execute-red ..."
        status: pass
      - kind: unit
        ref: "tests/test_authorized_execution_v2.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "The published successor set resumes byte-identically with no writes and preserves predecessor namespace absence."
    requirement: TS-11
    verification:
      - kind: integration
        ref: "SHA-256, size, and mtime snapshots before and after exact execute-red resume"
        status: pass
      - kind: unit
        ref: "tests/test_authorized_execution_v2.py"
        status: pass
    human_judgment: false
  - id: D3
    description: "Red retains zero-cell and conditional G/Y requirement semantics without model output or permanent G/Y closure."
    requirement: TS-12
    verification:
      - kind: unit
        ref: "tests/test_authorized_execution_v2.py"
        status: pass
    human_judgment: false
duration: multi-session
completed: 2026-08-05
status: complete
---

# Phase 05 Plan 05: Red Successor Evidence Publication Summary

**A Gate-A/Gate-B-bound Red no-call successor evidence set with a completed terminal receipt and byte-identical zero-write exact resume.**

## Performance

- **Duration:** Multi-session
- **Completed:** 2026-08-05
- **Tasks:** 3/3
- **Files modified:** 13 formal/publication files plus planning metadata

## Accomplishments

- Published the complete locked successor inventory in local commit `5f5afc34`: ten formal machine leaves, `receipts/red-execution-v2.json`, and `reports/red-execution/red-execution-v2.md`.
- Confirmed the terminal receipt remains `status=completed` and binds the approved distinct `policy_sha256`, `runtime_closure_sha256`, and `gate_a_projection_sha256` values, including Gate-A projection `18e4a9a7ec40e881ff6d3994db4554a3907298a01511c566769177b51d40bdec`.
- Re-ran the exact production command locally as an existing-complete-set resume. SHA-256, file size, and modification-time snapshots of the whole successor set were identical before and after the command.
- Verified `runs/red-attempts-v2`, `runs/red-successors-v2`, and all predecessor formal targets remain absent.

## Task Commits

1. **Task 1–3: rehearsal, Gate B, and successor Red publication** — `5f5afc34` (`feat`)

**Plan metadata:** recorded separately after this Summary is validated.

## Files Created/Modified

- `experiments/specchoice-v1.3.2/runs/red-execution-v2/` — ten immutable formal Red machine leaves, including the empty call ledger and runtime/structural no-call audits.
- `experiments/specchoice-v1.3.2/receipts/red-execution-v2.json` — terminal receipt for the completed Red successor evidence root.
- `experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v2.md` — deterministic non-authoritative Markdown projection.
- `.planning/STATE.md` — persisted explicit Gate-B decision prior to publication; final execution position is updated by this metadata commit.

## Decisions Made

- Gate B confirmed only the unchanged external Gate-A projection. The authorization was consumed for one local successor Red no-call publication and its exact-resume check.
- The published result remains a Red feasibility-evidence record: no real model calls, zero A/B/C cells, no metrics or feasibility conclusion, and TS-11/TS-12 remain conditional pending Phase 7.

## Verification

Passed:

```text
cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_execution.cli_v2 execute-red --repo-root . --policy config/execution/red-execution-policy-v2.json --authority phase4/branch-authority-v6.json --packet reports/h3/h3-red-review-v6/review-packet.json --readiness receipts/h3-branch-readiness-v6.json --decision reviews/h3-branch-decision-v6.json --attempt-root runs/red-attempts-v2 --formal-root runs/red-execution-v2 --receipt receipts/red-execution-v2.json --report reports/red-execution/red-execution-v2.md
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution_v2 -q
../../.venv/bin/ruff check --isolated src/specchoice_execution tests/test_authorized_execution.py tests/test_authorized_execution_v2.py
```

The focused unittest selectors written in the plan no longer exist in `AuthorizedExecutionV2Tests`; the complete current `tests.test_authorized_execution_v2` module passed and covers exact replay, formal receipt binding, and predecessor namespace protection.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Replaced stale focused unittest selectors with the complete current authorization-v2 module.**
- **Found during:** Task 3 verification
- **Issue:** All three plan-listed `AuthorizedExecutionV2Tests` selector names produced `AttributeError`; the tests were renamed to the current v2 contract vocabulary.
- **Fix:** Ran the complete current `tests.test_authorized_execution_v2` module, which includes the required exact-replay, receipt-binding, and v1-namespace protections.
- **Files modified:** None
- **Verification:** 9 tests passed; Ruff passed; exact-resume snapshots remained unchanged.
- **Committed in:** Metadata commit for this Summary.

---

**Total deviations:** 1 auto-fixed (1 verification-command bug).
**Impact on plan:** No source, policy, formal evidence, or authority bytes were changed.

## Issues Encountered

- The host shell did not resolve hashing utilities through its normal command lookup inside a strict shell block. Verification used their resolved absolute paths; no repository files were affected.

## Next Phase Readiness

- Plan 05-06 may perform its separate read-only successor audit; it must not mutate this immutable evidence root.
- No Plan 06 work was executed. No push or external publication occurred.

## Self-Check: PASSED

All ten formal leaves, the receipt, the Markdown projection, and publication commit `5f5afc34` exist locally.

---
*Phase: 05-authorized-execution-and-immutable-evidence*
*Completed: 2026-08-05*

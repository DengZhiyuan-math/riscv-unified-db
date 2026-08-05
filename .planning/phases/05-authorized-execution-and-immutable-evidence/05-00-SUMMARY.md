---
phase: 05-authorized-execution-and-immutable-evidence
plan: 00
subsystem: planning-toolchain-preflight
tags: [python, ruff, preflight, red-only, immutable-evidence]
requires:
  - phase: 04-offline-treatments-retrieval-and-branch-freeze
    provides: approved_red authority consumed only by later Phase 5 plans
provides:
  - A planning-only verification record for the restored local Python and Ruff pair
  - A no-write handoff proving all Phase 5 formal, attempt, and successor targets remain absent
affects: [05-01, red-execution, toolchain]
actuals:
  tokens: 152
  tasks: 2
  commits: 2
tech-stack:
  added: []
  patterns: [explicit repository-local executable gate, precondition-only false-authority record]
key-files:
  created:
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-TOOLCHAIN-PREFLIGHT.md
  modified: []
key-decisions:
  - "Wave 0 records only the restored local toolchain and explicitly grants no experiment or formal-evidence authority."
  - "The handoff is valid only while the pinned tools, pyproject digest, and empty formal target namespaces agree."
requirements-completed: [TS-07, TS-11, TS-12]
coverage:
  - id: D1
    description: Repository-local Python and Ruff preflight recorded with planning-only scope.
    requirement: TS-07
    verification:
      - kind: other
        ref: 05-00-PLAN.md Task 05-00-01 automated preflight
        status: pass
    human_judgment: false
  - id: D2
    description: Handoff revalidation proves formal, attempt, and successor targets remain absent.
    requirement: TS-12
    verification:
      - kind: other
        ref: 05-00-PLAN.md Task 05-00-02 automated replay
        status: pass
    human_judgment: false
duration: 3min
completed: 2026-08-05
status: complete
---

# Phase 05 Plan 00: Toolchain Preflight Summary

**Restored repository-local Python 3.12.13 and Ruff 0.16.0 are recorded as a digest-bound, non-authoritative precondition before the Red tracer.**

## Performance

- **Duration:** 3min
- **Started:** 2026-08-05T07:43:04Z
- **Completed:** 2026-08-05T07:46:32Z
- **Tasks:** 2/2
- **Files modified:** 1

## Accomplishments

- Verified only `.venv/bin/python` and `.venv/bin/ruff`; Python is 3.12.13 and Ruff is exactly 0.16.0.
- Recorded the exact `pyproject.toml` SHA-256 in a repository-relative, planning-only preflight record.
- Revalidated the record before handoff and confirmed every named formal, failed-attempt, and successor target remains absent.

## Task Commits

1. **Task 1: Verify and record the restored local pinned toolchain** — `a1c15f90` (chore)
2. **Task 2: Revalidate the preflight handoff before the tracer** — `7b748a26` (chore, no-write verification commit)

## Files Created/Modified

- `.planning/phases/05-authorized-execution-and-immutable-evidence/05-TOOLCHAIN-PREFLIGHT.md` — pinned local-tool record with explicitly false authority fields.

## Decisions Made

- Wave 0 is a precondition-only gate: it cannot satisfy the Red evidence contract or authorize an experiment, formal evidence, a branch, model use, publication, or evaluation.
- A future tracer must recheck the local toolchain; this record does not replace exact v6 admission, frozen-closure checks, human checkpoints, or formal validation.

## Deviations from Plan

None - plan executed exactly as written. The user-approved `.venv` restoration remained external to the plan and no installer, resolver, package manager, or network command ran.

## Issues Encountered

None.

## Known Stubs

None.

## Next Phase Readiness

Plan 05-01 may start through its explicit `depends_on: 05-00` edge, but it must independently enforce its own authority and frozen-closure admission. No experiment authority or formal evidence target was created by Wave 0.

## Self-Check: PASSED

- `05-TOOLCHAIN-PREFLIGHT.md` and this summary exist.
- Task commits `a1c15f90` and `7b748a26` exist in Git history.

---
phase: 05-authorized-execution-and-immutable-evidence
plan: 04
subsystem: immutable Red no-call execution contract
tags: [red, no-call, immutable-evidence, gate-a, runtime-closure]
requires:
  - phase: 04-offline-treatments-retrieval-and-branch-freeze
    provides: Phase 4 v6 Red authority as immutable input-only custody
provides:
  - Explicit human Gate-A approval for one exact successor Red no-call contract
  - Recomputable non-circular policy, runtime-closure, and Gate-A projection identities
  - Confirmation that all actual evidence namespaces remain absent before Plan 05-05
affects: [05-05, 05-06, phase-06, phase-07]
actuals:
  tokens: 8281
  tasks: 3
  commits: 5
tech-stack:
  added: []
  patterns: [external non-circular Gate-A projection, descriptor-held runtime closure, copied-root-only publication proof]
key-files:
  created:
    - experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v2.json
    - experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py
    - experiments/specchoice-v1.3.2/src/specchoice_execution/cli_v2.py
    - experiments/specchoice-v1.3.2/tests/test_authorized_execution_v2.py
  modified:
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-04-SUMMARY.md
key-decisions:
  - "Gate A approved only policy_sha256=1785acf527c4d5c08790a525937f4960896ac775d5c9a6635903b384c2c8835f, runtime_closure_sha256=29558e76c09dac2b82468915567667419e5a281091201611449a6960f0b7a811, and gate_a_projection_sha256=18e4a9a7ec40e881ff6d3994db4554a3907298a01511c566769177b51d40bdec."
  - "Phase 4 v6 remains input-only; this approval grants neither evidence publication nor any provider, network, metric, or final-conclusion authority."
patterns-established:
  - "Gate-A identity is external to raw policy bytes and excludes all future evidence targets."
requirements-completed: []
coverage:
  - id: D1
    description: Exact successor Red no-call contract is proven in disposable copied roots.
    verification:
      - kind: integration
        ref: "tests/test_authorized_execution_v2.py via python -m unittest tests.test_authorized_execution_v2 -q"
        status: pass
      - kind: other
        ref: "ruff check --isolated src/specchoice_execution/red_v2.py src/specchoice_execution/cli_v2.py tests/test_authorized_execution_v2.py"
        status: pass
    human_judgment: false
  - id: D2
    description: Gate A explicit human approval binds the exact reviewed hash set only.
    verification: []
    human_judgment: true
    rationale: Human authorization was required for the immutable contract boundary.
duration: multi-session
completed: 2026-08-05
status: complete
---

# Phase 05 Plan 04: Successor Red Contract Gate-A Summary

**A copied-root-only Red no-call successor contract with externally recomputable Gate-A identity, explicitly approved for Plan 05-05 pre-publication work only.**

## Performance

- **Duration:** Multi-session
- **Completed:** 2026-08-05
- **Tasks:** 3/3
- **Files modified:** 7 (four contract files and three planning metadata files)

## Accomplishments

- Proved the closed `execute-red` successor interface only in disposable copied roots; the exact ten options are `--repo-root`, `--policy`, `--authority`, `--packet`, `--readiness`, `--decision`, `--attempt-root`, `--formal-root`, `--receipt`, and `--report`.
- Recomputed a non-circular Gate-A review projection from persisted raw bytes, retaining distinct policy, runtime-closure, and projection identities.
- Recorded the explicit `approve-v2-contract` decision without creating a machine approval, a formal evidence leaf, an attempt package, or a drift-successor package.

## Approved Gate-A Contract

The human approved exactly the following persisted contract values:

| Field | Exact value |
| --- | --- |
| Raw policy | `config/execution/red-execution-policy-v2.json`, 2406 bytes, `1785acf527c4d5c08790a525937f4960896ac775d5c9a6635903b384c2c8835f` |
| Runtime closure | `29558e76c09dac2b82468915567667419e5a281091201611449a6960f0b7a811` |
| External Gate-A projection | `18e4a9a7ec40e881ff6d3994db4554a3907298a01511c566769177b51d40bdec` |
| Phase 4 v6 persisted input | `phase4/branch-authority-v6.json`: `363cf85c4088f5f268692f8319b70b50f7ed717f7145ed84a6923499ae992518` |
| Phase 4 v6 authority claim | `authority_sha256=f77cdbd908222209730058be07e5ffa363c905f72183b1f6970c4d9c36e315fb` |

The sorted non-policy closure contains the exact Phase 3/4 authority chain, canonical/filesystem/runtime-closure primitives, successor CLI and executor, diagnostics/strict-JSON/H3 dependencies, and `test_authorized_execution_v2.py`. The projection contains one external raw-policy entry and never embeds its own digest in raw policy or projection bytes.

The fixed inputs are Phase 3 data authority plus the Phase 4 authority, review packet, readiness receipt, and approved Red decision. The only production output targets remain `runs/red-attempts-v2`, `runs/red-execution-v2`, `receipts/red-execution-v2.json`, and `reports/red-execution/red-execution-v2.md`; the formal root has the locked ten-leaf inventory.

The contract preserves `branch=red`, `N_strict=0`, `repeat_count=0`, `expected_cells=0`, `actual_cells=0`, and `cells=[]`; all A/B/C partition counters are zero. TS-11 and TS-12 remain `conditional_not_applicable_red_pending_phase7` within the contract.

## Verification

Passed:

```text
cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution_v2 -q
../../.venv/bin/ruff check --isolated src/specchoice_execution/red_v2.py src/specchoice_execution/cli_v2.py tests/test_authorized_execution_v2.py
```

The suite covers external projection recomputation, self-reference/recursion rejection, exact input/target mismatch rejection, copied-root publication, replay/no-write, partial/symlink/traversal failure, all socket constructors, and forbidden-surface/future-output rejection. The structural scan returned `forbidden_findings=[]`.

Predecessor bytes remain unchanged:

| Path | SHA-256 |
| --- | --- |
| `config/execution/red-execution-policy-v1.json` | `c48b5c607aa3a6be532ca0accb7f9bfd685b1eab60f82dc2b4b4c4ce97285d15` |
| `src/specchoice_execution/red.py` | `ac65c91320f9df5b98d1ef92ada403beb6920657cb0afd7b64288aae98548d07` |
| `src/specchoice_execution/cli.py` | `80412f1a3ea9b42a025806ba2180f8763ccf7b1d261de30e2520fea116658bde` |
| `src/specchoice_execution/__init__.py` | `ab7c162eb6344772a958fa3524e435e263818de6a5f062332f45be0b1757284d` |
| `tests/test_authorized_execution.py` | `daa87f41d1b030600f3d8136ecc30fd9f70802e955d2ede6f4d93ee508ac53d6` |

At the time of approval, all actual repository targets are absent: `runs/red-execution-v2`, `runs/red-attempts-v2`, `runs/red-successors-v2`, `receipts/red-execution-v2.json`, `reports/red-execution/red-execution-v2.md`, and the predecessor `runs/red-execution-v1`, `runs/red-attempts`, and `runs/red-successors` namespaces.

## Task Commits

1. **Task 1: Prove the exact successor execute-red contract in a copied root** - `a55f9e7e` (test), `a3a7e003` (feat)
2. **Task 2: Freeze and adversarially close custody, socket, and projection edges** - `19f6fbb0` (test), `5a85f977` (fix)
3. **Task 3: Gate A — approve the exact successor contract** - this metadata commit (docs)

## Decisions Made

- The explicit user selection `approve-v2-contract` applies only to the exact three approved identities above and to no changed successor byte.
- Approval permits Plan 05-05 to recompute the same frozen set and seek its separate Gate-B confirmation; it does not publish evidence.
- No requirement checkbox is changed: this plan records a contract gate only, while Phase 7 retains the conditional TS-11/TS-12 closure authority.

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None.

## TDD Gate Compliance

Passed: the RED commit `a55f9e7e` precedes the GREEN implementation commit `a3a7e003`.

## Next Phase Readiness

Plan 05-05 may perform its pre-publication rehearsal only if it recomputes the identical approved values. Any byte, target, dependency, schema, CLI, or behavior drift invalidates this Gate-A approval and requires a forward-only successor gate.

## Self-Check: PASSED

Confirmed the four successor contract files and this summary exist; confirmed `a55f9e7e`, `a3a7e003`, `19f6fbb0`, and `5a85f977` are present in Git history; and reconfirmed every listed actual evidence/attempt/successor target is absent.

*Phase: 05-authorized-execution-and-immutable-evidence*
*Completed: 2026-08-05*

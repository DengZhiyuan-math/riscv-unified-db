---
phase: 05
slug: authorized-execution-and-immutable-evidence
status: active_successor_validation
nyquist_compliant: false
wave_0_complete: true
created: 2026-08-04
updated: 2026-08-05
---

# Phase 05 — Forward-Only Successor Validation Strategy

> Current validation and sampling contract for active Plans 05-04 through 05-06. Historical Plan 05-00/05-01 completion remains evidence; rejected 05-02 and superseded 05-03 are not active validation steps or requirement-completion claims.

## Truthful Lifecycle Baseline

| Plan / record | Lifecycle state | Validation meaning |
|---|---|---|
| `05-00-PLAN.md` / `05-00-SUMMARY.md` | Completed | The repository-local Python 3.12.13 and Ruff 0.16.0 preflight was executed and recorded in `05-TOOLCHAIN-PREFLIGHT.md`; it grants no experiment or publication authority. |
| `05-01-PLAN.md` / `05-01-SUMMARY.md` | Completed | The predecessor temporary-root Red tracer, structural scan, all-socket tests, and first human contract decision completed. Those results remain historical and do not authorize successor bytes. |
| `05-02-REJECTED.md` / `05-02-CANCELLATION.md` | Rejected, not completed | Partial implementation commits are preserved, the final-closure choice was rejection, Task 05-02-03 never ran, and no `05-02-SUMMARY.md` exists. It is not an active Nyquist mapping. |
| `05-03-SUPERSEDED.md` | Superseded, never executed | Its predecessor formal root was never published and no `05-03-SUMMARY.md` exists. It is not an active audit contract. |
| `05-04-PLAN.md` | Planned, not executed | Creates the successor policy/modules/test closure and non-circular Gate-A projection, then stops at Gate A. |
| `05-05-PLAN.md` | Planned, not executed | Recomputes the approved projection, rehearses in a disposable copy, stops at Gate B, and only after confirmation may publish plus run the first actual zero-write replay. |
| `05-06-PLAN.md` | Planned, not executed | Independently recomputes the formal graph and approved projection read-only, adds a validation-only native-guard regression harness outside the formal closure, then runs the formal zero-write audit and two guarded full regressions. |

The active discoverable Phase 5 plan set is exactly `05-00`, `05-01`, `05-04`, `05-05`, and `05-06`; exactly `05-00` and `05-01` are complete, so active completion is **2/5**. Rejected 05-02 and superseded/unexecuted 05-03 are neither active nor completed.

Current filesystem facts at this planning revision:

- `experiments/specchoice-v1.3.2/tests/test_authorized_execution.py` exists as completed predecessor coverage.
- `experiments/specchoice-v1.3.2/tests/test_authorized_execution_v2.py` does not yet exist; Task 05-04-01 creates it test-first.
- `experiments/specchoice-v1.3.2/validation/guarded_regress.py` and `experiments/specchoice-v1.3.2/tests/test_guarded_regress.py` do not yet exist; Task 05-06-02 creates them test-first after formal publication without changing any formal closure input.
- `runs/red-execution-v2`, `runs/red-attempts-v2`, `runs/red-successors-v2`, `receipts/red-execution-v2.json`, and `reports/red-execution/red-execution-v2.md` are absent. No successor execution or publication is claimed.

## Test Infrastructure and Sampling Commands

| Property | Current contract |
|---|---|
| Framework | Python standard-library `unittest`; project contract Python `>=3.12` |
| Pinned tools | `.venv/bin/python` 3.12.13 and `.venv/bin/ruff` 0.16.0, already recorded by 05-00 |
| Completed predecessor sampling | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution tests.test_treatments_h3 tests.test_canonical tests.test_filesystem_boundary -q` |
| Active successor quick sampling | After Task 05-04-01 creates the module: `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution_v2 -q && ../../.venv/bin/ruff check --isolated src/specchoice_execution/red_v2.py src/specchoice_execution/cli_v2.py tests/test_authorized_execution_v2.py` |
| Active full pre-gate sampling | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution_v2 tests.test_authorized_execution tests.test_treatments_h3 tests.test_canonical tests.test_filesystem_boundary -q && ../../.venv/bin/ruff check --isolated src/specchoice_execution tests/test_authorized_execution.py tests/test_authorized_execution_v2.py && git diff --check` |
| Guarded harness contract sampling | After Task 05-06-02 creates both files: `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_guarded_regress -q && ../../.venv/bin/ruff check --isolated validation/guarded_regress.py tests/test_guarded_regress.py`. Tests inject guard runners and temporary fake local commands; they open no real network connection and never invoke the real full regression. |
| Final Phase 5 sampling | After actual formal v2 publication, run the complete focused modules and identical production command/write observer named by 05-06-02, then from the repository root invoke `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root .` twice. Each harness invocation must preflight `/usr/bin/sandbox-exec`, execute exactly `./bin/regress --all` inside its explicit deny-network/protected-install profile, and prove the exact ten formal leaves plus receipt/report inventory and SHA-256 unchanged. Both full regressions are planned, not yet run; unavailable/nonfunctional guard, prohibited operation, mutation, or failure blocks closure, and bare regression is forbidden. |
| Feedback latency | Measure successor quick/full runtime when the v2 test module exists; no unmeasured runtime is treated as passing the 30-second sampling target. |

No validation command may install packages, use the network, substitute ambient tools, create a provider/model/credential/retrieval surface, or infer formal authority from a test result. The sole new process boundary is the validation-only harness's fixed `sandbox-exec ... ./bin/regress --all` argv; it is outside the formal v2 closure, accepts no caller-selected command, and is never imported or reached by `execute-red`.

## Non-Circular Gate-A Projection Contract

Gate A approves canonical projection bytes external to the raw policy; it does not approve a policy self-claim.

1. The raw `red-execution-policy-v2.json` declares `policy_path` plus a lexicographically sorted list of non-policy frozen paths. It contains neither its own final SHA-256 nor its own byte length, and the policy path cannot occur in the non-policy list.
2. The validator descriptor-reads raw policy bytes into `policy_entry={path,byte_length,sha256}` and descriptor-reads every other frozen input into sorted `{path,byte_length,sha256}` entries.
3. Canonical bytes for `red-execution-runtime-closure-basis-v2={schema,policy,entries}` produce `runtime_closure_sha256`. The Gate-A projection itself, checkpoint/summary state, future formal outputs, receipt, and report are excluded from this basis.
4. Canonical `red-execution-gate-a-projection-v2` bytes contain the policy entry, full closure basis/hash, command/target/audit/predecessor/Red-trigger/v6 bindings. `gate_a_projection_sha256` is calculated outside those bytes and recorded by Gate A and `05-04-SUMMARY.md`.
5. Copied and actual terminal receipts must contain three separate exact fields: `policy_sha256`, `runtime_closure_sha256`, and `gate_a_projection_sha256`. The receipt is a consumer of the approved projection, never an input to it.

Required positive test: `test_gate_a_projection_recomputes_non_circular_policy_and_closure_hashes` independently rebuilds the policy entry, sorted non-policy entries, closure-basis bytes/hash, projection bytes/hash, and distinct receipt fields from persisted raw bytes.

Required negative test: `test_policy_self_reference_and_projection_recursion_fail_closed` rejects an embedded own digest/length, duplicate policy-path membership, projection/basis recursion, or receipt/report/future-output membership before writer or socket activity.

Actual target absence is displayed at Gate A and Gate B as separately recomputed mutable prepublication state; it is not embedded in the immutable projection, so the approved projection remains recomputable after publication.

## Active Per-Task Verification Map

| Task | Wave | Requirement / threat | Automated or gate evidence | Artifact state | Execution state |
|---|---:|---|---|---|---|
| 05-04-01 | 2 | TS-07/11/12; D-01..13; non-circular projection | Exact copied-root command, parser mismatch tests, positive projection recomputation, negative self-reference/recursion rejection, v1 preservation, Ruff | v2 test absent until task starts | Planned; no result claimed |
| 05-04-02 | 2 | D-02/03/05..08/13..16 | Full `tests.test_authorized_execution_v2`, all-socket/forbidden-surface/fault/no-replace/attempt/drift cases, Ruff, actual-target absence | v2 test absent until 05-04-01 | Planned; no result claimed |
| 05-04-03 Gate A | 2 | D-01/05/09/13/15 | Full successor suite plus canonical external projection display; human chooses `approve-v2-contract` or `reject-v2-contract` | No machine approval artifact permitted | Planned blocking human gate |
| 05-05-01 | 3 | D-02/05/08/13 | Byte-for-byte Gate-A projection recomputation, exact copied-root production rehearsal, copied-root zero-write replay, full focused suite and Ruff | Actual targets must remain absent | Planned; no result claimed |
| 05-05-02 Gate B | 3 | D-01/05/09/13/15 | Gate-A versus final projection zero byte/field delta, three distinct hash fields, target absence, full suite; human confirms or rejects | No decision file permitted | Planned blocking human gate |
| 05-05-03 | 3 | TS-07/11/12; D-01..16 | Exact production command, terminal receipt projection binding, focused formal validators, then identical second invocation with a complete zero-write snapshot | Formal targets currently absent | Planned; no publication claimed |
| 05-06-01 | 4 | TS-07/11/12; T-05-06-01..06 | Read-only graph audit from descriptor-held bytes, independent projection recomputation, self-reference rejection, attempt/TS-07/matrix/no-call tests | Depends on complete 05-05 publication | Planned; no audit result claimed |
| 05-06-02 | 4 | D-02 formal zero-write audit, T-05-06-07/08 guarded release process, and bounded authority | TDD unavailable/bad guard, prohibited-operation, evidence-mutation, and fake-local-success contracts; identical production invocation under its own write observer; focused suite/Ruff/diff; then two `guarded_regress.py --repo-root .` invocations, each with exact twelve-file inventory/SHA-256 before/after and fixed native-confined `./bin/regress --all` | Depends on actual formal v2 publication and 05-06-01 pass | Planned; harness/tests absent and no audit or full-regression result claimed |

## Human Gates

| Gate | Preconditions | Human decision | Fail-closed outcome |
|---|---|---|---|
| Gate A — successor contract | v2 source/policy/test closure exists; positive/negative projection tests and full copied-root suite pass; actual targets are absent | Approve or reject the exact canonical external projection and displayed contract | Rejection, silence, test failure, recursion, or missing field leaves every actual target absent and blocks 05-05 |
| Gate B — final publication closure | Gate-A projection recomputes byte-for-byte; copied-root production and zero-write rehearsal pass; current projection has zero delta; actual targets are absent | Confirm or reject one exact actual publication | Rejection, silence, any delta, target occupancy, or validation failure prohibits the actual writer |

The two gates are separate and neither predecessor approval nor Phase 4 v6 input authority substitutes for either successor decision.

## Formal Zero-Write Audit

The 05-05 post-publication replay and 05-06 final audit must each:

1. Snapshot exact repository-relative inventory, bytes, SHA-256, and write-observable metadata for formal, optional attempt, receipt, and Markdown targets.
2. Invoke the identical ten-option `execute-red` command under the all-socket guard and write observer.
3. Require the same canonical receipt, exact snapshot equality, and a zero write count.
4. Independently rebuild the external approved projection rather than trusting receipt fields; require distinct matching policy, runtime-closure, and projection hashes.
5. Fail without repair, cleanup, overwrite, migration, successor approval, or summary normalization on any discrepancy.
6. Only after the actual formal v2 publication and both read-only audits pass, run `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root .` twice from the repository root. The harness must resolve and functionally preflight exactly `/usr/bin/sandbox-exec`, use explicit terminating deny rules for network, the exact formal-root/receipt/report targets, repository and user tool/dependency/cache roots, and system package prefixes plus offline/no-update controls, admit only literal `./bin/regress --all`, capture exit/output, and fail without a bare fallback on guard/profile/probe/prohibited-operation/regression error.
7. Within each guarded run, require the formal root to contain exactly `attempt-chain.json`, `evidence-span-audit.json`, `matrix-manifest.json`, `model-call-ledger.json`, `no-call-runtime-audit.json`, `no-call-structural-audit.json`, `ordered-diagnostics.json`, `parsed-evidence.json`, `raw-evidence.json`, and `red-trigger-evidence.json`, plus the exact receipt and report; compare repository-relative inventory and raw SHA-256 before/after and fail on change/add/remove. The second complete run is the deterministic zero-write proof.
8. Keep this native full-process guard separate from the formal `execute-red` runtime tripwire: the harness is not an evidence input, cannot authorize calls or requirements, and its narrow validation subprocess does not create a formal model/provider/credential/retrieval/network/subprocess surface.

## Nyquist Status and Sign-Off

- [x] Wave 0 is complete: pinned local tools and the non-authorizing preflight record exist.
- [x] Completed 05-01 predecessor tests and decision evidence remain preserved as historical coverage.
- [x] Rejected 05-02 and superseded 05-03 are explicitly excluded from the active task map.
- [x] Every active 05-04..06 implementation/audit task has a named automated command; both human decisions remain blocking gates.
- [ ] `test_authorized_execution_v2.py` exists and includes the exact positive recomputation and negative self-reference/recursion tests.
- [ ] `validation/guarded_regress.py` and `tests/test_guarded_regress.py` exist and pass unavailable guard, bad/nonfunctional profile, prohibited child, evidence mutation, and no-network fake-local-command contracts; production has no bare/full-command override.
- [ ] Gate A has passed and `05-04-SUMMARY.md` records the exact canonical projection fields/hash without claiming publication.
- [ ] Gate B has confirmed a zero-delta recomputation of that same projection.
- [ ] The actual formal set has published or failed with truthful immutable custody, and the 05-05 exact-resume audit has observed zero writes.
- [ ] The independent 05-06 graph audit and formal zero-write replay have passed without changing evidence.
- [ ] After actual formal v2 publication and the read-only audits, the guarded harness has run the exact `./bin/regress --all` command twice under functional native network/install denial, and both runs preserved the exact twelve-file successor evidence inventory/SHA-256 map without model/network activity.
- [ ] `nyquist_compliant: true` may be set only after every unchecked active item above is evidenced; it remains false now because successor tests, gates, publication, and audits have not executed.

**Approval:** pending active successor execution; no future validation is marked passed.

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

> Current validation and sampling contract for the sole active Plan 05-08. Completed Plans 05-00/05-01/05-04/05-05 remain evidence; rejected 05-02, superseded 05-03, and partial failed-closed 05-06/05-07 are not active validation steps or requirement-completion claims.

## Truthful Lifecycle Baseline

| Plan / record | Lifecycle state | Validation meaning |
|---|---|---|
| `05-00-PLAN.md` / `05-00-SUMMARY.md` | Completed | The repository-local Python 3.12.13 and Ruff 0.16.0 preflight was executed and recorded in `05-TOOLCHAIN-PREFLIGHT.md`; it grants no experiment or publication authority. |
| `05-01-PLAN.md` / `05-01-SUMMARY.md` | Completed | The predecessor temporary-root Red tracer, structural scan, all-socket tests, and first human contract decision completed. Those results remain historical and do not authorize successor bytes. |
| `05-02-REJECTED.md` / `05-02-CANCELLATION.md` | Rejected, not completed | Partial implementation commits are preserved, the final-closure choice was rejection, Task 05-02-03 never ran, and no `05-02-SUMMARY.md` exists. It is not an active Nyquist mapping. |
| `05-03-SUPERSEDED.md` | Superseded, never executed | Its predecessor formal root was never published and no `05-03-SUMMARY.md` exists. It is not an active audit contract. |
| `05-04-PLAN.md` / `05-04-SUMMARY.md` | Completed | Created the successor policy/modules/test closure and non-circular Gate-A projection, then recorded the exact Gate A approval without publication. |
| `05-05-PLAN.md` / `05-05-SUMMARY.md` | Completed | Recomputed the approved projection, obtained Gate B, published the fixed current Red evidence set, and proved exact-resume zero writes. |
| `05-06-FAILED-CLOSED.md` / `05-06-CANCELLATION.md` | Partial, failed closed, not completed | Preserves empty audit commit `d95fb748` and harness commit `46c34c8b`; native construction preflight emitted `GUARDED_REGRESS_NETWORK_PROBE_NOT_DENIED` before either full regression. No `05-06-SUMMARY.md` exists. |
| `05-07-FAILED-CLOSED.md` / `05-07-CANCELLATION.md` | Partial, failed closed, not completed | Exact validation-only worktree bytes pass 11 focused tests and Ruff, but the first guarded child stopped at Bundler platform admission because baseline `Gemfile.lock` omitted `arm64-darwin-23`; zero of two full regressions completed and no `05-07-SUMMARY.md` exists. |
| `05-08-PLAN.md` | Planned, not executed | Adopts the exact 05-07 validation bytes unchanged, adds only the missing native lockfile platform from pinned offline Bundler output, repeats formal zero-write exact-resume, and resumes two guarded full regressions. |

The active discoverable Phase 5 plan set is exactly `05-00`, `05-01`, `05-04`, `05-05`, and `05-08`; the first four are complete, so active completion is **4/5**. Rejected 05-02, superseded 05-03, and failed-closed 05-06/05-07 are historical and non-discoverable.

Current filesystem facts at this planning revision:

- `experiments/specchoice-v1.3.2/tests/test_authorized_execution.py` exists as completed predecessor coverage.
- `experiments/specchoice-v1.3.2/tests/test_authorized_execution_v2.py` exists and 05-04/05-05 summaries record its passing contract coverage.
- `experiments/specchoice-v1.3.2/validation/guarded_regress.py` and `experiments/specchoice-v1.3.2/tests/test_guarded_regress.py` contain the exact partial 05-07 native connection-use/toolchain admission correction bound by `05-07-CANCELLATION.md`; 05-08 may adopt those bytes unchanged but may not edit them.
- Baseline `Gemfile.lock` SHA-256 is `17d846146f4b16fcc31841885a526c3325901208d629d9cefadd9c79356d3900`; pinned local resolution adds only `arm64-darwin-23` and yields SHA-256 `e1231c14ab55d253450b20976e408a9c66a0c0156234d9e68a32504cd334b57c`.
- `runs/red-execution-v2`, `receipts/red-execution-v2.json`, and `reports/red-execution/red-execution-v2.md` exist as the completed 05-05 formal set; `runs/red-attempts-v2` and `runs/red-successors-v2` remain absent.

## Test Infrastructure and Sampling Commands

| Property | Current contract |
|---|---|
| Framework | Python standard-library `unittest`; project contract Python `>=3.12` |
| Pinned tools | `.venv/bin/python` 3.12.13 and `.venv/bin/ruff` 0.16.0, already recorded by 05-00 |
| Completed predecessor sampling | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution tests.test_treatments_h3 tests.test_canonical tests.test_filesystem_boundary -q` |
| Lock-platform read-only resolution | Before editing, Task 05-08-01 uses installed mise `2026.7.5`, Bundler `4.0.17`, `BUNDLE_DISABLE_VERSION_CHECK=true`, and `bundle lock --local --add-platform arm64-darwin-23 --print`; the printed bytes must differ from baseline only by the named platform line and match final SHA-256 `e1231c14...57c`. |
| Active successor quick sampling | Task 05-08-01 requires exact historical plan/partial validation/baseline lock hashes, then runs frozen/deployment `bundle check`, all 11 guarded-harness tests, Ruff, the identical formal command, and the first guarded full regression. |
| Guarded harness contract sampling | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_guarded_regress -q && ../../.venv/bin/ruff check --isolated validation/guarded_regress.py tests/test_guarded_regress.py`. Tests inject runner results only; they open no real socket, start no listener, contact no remote address, and never invoke the real full regression. |
| Final Phase 5 sampling | Task 05-08-01 invokes `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root .` once after offline lock/formal/focused checks; Task 05-08-02 reasserts every fixed hash and invokes the same harness once more. Each invocation must execute exactly `./bin/regress --all` inside the unchanged deny-network/protected-install profile and preserve the exact ten formal leaves plus receipt/report inventory/SHA-256. |
| Feedback latency | Focused unit and lint commands provide the fast loop; the two repository-wide regressions are terminal release gates and no partial output is treated as completion. |

No validation command may install packages, contact a remote network, substitute ambient tools, create a provider/model/credential/retrieval surface, or infer formal authority from a test result. Bundler resolution is local-only and changes no specification or version. The harness's fixed `sandbox-exec ... ./bin/regress --all` boundary remains outside the formal v2 closure, accepts no caller-selected command, and is never imported or reached by `execute-red`.

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
| 05-04 | 2 | TS-07/11/12; D-01..16; Gate A | Successor contract, non-circular projection, copied-root proof, adversarial closure, and exact Gate A approval are recorded in `05-04-SUMMARY.md`. | Current formal closure inputs exist and remain fixed. | Completed |
| 05-05 | 3 | TS-07/11/12; D-01..16; Gate B | Exact projection recomputation, Gate B, fixed-set publication, and zero-write exact resume are recorded in `05-05-SUMMARY.md`. | Current formal root, receipt, and report exist. | Completed |
| 05-06 historical | 4 | T-05-06 native preflight | Empty audit commit and harness commit are preserved; native construction probe emitted `GUARDED_REGRESS_NETWORK_PROBE_NOT_DENIED`. | Harness/tests exist; no formal byte changed and no full regression ran. | Failed closed; cancelled without summary |
| 05-07 historical | 4 | T-05-07 native/Bundler admission | Cancellation binds exact plan and validation worktree hashes; focused tests/Ruff pass, but baseline lock omits the current native platform and no full regression completed. | No formal byte changed; no 05-07 summary exists. | Failed closed; cancelled without summary |
| 05-08-01 | 4 | TS-07/11/12; D-02/05/06/08/13/15; T-05-08-01..05 | Exact one-line offline lock result, frozen bundle check, formal zero-write replay, focused tests/Ruff, and first guarded full regression with formal equality. | Adopts exact harness/tests unchanged and changes only one lockfile line. | Planned |
| 05-08-02 | 4 | TS-07/11/12; D-01/03/04/07/09/10/11/12/14/16; T-05-08-02..06 | Reassert every fixed hash/offline check, run the second guarded full regression, and create summary only after exact evidence equality. | Read-only beyond terminal non-authoritative summary. | Planned |

## Human Gates

| Gate | Preconditions | Human decision | Fail-closed outcome |
|---|---|---|---|
| Gate A — successor contract | Completed in 05-04 | Approved only the exact canonical external projection and displayed contract | Preserved; 05-08 cannot change or reinterpret it. |
| Gate B — final publication closure | Completed in 05-05 | Confirmed the unchanged Gate-A projection for exactly one current publication and exact resume | Preserved; 05-08 cannot change or reinterpret it. |

The two gates remain separate completed historical authorities. Plan 05-08 adds no human decision because the validation harness and `Gemfile.lock` are outside formal `closure_paths`, the exact platform line changes no dependency version, and the plan may not change a formal byte. Any formal-byte drift still requires a separately versioned successor and new authority.

## Formal Zero-Write Audit

The completed 05-05 post-publication replay and the planned 05-08 audit must each:

1. Snapshot exact repository-relative inventory, bytes, SHA-256, and write-observable metadata for formal, optional attempt, receipt, and Markdown targets.
2. Invoke the identical ten-option `execute-red` command under the all-socket guard and write observer.
3. Require the same canonical receipt, exact snapshot equality, and a zero write count.
4. Independently rebuild the external approved projection rather than trusting receipt fields; require distinct matching policy, runtime-closure, and projection hashes.
5. Fail without repair, cleanup, overwrite, migration, successor approval, or summary normalization on any discrepancy.
6. Before this audit begins, require the exact cancellation-bound validation hashes and the exact baseline-to-final one-line lockfile transition. Any harness, test, lock-resolution, dependency, or platform drift stops without formal/evidence writes and without regression admission.
7. Only after actual formal v2 publication, local-only Bundler validation, and the read-only audit pass, run `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root .` once in each 05-08 task. The harness must resolve and functionally preflight exactly `/usr/bin/sandbox-exec`, use explicit terminating deny rules for network, the exact formal-root/receipt/report targets, repository and user tool/dependency/cache roots, and system package prefixes plus offline/no-update controls, admit only literal `./bin/regress --all`, capture exit/output, and fail without a bare fallback on guard/profile/probe/prohibited-operation/regression error.
8. Within each guarded run, require the formal root to contain exactly `attempt-chain.json`, `evidence-span-audit.json`, `matrix-manifest.json`, `model-call-ledger.json`, `no-call-runtime-audit.json`, `no-call-structural-audit.json`, `ordered-diagnostics.json`, `parsed-evidence.json`, `raw-evidence.json`, and `red-trigger-evidence.json`, plus the exact receipt and report; compare repository-relative inventory and raw SHA-256 before/after and fail on change/add/remove. The second complete run is the deterministic zero-write proof.
9. Keep this native full-process guard separate from the formal `execute-red` runtime tripwire: the local lock check and harness are not evidence inputs, cannot authorize calls or requirements, and their narrow validation subprocesses do not create a formal model/provider/credential/retrieval/network/subprocess surface.

## Nyquist Status and Sign-Off

- [x] Wave 0 is complete: pinned local tools and the non-authorizing preflight record exist.
- [x] Completed 05-01 predecessor tests and decision evidence remain preserved as historical coverage.
- [x] Rejected 05-02, superseded 05-03, and partial failed-closed 05-06/05-07 are explicitly excluded from active discovery without fabricated summaries.
- [x] `test_authorized_execution_v2.py`, Gate A, Gate B, current formal publication, and 05-05 exact-resume zero writes are recorded by completed summaries.
- [x] The partial 05-06 harness/tests and construction-preflight diagnostic are preserved without claiming either full regression.
- [x] The partial 05-07 native correction, focused checks, exact file hashes, Bundler platform blocker, and zero completed full regressions are preserved without a summary.
- [ ] Task 05-08-01 proves the exact local-only one-line platform transition, repeats formal zero-write exact-resume, and completes the first guarded full regression with exact formal equality.
- [ ] Task 05-08-02 reasserts every fixed hash/offline contract and completes the second guarded full regression with exact formal equality before summary creation.
- [ ] `nyquist_compliant: true` may be set only after both 05-08 tasks are evidenced; it remains false while either full regression is incomplete.

**Approval:** no new authority gate is pending; only active 05-08 validation execution remains, and no future result is marked passed.

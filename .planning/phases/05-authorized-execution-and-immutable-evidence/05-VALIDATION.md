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

> Current validation and sampling contract for the sole active Plan 05-07. Completed Plans 05-00/05-01/05-04/05-05 remain evidence; rejected 05-02, superseded 05-03, and partial failed-closed 05-06 are not active validation steps or requirement-completion claims.

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
| `05-07-PLAN.md` | Planned, not executed | First performs a bounded read-only three-trial calibration of the exact native fixed-loopback denial tuple; only that stable result admits the harness/test correction, formal zero-write audit, and two guarded full regressions. |

The active discoverable Phase 5 plan set is exactly `05-00`, `05-01`, `05-04`, `05-05`, and `05-07`; the first four are complete, so active completion is **4/5**. Rejected 05-02, superseded 05-03, and failed-closed 05-06 are historical and non-discoverable.

Current filesystem facts at this planning revision:

- `experiments/specchoice-v1.3.2/tests/test_authorized_execution.py` exists as completed predecessor coverage.
- `experiments/specchoice-v1.3.2/tests/test_authorized_execution_v2.py` exists and 05-04/05-05 summaries record its passing contract coverage.
- `experiments/specchoice-v1.3.2/validation/guarded_regress.py` and `experiments/specchoice-v1.3.2/tests/test_guarded_regress.py` exist from partial 05-06 commit `46c34c8b`; their current construction-only network assertion is the failed-closed defect owned by 05-07.
- `runs/red-execution-v2`, `receipts/red-execution-v2.json`, and `reports/red-execution/red-execution-v2.md` exist as the completed 05-05 formal set; `runs/red-attempts-v2` and `runs/red-successors-v2` remain absent.

## Test Infrastructure and Sampling Commands

| Property | Current contract |
|---|---|
| Framework | Python standard-library `unittest`; project contract Python `>=3.12` |
| Pinned tools | `.venv/bin/python` 3.12.13 and `.venv/bin/ruff` 0.16.0, already recorded by 05-00 |
| Completed predecessor sampling | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution tests.test_treatments_h3 tests.test_canonical tests.test_filesystem_boundary -q` |
| Native-denial calibration | Before any implementation or formal/evidence access, Task 05-07-01 runs exactly three two-second-bounded `/usr/bin/sandbox-exec` trials under `(deny file-write*)` and `(deny network*)` of one `socket.AF_INET`/`socket.SOCK_STREAM` connect to numeric `127.0.0.1:0`, with no listener or DNS. It accepts only three identical tuples: return code `77`, stdout exactly `GUARDED_REGRESS_NETWORK_CONNECT_DENIED errno=1 diagnostic=Operation not permitted\n`, and empty stderr, emitted only for `errno.EPERM`. Any write attempt, success, other errno/diagnostic, timeout, signal, extra output, or instability escalates immediately with no formal/evidence/planning-result write and no regression admission. |
| Active successor quick sampling | After calibration succeeds, Task 05-07-02 runs the three exact `test_network_preflight_*` selectors plus every retained guard/evidence contract and Ruff command named in `05-07-PLAN.md`. |
| Guarded harness contract sampling | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_guarded_regress -q && ../../.venv/bin/ruff check --isolated validation/guarded_regress.py tests/test_guarded_regress.py`. Tests inject runner results only; they open no real socket, start no listener, contact no remote address, and never invoke the real full regression. |
| Final Phase 5 sampling | Task 05-07-03 first rechecks the exact calibrated tuple, then repeats the exact current formal command and full focused modules, and finally invokes `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root .` twice from the repository root. Each harness invocation must require socket construction followed by `connect(("127.0.0.1", 0))`, admit only the calibrated `errno.EPERM` plus exact diagnostic/return-code/stdout/stderr contract, execute exactly `./bin/regress --all` inside the unchanged deny-network/protected-install profile, and preserve the exact ten formal leaves plus receipt/report inventory/SHA-256. |
| Feedback latency | Focused unit and lint commands provide the fast loop; the two repository-wide regressions are terminal release gates and no partial output is treated as completion. |

No validation command may install packages, contact a remote network, substitute ambient tools, create a provider/model/credential/retrieval surface, or infer formal authority from a test result. The only intentional network operations are the bounded read-only calibration and the production preflight's sandboxed fixed numeric-loopback/port-zero connect-denial probes; neither creates a listener, performs DNS, admits a successful connection, or addresses a routable host. The harness's fixed `sandbox-exec ... ./bin/regress --all` boundary remains outside the formal v2 closure, accepts no caller-selected command, and is never imported or reached by `execute-red`.

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
| 05-07-01 | 4 | TS-12; T-05-07-01/02 | Three bounded read-only trials of the exact native fixed-loopback/port-zero command; terminal observation must be three identical EPERM/return-code/stdout/stderr tuples before any implementation or regression. | No file artifact; zero writes and immediate escalation on mismatch. | Planned |
| 05-07-02 | 4 | TS-12; D-05/06/15; T-05-07-01..03 | TDD exact calibrated-target/construct/connect/EPERM-diagnostic admission plus success/ordinary-failure/ambiguity rejection; retained harness tests and Ruff. | Changes only harness/tests after 05-07-01 passes. | Planned |
| 05-07-03 | 4 | TS-07/11/12; D-01..16; T-05-07-03..06 | Recheck calibrated native tuple, identical formal zero-write replay, full focused suite/Ruff/diff, then two guarded full regressions with exact evidence inventory/hash equality. | Read-only over formal and authority artifacts; summary only after every pass. | Planned |

## Human Gates

| Gate | Preconditions | Human decision | Fail-closed outcome |
|---|---|---|---|
| Gate A — successor contract | Completed in 05-04 | Approved only the exact canonical external projection and displayed contract | Preserved; 05-07 cannot change or reinterpret it. |
| Gate B — final publication closure | Completed in 05-05 | Confirmed the unchanged Gate-A projection for exactly one current publication and exact resume | Preserved; 05-07 cannot change or reinterpret it. |

The two gates remain separate completed historical authorities. Plan 05-07 adds no human decision because its validation-only harness is outside the formal closure; a formal-byte change would still require a separately versioned successor and new authority.

## Formal Zero-Write Audit

The completed 05-05 post-publication replay and the planned 05-07 final audit must each:

1. Snapshot exact repository-relative inventory, bytes, SHA-256, and write-observable metadata for formal, optional attempt, receipt, and Markdown targets.
2. Invoke the identical ten-option `execute-red` command under the all-socket guard and write observer.
3. Require the same canonical receipt, exact snapshot equality, and a zero write count.
4. Independently rebuild the external approved projection rather than trusting receipt fields; require distinct matching policy, runtime-closure, and projection hashes.
5. Fail without repair, cleanup, overwrite, migration, successor approval, or summary normalization on any discrepancy.
6. Before this audit begins, require Task 05-07-01's three stable read-only calibration tuples; Task 05-07-03 rechecks the same exact native tuple before formal access. Any host drift, successful connection, or non-EPERM/diagnostic mismatch stops without formal/evidence writes and without regression admission.
7. Only after the actual formal v2 publication, calibration/recheck, and both read-only audits pass, run `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root .` twice from the repository root. The harness must resolve and functionally preflight exactly `/usr/bin/sandbox-exec`, use explicit terminating deny rules for network, the exact formal-root/receipt/report targets, repository and user tool/dependency/cache roots, and system package prefixes plus offline/no-update controls, admit only literal `./bin/regress --all`, capture exit/output, and fail without a bare fallback on guard/profile/probe/prohibited-operation/regression error.
8. Within each guarded run, require the formal root to contain exactly `attempt-chain.json`, `evidence-span-audit.json`, `matrix-manifest.json`, `model-call-ledger.json`, `no-call-runtime-audit.json`, `no-call-structural-audit.json`, `ordered-diagnostics.json`, `parsed-evidence.json`, `raw-evidence.json`, and `red-trigger-evidence.json`, plus the exact receipt and report; compare repository-relative inventory and raw SHA-256 before/after and fail on change/add/remove. The second complete run is the deterministic zero-write proof.
9. Keep this native full-process guard separate from the formal `execute-red` runtime tripwire: the calibration and harness are not evidence inputs, cannot authorize calls or requirements, and their narrow validation subprocesses do not create a formal model/provider/credential/retrieval/network/subprocess surface.

## Nyquist Status and Sign-Off

- [x] Wave 0 is complete: pinned local tools and the non-authorizing preflight record exist.
- [x] Completed 05-01 predecessor tests and decision evidence remain preserved as historical coverage.
- [x] Rejected 05-02, superseded 05-03, and partial failed-closed 05-06 are explicitly excluded from active discovery without fabricated summaries.
- [x] `test_authorized_execution_v2.py`, Gate A, Gate B, current formal publication, and 05-05 exact-resume zero writes are recorded by completed summaries.
- [x] The partial 05-06 harness/tests and observed construction-preflight diagnostic are preserved without claiming either full regression.
- [ ] Task 05-07-01 records three identical bounded native `errno.EPERM` plus exact-diagnostic tuples in the terminal before any implementation/formal/evidence write; any mismatch escalates with no regression admission and no summary.
- [ ] Task 05-07-02 proves socket construction followed by fixed-loopback/port-zero connect and admits only the calibrated return-code/stdout/stderr contract; every success or ambiguity stops before regression.
- [ ] Task 05-07-03 rechecks the calibrated tuple, repeats the current formal zero-write audit, and runs the exact `./bin/regress --all` command twice through the corrected guard, preserving the exact twelve-file successor evidence inventory/SHA-256 map.
- [ ] `nyquist_compliant: true` may be set only after all three 05-07 tasks are evidenced; it remains false now because calibration, corrected native denial, and both full regressions have not passed.

**Approval:** no new authority gate is pending; only active 05-07 validation execution remains, and no future result is marked passed.

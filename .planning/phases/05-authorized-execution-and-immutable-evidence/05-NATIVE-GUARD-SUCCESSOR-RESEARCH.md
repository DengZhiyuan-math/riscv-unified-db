# Phase 5: Native-Guard Successor - Research

**Researched:** 2026-08-05  
**Domain:** Forward-only correction of the validation-only macOS native sandbox preflight  
**Confidence:** HIGH (local repository, local GSD workflow, and installed macOS manual pages; no network, model, or guarded full regression was run)

<user_constraints>
<!-- DATA_Qp7Lm4Xa_START: verbatim Context capture -->
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** A Phase 5 Red execution enters `completed` only when exact v6 authority validation, the immutable zero-entry call ledger, structural and runtime no-call proofs, preserved Red-trigger evidence, the zero-cell matrix, and the terminal receipt are complete and mutually bound. Missing material is blocking; `completed_with_warnings` is not a valid formal terminal state. — **Reversibility:** one-way — changing the completion contract after evidence publication requires a versioned successor evidence schema and complete revalidation.
- **D-02:** Re-executing identical frozen inputs must exactly resume byte-identical evidence with zero writes. Any mismatch fails closed and requires a versioned successor; evidence is never overwritten or silently regenerated in place.
- **D-03:** A failure before formal completion creates a separate immutable, non-authoritative attempt package. The formal Red evidence set is published only as a complete atomic file set; partial files cannot occupy the formal evidence boundary.
- **D-04:** `completed` grants only permission to evaluate the Red evidence in Phases 6 and 7. It does not authorize model calls, Green/Yellow execution, external publication, a final feasibility conclusion, or permanent closure of conditional Green/Yellow requirements.
- **D-05:** Zero-call proof is a three-layer closure bound to one attempt root: an authoritative zero-entry `model_call_ledger`, a structural scan proving provider/model/credentials/production-retrieval surfaces absent, and a runtime network tripwire. — **Reversibility:** one-way — weakening this proof after publication invalidates the evidence root and requires a successor run contract.
- **D-06:** Formal Red execution fails closed on every socket operation, including external, LAN, and loopback access. Any attempted socket creation or connection terminates the attempt and emits a stable diagnostic.
- **D-07:** The formal `model_call_ledger` represents real calls and must remain empty for completed Red evidence. Blocked socket or model-call attempts are recorded separately in the failed attempt's `security_events`; their presence prevents formal evidence publication without falsely claiming a real call occurred.
- **D-08:** Phase 5 must bind the Phase 4 v6 no-model root and independently rescan the actual Phase 5 execution closure, including CLI surfaces, imports, dependencies, configuration paths, and credential entry points. Both proof roots are bound into the attempt receipt.
- **D-09:** Red execution emits a canonical zero-cell matrix manifest with `branch=red`, `N_strict=0`, `repeat_count=0`, `expected_cells=0`, `actual_cells=0`, and `cells=[]`, bound to the exact v6 authority and Red trigger. It creates no N/A placeholder calls. — **Reversibility:** one-way — the manifest is part of the published evidence schema and changing its semantics requires a successor.
- **D-10:** TS-11 and TS-12 are recorded as `conditional_not_applicable_red_pending_phase7`. Phase 5 does not execute them and cannot permanently close them before Phase 7 validates the complete Red chain.
- **D-11:** The manifest proves absence of favorable-subset execution with `expected_cells = N_strict * 3 * repeat_count = 0`, treatment-partitioned A/B/C counts for expected, attempted, completed, failed, and retried cells all equal to zero, and a closure check showing no unregistered run or raw-response artifacts.
- **D-12:** Canonical JSON is the sole matrix authority. A deterministic Markdown projection may explain the Red trigger, zero-count formula, and conditional requirement state, but neither artifact may emit model metrics or claim extraction-experiment success.
- **D-13:** Any byte change in the frozen execution closure requires a versioned successor. The closure includes the v6 authority and bound roots, Phase 5 execution code, schemas, CLI allowlist, no-model policy, network policy, and evidence structure. A runtime fault with unchanged inputs creates a failed attempt and may be retried without a successor. — **Reversibility:** one-way — changed frozen bytes cannot inherit an authority issued for the predecessor root.
- **D-14:** Every drift or runtime failure preserves a complete failed-attempt package: attempt identity, frozen input inventory and hashes, expected/observed difference, stable diagnostics, termination stage, zero-call ledger, `security_events`, hashes and custody locations for any produced raw bytes, and explicit `authoritative=false` and `metrics_emitted=false` declarations.
- **D-15:** Tooling may construct a successor candidate, difference inventory, and readiness packet, but it cannot authorize the successor. Human approval of a new H3/Phase 5 binding chain is required. The v6 authority remains immutable historical authority and cannot authorize changed bytes.
- **D-16:** Every retry is a new immutable attempt. Failed attempts are never overwritten or deleted. Final successful evidence binds the complete ordered attempt sequence under the same execution root and proves every attempt's model-call ledger is empty; retries cannot change inputs or policy.

### the agent's Discretion

The planner may choose internal module names, CLI command names, schema decomposition, immutable attempt and evidence-directory names, additional stable diagnostic codes, the standard-library mechanism used for the socket tripwire, and the deterministic Markdown layout. These choices must reuse existing canonical JSON, strict parsing, descriptor-bound no-replace publication, exact-resume, runtime-closure, stable-diagnostic, and human-authority patterns. Do not add a dependency when the standard library or installed project code suffices.

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within the Red-only Phase 5 scope.
<!-- DATA_Qp7Lm4Xa_END -->
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| TS-07 | Immutable raw/parsed/diagnostic/span custody remains auditable. | The successor snapshots and prohibits changes to the already committed v2 formal inventory; it creates no evidence leaf. [VERIFIED: 05-06-PLAN.md:163-177] |
| TS-11 | Red retains the zero-cell, no-G/Y-execution boundary. | The receipt remains completed Red evidence; the harness is outside the formal closure and cannot alter the matrix. [VERIFIED: red-execution-policy-v2.json:1; red-execution-v2.json:1] |
| TS-12 | The real-call ledger remains empty with no missing calls. | Keep the formal Python all-socket tripwire intact; the native guard is a separate validation process and cannot authorize a call. [VERIFIED: red_v2.py:200-213; 05-06-PLAN.md:105-111] |
</phase_requirements>

## Project Constraints (from AGENTS.md)

- Reuse the smallest mature existing mechanism; prefer existing repository code, the standard library, and native platform capability before adding a dependency. [VERIFIED: AGENTS.md:18-21; 26-53]
- Run repository-wide release validation through `./bin/regress --all` when it is authorized by the plan. [VERIFIED: AGENTS.md:31-36; 124-128]
- Treat the repository as rapidly changing and revalidate current source rather than relying on stale schema/API assumptions. [VERIFIED: AGENTS.md:12-14]
- Do not alter unrelated user worktree files; current `git status --short` contains unrelated untracked files outside this successor scope. [VERIFIED: git status --short, 2026-08-05]

## Summary

The committed formal v2 evidence is already a completed, fixed Red no-call package. Its terminal receipt literally contains `"status":"completed"`, and the v2 policy’s closed `closure_paths` list ends with `"tests/test_authorized_execution_v2.py"`; neither lists the validation harness. The harness therefore remains outside formal authority, and this correction must not rewrite policy, formal evidence, receipt, report, v1/v2 closure inputs, or the formal all-socket guard. [VERIFIED: experiments/specchoice-v1.3.2/receipts/red-execution-v2.json:1; experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v2.json:1; 05-06-PLAN.md:105-111]

The 05-06 failure is an over-strong validation assertion, not a formal-evidence failure: the current preflight command is `"import socket; socket.socket()"`, while the profile is `(version 1)`, `(allow default)`, `(deny network*)`. The supplied failure observation says that this profile allows construction. The installed `sandbox(7)` manual independently says restrictions are generally enforced when an operating-system resource is acquired. The native guard must instead prove that a connection-use attempt is denied; socket construction alone is not a required denial when it performs no connection. [VERIFIED: validation/guarded_regress.py:48-56; 145-151; 189-212; VERIFIED: task-scope 05-06 failure observation; VERIFIED: local man sandbox(7)]

**Primary recommendation:** First make an administrative, forward-only cancellation of discoverable 05-06 without a summary; then execute a new `05-07-PLAN.md` that changes only the validation harness/tests to require an explicitly denied socket connection operation and repeats the two fixed guarded zero-write regressions.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Formal Red no-call enforcement | API / Backend | — | `red_v2.py` owns the all-socket tripwire and formal evidence lifecycle; it is frozen and out of scope. [VERIFIED: red_v2.py:200-213; 306-312] |
| Fixed regression process confinement | Host OS | Validation script | `/usr/bin/sandbox-exec` applies the native profile to the one fixed release command. [VERIFIED: validation/guarded_regress.py:48-56; 185-186; local man sandbox-exec(1)] |
| Guard admission and evidence immutability comparison | Validation script | Filesystem / Storage | `guarded_regress.py` constructs the profile and compares a descriptor-held v2 inventory before/after the child. [VERIFIED: validation/guarded_regress.py:89-105; 189-243] |
| GSD plan lifecycle recovery | Planning metadata | Git history | GSD dispatches incomplete `*-PLAN.md` files and stops if such a plan has commits but lacks its matching summary. [VERIFIED: execute-phase.md:178-191; 325-336] |

## Standard Stack

### Core

| Component | Version | Purpose | Why Standard |
|-----------|---------|---------|--------------|
| `/usr/bin/sandbox-exec` | host-provided | Mandatory process profile for the one fixed regression command. | It is present locally and accepts exactly one of `-f`, `-n`, or `-p`; no package install is needed. [VERIFIED: local `/usr/bin/sandbox-exec --help`, 2026-08-05] |
| Python standard library | existing project runtime | Build the profile, injectable runner, snapshots, hashes, and deterministic failures. | The committed harness already uses only standard-library modules plus repository filesystem primitives. [VERIFIED: validation/guarded_regress.py:9-31] |
| `specchoice_evidence.filesystem` | repository-local | No-follow authoritative enumeration and reads for the twelve protected v2 leaves. | Reuse it; do not duplicate path/no-follow/hash handling. [VERIFIED: validation/guarded_regress.py:27-31; 89-105] |

### Supporting

| Component | Purpose | When to Use |
|-----------|---------|-------------|
| `unittest` with injected runner | Assert admission behavior without opening a real socket or invoking full regression. | Every unit contract for unavailable guard, profile failure, denied connection probe, child failure, and evidence mutation. [VERIFIED: test_guarded_regress.py:15-115; 05-06-PLAN.md:211-217] |
| Existing v2 formal tripwire | Preserve formal all-socket denial and stable diagnostics. | Formal `execute-red` only; never replace it with the harness. [VERIFIED: red_v2.py:200-213; 05-06-PLAN.md:105-111] |

**Installation:** None. No package may be added, downloaded, upgraded, or installed. [VERIFIED: 05-06-PLAN.md:215-223]

## Package Legitimacy Audit

Not applicable: the successor installs no external package. [VERIFIED: 05-06-PLAN.md:215-223]

## Current-State Finding

<!-- DATA_Vr6Tz2Qn_START: verbatim relevant current constants -->
```python
_SANDBOX_EXEC = Path("/usr/bin/sandbox-exec")
_FIXED_REGRESSION_ARGV = ("./bin/regress", "--all")
_PREFLIGHT_NETWORK = ("/usr/bin/python3", "-c", "import socket; socket.socket()")
```
<!-- DATA_Vr6Tz2Qn_END -->

The same source creates the profile with `"(version 1)"`, `"(allow default)"`, and `"(deny network*)"`; it rejects a zero-returning network probe and has no bare regression branch. Preserve those properties exactly while changing only what the network probe proves. [VERIFIED: validation/guarded_regress.py:145-151; 189-212; 215-243]

<!-- DATA_Hn3Ka8Dw_START: verbatim lifecycle facts -->
```text
46c34c8b3e03b77138102db15bf48a3acdaa9c03
test(05-06): add guarded regression harness
A experiments/specchoice-v1.3.2/tests/test_guarded_regress.py
A experiments/specchoice-v1.3.2/validation/guarded_regress.py
```
<!-- DATA_Hn3Ka8Dw_END -->

This is a partial 05-06 implementation commit, but no `05-06-SUMMARY.md` exists. `phase-plan-index 05` consequently reports `05-06` as the sole incomplete plan; GSD’s safe-resume gate would stop before dispatch because a matching plan commit exists without a summary. Do not create a false summary merely to bypass that guard. [VERIFIED: git show --name-status 46c34c8b, 2026-08-05; VERIFIED: gsd-tools `phase-plan-index 05`, 2026-08-05; VERIFIED: execute-phase.md:178-191]

## Recommended Forward-Only Lifecycle

### Administrative reconciliation — before any executor dispatch

Make one documentation-only administrative commit outside normal plan execution:

1. Rename `05-06-PLAN.md` to `05-06-FAILED-CLOSED.md`, preserving its bytes as historical planning evidence and removing it from the discoverable `*-PLAN.md` set. [VERIFIED: 05-02-CANCELLATION.md:32-37; execute-phase.md:325-336]
2. Add `05-06-CANCELLATION.md` with `status: failed_closed_not_completed`, `partial_execution_commits: [46c34c8b]`, `requirements_completed: []`, `formal_publication: false`, and the recorded failure condition `GUARDED_REGRESS_NETWORK_PROBE_NOT_DENIED`. This is a proposed record schema constrained by the established 05-02 cancellation pattern. [VERIFIED: 05-02-CANCELLATION.md:1-37; VERIFIED: task-scope 05-06 failure observation]
3. Update `ROADMAP.md`, `STATE.md`, and `05-VALIDATION.md` to say that 05-06 is historical failed-closed work, not completed work, and that `05-07` is the sole active successor. Do not change TS-07/TS-11/TS-12 completion facts, formal authority, or any evidence byte. [VERIFIED: ROADMAP.md:307-332; STATE.md:5-17; 194-196; 05-VALIDATION.md:13-27]
4. Add discoverable `05-07-PLAN.md` only after step 1, with `depends_on: [05-05]` and wave 4. It is the next correction plan; it does not depend on a fictional completed 05-06. [VERIFIED: 05-06-PLAN.md:1-19; 05-02-CANCELLATION.md:51-61]

This is the same forward-only technique already used for rejected 05-02 and superseded 05-03: preserve the old bytes in a non-discoverable historical document and do not fabricate a `SUMMARY.md`, because a summary is the completion signal. [VERIFIED: 05-02-CANCELLATION.md:19-37]

### `05-07-PLAN.md` responsibilities

| Task | Files owned | Required result |
|------|-------------|-----------------|
| 05-07-01 — TDD the native semantics correction | `experiments/specchoice-v1.3.2/tests/test_guarded_regress.py` | Replace the construction-time expectation with a connection-use probe contract. Assert the runner receives a probe containing `.connect(...)`, preserve runner injection, and assert no real socket/full regression in unit tests. [VERIFIED: test_guarded_regress.py:34-47; 57-65; 05-06-PLAN.md:211-217] |
| 05-07-02 — minimally repair guard admission | `experiments/specchoice-v1.3.2/validation/guarded_regress.py` | Keep the exact native path, deterministic profile, fixed argv, evidence snapshot, offline environment, write probe, output hashes, and no-fallback behavior; alter only the network preflight so success means native denial of connection use. [VERIFIED: validation/guarded_regress.py:89-105; 145-170; 173-243] |
| 05-07-03 — read-only formal audit and two runs | no source/evidence ownership beyond the 05-07 summary | After focused validation is green, execute the existing read-only v2 replay/audit and invoke the corrected fixed harness twice. Each run must preflight, run only `./bin/regress --all` under the profile, and prove the twelve-leaf receipt/report inventory unchanged. [VERIFIED: 05-06-PLAN.md:215-238; 05-VALIDATION.md:89-100] |

### Correct native preflight semantics

The successor probe must exercise a socket operation that attempts a connection, not merely allocate a socket. A loopback-only controlled endpoint is the robust way to distinguish a sandbox denial from an unrelated connection-refused error: the child’s connection must be denied before the listener can accept it; an accepted connection is an admission failure. The listener and its temporary port are validation-only, exist only during preflight, and are never formal evidence, a provider/model/retrieval surface, or an external network action. [VERIFIED: task-scope requested correction; VERIFIED: local man sandbox(7); ASSUMED: controlled loopback listener is the minimal deterministic discriminator on this host]

Do not accept `returncode != 0` as sufficient proof of network denial: an unreachable endpoint can also fail without the sandbox. The harness should make the child emit a stable result that distinguishes native denial from any non-denial socket error, and it should fail closed on ambiguity. This is a required semantic strengthening of the preflight, not a change to formal D-06. [VERIFIED: task-scope requested correction; ASSUMED: host-specific native error classification must be observed during 05-07 implementation]

## Architecture Pattern

```text
operator --repo-root
        |
        v
guarded_regress.py
  |-- snapshot 12 v2 leaves + receipt + report (read-only)
  |-- require /usr/bin/sandbox-exec and build fixed profile
  |-- harmless profile-application preflight
  |-- controlled loopback connection probe -- denied before accept --> admit
  |                                                  \-- accepted/ambiguous --> fail closed
  |-- protected temporary-write probe -- denied --> admit
  |-- /usr/bin/sandbox-exec -p <profile> ./bin/regress --all
  |-- snapshot again; exact equality required
  '-- return non-authoritative diagnostics only

formal execute-red v2  <--- remains separate, all-socket/no-subprocess guarded, and unchanged
```

### Preserve, do not hand-roll

| Problem | Do not build | Use instead | Why |
|---------|--------------|-------------|-----|
| Formal v2 evidence parsing / path safety | A second evidence reader or ad hoc `Path` traversal | `enumerate_authoritative_files` and `read_authoritative_files` | Existing no-follow inventory/hash behavior already protects the exact v2 leaves. [VERIFIED: validation/guarded_regress.py:27-31; 89-105] |
| Formal network prohibition | A new native profile as formal authority | Existing `deny_all_sockets_v2` | The formal all-socket guard owns D-06 and is frozen in the v2 closure. [VERIFIED: red_v2.py:200-213; config/execution/red-execution-policy-v2.json:1] |
| Command selection | A generic runner or shell string | `_FIXED_REGRESSION_ARGV` through `_guard_argv` | The current interface is already closed to one argv and no shell evaluation. [VERIFIED: validation/guarded_regress.py:49; 185-186; 215-243] |
| Lifecycle bypass | A fabricated 05-06 summary | Non-discoverable archive plus cancellation record | GSD uses summaries to identify completed plans and otherwise stops when commits exist. [VERIFIED: execute-phase.md:178-191; 325-336] |

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Python standard-library `unittest` [VERIFIED: test_guarded_regress.py:1-15] |
| Quick command | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_guarded_regress -q` [VERIFIED: 05-VALIDATION.md:45-46] |
| Lint | `../../.venv/bin/ruff check --isolated validation/guarded_regress.py tests/test_guarded_regress.py` [VERIFIED: 05-VALIDATION.md:45-46] |
| Release command | Only the harness’s fixed `./bin/regress --all`, twice, after admission and focused checks. [VERIFIED: validation/guarded_regress.py:49; 05-06-PLAN.md:221-229] |

### Required tests for 05-07

| Behavior | Test type | Expected result |
|----------|-----------|-----------------|
| Socket construction is not the admission criterion | unit, injected runner | The preflight command contains a connection operation; a construction-only probe cannot satisfy the test. [VERIFIED: task-scope requested correction] |
| Connection use is natively denied | unit, injected runner; real preflight only at final execution | A denied connection result admits the child; accepted or ambiguous results stop before regression. [VERIFIED: task-scope requested correction; ASSUMED: exact host denial representation must be pinned by 05-07] |
| Guard/profile/write protections retain behavior | unit, injected runner | Missing guard, invalid profile, write success/sentinel creation, or child nonzero/signal is failure. [VERIFIED: test_guarded_regress.py:49-97; validation/guarded_regress.py:189-243] |
| Closed production argv and evidence mutation | unit, injected runner | No override or bare fallback; any changed/added/removed protected v2 leaf fails. [VERIFIED: validation/guarded_regress.py:89-105; 215-243] |
| End-to-end validation | manual release gate | Two successful guarded full regressions, each with before/after exact formal evidence equality and no install-surface write. [VERIFIED: 05-06-PLAN.md:221-229; 05-VALIDATION.md:89-100] |

## Security Domain

| ASVS Category | Applies | Control |
|---------------|---------|---------|
| V3 Session Management | No | No session surface is introduced. [VERIFIED: 05-06-PLAN.md:121-125] |
| V4 Access Control | Yes | Exact `/usr/bin/sandbox-exec`, fixed argv, no command override, and no bare fallback. [VERIFIED: validation/guarded_regress.py:173-186; 215-243] |
| V5 Input Validation | Yes | `--repo-root` is the only production argument; root and evidence leaves are validated before child execution. [VERIFIED: validation/guarded_regress.py:80-105; 262-277] |
| V6 Cryptography | Yes | Reuse SHA-256 evidence snapshots; do not implement a new digest format. [VERIFIED: validation/guarded_regress.py:89-105; 226-242] |

| Threat | STRIDE | Required mitigation |
|--------|--------|---------------------|
| Socket construction is mistaken for network-use denial | Elevation of Privilege | Preflight an actual connection-use operation and fail closed unless denial is distinguished from endpoint failure. [VERIFIED: task-scope requested correction; local man sandbox(7)] |
| Bare or caller-selected regression runs | Elevation of Privilege | Preserve literal fixed argv, exact sandbox path, mandatory profile, and no fallback. [VERIFIED: validation/guarded_regress.py:48-49; 173-186; 215-243] |
| Regression mutates formal evidence or install surfaces | Tampering | Keep protected profile paths, offline/no-update environment, and before/after exact v2 inventory/hash checks. [VERIFIED: validation/guarded_regress.py:112-170; 189-243] |
| Historical partial plan is accidentally re-executed or falsely completed | Repudiation | Archive 05-06 outside active `*-PLAN.md` discovery with an explicit failed-closed cancellation record and no summary. [VERIFIED: 05-02-CANCELLATION.md:19-37; execute-phase.md:178-191] |

## Human Gates

No new Gate A or Gate B is required: those gates bind the already completed formal v2 closure, while the policy’s closed `closure_paths` excludes this validation-only harness. The successor may not reinterpret either gate as permission to change formal bytes. [VERIFIED: red-execution-policy-v2.json:1; 05-04-SUMMARY.md:73-89; 05-05-SUMMARY.md:101-105]

Use an executor checkpoint only for the two expensive full regressions if an operator wants to inspect the corrected preflight transcript; it is a release-validation acknowledgement, not an evidence-authority or requirement-closing decision. [ASSUMED: optional operational checkpoint]

## Non-Goals and Risks

- Do not change any formal v1/v2 evidence, receipt, report, policy, `red_v2.py`, `cli_v2.py`, Phase 4 v6 authority, Gate-A/Gate-B bytes, or formal requirement status. [VERIFIED: 05-06-PLAN.md:117-125; red-execution-policy-v2.json:1]
- Do not create a `05-06-SUMMARY.md`, claim 05-06 completed, or make the 05-07 summary an evidence artifact. [VERIFIED: 05-02-CANCELLATION.md:19-37; 05-06-PLAN.md:105-111]
- Do not add packages, download/install/upgrade tools, change `HOME`, mutate firewall/routing/proxy/privilege settings, create provider/model credentials, or perform external network activity. [VERIFIED: validation/guarded_regress.py:154-170; 05-06-PLAN.md:215-223]
- The only intentional connection-use probe is local and must be denied by the child sandbox before acceptance; host-specific error/termination representation is the remaining implementation risk and must fail closed when unrecognized. [ASSUMED: native host behavior needs a one-time observed classification during 05-07]
- A successful broad regression does not grant formal authority; it only validates the release environment and protected evidence immutability. [VERIFIED: 05-06-PLAN.md:105-111; 221-233]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | A controlled loopback listener is the smallest deterministic way to distinguish native connection denial from an ordinary connection failure. | Correct native preflight semantics | The successor could need a different local native-denial classifier; it must not proceed on ambiguity. |
| A2 | The exact macOS denial representation can be pinned during 05-07’s first corrected preflight without changing formal evidence. | Required tests | Treat as a blocked validation result, not success, if it cannot be classified. |
| A3 | An optional operator checkpoint before the two full regressions is useful but not an authority gate. | Human Gates | Omit it if project workflow does not require acknowledgement. |

## Open Questions

1. **Which stable signal demonstrates a native `network*` denial on this exact host?**
   - What we know: construction succeeds under the observed profile; connection use is the required criterion. [VERIFIED: task-scope 05-06 failure observation]
   - What's unclear: whether the host reports the denial as a signal, a specific errno, or another stable stderr form.
   - Recommendation: implement the loopback-controlled preflight behind the existing runner seam; record and accept only an explicit denied classification, fail closed otherwise.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| `/usr/bin/sandbox-exec` | mandatory native profile | ✓ | host-provided; local usage supports `-p profile-string` | None — fail closed. [VERIFIED: local `ls -l /usr/bin/sandbox-exec` and `sandbox-exec --help`, 2026-08-05] |
| repository `.venv` and Ruff | existing harness toolchain preflight | required by current harness | current harness validates them before running | None — fail closed. [VERIFIED: validation/guarded_regress.py:246-259] |

## Sources

### Primary (HIGH confidence)

- `validation/guarded_regress.py` and `tests/test_guarded_regress.py` — current failed preflight semantics and retained guard boundaries. [VERIFIED: validation/guarded_regress.py:48-56; 145-243; test_guarded_regress.py:34-115]
- Phase 5 context, plans, summaries, cancellation history, validation, current policy, receipt, and GSD execution workflow — formal boundary and forward-only lifecycle. [VERIFIED: 05-CONTEXT.md:18-46; 05-02-CANCELLATION.md:19-61; 05-04-SUMMARY.md:73-89; 05-05-SUMMARY.md:81-105; execute-phase.md:178-191]
- Local macOS `sandbox(7)` and `sandbox-exec(1)` manual pages — resource-acquisition enforcement and fixed profile invocation syntax. [VERIFIED: local man sandbox(7); local man sandbox-exec(1)]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new package or external dependency is proposed.
- Architecture: HIGH — current harness, formal closure, receipt, and execution-discovery behavior were inspected locally.
- Native-denial classification: MEDIUM — installed manual page supports acquisition-time semantics; exact host denial signal must be pinned by the corrected preflight.

**Research date:** 2026-08-05  
**Valid until:** Any change to the native harness, GSD execution discovery, or formal v2 closure.

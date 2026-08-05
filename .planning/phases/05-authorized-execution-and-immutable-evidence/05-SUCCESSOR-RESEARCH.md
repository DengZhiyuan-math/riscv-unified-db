# Phase 5: Authorized Execution and Immutable Evidence — Formal-Publication Successor Research

**Researched:** 2026-08-05  
**Domain:** forward-only correction of an immutable Red no-call publication interface  
**Confidence:** HIGH (repository and local GSD-workflow evidence only; no network or package lookup was needed)

<user_constraints>
<!-- DATA_G7qL2mXr_START: verbatim Context capture -->
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
<!-- DATA_G7qL2mXr_END -->
</user_constraints>

## Project Constraints (from AGENTS.md)

- Reuse the simplest existing implementation; prefer standard library and installed code before a new dependency. [VERIFIED: AGENTS.md:10-14]
- Keep the prototype isolated under `experiments/specchoice-v1.3.2/`; do not change core UDB schemas or generated data. [VERIFIED: AGENTS.md:58-69]
- Use the repository’s current source as authoritative because its schemas and APIs are rapidly changing. [VERIFIED: AGENTS.md:12-14]
- The project validation gate is `./bin/regress --all`; Phase-specific focused commands remain the practical pre-publication gate. [VERIFIED: AGENTS.md:26-49; 116-128]

## Phase Requirements

| ID | Successor support |
|---|---|
| TS-07 | Preserve distinct immutable raw, parsed, diagnostics, and span-audit leaves; Red’s explicit empty finding set must not fabricate a model response. [VERIFIED: .planning/REQUIREMENTS.md:33; 78-82] |
| TS-11 | Retain the verbatim status `conditional_not_applicable_red_pending_phase7` and the zero-cell Red matrix; do not execute a G/Y cell. [VERIFIED: .planning/REQUIREMENTS.md:37; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:30-35] |
| TS-12 | Retain the exactly empty real-call ledger plus structural and runtime no-call proofs; blocked operations belong only to failed-attempt security events. [VERIFIED: .planning/REQUIREMENTS.md:38; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:23-28] |

## Current Facts and Evidence

1. Phase 4 v6 is immutable historical input, not an authorization for changed Phase-5 bytes. The canonical authority literally contains `"branch":"red"`, `"N_strict":0`, `"repeat_count":0`, `"external_calls_authorized":false`, `"model_execution_authorized":false`, `"production_retrieval_authorized":false`, and `"provider_config_present":false`. [VERIFIED: experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1]
2. Lifecycle work for Task 05-02-01 is present in commits `4d6d6edb` and `b5de8ce9`; the recorded final-closure decision is `reject-final-closure` in commit `42733101`. That commit explicitly states that Task 05-02-03 is prohibited and a versioned successor plus new gates are required. [VERIFIED: git show --name-status 4d6d6edb; git show --name-status b5de8ce9; git show 42733101; .planning/STATE.md:167-168]
3. Task 05-02-03 was never run: no `05-02-SUMMARY.md` exists, and the requested formal output set is absent. The checked literal protected paths are `experiments/specchoice-v1.3.2/runs/red-execution-v1/`, `experiments/specchoice-v1.3.2/receipts/red-execution-v1.json`, `experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v1.md`, `experiments/specchoice-v1.3.2/runs/red-attempts/`, and `experiments/specchoice-v1.3.2/runs/red-successors/`. [VERIFIED: repository filesystem inventory, 2026-08-05; .planning/phases/05-authorized-execution-and-immutable-evidence/05-02-PLAN.md:219-255]
4. The mismatch is concrete, not cosmetic: the frozen v1 policy literally exposes `"allowed_cli_commands":["execute-red-temporary"]`, and `cli.py` registers only `execute-red-temporary` with a single `--target` argument. [VERIFIED: experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json:1; experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py:21-35]
5. The old publication task requires `execute-red` with explicit authority, packet, readiness, decision, attempt, formal-root, receipt, and report inputs; those parameters do not exist on the v1 CLI. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-02-PLAN.md:236-255; experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py:21-35]
6. The current builder writes only the eleven v1 machine leaves below a caller-selected output root; it does not write the separately planned repository receipt or Markdown projection. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:53-66; 302-315; 567-613]
7. The executor discovers the first `*-PLAN.md` without a matching `*-SUMMARY.md`, and its documented incomplete-plan filtering skips only plans that already have summaries (plus optional wave/gap filters). A free-standing cancellation note therefore cannot by itself prevent rediscovery of old 05-02/05-03. [VERIFIED: GSD local workflow `execute-plan.md`:59-67; `execute-phase.md`:332-338]

## Summary and Primary Recommendation

Create a new `red-execution-policy-v2` and exact v2 closure, with one and only one production command named `execute-red`. It must consume the immutable v6 authority as input, publish only a v2 formal namespace, and bind a new human Phase-5 successor decision; it must never edit v1 policy, v1 closure, v1 output names, or Phase-4 authority. This is the smallest correction because it changes only the missing formal publication interface and the roots affected by that interface, while reusing canonical JSON, strict parsing, descriptor-bound no-replace publication, and runtime-closure helpers. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:37-46; experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:40-50; experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:251-259; experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py:187-256]

**Primary recommendation:** make the v2 policy the sole source of the exact `execute-red` input/target contract, then require a contract-approval gate and a final-closure gate before it may create any non-temporary evidence.

## Architectural Responsibility Map

| Capability | Primary tier | Secondary tier | Rationale |
|---|---|---|---|
| v2 command admission and exact input parsing | Local execution API | Storage | The CLI must reject a different command/argument set before any writer opens. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py:28-45] |
| v6 authority and v2 closure validation | Local execution API | Storage | Both are reconstructed from persisted bytes before writing. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:146-185; 188-224] |
| formal/attempt/successor publication | Storage | Local execution API | The existing descriptor publisher enforces relative paths and no-replace leaves. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:29-39; 251-259] |
| human successor authorization | Human gate | Local execution API | Code may validate a decision but may not create approval. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:39-42] |
| post-publication audit | Read-only verifier | Storage | A successor audit recomputes v2 roots without repairing outputs. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-03-PLAN.md:63-67; 107-163] |

## Recommended v2 Contract

### File-level boundary

| Role | Required v2 path | Contract |
|---|---|---|
| Frozen policy | `experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v2.json` | Closed canonical JSON; the authoritative command list is verbatim `["execute-red"]`. [ASSUMED: proposed successor path/value; must be frozen at Gate A] |
| Execution code | `experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py` | Add a versioned formal-publication entry point without rewriting the frozen v1 implementation or policy interpretation. [ASSUMED: minimal successor module; Gate A binds exact bytes] |
| CLI | `experiments/specchoice-v1.3.2/src/specchoice_execution/cli_v2.py` | Expose only v2 production `execute-red`; no temporary, model, provider, credential, retrieval, subprocess, or network command. [ASSUMED: successor interface; existing v1 is closed temporary-only at experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py:21-35] |
| Tests | `experiments/specchoice-v1.3.2/tests/test_authorized_execution_v2.py` | Use a disposable copied repository root to exercise the real v2 command and all v2 targets without changing the v1 test closure. [ASSUMED: successor test module; existing tests already use copied roots at experiments/specchoice-v1.3.2/tests/test_authorized_execution.py:30-59] |
| Formal root | `experiments/specchoice-v1.3.2/runs/red-execution-v2/` | New v2 namespace; never write `runs/red-execution-v1/`. [ASSUMED: proposed successor path; Gate A binds it] |
| Terminal receipt | `experiments/specchoice-v1.3.2/receipts/red-execution-v2.json` | Canonical authoritative receipt published in the same v2 operation as all formal leaves. [ASSUMED: proposed successor path; Gate A binds it] |
| Markdown projection | `experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v2.md` | Deterministic non-authoritative projection, bound to the canonical receipt. [ASSUMED: proposed successor path; Gate A binds it] |
| Failed attempts | `experiments/specchoice-v1.3.2/runs/red-attempts-v2/` | Conditional append-only non-authoritative custody only; no clean first-attempt directory. [ASSUMED: proposed successor path; D-03/D-14 constrain semantics] |
| Drift candidates | `experiments/specchoice-v1.3.2/runs/red-successors-v2/` | Conditional decision-free candidate/diff/readiness custody only; no authority leaf. [ASSUMED: proposed successor path; D-13/D-15 constrain semantics] |

All values in the v2 policy, receipt, audits, and Markdown must be repository-relative paths. The existing primitive rejects absolute, empty, `.`/`..`, and backslash-containing paths; keep that validator rather than implement a second path policy. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:29-39]

### Exact command and input/output rules

The v2 CLI module must accept `execute-red` only. Its explicit options must identify `--repo-root`, `--policy`, `--authority`, `--packet`, `--readiness`, `--decision`, `--attempt-root`, `--formal-root`, `--receipt`, and `--report`; every supplied path is repository-relative to `--repo-root`, and each must equal the canonical v2 policy inventory before admission. This exact surface repairs the missing interface in old Task 05-02-03 while forbidding caller-selected output locations, without rewriting the historical v1 `execute-red-temporary` module. [ASSUMED: proposed v2 CLI contract; old required option set is documented at .planning/phases/05-authorized-execution-and-immutable-evidence/05-02-PLAN.md:236-255]

Before a writer opens, v2 must:

1. strictly parse canonical policy/authority inputs; validate the Phase-4 v6 authority; re-hash all exact authority leaves; and reject every input/path not declared by policy. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:90-98; 146-185]
2. reconstruct and verify a frozen runtime closure from all v2 execution code, policy, tests, directly imported evidence/strict-json/H3 modules, Phase-3 trigger input, Phase-4 authority chain, and toolchain contract files. The required frozen map must include each repository-relative path, byte length, and SHA-256; policy and closure hashes are distinct fields. [ASSUMED: v2 closure expansion; existing closure entries use exactly `"byte_length"`, `"path"`, and `"sha256"` at experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py:203-226]
3. install the all-socket guard before admission and carry the runtime-audit/security-event object through completion; no provider/model/network/credential/retrieval/process action may occur on any path. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:227-240; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:23-28]
4. build every formal JSON leaf, terminal receipt, and Markdown projection in memory; validate all internal hashes and the complete fixed inventory; publish exactly once with descriptor-bound no-replace semantics; then reopen through held descriptors and validate again. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:251-259; .planning/phases/05-authorized-execution-and-immutable-evidence/05-02-PLAN.md:237-241]
5. on an exact existing v2 set, perform descriptor-read validation and return the same canonical receipt with zero writes; on partial, occupied, divergent, symlink, path-escape, concurrency, or closure mismatch, fail closed without repair. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:596-613; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-21]

### Required formal values and claims

The formal v2 package must retain the following values verbatim: `"branch":"red"`, `"N_strict":0`, `"repeat_count":0`, `"expected_cells":0`, `"actual_cells":0`, `"cells":[]`, `"calls":[]`, and `"conditional_not_applicable_red_pending_phase7"` for both TS-11 and TS-12. It must have status `"completed"` only after every v2 binding validates. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-35; experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:259-266; 277-300]

The v2 receipt must grant only a literal `"downstream_red_evidence_evaluation_only"` scope (or an equivalent closed enum whose only members are Phase-6/Phase-7 Red evidence evaluation) and must not contain metrics, extraction-success, feasibility-conclusion, provider, model, network, credential, or external-publication authority. [ASSUMED: exact v2 receipt spelling; the existing v1 permission list is verbatim `["phase6_red_evidence_evaluation","phase7_red_evidence_evaluation"]` and forbids model authorization at experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:285-300]

## Frozen Hash Set and Human Gates

### Gate A — approve the v2 successor contract

This blocking human gate occurs after v2 code/tests/policy are committed and disposable-root tests pass, but before an execution may write any repository formal, attempt, or successor target. The review packet must bind:

- raw SHA-256 of `red-execution-policy-v2.json`, `red_v2.py`, `cli_v2.py`, `test_authorized_execution_v2.py`, every direct local dependency in the v2 closure, and every Phase-3/Phase-4 authority input;
- canonical SHA-256 of the sorted runtime-closure inventory, the sorted policy target inventory, the allowed-command/argument schema, and the forbidden-surface scan report;
- the exact v6 authority SHA-256 `363cf85c4088f5f268692f8319b70b50f7ed717f7145ed84a6923499ae992518`; and
- the verified absence of every v2 formal/attempt/successor target.

The decision is `approved` or `rejected` only; automation may validate it but cannot create it. It does not change Phase-4 authority or authorize any call beyond the exact v2 Red no-call run. [VERIFIED: experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:39-42]

### Gate B — confirm the final v2 publication closure

This separate blocking human gate occurs after all pre-publication tests and the final closure recomputation, immediately before one-way publication. It must display the Gate-A-to-final diff; any policy, command surface, output inventory, schema, authority binding, socket/no-call behavior, or hash mismatch is a rejection. Confirmation permits only one exact v2 publication; silence, test failure, or target occupancy permits none. This repeats the two-gate requirement recorded with the rejected final closure rather than treating the prior v1 approval as transferable. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-02-PLAN.md:180-216; .planning/STATE.md:167-168]

No H4/provider decision is required or allowed: the immutable v6 authority has `"h4_required":false` and all execution/provider/retrieval flags false. [VERIFIED: experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1]

## GSD Forward-Only Lifecycle Treatment

### Why records alone are insufficient

Do not create `05-02-SUMMARY.md`: a summary is the executor’s completion signal, while the old plan is rejected and Task 05-02-03 never ran. Do not create a summary for `05-03-PLAN.md` either: it audits a v1 root that must remain absent. [VERIFIED: GSD local workflow `execute-plan.md`:59-67; .planning/phases/05-authorized-execution-and-immutable-evidence/05-03-PLAN.md:99-103]

### Required administrative reconciliation before normal execution resumes

In one forward-only planning commit, preserve the old plan bytes under non-discoverable historical filenames (for example `05-02-PLAN.REJECTED.md` and `05-03-PLAN.SUPERSEDED.md`) and add a separate `05-02-CANCELLATION.md`. The cancellation record must bind `42733101`, `4d6d6edb`, `b5de8ce9`, the rejected checkpoint choice, the exact fact that Task 05-02-03 never ran, and the absence snapshot of every v1 protected target. It must say `status: rejected_not_completed`, `requirements_completed: []`, `formal_publication: false`, and name the future successor plans. [ASSUMED: proposed administrative record schema; the evidence it must bind is verified at .planning/STATE.md:167-168 and git show 42733101]

This rename-plus-record approach preserves historical content in Git, avoids falsely marking the plans successful, and removes the obsolete files from the executor’s `*-PLAN.md` discovery set. A cancellation note without the non-discoverable rename leaves the documented first-missing-summary selection and safe-resume stop in place. [VERIFIED: GSD local workflow `execute-plan.md`:59-67; `execute-phase.md`:178-187]

### Successor plan numbering and ordering

| Order | New plan | Purpose | Publication authority |
|---|---|---|---|
| 0 | administrative reconciliation (outside executor selection) | Preserve 05-02/05-03 as rejected/superseded history and add the cancellation record. | None. [ASSUMED: required workflow repair] |
| 1 | `05-04-PLAN.md` | TDD the v2 policy, exact `execute-red` CLI, full formal writer/validator, v2 path inventory, and no-call/zero-write tests in copied roots; conclude at Gate A. | No repository custody target. [ASSUMED: successor plan] |
| 2 | `05-05-PLAN.md` | Recompute the exact v2 closure, run the pinned gate, obtain Gate B, then invoke `execute-red` once against the repository v2 targets. | Gate B only. [ASSUMED: successor plan] |
| 3 | `05-06-PLAN.md` | Perform a fresh v2 read-only audit and exact-resume zero-write replay. This replaces, rather than edits, old 05-03. | No new authority; Phase 6/7 Red evidence evaluation only. [ASSUMED: successor plan] |

## Invariants and Threat List

| Invariant / threat | Required mitigation |
|---|---|
| v1 approval is misused for v2 bytes | Gate A and Gate B bind the v2 hash set; v6 remains input-only history. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:37-42] |
| Caller redirects output to an arbitrary path | Exact policy equality for every repository-relative CLI input/output; reject undeclared values before opening a writer. [ASSUMED: v2 command admission rule] |
| Missing receipt/report weakens the formal boundary | Treat formal root, receipt, and Markdown as one fixed prevalidated file set; no partial success state exists. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-21; .planning/phases/05-authorized-execution-and-immutable-evidence/05-02-PLAN.md:237-241] |
| Socket attempt is falsely reported as no call | All-socket guard records `"RED_SOCKET_DENIED"` only in failed-attempt `security_events`; completed ledger remains `"calls":[]`. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:227-240; 583-595] |
| Retry hides a failed attempt | Require a contiguous immutable ordered chain, empty ledger per attempt, and receipt binding of every prior attempt. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:409-443; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:39-42] |
| Symlink, traversal, partial, or concurrent write corrupts custody | Reuse `require_relative_posix_path` and descriptor-bound no-replace publication; fail closed with no cleanup/overwrite. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:29-39; 251-259] |
| New CLI/import bypasses static scan | Include CLI and all direct execution imports in the v2 closure; test a forbidden import/command and dynamic import/eval/exec rejection. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:188-224] |
| Red zeros become G/Y or conclusion claims | Closed receipt/matrix/report validators reject placeholders, metrics, extraction success, feasibility conclusions, and permanent TS-11/TS-12 closure. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:30-35] |

## Test and Validation Matrix

| Behavior | Required test / command | Expected result |
|---|---|---|
| Exact v2 CLI surface | Unit-test `build_parser()` and invoke copied-root `execute-red` with every required option; reject `execute-red-temporary`, unknown options, model/provider commands, absolute paths, and policy-path disagreement. [ASSUMED: v2 test] | No writer/no socket operation on rejection. |
| Formal atomic publication | In a copied root, run the real v2 command and assert the full v2 formal inventory, receipt, and report exist and are mutually hash-bound. [ASSUMED: v2 integration test] | `completed`; no v1 target is created. |
| Exact resume | Snapshot every v2 output byte and metadata, rerun the identical real command, and use a write observer. [ASSUMED: v2 replay test] | Same canonical receipt and zero writes. |
| Negative publication cases | Fault-inject partial/occupied/symlink/path-escape/concurrency/interruption and closure drift. [ASSUMED: v2 adversarial test] | No repair/overwrite; only complete v2 failed-attempt or decision-free v2 successor custody when applicable. |
| No-call closure | Exercise all socket constructors and loopback/LAN/external addresses in the real v2 execution body. [VERIFIED: experiments/specchoice-v1.3.2/tests/test_authorized_execution.py:123-155] | Stable denial, empty real-call ledger, no formal set. |
| Frozen semantics | Validate literal `"branch":"red"`, zero values, `"cells":[]`, empty ledger, and `"conditional_not_applicable_red_pending_phase7"`. [VERIFIED: experiments/specchoice-v1.3.2/tests/test_authorized_execution.py:79-100] | No metrics/placeholder/call. |
| Final pre-publication gate | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution tests.test_authorized_execution_v2 tests.test_treatments_h3 tests.test_canonical tests.test_filesystem_boundary -q && ../../.venv/bin/ruff check --isolated src/specchoice_execution tests/test_authorized_execution.py tests/test_authorized_execution_v2.py && git diff --check` [ASSUMED: v2 extension of the current validated command at .planning/phases/05-authorized-execution-and-immutable-evidence/05-VALIDATION.md:20-36] | Must pass under the pinned local Python/Ruff pair before Gate B. |
| Repository-wide release gate | `./bin/regress --all` [VERIFIED: AGENTS.md:26-49; 116-128] | Run when its configured environment is available; it does not replace the focused v2 no-call tests. |

## Don’t Hand-Roll

| Problem | Use | Do not build |
|---|---|---|
| Canonical bytes and hash binding | `specchoice_evidence.canonical` | A new JSON normalizer or hash implementation. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:40-50] |
| Relative-path/symlink/no-replace safety | `specchoice_evidence.filesystem` | A new path sanitizer or overwrite writer. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:29-39; 251-259] |
| Runtime closure | `specchoice_evidence.runtime_closure` | A second closure/inventory format. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py:187-256] |
| Strict JSON and diagnostics | `specchoice_measurement.strict_json` and `diagnostics` | Tolerant JSON parsing or unordered exception strings. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:26-27; 90-98] |
| v6 authority validation | `validate_h3_red_authority_v6` | A lookalike/red-only authority parser. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py:28-34; 162-184] |

## Non-goals

- Do not mutate `red-execution-policy-v1.json`, the v1 CLI contract, Phase-4 v6 authority, old 05-02/05-03 plan content, historical commits, or any v1 protected target. [VERIFIED: .planning/STATE.md:167-168; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:37-42]
- Do not create a provider/model adapter, credentials route, production retrieval, network access, subprocess path, model metric, extraction-success assertion, feasibility conclusion, public action, or Phase-7 requirement closure. [VERIFIED: .planning/REQUIREMENTS.md:78-88; 105-125; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-35]
- Do not publish formal/attempt/successor custody while researching, implementing v2, running disposable tests, or awaiting either human gate. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:37-42]
- Do not retrofit old 05-03 to audit a v2 root; preserve it as superseded historical planning and create 05-06 as the v2 audit successor. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-03-PLAN.md:83-103]

## Open Questions

None that block planning. The final v2 policy hash, closure hash, exact receipt enum spelling, and v2 target inventory must be generated by implementation and presented at Gate A; they must not be guessed or pre-authorized in this research. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-02-PLAN.md:205-210]

## Sources and Confidence

- **HIGH:** repository state, `42733101`, Phase-5 plans/context/summaries, current policy/CLI/execution/tests, Phase-4 v6 authority, and local GSD execution workflow were inspected in this session.
- **MEDIUM:** none; no external documentation was consulted because the successor is local-only and adds no package/service.
- **LOW / gated:** all v2 names, exact final v2 hash values, and proposed record schema are marked `[ASSUMED]` and require Gate A before becoming a locked interface.

**Research validity:** until the next change to the current Phase-5 source/policy, Phase-4 v6 authority, or GSD execution workflow.

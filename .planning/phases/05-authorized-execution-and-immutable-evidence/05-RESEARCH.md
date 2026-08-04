# Phase 5: Authorized Execution and Immutable Evidence - Research

**Researched:** 2026-08-04
**Domain:** local-only immutable execution evidence and no-call enforcement
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

### Red Execution Completion and Lifecycle

- **D-01:** A Phase 5 Red execution enters `completed` only when exact v6 authority validation, the immutable zero-entry call ledger, structural and runtime no-call proofs, preserved Red-trigger evidence, the zero-cell matrix, and the terminal receipt are complete and mutually bound. Missing material is blocking; `completed_with_warnings` is not a valid formal terminal state. — **Reversibility:** one-way — changing the completion contract after evidence publication requires a versioned successor evidence schema and complete revalidation.
- **D-02:** Re-executing identical frozen inputs must exactly resume byte-identical evidence with zero writes. Any mismatch fails closed and requires a versioned successor; evidence is never overwritten or silently regenerated in place.
- **D-03:** A failure before formal completion creates a separate immutable, non-authoritative attempt package. The formal Red evidence set is published only as a complete atomic file set; partial files cannot occupy the formal evidence boundary.
- **D-04:** `completed` grants only permission to evaluate the Red evidence in Phases 6 and 7. It does not authorize model calls, Green/Yellow execution, external publication, a final feasibility conclusion, or permanent closure of conditional Green/Yellow requirements.

### Zero-Call Ledger and No-Network Proof

- **D-05:** Zero-call proof is a three-layer closure bound to one attempt root: an authoritative zero-entry `model_call_ledger`, a structural scan proving provider/model/credentials/production-retrieval surfaces absent, and a runtime network tripwire. — **Reversibility:** one-way — weakening this proof after publication invalidates the evidence root and requires a successor run contract.
- **D-06:** Formal Red execution fails closed on every socket operation, including external, LAN, and loopback access. Any attempted socket creation or connection terminates the attempt and emits a stable diagnostic.
- **D-07:** The formal `model_call_ledger` represents real calls and must remain empty for completed Red evidence. Blocked socket or model-call attempts are recorded separately in the failed attempt's `security_events`; their presence prevents formal evidence publication without falsely claiming a real call occurred.
- **D-08:** Phase 5 must bind the Phase 4 v6 no-model root and independently rescan the actual Phase 5 execution closure, including CLI surfaces, imports, dependencies, configuration paths, and credential entry points. Both proof roots are bound into the attempt receipt.

### Zero-Cell A/B/C Matrix

- **D-09:** Red execution emits a canonical zero-cell matrix manifest with `branch=red`, `N_strict=0`, `repeat_count=0`, `expected_cells=0`, `actual_cells=0`, and `cells=[]`, bound to the exact v6 authority and Red trigger. It creates no N/A placeholder calls. — **Reversibility:** one-way — the manifest is part of the published evidence schema and changing its semantics requires a successor.
- **D-10:** TS-11 and TS-12 are recorded as `conditional_not_applicable_red_pending_phase7`. Phase 5 does not execute them and cannot permanently close them before Phase 7 validates the complete Red chain.
- **D-11:** The manifest proves absence of favorable-subset execution with `expected_cells = N_strict * 3 * repeat_count = 0`, treatment-partitioned A/B/C counts for expected, attempted, completed, failed, and retried cells all equal to zero, and a closure check showing no unregistered run or raw-response artifacts.
- **D-12:** Canonical JSON is the sole matrix authority. A deterministic Markdown projection may explain the Red trigger, zero-count formula, and conditional requirement state, but neither artifact may emit model metrics or claim extraction-experiment success.

### Drift, Failed Attempts, and Successors

- **D-13:** Any byte change in the frozen execution closure requires a versioned successor. The closure includes the v6 authority and bound roots, Phase 5 execution code, schemas, CLI allowlist, no-model policy, network policy, and evidence structure. A runtime fault with unchanged inputs creates a failed attempt and may be retried without a successor. — **Reversibility:** one-way — changed frozen bytes cannot inherit an authority issued for the predecessor root.
- **D-14:** Every drift or runtime failure preserves a complete failed-attempt package: attempt identity, frozen input inventory and hashes, expected/observed difference, stable diagnostics, termination stage, zero-call ledger, `security_events`, hashes and custody locations for any produced raw bytes, and explicit `authoritative=false` and `metrics_emitted=false` declarations.
- **D-15:** Tooling may construct a successor candidate, difference inventory, and readiness packet, but it cannot authorize the successor. Human approval of a new H3/Phase 5 binding chain is required. The v6 authority remains immutable historical authority and cannot authorize changed bytes.
- **D-16:** Every retry is a new immutable attempt. Failed attempts are never overwritten or deleted. Final successful evidence binds the complete ordered attempt sequence under the same execution root and proves every attempt's model-call ledger is empty; retries cannot change inputs or policy.

### the agent's Discretion

The planner may choose internal module names, CLI command names, schema decomposition, immutable attempt and evidence-directory names, additional stable diagnostic codes, the standard-library mechanism used for the socket tripwire, and the deterministic Markdown layout. These choices must reuse existing canonical JSON, strict parsing, descriptor-bound no-replace publication, exact-resume, runtime-closure, stable-diagnostic, and human-authority patterns. Do not add a dependency when the standard library or installed project code suffices.

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within the Red-only Phase 5 scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|---|---|---|
| TS-07 | The reviewer can audit at least one non-empty verbatim evidence span for every surfaced finding and inspect immutable raw outputs, parsed outputs, and parser diagnostics separately. | Preserve immutable upstream trigger/construction evidence by hash; keep any produced raw bytes, parsed records, diagnostics, security events, and the zero-call ledger as distinct leaves. Do not fabricate a model raw response or an N/A call for the zero-cell Red branch. [VERIFIED: .planning/REQUIREMENTS.md:33; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:118-121] |
| TS-11 | On an authorized G/Y branch, execute every preregistered strict-core A/B/C cell under identical frozen controls except treatment. | Record the requirement as `conditional_not_applicable_red_pending_phase7`; validate the frozen authority before any write and produce a zero-cell A/B/C matrix instead of executing a favorable subset. [VERIFIED: .planning/REQUIREMENTS.md:37; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:32-35] |
| TS-12 | On an authorized G/Y branch, retain complete per-call metadata, raw/parse/retry state, and no missing strict-core A/B/C cell. | Record the same conditional state; a completed Red chain proves zero real calls through the empty ledger, structural scan, all-socket tripwire, zero-cell matrix, and complete ordered attempt history. [VERIFIED: .planning/REQUIREMENTS.md:38; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:25-28; 39-42] |
</phase_requirements>

## Project Constraints (from AGENTS.md)

- Prefer the simplest mature solution: do not implement unnecessary behavior; reuse repository code before adding code; prefer the standard library, native capability, and installed dependencies before a new dependency. [VERIFIED: AGENTS.md:10-14]
- Keep the prototype isolated from core UDB schemas and generated data; Phase 5 artifacts stay inside `experiments/specchoice-v1.3.2/`. [VERIFIED: AGENTS.md:58-69; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:106-111]
- The repository is rapidly changing, so treat schemas and APIs as unstable and validate the current checked-out source before implementation. [VERIFIED: AGENTS.md:12-14]
- Follow the project validation rules: pre-commit runs formatting/schema checks, and the repository-wide release gate is `./bin/regress --all`. [VERIFIED: AGENTS.md:116-128]

## Summary

Phase 5 is a Red-only evidence lifecycle, not a model-execution integration. The current authority is the closed Phase 4 v6 record: `"branch":"red"`, `"N_strict":0`, `"repeat_count":0`, `"external_calls_authorized":false`, `"model_execution_authorized":false`, `"production_retrieval_authorized":false`, and `"provider_config_present":false`. These exact values must be re-derived through `validate_h3_red_authority_v6`, not accepted from an older authority or a self-reported copy. [VERIFIED: experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1; experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:3175-3195]

Implement one closed local execution surface that validates that authority and a Phase-5 frozen closure before it can stage any evidence. It must emit either (a) a full immutable Red package with an empty real-call ledger, zero-cell matrix, static no-surface audit, runtime socket-denial proof, preserved trigger evidence, and terminal receipt, or (b) a separate immutable failed-attempt package. Existing canonical serialization, descriptor-bound file-set publication, strict parsing, diagnostics ordering, runtime-closure validation, and H3 v6 validation cover the difficult primitives; no package installation is warranted. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-42; experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:40-50; experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:251-259; experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py:187-226]

The prior frozen baseline outside the repository is absent and must not be recreated or inferred. Treat the repository-local v6 chain as the only input authority until an exact-byte successor decision says otherwise. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:80-82]

**Primary recommendation:** Build a small standard-library-only `specchoice_execution` boundary [ASSUMED] that validates the exact v6 authority and frozen closure, runs wholly under an all-socket tripwire, and publishes only self-validating, descriptor-bound canonical evidence packages.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| H3/v6 authority admission | API / Backend | Database / Storage | Local execution code must recompute and validate the persisted authority before evidence construction; a client does not own this authorization. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:3175-3195] |
| Frozen execution closure and drift detection | API / Backend | Database / Storage | Code hashes a finite, repository-relative input inventory before a writer opens outputs. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py:187-226; 229-256] |
| Immutable attempt and terminal-evidence custody | Database / Storage | API / Backend | Descriptor-rooted no-replace publication owns path traversal, leaf creation, and postflight evidence; orchestration only supplies canonical bytes. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:198-234; 251-259] |
| Zero-call and zero-cell proof | API / Backend | Database / Storage | The execution layer builds the ledger/audits/matrix and the storage layer binds their hashes in the attempt receipt. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:25-35] |
| Human interpretation in later phases | — | API / Backend | A completed package permits Phase 6/7 evidence evaluation only; it cannot select a broader execution branch. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:21; 42] |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---|---|---|---|
| Python standard library | Python `>=3.12` project contract | Canonical evidence orchestration, JSON, hashing, AST audit, socket tripwire, and `unittest`. | The experiment workspace already declares a standard-library-first boundary, and H3 already uses `argparse`, `ast`, `contextlib`, `io`, and `pathlib`. [VERIFIED: pyproject.toml:4-20; experiments/specchoice-v1.3.2/README.md:1-7; experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:6-11] |
| `specchoice_evidence.canonical` | repository-local | Canonical UTF-8/LF JSON and SHA-256. | `canonical_json_bytes` deterministically encodes sorted-key JSON with a trailing LF, while `sha256_bytes` hashes raw bytes. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:40-50] |
| `specchoice_evidence.filesystem` | repository-local | Descriptor-bound authoritative reads and exact no-replace file-set publication. | The implementation preflights and postflights one held authority root and rejects unsafe path forms. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:29-39; 251-259] |
| `specchoice_evidence.runtime_closure` | repository-local | Sorted finite inventory, exact-byte verification, and target-occupancy preflight. | Its verified closure APIs distinguish frozen inputs from future outputs and fail on mismatch/occupied targets. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py:187-226; 229-256] |
| `specchoice_treatments.h3` | repository-local | Exact Phase 4 v6 authority and no-model-root validation. | The v6 validator rebuilds the expected authority from persisted decision bytes and rejects any unequal object. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:3175-3195] |

### Supporting

| Library | Version | Purpose | When to Use |
|---|---|---|---|
| `specchoice_measurement.strict_json` | repository-local | Duplicate-key rejection and closed JSON validation. | Reuse for every Phase 5 input schema and machine-readable receipt/audit validator. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/strict_json.py:32-52; 69-89] |
| `specchoice_measurement.diagnostics` | repository-local | Stable `Diagnostic` shape and deterministic ordering. | Use for frozen-input drift, forbidden surface, socket tripwire, and publication failure diagnostics. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/diagnostics.py:10-48] |
| `unittest` | Python standard library | Unit, custody, and adversarial tests. | Existing phase tests run with `PYTHONPATH=src` and do not require a Phase 5 framework install. [VERIFIED: .planning/phases/04-offline-treatments-retrieval-and-branch-freeze/04-VALIDATION.md:22-25; 61-64] |
| Ruff | `0.16.0` pinned in project dev group | Lint the new execution package and its test module. | The repository declares the pinned dev-tool version and lint configuration. [VERIFIED: pyproject.toml:15-24] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|---|---|---|
| Repository-local standard-library boundary | Provider SDK, HTTP client, model adapter, credentials loader, or production retrieval client | Prohibited by the locked Red authority and would invalidate the no-call structural proof. [VERIFIED: experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:9; 25-28] |
| Descriptor-bound publication | A custom temp-directory/rename publisher | The existing descriptor layer already handles path escape, symlink rejection, exclusive creation, fsync, and cross-leaf postflight; duplicating it adds custody risk. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:29-39; 198-234; 251-259] |
| New closed Phase 5 attempt schema | Direct reuse of `specchoice_measurement.attempts.run_measurement_attempt` | The Phase 2 writer permits a `"completed_with_warnings"` role/status and deletes staging on failure; D-01/D-03/D-14 instead require no formal warning terminal state and preserved failed attempts. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/attempts.py:72-79; 168-241; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-20; 39-42] |

**Installation:** None. Do not add a package. [VERIFIED: experiments/specchoice-v1.3.2/README.md:3-7; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:44-46]

## Package Legitimacy Audit

No external package is proposed or installed in this phase, so the package-legitimacy gate is not applicable. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:44-46]

## Architecture Patterns

### System Architecture Diagram

```text
Persisted Phase 4 v6 authority + bound decision/readiness/no-model roots
                                  |
                                  v
                  [exact authority + closure validation]
                                  |
                    drift / malformed / forbidden surface
                         |                         |
                         v                         v
       [immutable failed attempt package]   [all-socket tripwire]
                         |                         |
                         +-----------+-------------+
                                     |
                                     v
    [Red-only evidence constructor: empty real-call ledger + static scan
      + runtime proof + preserved trigger evidence + zero-cell A/B/C matrix]
                                     |
                             self-validate all hashes
                                     |
                                     v
             [descriptor-bound full file-set publication / exact resume]
                                     |
                                     v
          [terminal receipt: ordered attempt chain + Phase 6/7-only permission]
```

The diagram is the required one-way flow: no provider/model/retrieval branch exists after authority admission. The formal package is available only after all required evidence leaves validate; a failed attempt never occupies that formal boundary. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-28; 39-42]

### Recommended Project Structure

```text
experiments/specchoice-v1.3.2/
├── src/specchoice_execution/       # [ASSUMED] Red-only authority, closure, ledger, matrix, and receipt code
├── config/execution/               # [ASSUMED] closed canonical Phase 5 schemas/policy declaration
├── runs/red-attempts/              # [ASSUMED] append-only failed and completed attempt packages
├── reports/red-execution/          # [ASSUMED] deterministic non-authoritative Markdown projection
├── receipts/                       # existing canonical receipt namespace
└── tests/test_authorized_execution.py # [ASSUMED] unit/integration/adversarial Phase 5 coverage
```

All proposed paths are repository-relative and subject to the phase's frozen-closure/target-occupancy schema; the names are discretionary, not pre-existing interfaces. [ASSUMED]

### Pattern 1: Validate Before Any Write, Then Self-Validate Before Publication

**What:** Read the persisted v6 authority through its validator, recompute the Phase 5 closure, inspect expected output occupancy, construct every output in memory, validate all closed schemas and hashes, then publish the complete canonical file set with the existing no-replace primitive. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:3175-3195; experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py:229-256; experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:251-259]

**When to use:** Every formal evidence attempt and terminal receipt. An exact rerun reads/validates existing canonical bytes and returns without writes; a byte mismatch fails closed. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:19-20; experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:3241-3258]

**Example:**

```python
# Source: repository-local canonical and filesystem primitives
payload_bytes = canonical_json_bytes(payload)
payload_sha256 = sha256_bytes(payload_bytes)
write_exact_descriptor_files(root, payloads)
```

`canonical_json_bytes` and `sha256_bytes` are existing functions; `write_exact_descriptor_files` is the repository's exact descriptor-rooted publisher. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:40-50; experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:251-259]

### Pattern 2: Separate Formal Completion from Failed-Attempt Custody

**What:** Create a fresh immutable failed-attempt package for every fault (including tripwire failure, authority/closure drift, or partial publication). A successful package must bind the sorted full attempt sequence and contain no `completed_with_warnings` terminal state. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-20; 39-42]

**When to use:** Any pre-completion exception. Never erase, overwrite, or reclassify a previous failed attempt. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:20; 40-42]

### Pattern 3: Three-Layer Absence Proof

**What:** Bind three independent facts into the same attempt root: an empty real-call ledger, a current source/CLI/dependency/config/credential surface scan, and a runtime all-socket tripwire. Blocked operations are security events in the failed package, never ledger entries. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:25-28]

**When to use:** The only formal Red branch. The static scan must include the newly introduced Phase 5 modules and CLI, not merely reuse the Phase 4 report. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:28]

**Implementation note:** Use an in-process standard-library test/context guard that denies `socket.socket`, `socket.create_connection`, `socket.create_server`, `socket.socketpair`, and `socket.fromfd`, and prohibit process-spawning/network imports in the audited closure. This is an implementation recommendation that must be proven by focused adversarial tests before formal use. [ASSUMED]

### Anti-Patterns to Avoid

- **Treating the Phase 4 v6 report as sufficient runtime proof:** It audits the Phase 4 treatment closure, while D-08 requires a fresh Phase 5 closure scan and binds both roots. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:28; experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:2958-2985]
- **Writing a partial formal package, then repairing it:** Formal evidence must be an exact complete atomic file set; faults create a distinct non-authoritative package. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:20; 40]
- **Inventing a no-op A/B/C call or raw response:** Red must have `cells=[]` and no N/A placeholder calls; fabricated call artifacts would make the ledger untruthful. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:32-35]
- **Reusing Phase 2 warning/cleanup semantics:** Its general attempt writer supports a warning terminal role and removes a temporary directory on errors, which conflicts with required failed-attempt preservation. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/attempts.py:72-79; 168-241]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---|---|---|---|
| Canonical JSON and digest calculation | A second JSON normalizer or hash wrapper | `specchoice_evidence.canonical` | It already specifies NFC/LF normalization, sorted compact UTF-8 JSON, trailing LF, and raw-byte SHA-256. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:24-50] |
| Authoritative file writes/reads | `Path.write_bytes`, rename-only publication, or a new symlink checker | `specchoice_evidence.filesystem` | Existing code rejects escape syntax/symlinks and publishes exact no-replace payloads through held descriptors. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:29-39; 198-234; 251-259] |
| Exact frozen-input and future-output checks | An ad hoc file hashing loop | `build_runtime_closure`, `verify_runtime_closure`, and `validate_v6_preflight_inventory` patterns | Existing code specifies sorted finite input evidence and target-occupancy rejection. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py:187-256] |
| Phase 4 authority interpretation | A new parser for `branch-authority-v6.json` | `validate_h3_red_authority_v6` with the persisted decision/readiness roots | The validator enforces the closed key set and reconstructs the expected authority from persisted decision bytes. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:2741-2777; 3175-3195] |
| Closed evidence-input parsing and ordered diagnostics | Loose `json.loads` and unordered exception text | `strict_json` and `diagnostics` | Existing primitives reject duplicate keys and define a stable diagnostic ordering. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/strict_json.py:32-52; experiments/specchoice-v1.3.2/src/specchoice_measurement/diagnostics.py:10-48] |

**Key insight:** Phase 5 needs a new *schema*, not new low-level custody mechanics. Reusing existing primitives while defining a narrow Red-specific state machine prevents the obsolete measurement attempt contract from weakening the new formal boundary. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:44-46; experiments/specchoice-v1.3.2/src/specchoice_measurement/attempts.py:72-79; 168-241]

## Common Pitfalls

### Pitfall 1: Accepting a Merely Similar Authority

**What goes wrong:** A planner reads an older v1–v5 artifact, a copy of the v6 JSON, or an unvalidated object and treats it as current authority.
**Why it happens:** The repository deliberately preserves historical predecessor and failed-publication evidence.
**How to avoid:** Require the persisted v6 decision/readiness/authority bytes, call the v6 validator, and reject any non-exact object before staging.
**Warning signs:** Missing/unknown authority keys, a different self-hash, or any v1–v5 fallback. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:2740-2777; 3175-3195; .planning/phases/04-offline-treatments-retrieval-and-branch-freeze/04-VERIFICATION.md:36-41]

### Pitfall 2: Calling the Ledger Empty While Leaving a Reachable Network Path

**What goes wrong:** A zero-row ledger alone cannot prove that the code lacked a provider/model/credential/retrieval surface or that runtime socket creation would stop.
**Why it happens:** Phase 4's current audit checks a different source/CLI closure and tests a patched `socket.create_connection` only around its own audit.
**How to avoid:** Rescan all Phase 5 execution files and CLI surfaces, reject forbidden imports/config paths, and add a dedicated all-socket tripwire test suite.
**Warning signs:** New network-related import, CLI subcommand, provider/config/credential path, process spawn, or a tripwire event. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:25-28; experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:268-387; experiments/specchoice-v1.3.2/tests/test_treatments_h3.py:143-153]

### Pitfall 3: Hiding a Failed Retry in Staging Cleanup

**What goes wrong:** An exception removes evidence of the first attempt and a later successful execution appears as the only history.
**Why it happens:** The legacy measurement writer deletes its temporary directory in its exception handler.
**How to avoid:** Persist a self-validating failed package to an immutable attempt identifier before returning a stable failure; bind every prior attempt into the terminal receipt.
**Warning signs:** No failed-attempt artifact after a fault, a reused attempt ID, or a terminal receipt that lists only the final attempt. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/attempts.py:212-241; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:39-42]

### Pitfall 4: Treating Zero Cells as Requirement Closure

**What goes wrong:** TS-11/TS-12 are marked permanently complete, or a fake placeholder call is emitted to make a matrix look populated.
**Why it happens:** Green/Yellow call-matrix expectations are mistaken for Red's evidence-only branch.
**How to avoid:** Emit the canonical empty matrix and machine-readable conditional state, retain no raw response/call artifacts, and defer permanent closure to Phase 7.
**Warning signs:** `actual_cells` nonzero, a raw response leaf, a model metric, or a status other than the locked conditional state. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:32-35]

### Pitfall 5: Using an unpinned local toolchain as the phase gate

**What goes wrong:** Local validation is claimed green under a runtime different from the repository's declared contract.
**Why it happens:** The current shell exposes Python 3.11.14 and Ruff 0.12.0, while the project declares Python `>=3.12` and Ruff `0.16.0`.
**How to avoid:** Restore/use the repository-pinned toolchain before Phase 5 validation; do not downgrade the gate to match the ambient shell.
**Warning signs:** `python3 --version` below 3.12 or `ruff --version` below 0.16.0. [VERIFIED: environment audit 2026-08-04; pyproject.toml:4-20]

## Code Examples

Verified patterns from repository-local sources:

### Canonical, Descriptor-Bound Publication

```python
# Source: experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py
#         experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py
evidence_bytes = canonical_json_bytes(evidence)
evidence_sha256 = sha256_bytes(evidence_bytes)
write_exact_descriptor_files(root, payloads)
```

This pattern uses only repository-owned canonical bytes and the existing no-replace publisher. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:40-50; experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:251-259]

### Exact v6 Authority Admission

```python
# Source: experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py
validated_authority = validate_h3_red_authority_v6(
    authority=authority,
    freeze_inputs=freeze_inputs,
    packet=packet,
    readiness=readiness,
    decision_raw=decision_raw,
)
```

The existing validator checks the exact declared key set, the v6 schema version, the self-hash, and equality with the authority reconstructed from persisted decision bytes. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:3175-3195]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|---|---|---|---|
| Phase 4 v5 authority publication | Phase 4 v6 closed authority contract | v6 lifecycle successor | v5 is immutable failed-publication history, while v6 is the only current Red authority Phase 5 may consume. [VERIFIED: experiments/specchoice-v1.3.2/phase4/h3-v6-lifecycle-contract.md:3-20; .planning/phases/04-offline-treatments-retrieval-and-branch-freeze/04-VERIFICATION.md:36-41] |
| Generic Phase 2 measurement attempt | Red-specific immutable no-call attempt chain | Phase 5 planned | Generic attempts support measurement roles and cleanup semantics that do not meet the locked Red formal-completion and failed-custody contract. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/attempts.py:72-79; 168-241; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-20; 39-42] |

**Deprecated/outdated:** Treating any Phase 4 v1–v5 leaf as execution authority is prohibited; the preserved history remains audit evidence only. [VERIFIED: .planning/phases/04-offline-treatments-retrieval-and-branch-freeze/04-VERIFICATION.md:36-41]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|---|---|---|
| A1 | The new Red-only implementation package can be named `specchoice_execution` and the suggested relative output layout can be adopted. | Summary; Recommended Project Structure | Names may conflict with an existing planned interface; planner must select the final names and include them in the frozen closure. |
| A2 | An in-process guard that patches all listed standard-library socket constructors, combined with a no-process-spawn static audit, is sufficient for the stated runtime tripwire. | Pattern 3 | Incomplete interception would leave an unauthorized network route; adversarial tests and a human security review must validate the selected mechanism. |

## Open Questions

1. **Pinned validation runtime is unavailable in the current shell.**
   - What we know: The project requires Python `>=3.12` and pins Ruff `0.16.0`; the ambient shell reports Python 3.11.14 and Ruff 0.12.0. [VERIFIED: pyproject.toml:4-20; environment audit 2026-08-04]
   - What's unclear: Whether the repository's intended `uv`/setup environment can be restored locally without violating the no-network execution boundary.
   - Recommendation: Make restoration of the pinned local developer toolchain a Wave 0/pre-execution prerequisite. Do not let the implementation run a package installation, network call, or model call as part of Phase 5 evidence construction. [VERIFIED: AGENTS.md:16-22; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:9]

2. **Socket-tripwire coverage must be proven, not assumed.**
   - What we know: The previous test patches `socket.create_connection` and asserts it is unused; D-06 raises the contract to every socket operation. [VERIFIED: experiments/specchoice-v1.3.2/tests/test_treatments_h3.py:143-153; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:25-27]
   - What's unclear: The final standard-library-only hook set and exact stable diagnostic names.
   - Recommendation: Select them in the first implementation plan, add one adversarial test per denied constructor plus loopback/LAN/external address cases, and freeze the resulting policy into the closure. [ASSUMED]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|---|---|---|---|---|
| Python | Phase 5 execution/tests | ✗ wrong version in ambient shell | 3.11.14; project requires `>=3.12` | Restore repository-pinned toolchain before execution. [VERIFIED: environment audit 2026-08-04; pyproject.toml:4-8] |
| Ruff | Phase lint gate | ✗ wrong version in ambient shell | 0.12.0; project pins `0.16.0` | Restore pinned development toolchain; do not lower the lint gate. [VERIFIED: environment audit 2026-08-04; pyproject.toml:15-24] |
| Git | frozen identity/custody commands | ✓ | 2.54.0 | — [VERIFIED: environment audit 2026-08-04] |
| External model/provider/network | Formal Red evidence | Deliberately unavailable | — | No fallback; its absence is what the package proves. [VERIFIED: experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:25-28] |

**Missing dependencies with no fallback:**

- The pinned Python/Ruff validation toolchain is absent from the ambient shell. The planner must include a non-evidence prerequisite or explicitly pause before Phase 5 execution. [VERIFIED: environment audit 2026-08-04; pyproject.toml:4-20]

**Missing dependencies with fallback:**

- None. [VERIFIED: environment audit 2026-08-04]

## Validation Architecture

### Test Framework

| Property | Value |
|---|---|
| Framework | Python standard-library `unittest`; repository project contract Python `>=3.12`. [VERIFIED: .planning/phases/04-offline-treatments-retrieval-and-branch-freeze/04-VALIDATION.md:22-25; pyproject.toml:4-8] |
| Config file | `pyproject.toml` for Ruff; no unittest config, tests use `PYTHONPATH=src`. [VERIFIED: pyproject.toml:22-24; .planning/phases/04-offline-treatments-retrieval-and-branch-freeze/04-VALIDATION.md:22-25] |
| Quick run command | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_authorized_execution tests.test_treatments_h3 tests.test_canonical tests.test_filesystem_boundary -q` [ASSUMED] |
| Full suite command | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_data_admission tests.test_data_splits tests.test_data_relevance tests.test_data_h2 tests.test_treatments_frame tests.test_treatments_prompts tests.test_treatments_retrieval tests.test_treatments_h3 tests.test_authorized_execution tests.test_canonical tests.test_filesystem_boundary -q && ruff check --isolated src/specchoice_execution tests/test_authorized_execution.py && git diff --check` [ASSUMED] |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|---|---|---|---|---|
| TS-07 | Separate raw-byte custody (when produced), parsed output, diagnostics, security events, immutable trigger evidence, and no fabricated raw response in a zero-call attempt. | unit/integration/adversarial | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_authorized_execution -q` [ASSUMED] | ❌ Wave 0 |
| TS-11 | Exact v6 Red admission produces `expected_cells=0`, `actual_cells=0`, no placeholder cell, and conditional Phase-7 requirement status. | unit/integration | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_authorized_execution tests.test_treatments_h3 -q` [ASSUMED] | ❌ Wave 0 |
| TS-12 | Empty real-call ledger, structural scan, all-socket tripwire, blocked-event failed custody, and complete ordered retry chain fail closed. | security/runtime/adversarial | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_authorized_execution tests.test_filesystem_boundary -q` [ASSUMED] | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** Run the new execution test module plus `tests.test_canonical`, `tests.test_filesystem_boundary`, and the relevant H3 v6 authority test. [ASSUMED]
- **Per wave merge:** Run the full command above only after the pinned Python/Ruff toolchain is available. [ASSUMED]
- **Phase gate:** Full suite, pinned Ruff, `git diff --check`, exact-resume/no-write check, and required human review must be green before Phase 6 consumes the root. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-21; AGENTS.md:116-128]

### Wave 0 Gaps

- [ ] `experiments/specchoice-v1.3.2/tests/test_authorized_execution.py` — authority/closure admission, zero ledger/matrix, receipt, failed-custody, resume, drift, and tripwire coverage. [ASSUMED]
- [ ] Final selected Phase 5 module/schema names and their inclusion in the closure inventory. [ASSUMED]
- [ ] Repository-pinned Python/Ruff developer toolchain. [VERIFIED: environment audit 2026-08-04; pyproject.toml:4-20]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---|---|---|
| V2 Authentication | no | No service, user login, or remote API is in the Red-only execution boundary. [VERIFIED: experiments/specchoice-v1.3.2/README.md:3-7; experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1] |
| V3 Session Management | no | No session/cookie/remote process exists in the allowed execution surface. [VERIFIED: experiments/specchoice-v1.3.2/README.md:3-7; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:9] |
| V4 Access Control | yes | Exact persisted H3 v6 authority validation is the capability gate; `completed` cannot authorize a broader branch. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:3175-3195; .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:21] |
| V5 Input Validation | yes | Closed schemas, duplicate-key rejection, exact authority reconstruction, relative-path validation, and closure-byte checks fail closed. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/strict_json.py:32-89; experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:29-39; experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py:203-226] |
| V6 Cryptography | yes | Reuse canonical raw-byte SHA-256 bindings; do not implement custom hashes. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:40-50] |

### Known Threat Patterns for the Stack

| Pattern | STRIDE | Standard Mitigation |
|---|---|---|
| Older or altered authority presented as current | Elevation of Privilege / Tampering | Validate exact v6 persisted decision/readiness/authority roots and reject object inequality. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:3175-3195] |
| Provider/model/credential/retrieval surface introduced | Elevation of Privilege / Information Disclosure | Fresh static closure scan plus all-socket runtime tripwire; no dependency or CLI expansion. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:25-28] |
| Network attempt represented as no call | Repudiation / Tampering | Keep the real-call ledger empty only for completed evidence; record blocked events separately in a failed package. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:26-28; 40] |
| Symlink/path substitution or partial evidence publish | Tampering | Descriptor-rooted path checks and exact no-replace full file-set publication. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:29-39; 198-234; 251-259] |
| Favorable-subset or hidden-retry selection | Repudiation / Tampering | Canonical zero-cell A/B/C matrix, closure check for raw/run artifacts, and terminal binding of every ordered attempt. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:32-35; 42] |

## Sources

### Primary (HIGH confidence)

- `experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json` — current exact Red authority values. [VERIFIED: experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1]
- `experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py` — v6 authority construction/validation and historical-state handling. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:2740-2777; 2854-2955; 3175-3309]
- `experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py`, `filesystem.py`, and `runtime_closure.py` — canonical bytes, descriptor custody, and closure/target-preflight primitives. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:40-50; experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py:251-259; experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py:187-256]
- `.planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md` — locked Phase 5 Red lifecycle, no-call proof, matrix, retry, and scope decisions. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-46]
- `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` — TS-07/TS-11/TS-12 and Phase 5 success criteria. [VERIFIED: .planning/REQUIREMENTS.md:33-38; .planning/ROADMAP.md:285-306]

### Secondary (MEDIUM confidence)

- None; no external documentation was consulted because this locked, local-only phase introduces no external library or service surface. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:9; 44-46]

### Tertiary (LOW confidence)

- Proposed module/output names and final all-socket patch set are explicitly listed in the Assumptions Log. [ASSUMED]

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — no new dependency is required; existing local primitives and the project manifest define the implementation boundary. [VERIFIED: experiments/specchoice-v1.3.2/README.md:3-7; pyproject.toml:4-24]
- Architecture: HIGH — locked Context plus direct source inspection identifies the exact authority, canonicalization, filesystem, closure, parser, and diagnostics seams. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:89-111; experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py:3175-3195]
- Pitfalls: HIGH — they follow from explicit formal-completion/no-call/retry constraints and the direct comparison with the legacy attempt writer. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md:18-42; experiments/specchoice-v1.3.2/src/specchoice_measurement/attempts.py:168-241]

**Research date:** 2026-08-04
**Valid until:** 2026-09-03, unless the v6 authority, Phase 5 Context, or toolchain contract changes first. [VERIFIED: experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1; pyproject.toml:4-20]

# Phase 5: Authorized Execution and Immutable Evidence - Context

**Gathered:** 2026-08-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 5 consumes only the verified Phase 4 v6 `approved_red` authority and closes the local Red execution-evidence lifecycle without making a real model call. It produces an immutable, exactly resumable Red attempt chain, a machine-verifiable zero-entry model-call ledger, fresh structural and runtime no-network evidence, a canonical zero-cell A/B/C manifest, separate failed-attempt custody, and a terminal receipt that binds the complete evidence set. This phase does not create a provider/model adapter, credentials path, production retrieval surface, Green/Yellow execution, model metrics, external publication, or final feasibility conclusion. Phase 5 completion authorizes only downstream Red evidence evaluation in Phases 6 and 7.

</domain>

<decisions>
## Implementation Decisions

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

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase Scope and Requirements

- `.planning/PROJECT.md` — Defines the evaluation-first scope, Red as a valid feasibility path, human authority, isolation boundary, and prohibited external/upstream expansion.
- `.planning/REQUIREMENTS.md` — Defines Phase 5 requirements TS-07, TS-11, and TS-12, the ALL versus G/Y path contract, immutable raw/parsed/diagnostic separation, and frozen-input change control.
- `.planning/ROADMAP.md` — Defines the Phase 5 goal, Red vertical increment, human checkpoint, success criteria, and three planned capability increments.

### Current Red Authority

- `.planning/phases/04-offline-treatments-retrieval-and-branch-freeze/04-CONTEXT.md` — Locks Red-only execution, zero counts, H4 absence, no provider/model/credentials surface, and Phase 5 consumption boundaries.
- `.planning/phases/04-offline-treatments-retrieval-and-branch-freeze/04-VERIFICATION.md` — Verifies Phase 4 closure on the v6 Red authority and states that Phase 5 may consume only that no-call authority.
- `experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json` — Current canonical authority: `branch=red`, `N_strict=0`, `repeat_count=0`, H4 not required, and all model, external-call, provider, credentials, and production-retrieval permissions false or not applicable.
- `experiments/specchoice-v1.3.2/phase4/h3-v6-lifecycle-contract.md` — Defines the v6 exact authority schema, predecessor history, descriptor-re-read publication state machine, exact-resume behavior, and fail-closed drift conditions.
- `experiments/specchoice-v1.3.2/reports/h3/h3-red-review-v6/review-packet.json` — Decision-free v6 Red packet bound by the current authority.
- `experiments/specchoice-v1.3.2/receipts/h3-branch-readiness-v6.json` — Exact v6 readiness identity approved by the human H3 decision.
- `experiments/specchoice-v1.3.2/reviews/h3-branch-decision-v6.json` — Human `approved_red` decision whose persisted bytes and self-hash are bound by the v6 authority.

### Inherited Evidence Contracts

- `experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py` — Canonical UTF-8/LF JSON and SHA-256 primitives.
- `experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py` — Descriptor-rooted, durable no-replace file-set publication and exact-resume verification.
- `experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py` — Frozen runtime inventory, exact-byte verification, future-target occupancy, and lifecycle successor patterns.
- `experiments/specchoice-v1.3.2/src/specchoice_measurement/strict_json.py` — Duplicate-key rejection, closed-schema parsing, and exact verbatim evidence-span checks.
- `experiments/specchoice-v1.3.2/src/specchoice_measurement/diagnostics.py` — Stable structured diagnostics and deterministic ordering.
- `experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py` — Current Red authority validation, no-model reachability inventory, and descriptor-bound publication patterns.

### Known Unavailable Historical Reference

- `../../Downloads/LFX_RISCV_SpecChoice_v1.3.2_frozen_execution_baseline.md` — Previously cited as the external frozen execution contract but absent on 2026-08-04. Do not reconstruct or guess its contents. Planning must rely on the repository-local, verified v6 authority chain above unless the exact external bytes are restored and independently bound by a successor decision.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `specchoice_evidence.canonical`: Reuse canonical serialization and hash validation for attempt roots, ledgers, matrix manifests, receipts, and projections.
- `specchoice_evidence.filesystem`: Reuse descriptor-bound exact file-set publication so complete evidence publishes atomically and exact reruns perform zero writes.
- `specchoice_evidence.runtime_closure`: Reuse finite inventory and exact-byte verification patterns for the Phase 5 frozen execution closure and successor boundary.
- `specchoice_measurement.strict_json` and `specchoice_measurement.diagnostics`: Reuse closed schemas, duplicate rejection, raw-byte evidence-span validation, and deterministic diagnostics.
- `specchoice_treatments.h3`: Reuse the current v6 authority validator, no-model reachability inventory, predecessor bindings, and human-decision separation.

### Established Patterns

- Canonical JSON is authoritative; Markdown is a deterministic, non-authoritative projection.
- Machine readiness and human decisions remain separate and content-bound.
- Immutable attempts and versioned successors replace in-place repair or overwrite.
- Failed and historical attempts remain auditable but never become current authority implicitly.
- Raw bytes, parsed structures, diagnostics, security events, ledgers, and aggregate receipts remain separate one-way evidence layers connected by exact hashes.
- The prototype remains standard-library-first and isolated under `experiments/specchoice-v1.3.2/`.

### Integration Points

- Phase 5 implementation, schemas, CLI, tests, attempts, ledgers, matrices, receipts, reports, and projections remain under `experiments/specchoice-v1.3.2/`.
- Admission starts by validating the persisted `phase4/branch-authority-v6.json` and its exact decision/readiness/no-model roots; historical v1-v5 artifacts cannot be fallback authority.
- The formal execution surface is Red-only. It may verify and materialize no-call evidence but must expose no provider, model, credentials, production retrieval, or external network path.
- Phase 5 outputs feed Phase 6 and Phase 7 only through the completed immutable Red evidence root and its complete attempt history.

</code_context>

<specifics>
## Specific Ideas

- Treat absence as positive evidence: use a closed zero-entry call ledger, fresh structural scan, runtime all-socket tripwire, and zero-cell matrix rather than merely omitting run files.
- Keep blocked call attempts in `security_events`, separate from the real-call ledger, so the record is both truthful and fail-closed.
- Make conditional requirement status explicit and machine-readable: `conditional_not_applicable_red_pending_phase7`.
- Bind all failed and retried attempts into the final ordered attempt chain so a convenient final run cannot hide earlier behavior.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within the Red-only Phase 5 scope.

</deferred>

---

*Phase: 05-authorized-execution-and-immutable-evidence*
*Context gathered: 2026-08-04*

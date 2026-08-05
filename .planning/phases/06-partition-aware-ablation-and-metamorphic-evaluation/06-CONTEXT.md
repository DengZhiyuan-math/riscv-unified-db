# Phase 6: Partition-Aware Ablation and Metamorphic Evaluation - Context

**Gathered:** 2026-08-05
**Status:** Context complete; planning and execution gated on verified Phase 5 closure

<domain>
## Phase Boundary

Phase 6 evaluates the exact frozen branch at case level without pooling authority domains, partitions, treatments, repeats, or denominators. On the current Red path, it combines two independently bound tracks: the Phase 2 deterministic measurement evidence required by TS-06 and the completed Phase 5 Red execution/construction evidence. It produces branch-first applicability accounting, closed case joins, partition population manifests, independent metrics, warning and failure ledgers, construction-feasibility audit, and a human-reviewed evaluation package. It does not create model calls, Green/Yellow observations, placeholder cases, post-hoc gold or threshold changes, a combined headline score, the final Phase 7 feasibility narrative, or external publication authority.

Phase 6 may not be planned as executable work or treated as ready to run until Phase 5 has a passed verification artifact and canonical lifecycle closure. Existing Phase 5 formal evidence is an input candidate, not sufficient proof of current phase completion while the roadmap remains 4/5 and Phase 5 has no verification closure.

</domain>

<decisions>
## Implementation Decisions

### Red Metric Representation

- **D-01:** Keep every Green/Yellow-only metric ID visible on Red with `applicability=not_applicable_red`, a stable reason, and exact authority bindings. Omit numerator, denominator, and score for these metrics. Partition population counts are recorded separately. — **Reversibility:** one-way — changing applicability semantics after publication would alter the machine-readable evaluation contract and every downstream Phase 7 interpretation.
- **D-02:** Keep `deterministic_measurement` and `red_execution_evidence` as independent authority namespaces. The former binds Phase 2 case-level measurement authority; the latter binds Phase 5 zero-call, zero-cell, and construction-feasibility evidence. Their denominators and results must never be pooled or reduced to a combined headline score.
- **D-03:** Use exactly four result states: `measured`, `empty_population`, `not_applicable_red`, and `invalid_withheld`. Only `measured` may carry a score. `empty_population` may carry population counts but no ratio. `invalid_withheld` requires blocking diagnostics and emits no metric.
- **D-04:** Lead the reviewer-facing package with the Red authority, `N_strict=0`, `repeat_count=0`, and the verified no-model-call fact. Follow with a complete applicability matrix before case, metric, warning, failure, or evidence detail.

### Case-Level and Partition Ledgers

- **D-05:** The smallest result record is an atomic row bound to `authority_domain`, `partition`, `case_id`, `treatment`, and `repeat_id`. Inapplicable dimensions use an explicit schema branch; Red must not fabricate placeholder cases, treatments, or repeats. — **Reversibility:** one-way — row identity is the traceability contract for joins, metrics, warnings, and review decisions.
- **D-06:** Freeze one population manifest per partition with an ordered eligible ID set and set hash. Every metric binds its population ID and hash, included IDs, and excluded IDs with stable reasons. The denominator is independently recomputed from the eligible set length rather than trusted as a standalone number.
- **D-07:** Store every repeat as an immutable observation. Store repeat comparisons separately and bind them to exact repeat IDs. Repeat-disagreement has its own population, IDs, and denominator. Red preserves an explicit empty repeat population but creates no observations or comparisons.
- **D-08:** Scoring requires a closed join manifest binding exact identities and hashes for gold, prediction, prompt, raw response, parsed response, evidence spans, treatment, and repeat. Missing, extra, duplicate, cross-partition, or hash-mismatched records make the affected authority domain `invalid_withheld`; partial scoring is forbidden. — **Reversibility:** one-way — weakening closure would make published denominators and case traceability incomparable.

### Failure Classification Boundaries

- **D-09:** Every failure or warning has a stable code plus three orthogonal fields: `domain` (`authority`, `join`, `construction`, `evaluation`, or `experimental_outcome`), `severity` (`blocking` or `advisory`), and `effect` (`withhold_domain`, `exclude_case`, or `report_only`). Construction and evaluation failures cannot map to model correctness or experimental outcomes.
- **D-10:** Advisory warnings, including frozen `FRAME_COMBINATION_REQUIRES_REVIEW` patterns, live in an independent warning ledger linked by case and outcome IDs. Each warning binds its pattern version and trigger evidence. Warnings may be counted and reviewed but cannot alter axes, disposition, identity, correctness, eligibility, or denominators.
- **D-11:** Audit all Phase 5 rejected, failed-closed, superseded, and successful successor attempts in immutable predecessor/successor order on a separate `construction_feasibility` track. Verify recorded status, evidence custody, and terminal authority without reclassification. No attempt participates in an experimental denominator or success-rate metric.
- **D-12:** Propagate blockers through an explicit dependency graph. The directly affected authority domain and every dependent result become `invalid_withheld`. A genuinely independent authority domain remains auditable, but the Phase 6 package cannot be `complete` or `conclusion_ready` while any blocking domain remains unresolved.

### Review and Dispute Lifecycle

- **D-13:** Follow the established two-layer approval pattern: generate a decision-free canonical review packet and readiness identity, then require a separate human decision bound to their exact hashes. Machine readiness never implies approval. — **Reversibility:** one-way — review authority must remain distinct from machine computation and later Phase 7 interpretation authority.
- **D-14:** Allow package dispositions `approved`, `disputed`, and `incomplete`, with explicit per-domain and per-item responses. Only `approved` with no blocking dispute closes Phase 6. `disputed` and `incomplete` preserve all evidence and block `conclusion_ready` status.
- **D-15:** A dispute may annotate a frozen same-version record but cannot relabel gold, partition membership, relevance, metamorphic expectations, warnings, or failure classes in place. Semantic or frozen-input changes require a new experiment version and symmetric regeneration. Evaluator or packaging changes require a versioned successor closure and full revalidation while preserving predecessor evidence.
- **D-16:** Phase 6 approval grants only permission for Phase 7 to interpret the exact reviewed evaluation package. It does not approve the final feasibility narrative, permanently close conditional Green/Yellow requirements, authorize model calls, or authorize external publication. H5 interpretation and any later H6 publication authority remain separate.

### the agent's Discretion

The user delegated the Review and Dispute Lifecycle area to the agent; D-13 through D-16 record the resulting decisions. The planner may choose internal module names, schema decomposition, CLI command names, immutable generation names, stable diagnostic-code suffixes, deterministic Markdown layout, and review-packet directory structure. Those choices must reuse existing standard-library canonical JSON, strict parsing, descriptor-bound no-replace publication, runtime-closure, ordered-diagnostic, exact-resume, and human-decision patterns. Do not add a dependency when the standard library or existing project code suffices.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase Scope and Requirements

- `.planning/PROJECT.md` — Defines the evaluation-first scope, branch isolation, human authority, Red success path, and prohibited claims or external actions.
- `.planning/REQUIREMENTS.md` — Defines TS-06, TS-13, H1-02, H1-03, H1-04, H2-03, and H2-04 plus separate-denominator, warning, relevance, and metamorphic requirements.
- `.planning/ROADMAP.md` — Defines the Phase 6 goal, dependency on Phase 5, four planned increments, human checkpoint, and Red-specific success criterion.

### Deterministic Measurement Authority

- `.planning/phases/02-deterministic-measurement-spine/02-VERIFICATION-02-22.md` — Verifies the terminal Phase 2 successor and its deterministic measurement authority.
- `.planning/phases/02-deterministic-measurement-spine/02-REVIEW-02-22.md` — Records the reviewed Phase 2 source and lifecycle bindings.
- `experiments/specchoice-v1.3.2/phase2/source-authority.json` — Current accepted Phase 2 source authority.
- `experiments/specchoice-v1.3.2/runs/measurement-attempts/formal-golden-pr2164-v6/attempt.json` — Formal deterministic attempt identity and bindings.
- `experiments/specchoice-v1.3.2/runs/measurement-attempts/formal-golden-pr2164-v6/case-outcomes.json` — Existing case-level outcomes consumed by the deterministic-measurement track.
- `experiments/specchoice-v1.3.2/runs/measurement-attempts/formal-golden-pr2164-v6/metrics.json` — Existing independently denominated TS-06 metric source.
- `experiments/specchoice-v1.3.2/runs/measurement-attempts/formal-golden-pr2164-v6/diagnostics.json` — Existing stable diagnostic evidence.

### Frozen Data, Branch, and Red Execution Authority

- `.planning/phases/03-human-reviewed-data-preregistration/03-CONTEXT.md` — Locks partition, relevance, metamorphic, no-quota-filling, and same-version semantic boundaries.
- `.planning/phases/04-offline-treatments-retrieval-and-branch-freeze/04-CONTEXT.md` — Locks Red applicability, zero counts, no model surface, and advisory warning behavior.
- `.planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md` — Locks the Red evidence lifecycle, zero-cell matrix, attempt custody, exact resume, and downstream-only evaluation authority.
- `.planning/phases/05-authorized-execution-and-immutable-evidence/05-08-SUMMARY.md` — Latest Phase 5 successor summary; planning must verify it against eventual canonical Phase 5 closure rather than treating the summary alone as authority.
- `experiments/specchoice-v1.3.2/data/preregistration/pair-relevance-registry-v1.json` — Frozen preregistered relevance population; it cannot be expanded or re-ranked in Phase 6.
- `experiments/specchoice-v1.3.2/data/preregistration/metamorphic-registry-v1.json` — Frozen four-direction registry with current Red unavailability records.
- `experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json` — Current Red branch authority with `N_strict=0`, `repeat_count=0`, and no model/external-call authority.
- `experiments/specchoice-v1.3.2/receipts/red-execution-v2.json` — Candidate terminal Phase 5 Red evidence receipt; it is consumable only after Phase 5 lifecycle verification closes.
- `experiments/specchoice-v1.3.2/runs/red-execution-v2/attempt-chain.json` — Ordered Red execution attempt authority.
- `experiments/specchoice-v1.3.2/runs/red-execution-v2/matrix-manifest.json` — Canonical zero-cell A/B/C manifest.
- `experiments/specchoice-v1.3.2/runs/red-execution-v2/model-call-ledger.json` — Canonical zero-entry real-call ledger.
- `experiments/specchoice-v1.3.2/runs/red-execution-v2/no-call-structural-audit.json` — Structural no-model/no-provider evidence.
- `experiments/specchoice-v1.3.2/runs/red-execution-v2/no-call-runtime-audit.json` — Runtime no-network/no-call evidence.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `experiments/specchoice-v1.3.2/src/specchoice_measurement/scoring.py` — Reuse `Metric`, `CaseOutcome`, `ScoreResult`, independent denominator construction, score withholding, and evidence-integrity checks.
- `experiments/specchoice-v1.3.2/src/specchoice_measurement/diagnostics.py` — Reuse stable structured diagnostics and deterministic ordering.
- `experiments/specchoice-v1.3.2/src/specchoice_data/relevance.py` — Reuse exact relevance-registry, metamorphic-direction, readiness, and human-decision validation.
- `experiments/specchoice-v1.3.2/src/specchoice_treatments/schema.py` — Reuse parsed treatment contracts and versioned advisory-pattern evaluation.
- `experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py` — Reuse v6 Red authority validation, fixed formal inventory, zero ledger/matrix validation, and exact-resume behavior.
- `experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py` — Reuse canonical UTF-8/LF JSON and SHA-256 identities.
- `experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py` — Reuse descriptor-bound read and durable no-replace file-set publication.
- `experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py` — Reuse frozen runtime inventory and versioned successor validation.

### Established Patterns

- Canonical JSON is authoritative; Markdown is a deterministic reviewer projection.
- Complete-batch preflight and closed schemas fail before metric emission.
- Machine readiness and human approval are separate content-bound artifacts.
- Immutable attempts and versioned successors preserve failed and superseded history without in-place repair.
- Raw bytes, parsed objects, case outcomes, diagnostics, warnings, metrics, and review decisions remain separate one-way evidence layers connected by hashes.
- The prototype remains dependency-light and isolated under `experiments/specchoice-v1.3.2/`.

### Integration Points

- Phase 6 schemas, validators, ledgers, manifests, tests, reports, readiness, and review decisions remain under `experiments/specchoice-v1.3.2/`; no core UDB schema or generated architecture data changes are in scope.
- Admission must validate the exact Phase 2 authority and the verified terminal Phase 5 Red evidence root independently before building either evaluation namespace.
- Case joins consume existing Phase 2 case outcomes and, on Red, explicit empty Phase 3/4/5 partition and execution evidence without manufacturing G/Y rows.
- The approved Phase 6 review decision is the only package-level input Phase 7 may interpret; Phase 7 must not infer approval from report existence.

</code_context>

<specifics>
## Specific Ideas

- Make the first reviewer screen or report section a branch declaration followed by a complete applicability matrix.
- Keep zero, empty population, Red inapplicability, and invalid-withheld evidence visibly distinct in both JSON and Markdown.
- Emit exact population ID sets and hashes beside every independently calculated denominator.
- Show construction-feasibility history as an ordered evidence track, not as an experiment score or attempt success rate.
- Never emit a combined headline score across deterministic measurement, Red execution evidence, partitions, or failure domains.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within Phase 6 scope.

</deferred>

---

*Phase: 06-partition-aware-ablation-and-metamorphic-evaluation*
*Context gathered: 2026-08-05*

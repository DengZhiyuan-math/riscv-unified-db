# Phase 06: Partition-Aware Ablation and Metamorphic Evaluation - Research

**Researched:** 2026-08-06
**Domain:** Offline, partition-aware evaluation of immutable experimental evidence
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

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

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within Phase 6 scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|---|---|---|
| TS-06 | The reviewer receives independently calculated surfacing, disposition, exact/incorrect/missing identity, classify-out, and evidence-integrity outcomes; Green/Yellow additionally reports each frame axis and retrieval quality separately. | Retain the existing case-level `ScoreResult` metrics as the deterministic namespace; create independently bound population/metric manifests for every additional dimension. [VERIFIED: .planning/REQUIREMENTS.md:32-32; experiments/specchoice-v1.3.2/src/specchoice_measurement/scoring.py:13-78] |
| TS-13 | The operator can run four frozen, human-reviewed metamorphic minimal pairs covering choice-space origin, true WARL versus fixed legal set, hardware versus software authority, and normative versus NOTE/example language, and report the expected directional relation. | Validate and report the frozen direction registry. Red reports its four unavailable directions as inapplicable, never as failed or zero-scored execution. [VERIFIED: .planning/REQUIREMENTS.md:39-39; experiments/specchoice-v1.3.2/src/specchoice_data/relevance.py:19-34,313-372] |
| H1-02 | The reviewer can compare paired B-minus-A case outcomes where A and B use the same two fixed complete contrastive pairs and all shared controls, with the DelegationFrame as the intended intervention. | Implement a closed paired-comparison population only for an authorized G/Y branch; Red emits its metric identity with `not_applicable_red` and no synthetic A/B rows. [VERIFIED: .planning/REQUIREMENTS.md:46-46; .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-30] |
| H1-03 | The reviewer receives separate accuracy for all three frame axes and frozen `FRAME_COMBINATION_REQUIRES_REVIEW` warnings that remain non-blocking and cannot alter axis or disposition correctness. | Reuse parsed frame/advisory validation; keep warnings in a separate advisory ledger outside case eligibility and metric calculation. [VERIFIED: .planning/REQUIREMENTS.md:47-47; .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:32-37] |
| H1-04 | The reviewer can determine whether the frame changes shortcut-family errors and required metamorphic directions without post-hoc prompt, label, family, or threshold changes. | Bind all comparison and metamorphic populations to frozen upstream IDs/hashes; fail closed on any mismatched or missing input. [VERIFIED: .planning/REQUIREMENTS.md:48-48; experiments/specchoice-v1.3.2/src/specchoice_data/h2.py:249-305] |
| H2-03 | The reviewer can inspect a versioned and hashed relevance registry frozen before retrieval, per-case retrieved pair IDs, and `PairHit@K` calculated only for cases with preregistered human relevance judgments. | Reuse strict relevance validation and its eligible-ID list; calculate PairHit only from that exact list. Red preserves an explicit empty population and omits the ratio. [VERIFIED: .planning/REQUIREMENTS.md:54-54; experiments/specchoice-v1.3.2/src/specchoice_data/relevance.py:76-170] |
| H2-04 | The reviewer can compare paired C-minus-B outcomes where B and C share the identical frame, adjudication, context, evidence, model, pair-count, and repeat controls, with complete-pair selection method as the only intended intervention. | Implement the same closed-pair contract as H1-02, with its own population identity and denominator; never combine it with B-minus-A. [VERIFIED: .planning/REQUIREMENTS.md:55-55; .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-30] |
</phase_requirements>

## Project Constraints (from AGENTS.md)

- Keep the change inside `experiments/specchoice-v1.3.2/`; Phase 6 must not modify core UDB schemas or generated architecture data. [VERIFIED: AGENTS.md:63-75; .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:114-120]
- Prefer the dependency-light, standalone experiment boundary. The workspace documents Python standard library and Git CLI as sufficient, and expressly says that the full UDB toolchain is not required or probed. [VERIFIED: experiments/specchoice-v1.3.2/README.md:3-7]
- Follow existing deterministic canonical-JSON, strict-validation, immutable/no-replace, ordered-diagnostic, and exact-resume implementations rather than adding a dependency or parallel implementation. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:94-112]
- Use isolated Python `unittest` modules for fast phase validation; if this work later becomes a PR, repository policy requires `./bin/regress --all` to pass. [VERIFIED: AGENTS.md:16-39,104-109]
- Preserve the pre-existing dirty worktree paths; this research and its future plan must stage only Phase 6-owned paths. [VERIFIED: current `git status --short`, inspected 2026-08-06]

## Summary

Phase 6 should be planned as an immutable **evaluation package constructor** with two separately admitted namespaces: `deterministic_measurement` receives the Phase 2 case outcomes and independently calculated metrics, while `red_execution_evidence` receives the Phase 5 completed no-call/zero-cell evidence and construction-feasibility chain. It must never form a cross-namespace score, denominator, or experimental success rate. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-23,27-37,114-120]

The current branch is demonstrably Red, not a missing-data approximation. The following source-of-truth values were opened this session:

```text
DATA_G7K9M2QX_START
"branch":"red","N_strict":0,"repeat_count":0,"model_execution_authorized":false,"external_calls_authorized":false,"production_retrieval_authorized":false,"provider_config_present":false
DATA_G7K9M2QX_END
```

[VERIFIED: experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1]

Phase 5 is now a valid input candidate: its verification report is `passed` with `4/4 must-haves verified`, and STATE records Phase 05 as complete with no new model, G/Y, publication, metric, or final-conclusion authority. This removes the Context's planning gate but does not widen Phase 6 authority. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-VERIFICATION.md:1-14,102-110; .planning/STATE.md:5-17,29-36]

**Primary recommendation:** Build one small `specchoice_evaluation` package that first admits immutable Phase 2/Phase 5 roots, then constructs per-domain population and closed-join manifests, then projects only valid results into a decision-free review packet; publish the packet/readiness/decision as a new no-replace successor. [ASSUMED]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| Immutable authority admission | API / Backend | Database / Storage | Local validators must re-open and hash-bound-check the frozen Phase 2, Phase 4, and Phase 5 artifacts before evaluation. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py:143-168,279-293] |
| Population and closed-join construction | API / Backend | Database / Storage | The evaluation layer owns deterministic set equality, duplicate detection, exclusion reasons, and denominator recomputation over local artifact identities. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:27-30] |
| Metric and paired-result calculation | API / Backend | — | Existing pure scoring already generates sorted case outcomes and independently denominated metrics; Phase 6 should extend this at an evaluation boundary, not in a UI. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/scoring.py:313-385] |
| Warning/failure classification | API / Backend | — | Ordered diagnostics and advisory warnings are machine evidence, and the Context forbids their changing correctness or denominators. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/diagnostics.py:10-46; .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:32-37] |
| Review packet and human decision | API / Backend | Browser / Client | The backend produces canonical JSON plus deterministic Markdown; a human consumes it and records a separate content-bound decision. No interactive service/UI is in scope. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_data/relevance.py:375-481; experiments/specchoice-v1.3.2/README.md:23-25] |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---|---|---|---|
| Python standard library (`dataclasses`, `json`, `hashlib`, `pathlib`) | CPython 3.12.13 locally available | Immutable records, strict local artifact parsing, canonical serialization, hashes, and filesystem paths | Existing scoring uses frozen dataclasses and the evidence package already implements canonical JSON/SHA-256. No installation is needed. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/scoring.py:6-20; experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:24-48; local `.venv/bin/python --version`, 2026-08-06] |
| Existing `specchoice_*` packages | repository current checkout | Authority validation, strict parsing, score calculation, relevance/metamorphic validation, Red evidence validation, canonical output | Reuse is an explicit locked constraint; it retains the known closure and integrity behavior. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:94-112] |

### Supporting

| Library | Version | Purpose | When to Use |
|---|---|---|---|
| Python `unittest` | CPython 3.12.13 locally available | Isolated contract, tamper, exact-resume, and output-projection tests | Add Phase 6-focused tests before implementation; current tests already use `unittest.TestCase`. [VERIFIED: experiments/specchoice-v1.3.2/tests/test_measurement_scoring.py:6-25; local `.venv/bin/python --version`, 2026-08-06] |
| Ruff | 0.16.0 locally available | Isolated style/static checks for changed Python files | Run after focused unit tests; reuse the existing `--isolated` convention. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-08-SUMMARY.md:27-28; local `.venv/bin/ruff --version`, 2026-08-06] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|---|---|---|
| Local canonical JSON and existing validators | New database, dataframe library, reporting framework, or service | Rejected: introduces unneeded storage/dependency/authority surface and violates the locked dependency-light isolated boundary. [VERIFIED: experiments/specchoice-v1.3.2/README.md:3-7; .planning/REQUIREMENTS.md:111-125] |
| Separate namespace manifests | A blended score table | Rejected: a single blended headline score is explicitly out of scope and would erase denominator boundaries. [VERIFIED: .planning/REQUIREMENTS.md:123-123; .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-23] |

**Installation:** None. This phase must not add packages. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:46-49; experiments/specchoice-v1.3.2/README.md:3-7]

## Architecture Patterns

### System Architecture Diagram

```text
Phase 2 source authority + case outcomes/metrics ─┐
                                                   ├─► independent admission ─► deterministic_measurement
Phase 4 Red authority + Phase 5 receipt/evidence ─┘                                  │
                                                                                       ├─► population manifests
Frozen relevance/metamorphic registries ─────────────────────────────────────────────►│   + closed joins
                                                                                       │
Phase 5 predecessor/successor attempt chain ─────────────────────────────────────────► construction_feasibility
                                                                                       │
deterministic_measurement + red_execution_evidence + construction_feasibility ───────► applicability matrix
                                                                                          │
                                                                                          ├─► canonical evaluation packet
                                                                                          ├─► deterministic Markdown projection
                                                                                          ├─► readiness identity
                                                                                          └─► human decision (approved/disputed/incomplete)
```

The diagram intentionally keeps construction feasibility outside experimental metrics and treats review approval as a separate final input. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-23,32-44]

### Recommended Project Structure

```text
experiments/specchoice-v1.3.2/
├── src/specchoice_evaluation/          # [ASSUMED] proposed Phase 6-only package
│   ├── admission.py                    # [ASSUMED] bind and validate upstream immutable roots
│   ├── manifests.py                    # [ASSUMED] population and closed-join manifests
│   ├── evaluation.py                   # [ASSUMED] per-domain result construction, not blended scoring
│   ├── review.py                       # [ASSUMED] canonical packet/readiness/decision validators
│   └── cli.py                          # [ASSUMED] one deterministic local entry point
├── tests/test_partition_evaluation.py  # [ASSUMED] Phase 6 contract/tamper tests
├── runs/phase6-evaluation-*/           # [ASSUMED] immutable output generation; exact name selected in plan
├── receipts/phase6-evaluation-*.json   # [ASSUMED] readiness and successor identities
└── reviews/phase6-evaluation-*.json    # [ASSUMED] human decision bound to packet/readiness hashes
```

### Pattern 1: Admit First, Then Build Independent Namespaces

**What:** Validate each upstream root and its content/hash bindings before any population, join, or metric object exists. Construct `deterministic_measurement`, `red_execution_evidence`, and `construction_feasibility` independently; only a review packet may reference all three. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-23,114-120]

**When to use:** Always. A Phase 2 admission failure must withhold its dependent deterministic result without fabricating a Phase 5 failure; a Phase 5 closure failure has the converse behavior. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:37-37]

### Pattern 2: Manifest Before Metric

**What:** For each metric, serialize a population manifest with ordered eligible IDs, hash, included IDs, excluded IDs/reasons, and a recomputed denominator. The metric stores that manifest identity, never an unbound denominator. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:27-30]

**When to use:** Both the Phase 2 metrics and every G/Y-only future metric. On Red, serialize a visible empty/inapplicable population rather than an experimental zero. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-24]

### Pattern 3: Closed Join Before Any Scoring

**What:** Require set equality and hash equality across the identities relevant to the result. A missing, extra, duplicate, cross-partition, or mismatched member blocks the affected domain and emits no partial score. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:27-30]

**When to use:** Before every deterministic measurement projection, A/B/C comparison, PairHit, metamorphic outcome, and repeat comparison. Existing scoring follows the same fail-closed shape: blocker diagnostics return `metrics=None`. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/scoring.py:335-385]

### Pattern 4: Decision-Free Packet, Then Human Decision

**What:** Generate canonical packet and deterministic Markdown, bind readiness to their hashes, then validate a distinct reviewer decision with explicit per-domain/per-item dispositions. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:39-44; experiments/specchoice-v1.3.2/src/specchoice_data/relevance.py:375-481]

**When to use:** At Phase 6 closure. Report existence or machine readiness must never imply `approved`. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:39-44]

### Anti-Patterns to Avoid

- **Representing absent Red execution as a zero:** It falsely turns an inapplicable experiment into evidence; keep `not_applicable_red` with no score/ratio. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-24]
- **Pooling Phase 2 and Phase 5 counts:** It creates a misleading headline metric and crosses authority domains. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-23]
- **Partial scoring after a join failure:** It hides denominator/custody corruption; withhold the affected domain and propagate dependencies. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:27-37]
- **Letting an advisory warning change a score:** Warnings are review evidence only, not new gold, correctness, or eligibility. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:32-37]
- **Repairing a frozen input or relabeling a same-version item:** semantic/frozen changes require a new experiment version; evaluator/packaging changes require a preserved-successor revalidation. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:39-44; experiments/specchoice-v1.3.2/src/specchoice_data/h2.py:301-305]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---|---|---|---|
| Canonical JSON and SHA-256 identity | New serializer or ad-hoc JSON hashing | `canonical_json_bytes`, `sha256_bytes`, and `require_sha256` | Existing implementation normalizes text and produces canonical UTF-8/LF bytes. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:24-60] |
| Ordered diagnostics | Ad-hoc sorting in each new ledger | `Diagnostic` and `ordered_diagnostics` | The current sole ordering is deterministic by severity/code/identity/field/occurrence. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/diagnostics.py:10-46] |
| Red authority/evidence validation | A Phase 6 reimplementation of the no-call proof | `validate_red_authority_v2` and `validate_red_evidence_v2` | Existing code reconstructs authority and verifies the zero ledger, zero matrix, and empty parsed findings. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py:143-168,279-293] |
| Relevance/metamorphic registry validation | A looser Phase 6 schema | `validate_pair_relevance_registry_v1` and `validate_metamorphic_registry_v1` | Existing validators enforce complete relevance coverage, frozen bindings, four directions, and explicit unavailability. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_data/relevance.py:76-170,313-372] |
| No-replace publication and authoritative local reads | Check-then-overwrite file I/O | Existing descriptor-bound filesystem primitives and exact-resume pattern | Existing Red execution treats an occupied partial/different target as an error and validates identical complete output only. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py:296-319] |

**Key insight:** Phase 6 adds cross-artifact evaluation semantics, not a new experiment runtime. Its smallest safe addition is a thin composition layer over existing trusted primitives. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:94-120]

## Common Pitfalls

### Pitfall 1: Collapsing Four Different Non-Positive States

**What goes wrong:** An empty population, Red inapplicability, withheld-invalid data, and a measured zero are rendered the same way.
**Why it happens:** Generic metric objects usually assume numerator/denominator are always present.
**How to avoid:** Model the locked four-state result union before metric code. Only `measured` carries a score; `empty_population` has counts but no ratio; `not_applicable_red` has authority/reason; `invalid_withheld` has blocking diagnostics and no metric.
**Warning signs:** Any Red metric serializes `0/0`, `0/N`, a score, or a fabricated row. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-24]

```text
DATA_R8V2L6KC_START
`measured`, `empty_population`, `not_applicable_red`, and `invalid_withheld`
DATA_R8V2L6KC_END
```

[VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-23]

### Pitfall 2: Trusting a Declared Denominator

**What goes wrong:** A report lists a denominator whose IDs cannot be reconstructed.
**Why it happens:** A metric is copied from Phase 2 or calculated before filtering/exclusions are frozen.
**How to avoid:** Serialize eligible/included/excluded IDs and a set hash first; recompute denominator from eligible-ID length and reject a disagreement.
**Warning signs:** A metric has a count but no manifest identity, or an exclusion lacks a stable reason. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:27-30]

### Pitfall 3: Treating Construction History as Experimental Outcomes

**What goes wrong:** Failed-closed/superseded construction attempts affect a metric, success rate, or model-correctness label.
**Why it happens:** Both evidence tracks are stored in one report without a domain field.
**How to avoid:** Keep an ordered `construction_feasibility` audit that verifies custody/status only and has no experimental denominator.
**Warning signs:** A construction attempt appears in a case-level outcome table or changes a score. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:32-37]

### Pitfall 4: Approving by File Existence

**What goes wrong:** A generated report is treated as human approval.
**Why it happens:** Machine readiness and decision state are serialized in one mutable artifact.
**How to avoid:** Reuse the packet → readiness → decision sequence and bind the decision to exact hashes.
**Warning signs:** A package has no reviewer identity, disposition, or content-hash binding. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:39-44; experiments/specchoice-v1.3.2/src/specchoice_data/relevance.py:420-481]

## Code Examples

### Locked Result-State Gate

The following is prescriptive pseudocode for a new evaluation result constructor; only the four literals are locked. New function/module names are deliberately left to planning discretion. [ASSUMED]

```python
if blocking_diagnostics:
    return result_state("invalid_withheld")
if branch_is_red and metric_is_green_yellow_only:
    return result_state("not_applicable_red")
if not eligible_ids:
    return result_state("empty_population")
return result_state("measured")
```

The string literals appear verbatim in the locked Context quote above; the measured branch must bind the population manifest and independently recomputed denominator before adding its score. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-30]

### Reuse Existing Fail-Closed Scoring Semantics

Phase 6 should adapt, not weaken, current scoring behavior: blocker diagnostics cause `metrics=None`; otherwise the scorer produces sorted case outcomes and independently denominated metrics. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_measurement/scoring.py:335-385]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|---|---|---|---|
| Treat a Red path as a blocked absence of evaluation | Phase 5 has a passed Red no-call/zero-cell evidence root; Phase 6 evaluates it as a separate construction-feasibility namespace | Phase 5 re-verification on 2026-08-06 | The planner can build a bounded Red package now, but cannot create G/Y rows, calls, scores, or authority. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-VERIFICATION.md:35-53,102-110; .planning/STATE.md:29-36] |
| Generic aggregate metrics | Case-level, population-bound metrics with separate authority namespaces and no blended headline score | Locked by Phase 6 Context | Planning must make manifests and closed joins first-class artifacts. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-30] |

**Deprecated/outdated:** Any plan that treats the earlier “Phase 5 lacks verification closure” condition as current is outdated; Phase 5 now has a passed verification artifact and STATE marks it complete. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-VERIFICATION.md:1-14; .planning/STATE.md:5-17]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|---|---|---|
| A1 | `specchoice_evaluation` is the best new package name and the proposed five-module layout is appropriate. | Recommended Project Structure | Low; the Context delegates module/CLI/directory names to the planner. |
| A2 | One Phase 6 local CLI should construct the full immutable package. | Summary / Project Structure | Medium; may need separate build/verify entry points to match existing CLI conventions. |
| A3 | The result-state pseudocode is the minimal safe new API shape. | Code Examples | Medium; exact schema field names and constructor signatures need Wave 0 contract tests before implementation. |

## Open Questions

1. **No blocking product or authority question remains.**
   - What we know: Phase 5 verification is passed and lifecycle state is complete; the Phase 4 branch remains Red with no model/call/retrieval/provider authority. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-VERIFICATION.md:1-14,102-110; experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1]
   - What's unclear: Only implementation-local names and exact immutable generation paths are delegated, not semantic decisions. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:46-49]
   - Recommendation: Decide these in PLAN.md, preserve them in a new versioned output schema, and make every choice testable before generation. [ASSUMED]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|---|---|---|---|---|
| Local CPython | Phase 6 evaluator and unit tests | ✓ | 3.12.13 | None required; use the existing `.venv` interpreter. [VERIFIED: local `.venv/bin/python --version`, 2026-08-06] |
| Python standard library | Canonical JSON, hashes, dataclasses, filesystem | ✓ | bundled with CPython 3.12.13 | No third-party dependency is authorized. [VERIFIED: experiments/specchoice-v1.3.2/README.md:3-7; local `.venv/bin/python --version`, 2026-08-06] |
| Ruff | Style/static validation | ✓ | 0.16.0 | Use existing isolated invocation. [VERIFIED: local `.venv/bin/ruff --version`, 2026-08-06] |
| Network/provider/model/retrieval credentials | No Phase 6 behavior | Intentionally unavailable/unauthorized | — | No fallback; Phase 6 must remain local Red evaluation. [VERIFIED: experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1; .planning/phases/05-authorized-execution-and-immutable-evidence/05-VERIFICATION.md:102-110] |

**Missing dependencies with no fallback:** None for the authorized Red path. [VERIFIED: experiments/specchoice-v1.3.2/README.md:3-7]

**Missing dependencies with fallback:** None; do not add a substitute model, provider, retriever, or package. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:46-49]

## Validation Architecture

### Test Framework

| Property | Value |
|---|---|
| Framework | Python `unittest` under CPython 3.12.13. [VERIFIED: experiments/specchoice-v1.3.2/tests/test_measurement_scoring.py:6-25; local `.venv/bin/python --version`, 2026-08-06] |
| Config file | None; focused modules run with `PYTHONPATH=src`. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-08-SUMMARY.md:27-28] |
| Quick run command | `cd experiments/specchoice-v1.3.2 && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_partition_evaluation -q` [ASSUMED: new Wave 0 test module] |
| Existing regression command | `./bin/regress --all` for eventual PR-level repository validation. [VERIFIED: AGENTS.md:16-39,104-109] |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|---|---|---|---|---|
| TS-06 | Independent deterministic metrics; Red inapplicable G/Y metric identities omit scores; no blended score | unit + frozen-artifact integration | `... unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_red_metrics_preserve_applicability_and_separate_denominators -q` [ASSUMED] | ❌ Wave 0 |
| TS-13 | Exact four frozen directions retain availability/reason and no Red execution result | unit + frozen-artifact integration | `... unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_red_metamorphic_registry_is_complete_and_unscored -q` [ASSUMED] | ❌ Wave 0 |
| H1-02 | B-A comparison is absent/inapplicable on Red; future G/Y requires a closed pair population | unit | `... unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_pair_join_rejects_missing_duplicate_and_cross_partition_rows -q` [ASSUMED] | ❌ Wave 0 |
| H1-03 | Axis metrics remain independent; advisory warning cannot alter metrics | unit | `... unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_frame_warning_is_report_only -q` [ASSUMED] | ❌ Wave 0 |
| H1-04 | Frozen family/metamorphic identities reject drift | tamper/contract | `... unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_frozen_binding_drift_withholds_dependent_domain -q` [ASSUMED] | ❌ Wave 0 |
| H2-03 | PairHit derives only from preregistered eligible IDs and does not ratio-score empty Red population | unit + frozen-artifact integration | `... unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_pairhit_uses_only_frozen_eligible_ids -q` [ASSUMED] | ❌ Wave 0 |
| H2-04 | C-B population is independent from B-A and cannot pool denominator/identity | unit | `... unittest tests.test_partition_evaluation.PartitionEvaluationTests.test_c_minus_b_population_is_independent -q` [ASSUMED] | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** Run the Phase 6-focused `unittest` module plus Ruff on changed Phase 6 Python/tests. [ASSUMED]
- **Per wave merge:** Run focused upstream reuse tests: `tests.test_measurement_scoring`, `tests.test_data_relevance`, and `tests.test_authorized_execution_v2`; these passed locally during this research. [VERIFIED: local focused test run, 2026-08-06]
- **Phase gate:** Full Phase 6-focused suite, reuse suite, Ruff, `git diff --check`, exact-resume/tamper tests, and required human decision before `$gsd-verify-work`. [ASSUMED]

### Wave 0 Gaps

- [ ] `experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py` — Phase 6 result union, population, closed-join, authority-boundary, warning, packet/readiness/decision, exact-resume, and tamper contracts. [ASSUMED]
- [ ] `experiments/specchoice-v1.3.2/src/specchoice_evaluation/` — the narrow composition package proposed above. [ASSUMED]
- [ ] No framework installation — existing standard library/unittest and Ruff infrastructure is sufficient. [VERIFIED: experiments/specchoice-v1.3.2/README.md:3-7]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---|---|---|
| V2 Authentication | No | No login/identity endpoint is in scope; review identity is an evidence field, not an authentication service. [VERIFIED: experiments/specchoice-v1.3.2/README.md:23-25] |
| V3 Session Management | No | No service/session surface is in scope. [VERIFIED: experiments/specchoice-v1.3.2/README.md:23-25] |
| V4 Access Control | No | The authorized operation is local artifact validation; it must not add network/provider/publication capability. [VERIFIED: experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json:1; .planning/phases/05-authorized-execution-and-immutable-evidence/05-VERIFICATION.md:102-110] |
| V5 Input Validation | Yes | Strict canonical parsing, exact key/binding checks, descriptor-bound reads, closed joins, and fail-closed diagnostics. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_data/relevance.py:132-170; experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py:279-293] |
| V6 Cryptography | Yes, integrity only | Reuse canonical SHA-256 identifiers; do not implement a custom cryptographic primitive. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py:40-60] |

### Known Threat Patterns for the Local Evidence Stack

| Pattern | STRIDE | Standard Mitigation |
|---|---|---|
| Substituted/tampered authority or evidence input | Tampering | Rebuild/validate Phase 4 authority and verify receipt/component identities before admitting a namespace. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py:143-168,279-293] |
| Missing, duplicate, extra, cross-partition, or hash-mismatched case row | Tampering | Closed join rejects the affected domain and emits `invalid_withheld`, never a partial metric. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:27-30] |
| Denominator manipulation via omitted/excluded IDs | Tampering | Ordered population manifest, hash, explicit exclusions/reasons, independently recomputed denominator. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:27-30] |
| Evidence overwrite or partial publication | Tampering / Repudiation | Reuse no-replace and exact-resume behavior; occupied partial/different outputs fail closed. [VERIFIED: experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py:296-319] |
| Advisory warning changes correctness | Elevation of Privilege | Separate warning ledger with report-only effect; warnings cannot alter axes, disposition, identity, correctness, eligibility, or denominator. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:32-37] |

## Sources

### Primary (local, HIGH confidence)

- `.planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md` — locked result, population, failure, review, and scope decisions. [VERIFIED: :18-49,91-139]
- `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` — Phase 6 requirement semantics, success criteria, and planned increments. [VERIFIED: .planning/REQUIREMENTS.md:32-55; .planning/ROADMAP.md:360-383]
- `.planning/phases/05-authorized-execution-and-immutable-evidence/05-VERIFICATION.md` and `.planning/STATE.md` — completed Phase 5 gate and remaining authority boundary. [VERIFIED: .planning/phases/05-authorized-execution-and-immutable-evidence/05-VERIFICATION.md:1-14,35-53,102-110; .planning/STATE.md:5-17,29-36]
- `experiments/specchoice-v1.3.2/src/specchoice_measurement/scoring.py`, `diagnostics.py`, `specchoice_data/relevance.py`, and `specchoice_execution/red_v2.py` — reusable scoring, diagnostics, preregistration, and no-call evidence patterns. [VERIFIED: cited line ranges above]

### Secondary (local, HIGH confidence)

- `experiments/specchoice-v1.3.2/tests/test_measurement_scoring.py`, `tests/test_data_relevance.py`, and `tests/test_authorized_execution_v2.py` — current test conventions; the focused three-module suite passed during this research. [VERIFIED: experiments/specchoice-v1.3.2/tests/test_measurement_scoring.py:1-25; local focused test run, 2026-08-06]

### Tertiary (LOW confidence)

- None. All domain facts above were checked locally; proposed names and new test/module layout remain explicitly listed in the Assumptions Log.

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — existing source, local interpreter/linter availability, and locked no-dependency constraint agree. [VERIFIED: experiments/specchoice-v1.3.2/README.md:3-7; local tool probes, 2026-08-06]
- Architecture: HIGH — locked Phase 6 decisions directly define ownership, artifact flow, and failure boundaries. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:18-49,91-120]
- Pitfalls: HIGH — each is a locked failure/authority rule or a tested fail-closed pattern. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:20-44; experiments/specchoice-v1.3.2/src/specchoice_measurement/scoring.py:335-385]

**Research date:** 2026-08-06
**Valid until:** Phase 6 plan is approved, or any upstream Phase 2/4/5 authority artifact changes; frozen-input changes require a forward-only successor. [VERIFIED: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md:39-44]

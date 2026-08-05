# Phase 6: Partition-Aware Ablation and Metamorphic Evaluation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-08-05
**Phase:** 06-partition-aware-ablation-and-metamorphic-evaluation
**Areas discussed:** Red metric representation, case-level and partition ledgers, failure classification boundaries, review and dispute lifecycle

---

## Red Metric Representation

| Question | Options considered | Selected |
|----------|--------------------|----------|
| G/Y-only metric encoding on Red | Typed N/A without numeric fields; N/A with zero denominator; omit the metric | Typed N/A without numeric fields |
| TS-06 measurement versus Phase 5 evidence | Independent namespaces; unified case ledger; Phase 5 only | Independent namespaces |
| Machine result states | Four distinct states; three simplified states; numeric values with reasons | `measured`, `empty_population`, `not_applicable_red`, `invalid_withheld` |
| Reviewer entry order | Branch then applicability; deterministic results first; evidence inventory first | Branch then applicability |

**User's choice:** The user selected the recommended option for all four questions.
**Notes:** Numeric fields are present only for measured results. No combined headline score is permitted.

---

## Case-Level and Partition Ledgers

| Question | Options considered | Selected |
|----------|--------------------|----------|
| Smallest result grain | Atomic result rows; per-case summary rows; per-metric tables | Atomic result rows |
| Denominator proof | Frozen population manifests; derive from rows; counts only | Frozen population manifests |
| Repeat modeling | Separate observations and comparisons; majority collapse; nested case arrays | Separate observations and comparisons |
| Incomplete joins | Require complete closure; allow partial scoring; local file validation only | Require complete closure |

**User's choice:** The user selected the recommended option for all four questions.
**Notes:** Red preserves explicit empty populations but no placeholder observations, treatments, or repeats.

---

## Failure Classification Boundaries

| Question | Options considered | Selected |
|----------|--------------------|----------|
| Failure taxonomy | Orthogonal domain/severity/effect; stage only; flat blocker/warning list | Orthogonal domain/severity/effect |
| Advisory warning storage | Independent ledger; embed in result rows; score penalty | Independent ledger |
| Phase 5 attempt history | Construction-feasibility track; terminal evidence only; attempt success rate | Construction-feasibility track |
| Blocker propagation | Dependency graph and domain closure; invalidate all domains; case-local exclusion | Dependency graph and domain closure |

**User's choice:** The user selected the recommended option for all four questions.
**Notes:** Construction and evaluation failures cannot become model outcomes. Independent domains remain auditable, but an unresolved blocker prevents package completion.

---

## Review and Dispute Lifecycle

| Decision | Selected approach |
|----------|-------------------|
| Review authority | Decision-free packet and readiness, followed by a separate hash-bound human decision |
| Dispositions | `approved`, `disputed`, `incomplete`; only unblocked approval closes Phase 6 |
| Dispute correction | No same-version relabeling; semantic changes create a new experiment version, while evaluator/package changes create a fully revalidated successor |
| Downstream authority | Approval permits only Phase 7 interpretation of the exact reviewed package |

**User's choice:** The user explicitly delegated this entire area to the agent.
**Notes:** The selected lifecycle reuses the project's established readiness/decision separation and preserves H5 interpretation and any later H6 publication as separate authorities.

## the agent's Discretion

- Review and dispute lifecycle decisions were delegated by the user and are recorded in CONTEXT.md D-13 through D-16.
- Internal module names, schema decomposition, CLI names, generation names, diagnostic suffixes, and deterministic report layout remain planner discretion within the locked contracts.

## Deferred Ideas

None.

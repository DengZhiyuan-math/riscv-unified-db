# Phase 5: Authorized Execution and Immutable Evidence - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-08-04
**Phase:** 05-authorized-execution-and-immutable-evidence
**Areas discussed:** Red execution completion condition, zero-call ledger proof strength, zero-cell matrix representation, drift and failed-attempt preservation

---

## Red Execution Completion Condition

| Question | Options considered | Selected |
|----------|--------------------|----------|
| When may execution enter `completed`? | Complete atomic evidence set; ledger-first completion; partial completion with warnings | Complete atomic evidence set |
| How should identical input handle existing complete evidence? | Exact zero-write resume; new attempt every run; temporary rebuild and compare | Exact zero-write resume |
| How should pre-completion failures be saved? | Separate immutable failed attempt; zero persistent writes; partial formal evidence | Separate immutable failed attempt |
| What does Phase 5 completion authorize? | Red evidence evaluation only; final Red conclusion; permanent G/Y closure | Red evidence evaluation only |

**User's choices:** The recommended first option was selected for all four questions.
**Notes:** Completion is atomic and one-way, exact reruns are zero-write, failures are non-authoritative, and Phase 5 does not grant model, publication, or final-conclusion authority.

---

## Zero-Call Ledger Proof Strength

| Question | Options considered | Selected |
|----------|--------------------|----------|
| What jointly proves zero real model calls? | Ledger + structural scan + runtime tripwire; ledger + scan; ledger only | Three-layer closure |
| What does the network tripwire block? | Every socket including loopback; external only; observe without blocking | Every socket including loopback |
| How is a blocked call attempt recorded? | Separate real-call ledger and security events; one combined ledger; diagnostic only | Separate real-call ledger and security events |
| How is Phase 4 no-model proof used? | Bind v6 proof and rescan Phase 5; reuse only v6; use only a new scan | Bind v6 proof and rescan Phase 5 |

**User's choices:** The recommended first option was selected for all four questions.
**Notes:** A valid completed run has an empty real-call ledger. Blocked attempts remain visible in failed-attempt security evidence and prevent publication.

---

## Zero-Cell Matrix Representation

| Question | Options considered | Selected |
|----------|--------------------|----------|
| Should Red produce an A/B/C matrix artifact? | Canonical zero-cell manifest; no manifest; N/A placeholder cells | Canonical zero-cell manifest |
| How are TS-11 and TS-12 represented? | Conditional N/A pending Phase 7; closed N/A; ordinary pending | Conditional N/A pending Phase 7 |
| How is favorable-subset absence proven? | Formula + A/B/C partition counts + closure scan; aggregate zero only; ledger only | Formula + A/B/C partition counts + closure scan |
| What reviewer outputs are produced? | Canonical JSON + deterministic Markdown; JSON only; Markdown only | Canonical JSON + deterministic Markdown |

**User's choices:** The recommended first option was selected for all four questions.
**Notes:** No placeholder calls or metrics are created. The machine-readable requirement state is `conditional_not_applicable_red_pending_phase7`.

---

## Drift and Failed-Attempt Preservation

| Question | Options considered | Selected |
|----------|--------------------|----------|
| Which changes require a successor? | Any frozen-closure byte change; every failure; authority file only | Any frozen-closure byte change |
| What does a failed attempt preserve? | Complete failed-attempt package; minimal receipt; partial formal evidence | Complete failed-attempt package |
| How does a successor gain authority? | New human gate; inherit v6 automatically; modify v6 in place | New human gate |
| How are retries preserved? | New immutable attempt each time; final result only; mutate one attempt | New immutable attempt each time |

**User's choices:** The recommended first option was selected for all four questions.
**Notes:** Transient failures can retry only with identical inputs and policy. Final success binds the complete ordered attempt history and proves every model-call ledger is empty.

---

## the agent's Discretion

- Internal module, schema, CLI, directory, diagnostic-code, tripwire-implementation, and Markdown-layout choices remain with the planner within the locked evidence and authority boundaries.

## Deferred Ideas

- None.

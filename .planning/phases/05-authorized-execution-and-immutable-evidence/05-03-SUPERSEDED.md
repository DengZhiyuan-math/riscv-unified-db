---
phase: 05-authorized-execution-and-immutable-evidence
plan: 03
type: execute
wave: 3
depends_on:
  - 05-02
files_modified: []
autonomous: true
requirements:
  - TS-07
  - TS-11
  - TS-12
estimate:
  tokens: 30000
  raw_tokens: 30000
  tasks: 2
  confidence: low
must_haves:
  truths:
    - "D-02: an identical formal invocation is byte-identical and performs exactly zero writes across attempts, formal leaves, receipt, and Markdown."
    - "D-08/D-11: read-only closure proves the exact v6 and Phase 5 roots still match and no unregistered run, raw-response, provider/model, credential, retrieval, network, or process surface exists."
    - "D-14/D-16: every attempt is present in immutable ordinal order, every attempt ledger is empty, and no deletion, replacement, reordering, or favorable retry is hidden."
    - "TS-07: raw, parsed, ordered-diagnostic, and span-audit leaves independently validate; surfaced findings stay distinct with non-empty verbatim spans and zero findings use the explicit canonical empty set."
    - "TS-11/TS-12: expected_cells=0*3*0=0, all A/B/C expected/attempted/completed/failed/retried counts are exact integer zeros, cells=[], the completed ledger is exactly empty, and both statuses remain conditional_not_applicable_red_pending_phase7."
    - "The final audit emits no new formal leaf, no metric, no extraction-success/feasibility conclusion, and no broader authority; it authorizes only downstream Red evidence evaluation."
  artifacts:
    - path: experiments/specchoice-v1.3.2/runs/red-execution-v1/
      provides: "Read-only verified complete formal Red evidence set; this plan does not rewrite it."
    - path: experiments/specchoice-v1.3.2/receipts/red-execution-v1.json
      provides: "Read-only verified terminal receipt and complete attempt-chain binding."
    - path: experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v1.md
      provides: "Read-only verified deterministic projection derived from the canonical receipt."
  key_links:
    - from: experiments/specchoice-v1.3.2/receipts/red-execution-v1.json
      to: experiments/specchoice-v1.3.2/runs/red-execution-v1/
      via: "descriptor-held exact inventory and SHA-256 recomputation of every required leaf"
      pattern: "completed|downstream_red_evidence_evaluation_only"
    - from: experiments/specchoice-v1.3.2/runs/red-execution-v1/attempt-chain.json
      to: experiments/specchoice-v1.3.2/runs/red-attempts/
      via: "strictly ordered complete ordinal/digest reconciliation"
      pattern: "attempt_chain"
    - from: experiments/specchoice-v1.3.2/runs/red-execution-v1/matrix-manifest.json
      to: experiments/specchoice-v1.3.2/runs/red-execution-v1/model-call-ledger.json
      via: "independent zero-cell and zero-real-call validation under one terminal root"
      pattern: "conditional_not_applicable_red_pending_phase7"
  prohibitions:
    - statement: "The audit must not rewrite, repair, delete, reorder, migrate, or add any attempt or formal evidence leaf."
      status: planned
      verification: "filesystem snapshot before/after exact resume and read-only verification"
    - statement: "No G/Y requirement is permanently closed and no placeholder, metric, extraction-success claim, or feasibility conclusion is emitted."
      status: planned
      verification: "closed receipt/matrix/report schemas and prohibited-claim tests"
    - statement: "No frozen closure weakening is accepted without a versioned successor and new human gate."
      status: planned
      verification: "mutation audit requires successor state and rejects current completion"
---

## Phase Goal

**As a** reviewer, **I want to** inspect a complete immutable Red no-call evidence chain, **so that** downstream evaluation can proceed without unauthorized calls, hidden repair, asymmetric retries, or favorable-subset execution.

<objective>
Audit the complete formal Red evidence root and prove byte-identical zero-write replay, complete attempt history, truthful absence claims, and bounded downstream authority without modifying frozen bytes.

Purpose: Close Phase 5 through independent read-only verification rather than by trusting the terminal receipt's self-claims.
Output: Passing read-only evidence, retry, no-call, no-cell, TS-07 lineage, exact-resume, pinned-toolchain, and prohibited-claim checks recorded in the plan summary; no new formal evidence leaf.
</objective>

<execution_context>
Follow the repository-configured GSD execute-plan and summary contracts; every path in this plan is repository-relative.
</execution_context>

<context>
@AGENTS.md
@.planning/PROJECT.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-RESEARCH.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-VALIDATION.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-02-SUMMARY.md
@experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json
@experiments/specchoice-v1.3.2/src/specchoice_execution/red.py
@experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py
@experiments/specchoice-v1.3.2/tests/test_authorized_execution.py
@experiments/specchoice-v1.3.2/runs/red-execution-v1/
@experiments/specchoice-v1.3.2/receipts/red-execution-v1.json
@experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v1.md

<interfaces>
- Invoke the same closed `execute-red` path against the exact existing targets to prove resume; do not introduce an auditor that changes the frozen closure after publication.
- Use the existing read-only validation API and descriptor-held bytes to recompute every root and cross-link independently of receipt self-claims.
- Capture filesystem inventories, byte hashes, and metadata needed for a write-observer assertion before and after replay; the summary records results but does not become evidence authority.
</interfaces>
</context>

## Artifacts this phase produces

- No new formal machine artifact. The plan validates the exact existing `runs/red-execution-v1/`, `receipts/red-execution-v1.json`, and deterministic Markdown bytes without writes.
- Execution record: `.planning/phases/05-authorized-execution-and-immutable-evidence/05-03-SUMMARY.md`, which reports commands/results and authorizes only downstream Red evidence evaluation; it is not part of the immutable evidence root.
- Spec-less fallback edge coverage: `applicable=15`, `resolved=15`, `unresolved=0`, `explicit=15`, `backstop=0`.

<tasks>

<task type="auto">
  <name>05-03-01: Recompute the complete evidence and attempt graph read-only</name>
  <precondition>The formal Red directory, terminal receipt, Markdown projection, exact v6 authority chain, reviewed Phase 5 closure, and repository-pinned Python >=3.12/Ruff 0.16.0 exist and validate; an absent or partial formal set is a blocking Phase 5 failure, not an audit input to repair.</precondition>
  <files>experiments/specchoice-v1.3.2/runs/red-execution-v1/, experiments/specchoice-v1.3.2/runs/red-attempts/, experiments/specchoice-v1.3.2/receipts/red-execution-v1.json, experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v1.md</files>
  <read_first>
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-02-SUMMARY.md
    - experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json
    - experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v1/raw-evidence.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v1/parsed-evidence.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v1/ordered-diagnostics.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v1/evidence-span-audit.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v1/model-call-ledger.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v1/matrix-manifest.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v1/attempt-chain.json
    - experiments/specchoice-v1.3.2/receipts/red-execution-v1.json
  </read_first>
  <action>Run the read-only validator from descriptor-held bytes. Independently revalidate the exact persisted v6 chain and Phase 5 closure per D-08/D-13; enumerate the formal and attempt namespaces; reject extra/missing/unregistered run or raw-response leaves; validate every terminal-receipt hash/link; verify all attempt ordinals/digests/root identities and empty ledgers in order per D-14/D-16; validate the separate raw/parsed/ordered-diagnostic/span leaves, distinct findings, non-empty verbatim spans, empty-span failure rule, explicit zero-finding set, and deterministic order for TS-07; independently recompute the D-11 zero formula/partitions and the D-07 empty real-call ledger. Any discrepancy fails and proposes no repair, deletion, reorder, migration, successor approval, or alternate authority.</action>
  <acceptance_criteria>
    - The exact v6 authority and reviewed Phase 5 closure are recomputed from persisted bytes; no predecessor or self-reported substitution passes.
    - The complete declared formal inventory exists with no extra/unregistered run/raw-response leaf, and every receipt link matches raw-byte SHA-256.
    - Raw/parsed/diagnostic/span artifacts remain separate; findings are distinct and deterministically ordered; every surfaced span is non-empty/verbatim; zero findings use the explicit canonical empty set.
    - The ledger is exactly empty; any real-call/cell entry fails; blocked events exist only in failed security_events.
    - The matrix formula, exact integer counts, all A/B/C partitions, empty cells, and conditional TS-11/TS-12 states independently recompute exactly.
    - The complete attempt namespace matches one contiguous ordered immutable chain with no deleted, replaced, reordered, or hidden retry and every ledger empty.
    - The validator performs no write, cleanup, repair, migration, or authority change.
  </acceptance_criteria>
  <verify>
    <automated>.venv/bin/python -c 'import sys; assert sys.version_info &gt;= (3, 12)' &amp;&amp; .venv/bin/ruff --version | rg '^ruff 0\.16\.0$' &amp;&amp; cd experiments/specchoice-v1.3.2 &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution.AuthorizedExecutionTests.test_read_only_audit_recomputes_every_root_and_inventory tests.test_authorized_execution.AuthorizedExecutionTests.test_attempt_chain_rejects_deletion_reorder_and_nonempty_ledgers tests.test_authorized_execution.AuthorizedExecutionTests.test_ts07_distinct_nonempty_spans_and_explicit_empty_set tests.test_authorized_execution.AuthorizedExecutionTests.test_zero_matrix_and_conditional_requirement_states -q</automated>
  </verify>
  <done>The reviewer can independently trace every formal leaf and attempt to exact v6/closure bytes and prove truthful TS-07 lineage, zero calls/cells, and complete immutable retry history.</done>
</task>

<task type="auto">
  <name>05-03-02: Prove exact zero-write replay and close only downstream Red evaluation authority</name>
  <files>experiments/specchoice-v1.3.2/runs/red-execution-v1/, experiments/specchoice-v1.3.2/runs/red-attempts/, experiments/specchoice-v1.3.2/receipts/red-execution-v1.json, experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v1.md</files>
  <read_first>
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-VALIDATION.md
    - experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py
    - experiments/specchoice-v1.3.2/tests/test_authorized_execution.py
    - experiments/specchoice-v1.3.2/receipts/red-execution-v1.json
    - experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v1.md
  </read_first>
  <action>Snapshot exact relative inventory, file bytes/hashes, and write-observable metadata for every attempt, formal leaf, receipt, and Markdown target. Invoke the identical explicit `execute-red` command from Plan 05-02 against the existing targets under the socket guard and write observer; require D-02 byte-identical success with zero writes. Then run the full pinned validation command, closure/no-network/prohibited-claim tests, Ruff 0.16.0, and `git diff --check`. Confirm status exactly `completed`, permission exactly `downstream_red_evidence_evaluation_only`, TS-11/TS-12 still `conditional_not_applicable_red_pending_phase7`, `metrics_emitted=false`, and no placeholder, extraction-success, feasibility-conclusion, external-publication, model/provider/credential/retrieval/network authority, or weakened closure. Any failure leaves Phase 5 unclosed and cannot be normalized by the summary.</action>
  <acceptance_criteria>
    - Identical resume returns the same canonical receipt and every snapshotted byte/hash/metadata value with a zero write-observer count.
    - Occupied/partial/concurrent/mismatched alternatives are already proven fail-closed and cannot be converted into resume.
    - The pinned quick/full suites, Ruff 0.16.0, no-network tests, and `git diff --check` pass; ambient older tools are not cited.
    - The terminal scope authorizes only Phase 6/7 Red evidence evaluation; it does not permanently close TS-11/TS-12 or authorize any real call/publication/final conclusion.
    - No metric, inferred zero performance, placeholder call/cell, extraction success, or feasibility conclusion appears in machine or Markdown evidence.
  </acceptance_criteria>
  <verify>
    <automated>.venv/bin/python -c 'import sys; assert sys.version_info &gt;= (3, 12)' &amp;&amp; .venv/bin/ruff --version | rg '^ruff 0\.16\.0$' &amp;&amp; cd experiments/specchoice-v1.3.2 &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_data_admission tests.test_data_splits tests.test_data_relevance tests.test_data_h2 tests.test_treatments_frame tests.test_treatments_prompts tests.test_treatments_retrieval tests.test_treatments_h3 tests.test_authorized_execution tests.test_canonical tests.test_filesystem_boundary -q &amp;&amp; ../../.venv/bin/ruff check --isolated src/specchoice_execution tests/test_authorized_execution.py &amp;&amp; git diff --check</automated>
  </verify>
  <done>Phase 5 closes only after exact zero-write replay and the pinned full gate prove the immutable Red evidence root without expanding authority or claims.</done>
</task>

</tasks>

## Spec-less Fallback Edge Coverage

| Edge | Resolution | Plan task |
|---|---|---|
| 1 | Findings remain identity-distinct. | 05-01-01, 05-03-01 |
| 2 | Every surfaced finding has at least one non-empty verbatim span. | 05-01-01, 05-03-01 |
| 3 | Raw, parsed, and ordered-diagnostic evidence are separate immutable leaves. | 05-01-01, 05-02-02 |
| 4 | A surfaced empty-span finding fails closed. | 05-01-01 |
| 5 | Zero findings require an explicit canonical empty set. | 05-01-01, 05-03-01 |
| 6 | Finding and diagnostic ordering is deterministic. | 05-01-01, 05-03-01 |
| 7 | Red fixes N_strict=0, repeat_count=0, and expected_cells=0*3*0=0. | 05-01-01, 05-02-02 |
| 8 | A/B/C expected/attempted/completed/failed/retried partitions are all exact zero integers. | 05-01-01, 05-03-01 |
| 9 | cells=[] and no N/A placeholder exists. | 05-01-01, 05-02-02 |
| 10 | Matrix serialization and ordering are canonical and deterministic. | 05-01-01, 05-03-01 |
| 11 | TS-11/TS-12 remain conditional_not_applicable_red_pending_phase7. | 05-01-01, 05-03-02 |
| 12 | Completed ledger is exactly empty; real call/cell fails; blocked events exist only in failed security_events. | 05-01-02, 05-02-01 |
| 13 | Closure proves no unregistered run/raw-response artifact. | 05-02-02, 05-03-01 |
| 14 | Attempt chain is ordered/immutable with exact zero counts and no inferred metrics. | 05-02-01, 05-03-01 |
| 15 | Identical resume is byte-identical/zero-write; occupied, partial, and concurrent targets fail closed. | 05-02-01, 05-03-02 |

**Coverage result:** applicable=15, resolved=15, unresolved=0, explicit=15, backstop=0.

## Multi-Source Coverage Audit

| Source | ID | Feature / constraint | Plan | Status |
|---|---|---|---|---|
| GOAL | — | Complete immutable authorized-branch evidence without unauthorized calls, hidden repair, asymmetric retries, or favorable subsets. | 05-01..03 | COVERED |
| REQ | TS-07 | Distinct surfaced findings with non-empty spans and separate raw/parsed/diagnostic custody. | 05-01, 05-02, 05-03 | COVERED |
| REQ | TS-11 | G/Y-only matrix preserved as exact Red zero boundary and conditional pending-Phase-7 state. | 05-01, 05-02, 05-03 | COVERED |
| REQ | TS-12 | G/Y-only call metadata preserved as truthful empty Red ledger, no-call proofs, and conditional state. | 05-01, 05-02, 05-03 | COVERED |
| RESEARCH | — | Exact v6 authority admission and closure validation before any write. | 05-01, 05-02 | COVERED |
| RESEARCH | — | Three-layer absence proof: empty ledger, structural audit, all-socket tripwire. | 05-01, 05-02 | COVERED |
| RESEARCH | — | Descriptor-bound full-set publication, exact resume, failed custody, and no legacy warning/cleanup semantics. | 05-01, 05-02, 05-03 | COVERED |
| RESEARCH | — | Standard library/current repository primitives only; recorded fail-closed pinned Python/Ruff preflight; no package install. | 05-00..03 | COVERED |
| CONTEXT | D-01 | Exact mutually bound completed contract; no warning completion. | 05-01, 05-02 | COVERED |
| CONTEXT | D-02 | Byte-identical zero-write resume; no overwrite/regeneration. | 05-01, 05-02, 05-03 | COVERED |
| CONTEXT | D-03 | Separate failed custody and all-or-nothing formal set. | 05-02 | COVERED |
| CONTEXT | D-04 | Completion permits only downstream Red evidence evaluation. | 05-01, 05-03 | COVERED |
| CONTEXT | D-05 | One-root three-layer zero-call proof. | 05-01, 05-02 | COVERED |
| CONTEXT | D-06 | Every socket operation fails closed. | 05-01 | COVERED |
| CONTEXT | D-07 | Empty real-call ledger; blocked operations only in security_events. | 05-01, 05-02 | COVERED |
| CONTEXT | D-08 | Bind v6 no-model root and independently scan Phase 5 closure. | 05-01, 05-03 | COVERED |
| CONTEXT | D-09 | Canonical exact Red zero-cell matrix without placeholders. | 05-01, 05-02 | COVERED |
| CONTEXT | D-10 | TS-11/TS-12 conditional pending-Phase-7 state. | 05-01, 05-03 | COVERED |
| CONTEXT | D-11 | Formula/partition zeros and no unregistered run/raw-response. | 05-01, 05-03 | COVERED |
| CONTEXT | D-12 | Canonical JSON authority, deterministic Markdown, no metrics/success claim. | 05-01, 05-02 | COVERED |
| CONTEXT | D-13 | Frozen-byte change requires a versioned successor and new gate. | 05-01, 05-02 | COVERED |
| CONTEXT | D-14 | Complete failed-attempt schema with false authority/metrics declarations. | 05-02, 05-03 | COVERED |
| CONTEXT | D-15 | Successor tooling cannot authorize; new human binding required. | 05-02 | COVERED |
| CONTEXT | D-16 | Every retry is immutable and complete ordered history is terminally bound. | 05-02, 05-03 | COVERED |

<threat_model>
## Trust Boundaries

| Boundary | Description |
|---|---|
| terminal receipt -> independently recomputed evidence graph | Every receipt claim is untrusted until raw bytes, inventories, hashes, schemas, and authorities recompute. |
| attempt namespace -> claimed complete history | Deleted/reordered/replaced attempts or nonempty ledgers can hide favorable retry selection. |
| identical replay -> filesystem | Any write during resume violates immutable evidence even if final bytes appear equal. |
| Red status -> downstream consumers | Conditional G/Y state can be falsely promoted into permanent closure, metrics, or feasibility claims. |

## STRIDE Threat Register — ASVS L1

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|---|---|---|---|---|---|
| T-05-12 | Repudiation / Tampering | terminal receipt and ledger claims | high | mitigate | Recompute every leaf hash/schema, v6/closure root, zero ledger/matrix, and unregistered-artifact inventory independently from descriptor-held bytes. |
| T-05-13 | Tampering | attempt deletion/reordering/replacement | high | mitigate | Reconcile contiguous ordinals and content digests against the complete namespace; reject any gap, reorder, replacement, root mismatch, or nonempty ledger. |
| T-05-14 | Tampering | exact-resume filesystem behavior | high | mitigate | Snapshot inventories/bytes/metadata, rerun the identical command under a write observer, and require zero writes plus byte-identical results. |
| T-05-15 | Elevation of Privilege | authority substitution or closure weakening | high | mitigate | Revalidate only exact v6 and reviewed Phase 5 closure; any mutation requires successor state and cannot be accepted by the audit. |
| T-05-16 | Repudiation | conditional requirement and claim boundary | high | mitigate | Closed matrix/receipt/Markdown tests require the exact pending-Phase-7 status and reject metrics, inferred zero performance, success, conclusion, or broader authority. |
| T-05-SC | Tampering | validation toolchain | high | mitigate | Run only repository-pinned Python >=3.12 and Ruff 0.16.0 with no install/new dependency; ambient older tools cannot close the phase. |
</threat_model>

<verification>
- Independently recompute every v6, closure, formal-leaf, receipt, Markdown, and attempt-chain link from descriptor-held bytes.
- Run identical execution under a write observer and prove byte-identical zero-write resume.
- Run the pinned full predecessor/Phase 5 unittest suite, Ruff 0.16.0, no-network/prohibited-claim checks, and `git diff --check`.
- Confirm 15/15 explicit fallback edges and the complete four-source audit have no missing item.
</verification>

<success_criteria>
- All formal and failed-attempt evidence is complete, immutable, ordered, and independently bound to exact v6 plus the reviewed Phase 5 closure.
- TS-07 raw/parsed/diagnostic/span behavior and every empty/finding/order edge pass.
- TS-11/TS-12 are truthful exact-zero Red evidence and remain conditional pending Phase 7, never falsely completed.
- Replay performs zero writes; partial/occupied/concurrent/mismatched alternatives remain fail-closed.
- Phase 5 authorizes only downstream Red evidence evaluation and emits no model/network call, metrics, feasibility conclusion, or external/public action.
</success_criteria>

<output>
Create `.planning/phases/05-authorized-execution-and-immutable-evidence/05-03-SUMMARY.md` when done.
</output>

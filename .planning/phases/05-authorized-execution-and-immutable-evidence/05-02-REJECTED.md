---
phase: 05-authorized-execution-and-immutable-evidence
plan: 02
type: execute
wave: 2
depends_on:
  - 05-01
files_modified:
  - experiments/specchoice-v1.3.2/src/specchoice_execution/red.py
  - experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py
  - experiments/specchoice-v1.3.2/tests/test_authorized_execution.py
  - experiments/specchoice-v1.3.2/runs/red-attempts/
  - experiments/specchoice-v1.3.2/runs/red-successors/
  - experiments/specchoice-v1.3.2/runs/red-execution-v1/
  - experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v1.md
  - experiments/specchoice-v1.3.2/receipts/red-execution-v1.json
autonomous: false
requirements:
  - TS-07
  - TS-11
  - TS-12
estimate:
  tokens: 42000
  raw_tokens: 42000
  tasks: 3
  confidence: low
must_haves:
  truths:
    - "D-02/D-03: a valid run publishes one complete no-replace formal set; an identical run performs zero writes; mismatch, occupied, partial, symlink, or concurrent state fails closed without repair or overwrite."
    - "D-07/D-14: a blocked socket/model operation never becomes a call ledger row and instead produces a separate immutable non-authoritative failed package with security_events and metrics_emitted=false."
    - "D-13/D-15: frozen-byte drift can create only a versioned successor candidate, difference inventory, and readiness packet; it cannot inherit v6 authority or authorize itself."
    - "D-16: every retry has a fresh immutable ordinal, no attempt is deleted/reordered/overwritten, and the final receipt binds the complete ordered sequence under one unchanged execution root."
    - "D-01/D-05/D-09: formal completion mutually binds exact v6 authority, separate TS-07 leaves, empty ledger, structural/runtime proofs, Red trigger, zero-cell matrix, attempt chain, and terminal receipt."
    - "TS-11/TS-12 remain conditional_not_applicable_red_pending_phase7; Phase 5 executes no real model/cell and cannot claim permanent G/Y closure."
    - "A clean successful first formal attempt leaves runs/red-attempts/ and runs/red-successors/ absent; if needed, those are the only repository targets for immutable failed attempts and non-authoritative successor candidates respectively."
  artifacts:
    - path: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py
      provides: "Immutable failed-attempt/retry/successor state machine plus final Red publication and exact-resume validation."
    - path: experiments/specchoice-v1.3.2/runs/red-attempts/
      provides: "Conditional sole repository namespace for immutable non-authoritative failed attempts; absent after a clean successful first attempt."
    - path: experiments/specchoice-v1.3.2/runs/red-successors/
      provides: "Conditional sole repository namespace for decision-free non-authoritative successor candidates; absent after a clean successful first attempt."
    - path: experiments/specchoice-v1.3.2/runs/red-execution-v1/
      provides: "Complete formal Red evidence directory containing separate raw/parsed/diagnostic/span, ledger, audit, trigger, matrix, and attempt-chain leaves."
    - path: experiments/specchoice-v1.3.2/receipts/red-execution-v1.json
      provides: "Canonical terminal receipt binding every formal leaf and the complete ordered attempt sequence."
    - path: experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v1.md
      provides: "Deterministic non-authoritative Markdown projection of the canonical receipt and Red conditional state."
  key_links:
    - from: experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json
      to: experiments/specchoice-v1.3.2/runs/red-execution-v1/
      via: "the reviewed target inventory and closure are revalidated immediately before descriptor-bound full-set publication"
      pattern: "write_exact_descriptor_files"
    - from: experiments/specchoice-v1.3.2/runs/red-attempts/
      to: experiments/specchoice-v1.3.2/receipts/red-execution-v1.json
      via: "canonical strictly increasing attempt ordinals and per-attempt empty-ledger hashes"
      pattern: "attempt_chain"
    - from: experiments/specchoice-v1.3.2/runs/red-successors/
      to: experiments/specchoice-v1.3.2/src/specchoice_execution/red.py
      via: "drift may create only a decision-free candidate/difference/readiness package and never a successor authority"
      pattern: "authoritative=false|metrics_emitted=false"
    - from: experiments/specchoice-v1.3.2/runs/red-execution-v1/model-call-ledger.json
      to: experiments/specchoice-v1.3.2/receipts/red-execution-v1.json
      via: "raw-byte SHA-256 binding under the same root as structural/runtime no-call audits"
      pattern: "model_call_ledger_sha256"
    - from: experiments/specchoice-v1.3.2/runs/red-execution-v1/matrix-manifest.json
      to: experiments/specchoice-v1.3.2/receipts/red-execution-v1.json
      via: "canonical Red zero formula, treatment partitions, empty cells, and conditional requirement states"
      pattern: "conditional_not_applicable_red_pending_phase7"
  prohibitions:
    - statement: "Formal evidence is never partial, overwritten, repaired in place, downgraded to completed_with_warnings, or substituted by a favorable retry."
      status: planned
      verification: "fault-injection/no-replace tests and complete ordered attempt binding"
    - statement: "Failed attempts are never deleted or reordered, and security events never masquerade as completed real calls."
      status: planned
      verification: "append-only attempt validator and ledger/security-event separation tests"
    - statement: "No N/A placeholder call/cell, real call, raw model response, model metric, extraction-success claim, or feasibility conclusion is emitted."
      status: planned
      verification: "closed output schemas and formal-root inventory validation"
---

## Phase Goal

**As a** reviewer, **I want to** inspect a complete immutable Red no-call evidence chain, **so that** downstream evaluation can proceed without unauthorized calls, hidden repair, asymmetric retries, or favorable-subset execution.

<objective>
Finish the immutable failure/retry/successor lifecycle, then execute the exact reviewed Red contract once and publish its complete canonical evidence set without any model or network call.

Purpose: Turn the approved temporary tracer into durable Red evidence while preserving every failure, forbidding authority inheritance after drift, and making formal completion an all-or-nothing descriptor-bound operation.
Output: Final lifecycle code/tests, zero or more immutable failed-attempt packages when faults occur, and one complete formal Red evidence directory plus terminal receipt/Markdown on success.
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
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-PATTERNS.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-01-SUMMARY.md
@experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json
@experiments/specchoice-v1.3.2/src/specchoice_execution/red.py
@experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py
@experiments/specchoice-v1.3.2/tests/test_authorized_execution.py
@experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py
@experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py

<interfaces>
- Keep the Plan 05-01 closed policy and evidence schemas byte-compatible; the approved checkpoint covers those public on-disk semantics.
- Implement failed-attempt and successor construction behind the existing `execute-red` contract; no alternate model/retrieval command or fallback authority is permitted.
- Publish every file set through `write_exact_descriptor_files`; validate existing exact bytes as resume and classify any mismatch/occupancy/partial/concurrency state as a stable failure.
- Read the Phase 4 and Phase 5 closure once through held descriptors, carry those bytes through validation and receipt binding, and never reopen pathname leaves to construct self-claims.
</interfaces>
</context>

## Artifacts this phase produces

- Conditional attempt namespace: `runs/red-attempts/attempt-<six-digit-ordinal>/` containing `attempt.json`, `frozen-inputs.json`, `observed-differences.json`, `ordered-diagnostics.json`, `model-call-ledger.json`, `security-events.json`, and `raw-custody.json`; it is the only allowed repository target for immutable failed attempts, and each package is immutable, `authoritative=false`, and `metrics_emitted=false`.
- Conditional successor namespace: `runs/red-successors/successor-<version>/` containing candidate closure, exact difference inventory, and decision-free readiness only; it is the only allowed repository target for non-authoritative successor candidates, and no authority leaf is produced.
- On a clean successful first attempt, neither conditional namespace is created; absence is the expected state rather than an empty directory or placeholder package.
- Formal leaves under `runs/red-execution-v1/`: `raw-evidence.json`, `parsed-evidence.json`, `ordered-diagnostics.json`, `evidence-span-audit.json`, `model-call-ledger.json`, `no-call-structural-audit.json`, `no-call-runtime-audit.json`, `red-trigger-evidence.json`, `matrix-manifest.json`, and `attempt-chain.json`.
- Terminal artifacts: `receipts/red-execution-v1.json` and deterministic `reports/red-execution/red-execution-v1.md`.
- Formal status: exactly `completed`; authority scope: exactly `downstream_red_evidence_evaluation_only`; TS-11/TS-12: exactly `conditional_not_applicable_red_pending_phase7`.

<tasks>

<task type="auto" tdd="true">
  <name>05-02-01: Preserve every failure, retry, and drift successor without authority substitution</name>
  <precondition>The Plan 05-01 evidence-contract checkpoint was explicitly approved, its policy/source/test bytes are present, and repository-pinned Python >=3.12 plus Ruff 0.16.0 are available; no network installation or ambient-tool substitution is allowed.</precondition>
  <files>experiments/specchoice-v1.3.2/src/specchoice_execution/red.py, experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py, experiments/specchoice-v1.3.2/tests/test_authorized_execution.py, experiments/specchoice-v1.3.2/runs/red-attempts/, experiments/specchoice-v1.3.2/runs/red-successors/</files>
  <read_first>
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-01-SUMMARY.md
    - experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json
    - experiments/specchoice-v1.3.2/src/specchoice_execution/red.py
    - experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py
    - experiments/specchoice-v1.3.2/tests/test_authorized_execution.py
    - experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py
    - experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py
    - experiments/specchoice-v1.3.2/src/specchoice_measurement/attempts.py
  </read_first>
  <behavior>
    - "Test 1 — D-03/D-14: authority drift, closure drift, socket denial, runtime fault, occupied/partial/concurrent formal targets, and interrupted publication each produce a complete immutable failed package and no authoritative formal receipt."
    - "Test 2 — D-07: failed packages keep the real-call ledger exactly empty; denied operations appear only as ordered security_events with raw custody hashes where bytes existed."
    - "Test 3 — D-16: retries use strictly increasing six-digit ordinals, preserve every prior byte, reject gaps/duplicates/reordering/deletion, and require the identical execution root/policy/input hashes."
    - "Test 4 — D-13/D-15: changed frozen bytes create only a versioned decision-free successor candidate/diff/readiness; v6 remains immutable history and no machine path can create successor authority."
    - "Test 5 — D-02: exact existing attempt/formal bytes are validated read-only; any divergent byte fails without overwrite, cleanup, or regeneration."
    - "Test 6: a clean successful first attempt leaves both conditional namespaces absent; failures can write only under runs/red-attempts/, and drift successor candidates can write only under runs/red-successors/."
  </behavior>
  <action>
1. Add fault-injection tests before implementation for every behavior above. Use temporary roots and write observers; include symlink/path escape, occupied leaf, partial set, concurrent creator, interrupted publication, authority/closure drift, all-socket denial, duplicate ordinal, missing ordinal, reordered chain, deleted prior attempt, and divergent exact-resume cases.
2. Implement a new closed Red-specific attempt state machine per D-03/D-14/D-16. Allocate the next six-digit ordinal only from a descriptor-enumerated contiguous prior chain; build the complete failure payload in memory; require attempt identity, exact frozen inventory/hashes, expected/observed difference, stable ordered diagnostics, termination stage, empty real-call ledger, separate security_events, raw byte hashes/custody paths, `authoritative=false`, and `metrics_emitted=false`; publish once with no-replace semantics only below `runs/red-attempts/`, the sole repository failed-attempt namespace. Never call the incompatible legacy cleanup/warning writer.
3. Distinguish runtime fault from frozen drift per D-13. An unchanged-input runtime retry may use the same execution root but must be a new immutable ordinal. Frozen authority/source/schema/CLI/policy/network/evidence-structure drift must stop, preserve the failure, and construct only a new versioned successor candidate, exact difference inventory, and machine readiness packet below `runs/red-successors/`, the sole repository successor-candidate namespace, per D-15; expose no authorizer, decision default, or authority writer.
4. Validate every prior attempt from held bytes before retry or success. Reject deletion, reordering, replacement, ordinal gaps/duplicates, differing input/policy roots, any nonempty real-call ledger, or any prior authoritative/metrics claim. Bind the exact ordered attempt digests into the later successful receipt.
5. Exercise a clean successful first attempt in a temporary root and assert that no empty `red-attempts` or `red-successors` directory is materialized. The namespaces are conditional custody only: absence is required until a real failure or drift candidate must be preserved.
  </action>
  <acceptance_criteria>
    - Every modeled pre-completion failure leaves a complete immutable non-authoritative package and no formal receipt.
    - Failed packages contain exact zero integer counts, an exactly empty real-call ledger, ordered security_events/diagnostics, raw custody where applicable, and no inferred metric.
    - Blocked calls appear only in security_events; no placeholder or blocked event is copied into the real-call ledger.
    - Retries never delete, overwrite, reorder, reuse, merge, or hide an attempt; the ordered chain is contiguous and content-bound.
    - Runtime retry requires identical inputs/policy; closure drift produces only a versioned successor candidate/diff/readiness and requires a new human gate.
    - `runs/red-attempts/` and `runs/red-successors/` remain absent on a clean successful first attempt and are the only allowed repository targets for failed attempts and non-authoritative successor candidates respectively.
    - Occupied, partial, symlink, path-escape, interrupted, or concurrently created targets fail closed without repair or cleanup.
    - The legacy `completed_with_warnings` and staging-deletion semantics are neither imported nor reproduced.
  </acceptance_criteria>
  <verify>
    <automated>.venv/bin/python -c 'import sys; assert sys.version_info &gt;= (3, 12)' &amp;&amp; .venv/bin/ruff --version | rg '^ruff 0\.16\.0$' &amp;&amp; cd experiments/specchoice-v1.3.2 &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution.AuthorizedExecutionTests.test_every_failure_has_immutable_non_authoritative_custody tests.test_authorized_execution.AuthorizedExecutionTests.test_retries_are_contiguous_append_only_and_input_identical tests.test_authorized_execution.AuthorizedExecutionTests.test_drift_builds_decision_free_successor_only tests.test_authorized_execution.AuthorizedExecutionTests.test_clean_success_leaves_conditional_namespaces_absent_and_roles_confined tests.test_authorized_execution.AuthorizedExecutionTests.test_occupied_partial_symlink_interrupted_and_concurrent_targets_fail_closed tests.test_filesystem_boundary -q &amp;&amp; ../../.venv/bin/ruff check --isolated src/specchoice_execution tests/test_authorized_execution.py</automated>
  </verify>
  <done>Every failure and retry is immutable and truthfully ordered, drift cannot substitute authority, and no failed state can occupy or repair the formal evidence boundary.</done>
</task>

<task type="checkpoint:decision" gate="blocking-human">
  <name>05-02-02: Confirm the final frozen closure before one-way publication</name>
  <files>experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json, experiments/specchoice-v1.3.2/src/specchoice_execution/red.py, experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py, experiments/specchoice-v1.3.2/tests/test_authorized_execution.py</files>
  <read_first>
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-01-SUMMARY.md
    - experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json
    - experiments/specchoice-v1.3.2/src/specchoice_execution/red.py
    - experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py
    - experiments/specchoice-v1.3.2/tests/test_authorized_execution.py
  </read_first>
  <decision>Confirm that the final post-failure-state implementation still matches the already approved D-01/D-05/D-09/D-13 schema, target inventory, closure, and no-call policy before immutable formal publication.</decision>
  <context>The preceding task finalized retry/failure/successor behavior and therefore changed frozen implementation bytes after the first contract checkpoint. Publication is one-way: an incorrect final closure cannot be repaired in place and must use a versioned successor plus another human gate.</context>
  <options>
    <option id="confirm-final-closure">
      <name>Confirm final closure</name>
      <pros>Permits one formal publication using the displayed final hashes and unchanged reviewed semantics.</pros>
      <cons>Any later frozen-byte or schema change requires a successor and complete revalidation.</cons>
    </option>
    <option id="reject-final-closure">
      <name>Reject final closure</name>
      <pros>Keeps formal targets absent while a versioned correction is prepared.</pros>
      <cons>Publication stops and the revised bytes must repeat the contract and final-closure gates.</cons>
    </option>
  </options>
  <action>Run the full focused pinned-toolchain suite and compute the final canonical policy, source, CLI, test, v6 authority, output-inventory, and forbidden-surface hashes without writing any formal target. Present the exact delta from the Plan 05-01 approved closure and prove it is limited to the reviewed failed-attempt/retry/successor implementation while all on-disk evidence schemas, Red zero semantics, conditional requirement states, socket policy, and publication targets remain unchanged. Record only the explicit checkpoint choice; do not infer approval or create a self-authorizing evidence leaf.</action>
  <acceptance_criteria>
    - Final closure hashes and the exact delta from the earlier approved tracer are displayed before publication.
    - Any schema, policy, target, authority, call-surface, zero-matrix, or conditional-state drift forces rejection and a versioned successor.
    - Confirmation grants only publication of the exact final Red closure and no broader model/network/evaluation/public authority.
    - Silence or failed verification leaves every formal target absent.
  </acceptance_criteria>
  <verify>
    <automated>cd experiments/specchoice-v1.3.2 &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution tests.test_treatments_h3 tests.test_canonical tests.test_filesystem_boundary -q &amp;&amp; ../../.venv/bin/ruff check --isolated src/specchoice_execution tests/test_authorized_execution.py</automated>
  </verify>
  <done>The human confirms the exact final closure for one-way publication, or execution stops with formal targets absent.</done>
  <resume-signal>Select `confirm-final-closure` to publish, or `reject-final-closure` and describe the required versioned correction.</resume-signal>
</task>

<task type="auto">
  <name>05-02-03: Execute and atomically publish the exact Red formal evidence set</name>
  <precondition>The reviewed Phase 5 policy/source/test closure and exact Phase 4 v6 authority chain validate under repository-pinned `.venv`; `runs/red-execution-v1/`, `receipts/red-execution-v1.json`, and `reports/red-execution/red-execution-v1.md` are either all absent or already form the exact valid byte-identical set, while any existing `runs/red-attempts/` or `runs/red-successors/` content validates as immutable conditional custody.</precondition>
  <reversibility rating="one-way">D-01/D-05/D-09/D-13 make this publication root immutable; changing its completion, no-call, matrix, or closure semantics requires a versioned successor and new human gate.</reversibility>
  <files>experiments/specchoice-v1.3.2/runs/red-attempts/, experiments/specchoice-v1.3.2/runs/red-successors/, experiments/specchoice-v1.3.2/runs/red-execution-v1/, experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v1.md, experiments/specchoice-v1.3.2/receipts/red-execution-v1.json</files>
  <read_first>
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-01-SUMMARY.md
    - experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json
    - experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json
    - experiments/specchoice-v1.3.2/reports/h3/h3-red-review-v6/review-packet.json
    - experiments/specchoice-v1.3.2/receipts/h3-branch-readiness-v6.json
    - experiments/specchoice-v1.3.2/reviews/h3-branch-decision-v6.json
    - experiments/specchoice-v1.3.2/src/specchoice_execution/red.py
    - experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py
    - experiments/specchoice-v1.3.2/tests/test_authorized_execution.py
  </read_first>
  <action>
1. Under pinned `.venv`, run the focused/full predecessor tests and Ruff before formal execution. Invoke the sole `execute-red` CLI with explicit repository-relative experiment root, policy, exact v6 authority/packet/readiness/decision inputs, attempt namespace, formal root, receipt, and Markdown target. The command itself must install the all-socket guard before admission and perform no network, process spawn, provider/model, credentials, or production retrieval action.
2. Revalidate the exact v6 chain and reviewed Phase 5 closure immediately before any writer opens per D-01/D-08/D-13. Build every formal leaf and terminal receipt in memory; validate closed schemas, raw-byte hashes, TS-07 spans/order/empty-set behavior, empty call ledger, structural/runtime proof roots, Red trigger custody, exact zero matrix/partitions, conditional TS-11/TS-12 states, complete prior attempt chain, and downstream-only permission per D-04/D-05/D-09/D-10/D-11/D-12/D-16.
3. Publish the complete declared formal set, receipt, and deterministic Markdown together using descriptor-bound no-replace file-set publication per D-02/D-03. If any fault or target conflict occurs, create the next immutable failed attempt only below `runs/red-attempts/` and stop with no valid terminal receipt; frozen drift may additionally create only a non-authoritative candidate below `runs/red-successors/`. Never repair a partial target or write either custody role elsewhere. If the exact set already exists, descriptor-read and validate every byte/link and return success with zero writes.
4. Reopen every published leaf through held descriptors, recompute the receipt and full inventory, assert status exactly `completed`, scope exactly `downstream_red_evidence_evaluation_only`, all attempt ledgers empty, no security events in the successful attempt, no unregistered run/raw-response leaf, no placeholders/metrics/conclusion, and then print only the canonical validated receipt to stdout.
5. When the first formal attempt succeeds without fault or drift, assert both conditional custody namespaces remain absent; do not create empty directories, placeholder attempts, or placeholder successor candidates.
  </action>
  <acceptance_criteria>
    - The formal set contains all ten declared machine leaves, one terminal receipt, and one deterministic Markdown projection; missing or extra formal leaves block completion.
    - Raw evidence, parsed evidence, ordered diagnostics, and evidence-span audit are separate immutable leaves with exact hashes and deterministic order.
    - Findings remain distinct; every surfaced finding has a non-empty verbatim raw-byte span; zero findings are an explicit canonical empty set.
    - The completed real-call ledger is exactly empty; any call/cell entry fails; blocked attempts remain only in failed-attempt security_events.
    - The matrix has exact integer zeros, `cells=[]`, no placeholder, deterministic canonical order, and both G/Y requirement states pending Phase 7.
    - The receipt proves no unregistered run/raw-response artifact and binds the complete ordered immutable attempt chain with every ledger empty.
    - Status is exactly `completed`; `completed_with_warnings`, formal partial evidence, inferred metrics, extraction success, feasibility conclusion, and broader authority are invalid.
    - Identical existing bytes resume with zero writes; occupied, partial, symlink, path-escape, interrupted, or concurrent targets fail closed without overwrite.
    - A clean successful first attempt leaves both conditional custody namespaces absent; any failed attempt or successor candidate is confined to its one declared repository namespace.
  </acceptance_criteria>
  <verify>
    <automated>.venv/bin/python -c 'import sys; assert sys.version_info &gt;= (3, 12)' &amp;&amp; .venv/bin/ruff --version | rg '^ruff 0\.16\.0$' &amp;&amp; cd experiments/specchoice-v1.3.2 &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_execution.cli execute-red --experiment-root . --policy config/execution/red-execution-policy-v1.json --authority phase4/branch-authority-v6.json --packet reports/h3/h3-red-review-v6/review-packet.json --readiness receipts/h3-branch-readiness-v6.json --decision reviews/h3-branch-decision-v6.json --attempt-root runs/red-attempts --formal-root runs/red-execution-v1 --receipt receipts/red-execution-v1.json --report reports/red-execution/red-execution-v1.md &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution tests.test_treatments_h3 tests.test_canonical tests.test_filesystem_boundary -q &amp;&amp; ../../.venv/bin/ruff check --isolated src/specchoice_execution tests/test_authorized_execution.py</automated>
  </verify>
  <done>The reviewed exact Red contract is published once as a complete mutually bound immutable evidence set, or execution stops with a separate failed attempt and no valid formal completion.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|---|---|
| closure/authority -> attempt state machine | Drift and runtime faults must be distinguished without inheriting or expanding authority. |
| attempt namespace -> retry/final receipt | Existing attempts are untrusted until descriptor-read, hash-validated, contiguous, ordered, and proven to have empty ledgers. |
| in-memory complete payload -> filesystem formal boundary | Path escape, symlink, occupancy, partial writes, interruption, and concurrency can corrupt or replace immutable evidence. |
| ledger/security events -> reviewer claims | A false empty ledger or hidden blocked event would misrepresent real-call behavior. |

## STRIDE Threat Register — ASVS L1

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|---|---|---|---|---|---|
| T-05-06 | Tampering | descriptor-bound paths and symlinks | high | mitigate | Validate repository-relative paths through held parent descriptors; reject traversal, symlink, special, and substituted leaves in focused filesystem tests. |
| T-05-07 | Tampering / Denial of Service | formal no-replace publication | high | mitigate | Prevalidate the full set, publish through `write_exact_descriptor_files`, require terminal receipt for authority, and fault-test occupied/partial/interrupted/concurrent targets without overwrite. |
| T-05-08 | Repudiation / Tampering | call ledger and security events | high | mitigate | Require an exactly empty real-call ledger for success; route every blocked operation only to a failed package security_event and bind both schemas independently. |
| T-05-09 | Repudiation / Tampering | attempt history | high | mitigate | Descriptor-enumerate contiguous ordinals, hash every package, reject deletion/reorder/gap/duplicate/root mismatch, and bind the full ordered chain in the terminal receipt. |
| T-05-10 | Elevation of Privilege | successor authority | high | mitigate | Drift tooling emits candidate/diff/readiness only; no successor authority writer exists, and tests require a new human gate before changed bytes can execute. |
| T-05-11 | Tampering | closure recheck at publication | high | mitigate | Recompute exact v6 plus Phase 5 closure immediately before the writer opens and again from descriptor-held published bytes; any mismatch fails the attempt. |
| T-05-SC | Tampering | dependency and package surface | high | mitigate | Install nothing; keep standard-library/repository imports closed and run Ruff/static closure tests under the pinned toolchain before formal execution. |
</threat_model>

<verification>
- Pinned Python/Ruff checks pass, followed by failed-attempt/retry/successor, occupancy/partial/concurrency, filesystem, exact v6, and full formal execution tests.
- The actual `execute-red` command returns a canonical validated receipt without any network/model/provider/retrieval call.
- Every formal target is complete and exact, or no terminal receipt exists and a separate failed package explains the stop.
- `git diff --check` passes; no out-of-boundary file, dependency, frontend/UI, or external integration is added.
</verification>

<success_criteria>
- Failed attempts are immutable, non-authoritative, complete, ordered, and never cleaned up or hidden by retries.
- Drift cannot reuse v6 authority and produces only a decision-free successor candidate requiring a new human gate.
- The complete Red evidence set truthfully proves zero calls/cells, separate TS-07 custody, no unregistered artifacts, and conditional G/Y states.
- Formal publication is no-replace and exact-resumable; overwrite, partial, path/symlink, interruption, and concurrency hazards fail closed.
- Phase completion grants only Phase 6/7 Red evidence evaluation and emits no metrics or feasibility conclusion.
</success_criteria>

<output>
Create `.planning/phases/05-authorized-execution-and-immutable-evidence/05-02-SUMMARY.md` when done.
</output>

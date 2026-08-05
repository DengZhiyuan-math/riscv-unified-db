---
phase: 05-authorized-execution-and-immutable-evidence
plan: 06
type: execute
wave: 4
depends_on:
  - 05-05
files_modified:
  - experiments/specchoice-v1.3.2/validation/guarded_regress.py
  - experiments/specchoice-v1.3.2/tests/test_guarded_regress.py
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
    - "D-01/D-04: an independent read-only audit recomputes the complete successor root and confirms that completed grants only downstream Red-evidence evaluation."
    - "D-02/D-03: the identical production invocation returns the same receipt with zero writes; the audit performs no repair, replacement, cleanup, migration, or new evidence publication."
    - "D-05/D-06/D-07/D-08: the exact v6 and successor closure, empty ledger, structural audit, and all-socket runtime proof independently validate with no unregistered call surface."
    - "D-09/D-10/D-11/D-12: the matrix and reports retain all exact Red zeros, canonical authority/projection separation, and conditional_not_applicable_red_pending_phase7 without metrics or success claims."
    - "D-13/D-14/D-15/D-16: every failed or successful attempt is present in immutable ordinal order with an empty ledger; drift or changed bytes cannot be audited into current authority."
    - "D-08/D-13: the audit independently rebuilds the external non-circular Gate-A projection and requires distinct receipt fields for raw policy, runtime closure, and approved projection; no self-referential policy or closure can validate."
    - "TS-07 raw, parsed, ordered-diagnostic, and span-audit leaves independently bind to exact source bytes; zero findings remain an explicit canonical empty set."
    - "TS-11/TS-12 remain limited Red evidence pending Phase 7; the audit does not permanently close them or authorize a G/Y run."
    - "The final repository-wide regression runs twice only through one repository-local native-guard harness after actual formal v2 publication and the read-only successor audits; each run proves the exact formal-root/receipt/report inventory and SHA-256 map unchanged, and missing/nonfunctional confinement, prohibited activity, install-surface mutation, or regression failure blocks Phase 5 closure without weakening the separate execute-red all-socket tripwire."
  artifacts:
    - path: experiments/specchoice-v1.3.2/runs/red-execution-v2/
      provides: "Read-only verified formal successor evidence root; this plan does not modify it."
    - path: experiments/specchoice-v1.3.2/receipts/red-execution-v2.json
      provides: "Read-only verified terminal receipt and complete attempt-chain binding."
    - path: experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v2.md
      provides: "Read-only verified deterministic projection."
    - path: experiments/specchoice-v1.3.2/validation/guarded_regress.py
      provides: "Validation-only macOS sandbox-exec harness that admits only the exact repository-wide regression command, denies network and installation-surface writes, and proves v2 evidence inventory/hash immutability before and after each run."
    - path: experiments/specchoice-v1.3.2/tests/test_guarded_regress.py
      provides: "Standard-library contract tests for unavailable/nonfunctional guard, prohibited-operation failure, exact evidence mutation detection, and a no-network fake-command success path."
  key_links:
    - from: experiments/specchoice-v1.3.2/receipts/red-execution-v2.json
      to: experiments/specchoice-v1.3.2/runs/red-execution-v2/
      via: "Independent descriptor-held inventory, schema, and raw SHA-256 recomputation rather than receipt self-claims."
      pattern: "completed|downstream_red_evidence_evaluation_only"
    - from: experiments/specchoice-v1.3.2/runs/red-execution-v2/attempt-chain.json
      to: experiments/specchoice-v1.3.2/runs/red-attempts-v2/
      via: "Complete contiguous ordinal/digest reconciliation, including the clean no-prior-failure case."
      pattern: "attempt_chain|model_call_ledger_sha256"
    - from: experiments/specchoice-v1.3.2/runs/red-execution-v2/matrix-manifest.json
      to: experiments/specchoice-v1.3.2/runs/red-execution-v2/model-call-ledger.json
      via: "Independent zero-cell and zero-real-call validation under the same terminal root."
      pattern: "conditional_not_applicable_red_pending_phase7|calls"
    - from: experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v2.json
      to: experiments/specchoice-v1.3.2/receipts/red-execution-v2.json
      via: "Descriptor-read raw policy identity and sorted non-policy entries rebuild the approved external projection; receipt self-claims are not accepted as inputs."
      pattern: "policy_sha256|runtime_closure_sha256|gate_a_projection_sha256"
    - from: experiments/specchoice-v1.3.2/validation/guarded_regress.py
      to: bin/regress
      via: "The production CLI has no caller-selected command and launches exactly ./bin/regress --all through a functionally preflighted /usr/bin/sandbox-exec profile; no bare fallback exists."
      pattern: "sandbox-exec|./bin/regress|--all"
    - from: experiments/specchoice-v1.3.2/validation/guarded_regress.py
      to: experiments/specchoice-v1.3.2/runs/red-execution-v2/
      via: "Each guarded run requires the exact ten formal filenames plus receipt and report, records repository-relative inventory and SHA-256 before and after, and fails on any change, addition, or removal."
      pattern: "attempt-chain.json|evidence-span-audit.json|matrix-manifest.json|model-call-ledger.json|no-call-runtime-audit.json|no-call-structural-audit.json|ordered-diagnostics.json|parsed-evidence.json|raw-evidence.json|red-trigger-evidence.json"
---

## Phase Goal

**As a** reviewer, **I want to** inspect a complete immutable Red no-call evidence chain, **so that** downstream evaluation can proceed without unauthorized calls, hidden repair, asymmetric retries, or favorable-subset execution.

<objective>
Independently audit the complete successor formal evidence and attempt graph, prove that the identical production command exact-resumes with zero writes, and run the repository-wide release gate twice through a fail-closed native confinement harness that preserves the exact v2 evidence inventory and limited downstream Red-evidence authority.

Purpose: Close Phase 5 by recomputation from held bytes rather than trusting terminal self-claims, while preserving every historical and formal byte.
Output: A repository-local guarded-regression harness and its contract tests plus a passing `05-06-SUMMARY.md` execution record; no new or modified formal, attempt, successor, execution-source, policy, requirement, or authority artifact.
</objective>

<execution_context>
Follow the repository-configured GSD execute-plan and summary contracts; every audit path and command argument is repository-relative.
</execution_context>

<context>
@AGENTS.md
@.planning/PROJECT.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-SUCCESSOR-RESEARCH.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-VALIDATION.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-02-CANCELLATION.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-04-SUMMARY.md
@.planning/phases/05-authorized-execution-and-immutable-evidence/05-05-SUMMARY.md
@experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v2.json
@experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py
@experiments/specchoice-v1.3.2/src/specchoice_execution/cli_v2.py
@experiments/specchoice-v1.3.2/tests/test_authorized_execution_v2.py
@experiments/specchoice-v1.3.2/runs/red-execution-v2/
@experiments/specchoice-v1.3.2/receipts/red-execution-v2.json
@experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v2.md

<interfaces>
- Use the existing successor read-only validator and the exact production command from 05-05; do not add an auditor module or change the frozen closure after publication.
- Read every formal, authority, policy, and attempt leaf through descriptor-held repository primitives, then recompute schemas, canonical bytes, inventories, and SHA-256 links independently.
- Reconstruct the exact `red-execution-runtime-closure-basis-v2` and `red-execution-gate-a-projection-v2` contracts from raw persisted inputs, never from terminal receipt values. The raw policy must have no own final digest/length; the policy path occurs only in the external policy entry; projection/summary/checkpoint/receipt/report/future-output bytes never enter the closure basis. Compare external `gate_a_projection_sha256` with both gate summaries and require the receipt to expose separate `policy_sha256`, `runtime_closure_sha256`, and `gate_a_projection_sha256` fields.
- Treat `runs/red-attempts-v2` as optional only when the terminal chain proves no earlier failure; if present, every attempt directory and leaf must reconcile exactly. `runs/red-successors-v2` is incompatible with current formal success unless a later separately approved contract explicitly supersedes this one.
- `validation/guarded_regress.py` is validation-only and outside the formal v2 policy/runtime closure. Neither `red_v2.py` nor `cli_v2.py` may import, call, or authorize it. Its only production subprocess boundary is the fixed argv `./bin/regress --all` launched through `/usr/bin/sandbox-exec`; this separate release guard complements, and never replaces or broadens, the formal `execute-red` all-socket/no-subprocess tripwire.
- The summary is an execution record, not evidence authority. It cannot normalize an audit failure, close TS-11/TS-12, or replace a formal leaf.
</interfaces>
</context>

## Artifacts Produced

- `experiments/specchoice-v1.3.2/validation/guarded_regress.py` and `experiments/specchoice-v1.3.2/tests/test_guarded_regress.py` as non-authorizing validation infrastructure outside the formal successor closure.
- No new formal, attempt, drift-successor, execution-source, policy, authority, receipt, report, or requirement artifact.
- `.planning/phases/05-authorized-execution-and-immutable-evidence/05-06-SUMMARY.md` only, recording the commands and results after successful read-only verification; it is not part of the evidence root.

## Scope Non-Goals

- Do not rewrite, repair, delete, reorder, replace, migrate, regenerate, or add any formal/attempt/successor leaf.
- Do not alter predecessor or successor execution source/policy/tests, Phase 4 authority, historical plan records, dependencies, roadmap semantics, or evidence schemas; the two new validation files remain unreachable from formal execution.
- Do not create calls, cells, placeholders, metrics, extraction-success or feasibility claims, external/public actions, model/provider/credential/retrieval/network surfaces, or permanent G/Y requirement closure. The validation harness has one closed process boundary solely for the guarded release command and creates no general command runner.

<tasks>

<task type="tracer">
  <name>05-06-01: Trace the complete successor authority, evidence, and attempt graph read-only</name>
  <precondition>`05-05-SUMMARY.md` records explicit Gate A and Gate B approval plus a complete validated successor formal root; absent, partial, drifted, or rejected publication is a blocking failure and must not be repaired by this audit.</precondition>
  <files>experiments/specchoice-v1.3.2/runs/red-execution-v2/, experiments/specchoice-v1.3.2/runs/red-attempts-v2/, experiments/specchoice-v1.3.2/runs/red-successors-v2/, experiments/specchoice-v1.3.2/receipts/red-execution-v2.json, experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v2.md</files>
  <read_first>
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-SUCCESSOR-RESEARCH.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-02-CANCELLATION.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-04-SUMMARY.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-05-SUMMARY.md
    - experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v2.json
    - experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py
    - experiments/specchoice-v1.3.2/src/specchoice_execution/cli_v2.py
    - experiments/specchoice-v1.3.2/tests/test_authorized_execution_v2.py
    - experiments/specchoice-v1.3.2/phase3/data-authority-v1.json
    - experiments/specchoice-v1.3.2/phase4/branch-authority-v6.json
    - experiments/specchoice-v1.3.2/reports/h3/h3-red-review-v6/review-packet.json
    - experiments/specchoice-v1.3.2/receipts/h3-branch-readiness-v6.json
    - experiments/specchoice-v1.3.2/reviews/h3-branch-decision-v6.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v2/attempt-chain.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v2/evidence-span-audit.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v2/matrix-manifest.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v2/model-call-ledger.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v2/no-call-runtime-audit.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v2/no-call-structural-audit.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v2/ordered-diagnostics.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v2/parsed-evidence.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v2/raw-evidence.json
    - experiments/specchoice-v1.3.2/runs/red-execution-v2/red-trigger-evidence.json
    - experiments/specchoice-v1.3.2/receipts/red-execution-v2.json
    - experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v2.md
  </read_first>
  <action>
1. Snapshot the complete formal, optional attempt, receipt, and Markdown namespaces before reading. Run the successor validator read-only from held descriptors. Rebuild the raw policy entry, lexicographically sorted non-policy closure entries, canonical runtime-closure basis/hash, and canonical external Gate-A projection bytes/hash; compare those bytes/hash with both gate summaries and the terminal receipt per D-01/D-05/D-08/D-13/D-15. Require separate matching `policy_sha256`, `runtime_closure_sha256`, and `gate_a_projection_sha256` fields. Reject raw-policy own digest/length, policy-path duplication, projection/basis/receipt/output recursion, field aliasing, predecessor, copied, self-reported, stale, or drifted authority/closure input.
2. Enumerate exactly the ten formal leaves plus receipt and Markdown. Recompute canonical bytes and raw SHA-256 for every leaf; reject missing, extra, unregistered run/raw-response, symlink, traversal, special-file, or substituted content. Validate canonical JSON as authority and Markdown as a deterministic non-authoritative projection per D-03/D-12.
3. Recompute TS-07 custody: raw, parsed, ordered diagnostics, and span audit remain distinct; findings are identity-distinct and deterministically ordered; every surfaced finding has a non-empty verbatim raw-byte span; zero findings use the explicit canonical empty set; no model response is fabricated.
4. Recompute the three-layer D-05 proof: completed ledger is exactly empty, the structural audit covers the entire successor closure and contains no forbidden surface, and the runtime audit proves the D-06 all-socket guard with no successful-attempt security event. A blocked event may exist only in an immutable failed package per D-07/D-14.
5. Recompute D-09 through D-11 and TS-11/TS-12: `branch=red`, `N_strict=0`, `repeat_count=0`, `expected_cells=0`, `actual_cells=0`, `cells=[]`, every A/B/C expected/attempted/completed/failed/retried count is the integer zero, no placeholder/call exists, and both statuses remain exactly pending Phase 7.
6. Reconcile D-02/D-14/D-16 attempt history: every optional failed attempt has a contiguous six-digit ordinal, immutable complete leaf set, identical frozen root, false authority/metrics, empty ledger, ordered diagnostics/security events, and receipt-bound digest. Reject deletion, replacement, reordering, gaps, duplicates, different inputs, nonempty ledgers, hidden retries, or any drift-successor custody alongside current formal success. Confirm D-04 downstream-only permission and no broader claim.
  </action>
  <acceptance_criteria>
    - Exact v6, approved successor closure, Gate A/Gate B bindings, every formal leaf, and every receipt link recompute from held bytes.
    - The raw policy contains no self-identity; the external runtime-closure basis and Gate-A projection recompute byte-for-byte, and receipt policy/closure/projection hashes are distinct and exact.
    - Formal inventory is exact and safe; no missing/extra/unregistered/symlink/special/path-substituted artifact exists.
    - TS-07 separation, span, identity, empty-set, and deterministic-order rules all validate.
    - The ledger is empty, structural/runtime proofs are independently valid, and any blocked event is confined to immutable failed custody.
    - Matrix, partitions, calls, and conditional requirement states match every exact Red value with no placeholder or metric.
    - The complete attempt chain is contiguous, immutable, input-identical, zero-ledger, and fully bound; no drift is normalized into current authority.
    - The before/after snapshot is unchanged; this task writes nothing.
  </acceptance_criteria>
  <verify>
    <automated>cd experiments/specchoice-v1.3.2 &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_authorized_execution_v2.AuthorizedExecutionV2Tests.test_read_only_audit_recomputes_every_root_inventory_and_gate tests.test_authorized_execution_v2.AuthorizedExecutionV2Tests.test_gate_a_projection_recomputes_non_circular_policy_and_closure_hashes tests.test_authorized_execution_v2.AuthorizedExecutionV2Tests.test_policy_self_reference_and_projection_recursion_fail_closed tests.test_authorized_execution_v2.AuthorizedExecutionV2Tests.test_complete_attempt_chain_rejects_gap_reorder_replacement_and_nonempty_ledger tests.test_authorized_execution_v2.AuthorizedExecutionV2Tests.test_ts07_and_zero_matrix_contract_are_independently_recomputed tests.test_authorized_execution_v2.AuthorizedExecutionV2Tests.test_no_call_closure_and_downstream_only_scope_recompute -q</automated>
  </verify>
  <done>The full successor authority/evidence/attempt graph independently validates read-only, including TS-07, exact Red zeros, three-layer no-call proof, and limited downstream authority.</done>
</task>

<task type="auto" tdd="true">
  <name>05-06-02: Build the native-guard regression harness, then prove exact-resume and two zero-write release gates</name>
  <precondition>Task 05-06-01 completed with an unchanged before/after snapshot and no audit discrepancy; actual formal v2 publication exists, and 05-00 records the restored repository-local toolchain. This task must still fail closed if the pinned tools or functional native guard are unavailable and must not install, download, or upgrade anything.</precondition>
  <files>experiments/specchoice-v1.3.2/validation/guarded_regress.py, experiments/specchoice-v1.3.2/tests/test_guarded_regress.py</files>
  <read_first>
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-CONTEXT.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-VALIDATION.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-TOOLCHAIN-PREFLIGHT.md
    - .planning/phases/05-authorized-execution-and-immutable-evidence/05-05-SUMMARY.md
    - .mise.toml
    - pyproject.toml
    - uv.lock
    - Gemfile
    - Gemfile.lock
    - package-lock.json
    - bin/regress
    - experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v2.json
    - experiments/specchoice-v1.3.2/src/specchoice_execution/cli_v2.py
    - experiments/specchoice-v1.3.2/tests/test_authorized_execution_v2.py
    - experiments/specchoice-v1.3.2/receipts/red-execution-v2.json
    - experiments/specchoice-v1.3.2/reports/red-execution/red-execution-v2.md
  </read_first>
  <behavior>
    - "Unavailable `/usr/bin/sandbox-exec`, a profile parse/apply failure, a harmless-command preflight failure, a network-denial probe that is not denied before connect, or a protected-write denial probe that can create its sentinel all fail before `./bin/regress --all` is admitted; no bare fallback exists."
    - "The production profile explicitly denies `network*` and write access to resolved dependency/toolchain/install/cache roots with terminating denial behavior, while offline/no-update environment controls prohibit download, install, or upgrade attempts without privileged firewall mutation."
    - "Before each admitted run, the harness requires exactly the ten policy-declared regular formal leaves plus the one receipt and one report, records their exact repository-relative inventory and SHA-256, and fails after the child exits if any file changed, appeared, disappeared, became non-regular, or moved."
    - "A nonzero/signal guard result, a regression failure, or any prohibited-operation denial is captured with stdout/stderr digests and a stable failure diagnostic; it is never normalized to success and grants no authority."
    - "Unit tests use injected runners and temporary local fake commands only: guard unavailable, invalid/nonfunctional profile, denied/prohibited child, evidence byte/add/remove mutation, and unchanged success are covered without opening a real network connection or invoking the real full regression."
    - "The production CLI accepts only `--repo-root`; its command is fixed internally to `./bin/regress --all`. The harness is never imported or reached by formal execute-red, so its narrow validation subprocess does not weaken the formal no-model/provider/credential/retrieval/network/subprocess boundary."
  </behavior>
  <action>
1. Write `test_guarded_regress.py` first against the named public helpers/constants and a runner-injection seam: `FORMAL_FILENAMES`, `snapshot_v2_evidence(repo_root)`, `build_sandbox_profile(repo_root)`, `preflight_native_guard(...)`, `run_guarded_command(...)`, and `main()`. Cover an unavailable exact native binary, malformed/profile-apply failure, a denial probe that unexpectedly succeeds, a simulated prohibited-operation signal/nonzero result, formal byte/add/remove mutation, and a successful unchanged temporary-root fake local command. Patch the runner/guard lookup in tests; do not create or connect a real socket and do not invoke the real regression from unit tests.
2. Implement `validation/guarded_regress.py` with Python standard library plus existing descriptor-held/hash primitives only. Hard-code the formal inventory to `attempt-chain.json`, `evidence-span-audit.json`, `matrix-manifest.json`, `model-call-ledger.json`, `no-call-runtime-audit.json`, `no-call-structural-audit.json`, `ordered-diagnostics.json`, `parsed-evidence.json`, `raw-evidence.json`, and `red-trigger-evidence.json`, plus `receipts/red-execution-v2.json` and `reports/red-execution/red-execution-v2.md`. Require exact set equality, regular no-follow leaves, repository-relative names, and raw SHA-256; return a deterministic in-memory manifest and never write below formal/receipt/report targets.
3. Make native confinement a mandatory admission check. Resolve exactly `/usr/bin/sandbox-exec`; construct a deterministic `(version 1)` profile with `(allow default)` and terminating deny rules, without `no-log`, for `network*`, every formal-root/receipt/report write, and the concrete install surfaces `.venv/`, `.mise/`, `node_modules/`, `vendor/bundle/`, `.bundle/`, `.mise.toml`, `pyproject.toml`, `uv.lock`, `Gemfile`, `Gemfile.lock`, `package-lock.json`, the resolved user mise/cache/package roots (`.local/share/mise`, `.cache`, `Library/Caches`, `.npm`, `.gem`, `.cargo`, `.rustup`), `/opt/homebrew`, `/usr/local`, and `/Library`. Set offline/no-index/no-update controls for mise, uv/pip, Bundler, npm, Cargo, and Git without changing `HOME` or system configuration. Preflight profile parse/application with a harmless local command, then prove the network rule denies at socket construction before any connect and prove the write rule denies a temporary protected sentinel; missing/nonfunctional guard, bad profile, or either unexpectedly successful probe fails before regression. Use no package install and no firewall, route, proxy, privilege, or OS mutation.
4. Keep the production interface closed: `main()` accepts only `--repo-root`, validates the restored local toolchain, snapshots the exact twelve evidence files, and invokes the literal argv `./bin/regress --all` only as `/usr/bin/sandbox-exec -p <profile> ./bin/regress --all`. There is no command override, shell evaluation, environment fallback, or bare-regression path. Capture exit status/signal and complete stdout/stderr outside evidence custody, replay them for the executor, emit stable failure diagnostics for guard/prohibited-operation/regression failures, then take the same inventory/hash snapshot and fail if it differs even when the child returned zero.
5. Preserve the formal audit separately. Snapshot every actual formal, optional attempt, receipt, and Markdown target, invoke the identical 05-05 production command under its own all-socket guard and write observer, require the same canonical receipt and exactly zero writes per D-02, then run the full focused predecessor/successor/data/treatment/canonical/filesystem plus guarded-harness unit suite under the pinned `.venv`, Ruff 0.16.0, and `git diff --check`. Recheck no formal provider/model/credential/retrieval/network/subprocess path and no predecessor output target.
6. Reassert D-01 through D-16 and TS-07/TS-11/TS-12 from the validated receipt and independently recomputed graph: status is `completed`; permission is downstream Red-evidence evaluation only; calls/cells/partitions are exact empty/zero; both G/Y requirements remain pending Phase 7; `metrics_emitted=false`; and no placeholder, inferred zero performance, extraction success, feasibility conclusion, external publication, or broader authority appears. Reconfirm the receipt binds the exact Gate-A/Gate-B projection through separate policy, runtime-closure, and projection hashes and contains no recursive identity basis.
7. Only after the formal replay, focused checks, and initial/final formal snapshot equality pass, invoke the guarded-regression CLI twice from the repository root. Both invocations must independently pass guard preflight, run exactly `./bin/regress --all` inside confinement, and prove the exact twelve-file v2 evidence inventory/SHA-256 map unchanged. The second full run is the determinism proof. Any unavailable guard, denied/prohibited operation, install-surface change, evidence mutation, or nonzero regression blocks closure; never substitute a bare command.
8. Record only commands, both guarded-run results, guard/profile identity, output digests, and before/after manifest equality in `05-06-SUMMARY.md`; do not make the harness, tests, summary, or regression result a root input or requirement-closing artifact. This validation evidence grants no model, network, execution, publication, or requirement-closing authority.
  </action>
  <acceptance_criteria>
    - The identical actual command returns the same receipt and performs zero writes across every formal, attempt, receipt, and Markdown target.
    - Guarded-harness contract tests prove unavailable guard, bad/nonfunctional profile, prohibited child failure, evidence mutation, and unchanged fake-local-command success without real network access; full pinned tests, Ruff, no-call/prohibited-claim checks, and `git diff --check` pass without altering evidence.
    - The production harness accepts no arbitrary command, validates the exact ten-leaf formal root plus receipt/report inventory and SHA-256, functionally preflights `/usr/bin/sandbox-exec`, and has no bare fallback.
    - After actual formal v2 publication and the focused read-only audits pass, two guarded invocations each run exactly `./bin/regress --all` from the repository root under explicit native network/install denial and each proves the same exact evidence inventory/hashes before and after; unavailable guard, prohibited operation, install-surface write, evidence mutation, or regression failure blocks closure.
    - The guarded regression neither authorizes nor performs a formal model/network call: the separate policy runtime tripwire and all-socket/no-subprocess formal invariant remain active, and the validation-only fixed subprocess boundary creates no new authority.
    - Status and permission remain exactly bounded; TS-11/TS-12 remain conditional pending Phase 7.
    - No metric, placeholder, call/cell, inferred performance, extraction success, final conclusion, external action, or broadened authority is introduced.
    - The summary records verification only and cannot supersede any formal byte or human gate.
  </acceptance_criteria>
  <verify>
    <automated>cd experiments/specchoice-v1.3.2 &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_guarded_regress.GuardedRegressTests.test_unavailable_guard_fails_before_child tests.test_guarded_regress.GuardedRegressTests.test_bad_or_nonfunctional_profile_fails_before_child tests.test_guarded_regress.GuardedRegressTests.test_prohibited_child_result_is_failure tests.test_guarded_regress.GuardedRegressTests.test_evidence_change_addition_and_removal_fail tests.test_guarded_regress.GuardedRegressTests.test_unchanged_fake_local_command_succeeds_without_network -q &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m specchoice_execution.cli_v2 execute-red --repo-root . --policy config/execution/red-execution-policy-v2.json --authority phase4/branch-authority-v6.json --packet reports/h3/h3-red-review-v6/review-packet.json --readiness receipts/h3-branch-readiness-v6.json --decision reviews/h3-branch-decision-v6.json --attempt-root runs/red-attempts-v2 --formal-root runs/red-execution-v2 --receipt receipts/red-execution-v2.json --report reports/red-execution/red-execution-v2.md &amp;&amp; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src ../../.venv/bin/python -m unittest tests.test_data_admission tests.test_data_splits tests.test_data_relevance tests.test_data_h2 tests.test_treatments_frame tests.test_treatments_prompts tests.test_treatments_retrieval tests.test_treatments_h3 tests.test_authorized_execution tests.test_authorized_execution_v2 tests.test_guarded_regress tests.test_canonical tests.test_filesystem_boundary -q &amp;&amp; ../../.venv/bin/ruff check --isolated src/specchoice_execution validation/guarded_regress.py tests/test_authorized_execution.py tests/test_authorized_execution_v2.py tests/test_guarded_regress.py &amp;&amp; git diff --check &amp;&amp; cd ../.. &amp;&amp; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root . &amp;&amp; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/specchoice-v1.3.2/validation/guarded_regress.py --repo-root .</automated>
  </verify>
  <done>Phase 5 closes only after independent graph validation, actual byte-identical formal replay, and two successful native-confined full regressions whose exact v2 evidence inventories and hashes remain unchanged, with authority limited to downstream Red evidence evaluation.</done>
</task>

</tasks>

## Plan-Set Multi-Source Coverage Audit

| Source | ID | Feature / constraint | Plan | Status |
|---|---|---|---|---|
| GOAL | — | Complete immutable authorized-branch evidence without unauthorized calls, hidden repair, asymmetric retries, or favorable subsets. | 05-04..06 | COVERED |
| REQ | TS-07 | Separate immutable raw/parsed/diagnostic/span custody and truthful explicit empty finding set. | 05-04..06 | COVERED |
| REQ | TS-11 | Red zero-cell boundary with no G/Y execution and pending-Phase-7 state. | 05-04..06 | COVERED |
| REQ | TS-12 | Empty real-call ledger, three-layer no-call proof, no missing hidden cell/call, and pending-Phase-7 state. | 05-04..06 | COVERED |
| RESEARCH | — | Preserve rejected history outside `*-PLAN.md` discovery with no fabricated summary. | cancellation, 05-04..06 | COVERED |
| RESEARCH | — | Separate successor policy/modules/tests and exact production command; predecessor bytes preserved. | 05-04 | COVERED |
| RESEARCH | — | Gate A contract approval and separate Gate B final-closure confirmation. | 05-04, 05-05 | COVERED |
| RESEARCH | — | Non-circular external projection binds raw policy identity and all other frozen inputs while terminal receipt keeps policy, closure, and projection hashes distinct. | 05-04..06 | COVERED |
| RESEARCH | — | Actual successor-only fixed-set publication, no-replace, exact resume, read-only audit, and a repository-local fail-closed native-guard full-regression harness with repeated evidence snapshots. | 05-05, 05-06 | COVERED |
| RESEARCH | — | Standard library/current repository primitives only; no dependency or external action. | 05-04..06 | COVERED |
| CONTEXT | D-01 | Exact mutually bound completed contract; no warning completion. | 05-04..06 | COVERED |
| CONTEXT | D-02 | Byte-identical zero-write resume; no overwrite/regeneration. | 05-04..06 | COVERED |
| CONTEXT | D-03 | Separate failed custody and all-or-nothing formal set. | 05-04..06 | COVERED |
| CONTEXT | D-04 | Completion permits only downstream Red evidence evaluation. | 05-04..06 | COVERED |
| CONTEXT | D-05 | One-root three-layer zero-call proof. | 05-04..06 | COVERED |
| CONTEXT | D-06 | Every socket operation fails closed. | 05-04..06 | COVERED |
| CONTEXT | D-07 | Empty real-call ledger; blocked operations only in security events. | 05-04..06 | COVERED |
| CONTEXT | D-08 | Bind v6 no-model root and independently scan the successor closure. | 05-04..06 | COVERED |
| CONTEXT | D-09 | Canonical exact Red zero-cell matrix without placeholders. | 05-04..06 | COVERED |
| CONTEXT | D-10 | TS-11/TS-12 conditional pending-Phase-7 state. | 05-04..06 | COVERED |
| CONTEXT | D-11 | Formula/partition zeros and no unregistered run/raw-response. | 05-04..06 | COVERED |
| CONTEXT | D-12 | Canonical JSON authority, deterministic Markdown, no metrics/success claim. | 05-04..06 | COVERED |
| CONTEXT | D-13 | Frozen-byte change requires a versioned successor and new gates. | 05-04..06 | COVERED |
| CONTEXT | D-14 | Complete immutable failed-attempt schema with false authority/metrics. | 05-04..06 | COVERED |
| CONTEXT | D-15 | Successor tooling cannot authorize; v6 cannot authorize changed bytes. | 05-04..06 | COVERED |
| CONTEXT | D-16 | Every retry is immutable and the complete ordered history is terminally bound. | 05-04..06 | COVERED |

<threat_model>
## Trust Boundaries

| Boundary | Description |
|---|---|
| terminal receipt -> independently recomputed graph | Every receipt claim is untrusted until raw bytes, schemas, hashes, inventories, and authorities recompute. |
| attempt namespace -> claimed complete history | Deleted, reordered, replaced, or input-divergent attempts can hide favorable retry selection. |
| identical invocation -> filesystem | Any write during resume violates immutability even if final bytes look equal. |
| repository regression -> network/install surfaces | A broad release suite may contain a hidden download, upgrade, or network path that the formal execute-red tripwire cannot constrain across a separate process. |
| repository regression -> successor evidence | A passing broad suite is invalid if it adds, removes, or changes any formal v2 leaf, receipt, or report. |
| Red status -> downstream consumers | Conditional G/Y state can be falsely promoted to metrics, permanent closure, or final conclusion. |

## STRIDE Threat Register — ASVS L1

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|---|---|---|---|---|---|
| T-05-06-01 | Repudiation / Tampering | terminal receipt self-claims | high | mitigate | Recompute exact v6, Gate A/Gate B hashes, every formal schema/hash, no-call proof, matrix, and inventory from descriptor-held bytes. |
| T-05-06-02 | Tampering | attempt deletion/reordering/replacement | high | mitigate | Reconcile contiguous ordinals and complete leaf digests against the namespace; reject any gap, reorder, replacement, root mismatch, or nonempty ledger. |
| T-05-06-03 | Tampering | exact-resume filesystem behavior | high | mitigate | Snapshot bytes/hashes/metadata, invoke the identical command under a write observer, and require exact equality plus zero writes. |
| T-05-06-04 | Elevation of Privilege | authority substitution or closure weakening | critical | mitigate | Accept only exact v6 plus the doubly approved successor closure; audit cannot approve, migrate, or normalize changed bytes. |
| T-05-06-05 | Repudiation / Elevation of Privilege | conditional requirement and claim boundary | high | mitigate | Closed validators require pending-Phase-7 status and reject metrics, inferred performance, success, conclusion, or broader authority. |
| T-05-06-06 | Tampering / Repudiation | non-circular projection audit | high | mitigate | Rebuild policy entry, sorted closure basis, and external projection from held raw bytes; require distinct receipt fields and reject policy/closure/projection recursion without trusting receipt self-claims. |
| T-05-06-07 | Elevation of Privilege / Tampering | separate full-regression process | critical | mitigate | Admit only the fixed full-regression argv through functionally preflighted sandbox-exec denial, protect install/toolchain roots, capture failure/output, and forbid a bare fallback. |
| T-05-06-08 | Tampering | formal evidence during full regression | critical | mitigate | Require the exact ten formal files plus receipt/report and compare repository-relative SHA-256 inventories before/after each of two guarded runs; any add/remove/change fails. |
| T-05-SC | Tampering | validation toolchain | high | mitigate | Use only pinned `.venv`, standard library, installed repository primitives, and the native guard; add no package and perform no download, upgrade, firewall, route, proxy, privilege, or OS mutation. |
</threat_model>

<verification>
- Independently recompute every v6, Gate A/Gate B external projection, raw policy, non-policy closure basis, formal-leaf, receipt, Markdown, and attempt-chain link from held bytes; reject every self-referential closure form.
- Run the identical actual command under a write observer and prove byte-identical zero-write resume.
- Run pinned full predecessor/successor/data/treatment/canonical/filesystem plus guarded-harness tests, Ruff 0.16.0, and `git diff --check`, then invoke `validation/guarded_regress.py --repo-root .` twice; each harness run must functionally preflight native confinement, execute exactly `./bin/regress --all` inside it, and prove the exact v2 formal-root/receipt/report inventory and SHA-256 map unchanged.
- Confirm the four-source audit has no missing item and all D-01 through D-16 remain enforced.
</verification>

<success_criteria>
- All successor formal and optional failed-attempt evidence is complete, immutable, ordered, and independently bound to exact v6 plus both human gates.
- TS-07 separation/span/empty-set rules and every Red zero/no-call invariant pass.
- TS-11/TS-12 remain conditional pending Phase 7 and are never falsely executed or closed.
- Exact replay performs zero writes and the audit creates no authority or evidence byte.
- Both final repository-wide regressions pass only through the native-guard harness after actual formal v2 publication and the read-only audits; missing/nonfunctional guard, failure, prohibited network/install/model activity, or successor-evidence mutation blocks closure while the separate formal runtime no-call/no-subprocess tripwire remains active.
- The approved projection is byte-recomputable outside the policy and receipt, with distinct matching policy, runtime-closure, and projection hashes.
- Phase 5 exposes only downstream Red-evidence evaluation with no metrics, conclusion, model/network action, or public effect.
</success_criteria>

<output>
Create `.planning/phases/05-authorized-execution-and-immutable-evidence/05-06-SUMMARY.md` when done.
</output>

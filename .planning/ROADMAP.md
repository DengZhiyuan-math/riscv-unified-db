# Roadmap: SpecChoice v1.3.2

## Overview

SpecChoice v1.3.2 proceeds through seven strict, dependency-ordered increments: isolate and pin the public evidence, prove the measurement contract, preregister human-owned data, build and freeze the controlled treatments, execute only the authorized branch, evaluate partitions and ablations without pooling, and publish a reproducible bounded conclusion. Green and Yellow authorize controlled A/B/C model execution; Red is a valid fail-closed feasibility path that prohibits real model calls and succeeds only through independently auditable measurement, construction, blocker, and reproducibility evidence. Optional discovery and upstream contribution remain v2 and are not roadmap phases.

## Path Contract

- `[ALL]` requirements apply to Green, Yellow, and Red.
- `[G/Y]` requirements apply only after H3 selects Green or Yellow and H4 authorizes the exact external model configuration.
- A Red selection does not fail the roadmap: Phases 5–7 run in no-model mode and produce the Red feasibility package.
- `[G/Y]` requirements become `Not Applicable — Red` only after Phase 7 verifies every Red success condition; Red never counts as extraction-experiment success.
- Production held-out retrieval and real model calls are prohibited until the human-reviewed registries, prompts, configuration, branch, `N_strict`, repeats, and freeze root are approved.

## Phases

- [x] **Phase 1: Isolated Evidence Boundary and Source Integrity** - Establish a dependency-light experiment boundary and independently verifiable public inputs. (completed 2026-07-31)
- [x] **Phase 2: Deterministic Measurement Spine** - Prove the frozen adjudication and diagnostic contract on all 11 fixtures before innovation. (completed 2026-08-03)
- [x] **Phase 3: Human-Reviewed Data Preregistration** - Produce leakage-safe, provenance-rich data whose semantic decisions are explicitly human-approved. (completed 2026-08-04)
- [x] **Phase 4: Offline Treatments, Retrieval, and Branch Freeze** - Make the controlled treatments inspectable offline, freeze them, and select exactly one fail-closed branch. (completed 2026-08-04)
- [x] **Phase 5: Authorized Execution and Immutable Evidence** - Execute the approved Green/Yellow call matrix or preserve a verifiable Red no-call record.
- [ ] **Phase 6: Partition-Aware Ablation and Metamorphic Evaluation** - Score the authorized branch without pooling partitions or collapsing distinct failure modes.
- [ ] **Phase 7: Reproducible Feasibility Conclusion** - Deliver a byte-stable, claim-bounded positive, negative, or Red conclusion for human acceptance.

## Phase Details

### Phase 1: Isolated Evidence Boundary and Source Integrity

**Goal:** The operator and reviewer can work from a self-contained experiment boundary whose public source identity is independently verifiable.
**Mode:** mvp
**Depends on:** Nothing (first phase)
**Requirements:** TS-01, TS-02
**Vertical increment:** A usable local evidence workspace and verified source-manifest report, without any core UDB schema or generated-data modification.
**Human checkpoint:** Reviewer accepts the experiment boundary, source identities, and any documented 90-minute standalone fallback before measurement implementation proceeds.
**Success Criteria** (what must be TRUE):

  1. The operator can create, test, and inspect all prototype artifacts under `experiments/specchoice-v1.3.2/` without changing core UDB schemas, generated architecture data, or root dependency state.
  2. The reviewer can verify every named PR snapshot against its frozen commit and reproduce the stable hash of every consumed source file.
  3. The operator can reproduce the recorded environment decision and, if full setup exceeded the frozen limit, use the documented dependency-light fallback without weakening source verification.

**Plans:** 7/7 plans complete

Plans:

- [x] 01-01-PLAN.md
- [x] 01-02-PLAN.md
- [x] 01-03-PLAN.md
- [x] 01-04-PLAN.md
- [x] 01-05-PLAN.md
- [x] 01-06-PLAN.md
- [x] 01-07-PLAN.md

**Wave 1**

- [x] 01-01: Capture the immutable phase-start baseline and enforce the exact filesystem boundary.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 01-02: Record standalone-first environment identity and the cumulative dependency-incident policy.

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 01-03: Prove pinned PR identities, preserve the #2192 rejection, and stage immutable raw/derived bundle content.

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 01-04: Verify the bundle offline and gate boundary/source integrity through canonical receipts and reviewer approval.

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 01-05: Preserve the v2 incident, create the D-15 gap-restart lineage, and make committed post-baseline changes fail closed.

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 01-06: Freeze the exact 11-fixture/28-raw-file registry and construct a verifier-rooted but ineligible candidate.

**Wave 7** *(blocked on Wave 6 completion)*

- [x] 01-07: Complete the separately authorized local-only acceptance transition and bind the exact Phase 2 source authority.

### Phase 2: Deterministic Measurement Spine

**Goal:** As a human RISC-V reviewer, I want to trust the experiment's adjudication semantics and diagnostics, so that I can review the measurement spine before any frame, retrieval, or model result is considered.
**Mode:** mvp
**Depends on:** Phase 1
**Requirements:** TS-03, TS-04, TS-05
**Vertical increment:** A runnable evaluator that produces correct, inspectable outcomes for all frozen fixtures, even if later innovation is never authorized.
**Human checkpoint:** H1 — Source/gold review approves the adapter's fixture interpretation and candidate semantics; failure blocks innovation but preserves the measurement increment.
**Success Criteria** (what must be TRUE):

  1. The operator can score golden predictions for all 11 pinned PR #2164 fixtures, including surfacing and then classifying out the candidate case.
  2. The operator sees strict rejection of unknown keys, invalid enums, duplicate/conflicting predictions, and every noncanonical no-finding state, with no silent repair.
  3. The reviewer can trace every failed or warning outcome to a stable diagnostic code and structured fields; a missing accepted name remains an identity warning and never rewrites disposition.
  4. The human reviewer can approve or dispute the frozen gold interpretation from the adapter audit without any model output being used to compensate for disputed semantics.

**Plans:** 22/22 plans resolved (19 executed, 3 superseded; 02-20 and 02-21 intentionally omit summaries by plan contract)

Plans:

- [x] 02-01-PLAN.md
- [x] 02-02-PLAN.md
- [x] 02-03-PLAN.md
- [x] 02-04-PLAN.md
- [x] 02-05-PLAN.md
- [x] 02-06-PLAN.md
- [x] 02-07-PLAN.md
- [x] 02-08-PLAN.md
- [x] 02-09-PLAN.md
- [x] 02-10-PLAN.md
- [x] 02-11-PLAN.md
- [x] 02-12-PLAN.md
- [x] 02-13-PLAN.md
- [x] 02-14-PLAN.md
- [x] 02-15-PLAN.md
- [x] 02-16-PLAN.md
- [x] 02-17-PLAN.md — superseded by the successor chain
- [x] 02-18-PLAN.md — partially executed, then superseded by 02-19 and the downstream-only successor
- [x] 02-19-PLAN.md — superseded downstream by 02-20 through 02-22
- [x] 02-20-PLAN.md
- [x] 02-21-PLAN.md
- [x] 02-22-PLAN.md

**Wave 1**

- [x] 02-01: Implement the versioned PR #2164 adapter and canonical adjudication domain model.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 02-02: Implement strict schema parsing, no-finding invariants, and stable diagnostics.

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 02-03: Implement golden fixture scoring, candidate behavior, identity-warning separation, and evidence checks.

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 02-04: Persist immutable formal and adversarial attempts with deterministic measurement artifacts.

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 02-05: Produce the hash-bound H1 source/gold review packet and validate the human decision gate.

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 02-06: Record the narrow custody-hardening governance override and restore the Phase 2 MVP goal contract.

**Wave 7** *(blocked on Wave 6 completion)*

- [x] 02-07: Bind adversarial lineage to a validated formal attempt and retain adapter conflict provenance.

**Wave 8** *(blocked on Wave 7 completion)*

- [x] 02-08: Route adapter, preflight, and H1 leaves through descriptor-bound reads and preserve the exact phase-aware regression partition.

**Wave 9** *(blocked on Wave 8 completion)*

- [x] 02-09: Build descriptor-rooted source-custody primitives with stable reads, exact tree snapshots, and parent-held publication.

**Wave 10** *(blocked on Wave 9 completion)*

- [x] 02-10: Create a byte-bound v3 construction proposal, require human construction authorization, and publish only an ineligible candidate.

**Wave 11** *(blocked on Wave 10 completion)*

- [x] 02-11: Require separate human local acceptance, materialize accepted v3 from held bytes, and create a non-effective pending transition.

**Wave 12** *(blocked on Wave 11 completion)*

- [x] 02-12: Generate accepted-v3 receipts and prove copied offline replay without repository or network authority.

**Wave 13** *(blocked on Wave 12 completion)*

- [x] 02-13: Rehearse adapter and preflight against pending v3 while the active authority remains unchanged.

**Wave 14** *(blocked on Wave 13 completion)*

- [x] 02-14: Rehearse the formal and adversarial held-read graph against pending v3 with independently validated lineage.

**Wave 15** *(blocked on Wave 14 completion)*

- [x] 02-15: Freeze the versioned H1 schema, explicit-schema packet bindings, readiness oracle, and seven-response decision contract.

**Wave 16** *(blocked on Wave 15 completion)*

- [x] 02-16: Perform the forward-only authority cutover, then generate all post-active measurement and H1 evidence.

**Wave 17** *(historical route superseded by Waves 18 and 19; resolved without terminal authority)*

- [x] 02-17: Validate fresh readiness, collect the human H1 disposition, and require four same-commit clean final reports. *(superseded)*

**Wave 18** *(Tasks 1-4 preserved; unfinished Tasks 5-13 superseded by Wave 19)*

- [x] 02-18: Execute the single versioned Phase 1/2 semantic-integrity successor across seven fresh-context segments, preserving v3 history and retaining four genuine human gates. *(partially executed, then superseded)*

**Wave 19** *(depends on completed 02-18 Tasks 1-4 and supersedes only unfinished Tasks 5-13)*

- [x] 02-19: Freeze the complete executable, tool, semantic-input, and authority-prestate closure before renewed construction authorization, then finish dual-gated v5 acceptance, deterministic measurement, seven-question H1 review, and four fresh reports. *(superseded downstream)*

**Waves 20-22** *(single downstream-only successor; supersedes further execution of 02-17 through 02-19 without rewriting their history)*

- [x] 02-20: Implement the authority-bound closure-v4, adapter, measurement, H1, and report code contracts, then freeze only committed code/tests/contracts. *(summary intentionally omitted by plan contract)*
- [x] 02-21: Bootstrap closure-v4 from that code-only commit and materialize fresh decision-free adapter, formal, adversarial, packet, and readiness evidence. *(summary intentionally omitted by plan contract)*
- [x] 02-22: Obtain the genuine three-state H1 decision and create four fresh reports plus the terminal summary only for an approved result.

### Phase 3: Human-Reviewed Data Preregistration

**Goal:** The reviewer can approve a defensible prototype and evaluation corpus before retrieval ranks or model outputs can influence semantic decisions.
**Mode:** mvp
**Depends on:** Phase 2
**Requirements:** TS-08, TS-09, H2-01
**Vertical increment:** An audited data package that independently determines whether Green, Yellow, or Red remains feasible.
**Human checkpoint:** H2 — Data review approves labels, membership, primary families, pair axes, relevance judgments, and metamorphic directions; machines report inconsistencies but never rewrite them.
**Success Criteria** (what must be TRUE):

  1. The reviewer can inspect and approve complete contrastive pairs with positive and contrast passages, shared structure, frames, final statuses, discriminating axes, evidence, provenance, and manual-verification records.
  2. Automated validation proves item provenance, registered and version-compatible primary families, zero prototype/held-out example overlap, zero prototype/strict-core primary-family overlap, and no held-out passage in demonstrations.
  3. The human reviewer can explicitly approve or dispute every label, membership decision, family, pair axis, relevance judgment, and metamorphic expectation without automated relabeling or quota-filling pairs.
  4. The reviewer receives audited counts showing either a possible Green/Yellow data threshold or the exact defensible evidence requiring Red.

**Plans:** 4/4 plans complete

Plans:

- [x] 03-01-PLAN.md
- [x] 03-02-PLAN.md
- [x] 03-03-PLAN.md
- [x] 03-04-PLAN.md

**Wave 1**

- [x] 03-01: Curate provenance-rich prototype pairs and held-out gold without fabricated quota filling.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 03-02: Define the versioned family registry and strict/auxiliary split manifest.

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 03-03: Preregister pair relevance and the four human-reviewed metamorphic directions.

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 03-04: Run leakage/provenance validation and assemble the H2 approval and branch-eligibility packet.

### Phase 4: Offline Treatments, Retrieval, and Branch Freeze

**Goal:** The reviewer can inspect the exact treatments offline and authorize one immutable Green, Yellow, or Red execution contract.
**Mode:** mvp
**Depends on:** Phase 3
**Requirements:** TS-10, H1-01, H2-02
**Vertical increment:** A replayable offline A/B/C prompt-and-retrieval bundle plus a verified freeze root that either enables one controlled path or fails closed.
**Human checkpoint:** H3 approves the manifest, branch, `N_strict`, and repeats. On Green/Yellow only, H4 separately approves the provider, immutable model snapshot, sampling/output settings, cost, credentials boundary, and external calls.
**Success Criteria** (what must be TRUE):

  1. The reviewer can inspect B and C outputs containing exactly `authority`, `choice_object`, and `choice_space_origin`, frozen enums with `unknown`, and a verbatim evidence span for every axis.
  2. The operator can retrieve exactly two complete pairs per controlled target using frozen TF-IDF/cosine settings, target-dependent rankings, and deterministic `pair_id` tie-breaking, with no embedding or learned retrieval component.
  3. The reviewer can compare rendered A/B/C prompt bytes and verify equal demonstration counts, shared target/rules/decision space/evidence requirements, intended treatment-only differences, and measured natural token differences without padding.
  4. The gate records exactly one approved branch plus `N_strict` and repeats; Red makes production retrieval and the real-model adapter unreachable, while Green/Yellow cannot call a model before the separate H4 approval verifies.

**Plans:** 4/4 plans complete

Plans:

- [x] 04-01-PLAN.md
- [x] 04-02-PLAN.md
- [x] 04-03-PLAN.md
- [x] 04-04-PLAN.md

**Wave 1**

- [x] 04-01: Freeze the three-axis frame schema, advisory patterns, and strict B/C output contract.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 04-02: Assemble treatment-controlled A/B/C prompts, serializers, structural diffs, and budget accounting.

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 04-03: Implement deterministic complete-pair retrieval and validate it offline with target-only inputs.

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 04-04: Hash every treatment-affecting artifact and implement H3/H4 branch authorization with Red fail-closed enforcement.

### Phase 5: Authorized Execution and Immutable Evidence

**Goal:** The authorized branch yields complete immutable evidence without unauthorized calls, hidden repair, asymmetric retries, or favorable-subset execution.
**Mode:** mvp
**Depends on:** Phase 4
**Requirements:** TS-07, TS-11, TS-12
**Vertical increment:** Green/Yellow yields a replayable complete call corpus; Red yields a machine-verifiable empty call ledger and preserved measurement/construction evidence.
**Human checkpoint:** Execution must match the H3 freeze root and, for Green/Yellow, the H4 model authorization exactly; any frozen-input drift stops the run, records a decision, increments the version, and requires symmetric reruns.
**Success Criteria** (what must be TRUE):

  1. The reviewer can inspect immutable raw outputs captured before parsing, parsed outputs, parser diagnostics, and verbatim evidence-span audits as separate artifacts.
  2. On Green/Yellow, the operator can execute every preregistered strict-core case under A, B, and C with the same frozen controls, exactly two pairs, and the approved repeat count, with no missing cell.
  3. On Green/Yellow, the reviewer can inspect each call's prompt hash, model snapshot, sampling and output settings, actual token use, raw response, parse result, refusal/truncation state, and retry/failure state.
  4. On Red, the reviewer can verify an empty real-model call ledger and preserved runner, construction, ambiguity, and trigger evidence; the G/Y requirements remain conditional until Phase 7 validates Red closure.

**Plans:** 6/6 plans complete

Plans:

- [x] 05-09-PLAN.md

- [x] 05-00-PLAN.md
- [x] 05-01-PLAN.md
- `05-02-REJECTED.md` — partial implementation followed by explicit final-closure rejection; not completed and no summary exists.
- `05-03-SUPERSEDED.md` — unexecuted predecessor audit; not completed and no summary exists.
- [x] 05-04-PLAN.md — implement and freeze the separate successor contract, then obtain Gate A approval.
- [x] 05-05-PLAN.md — rehearse the exact command, obtain Gate B confirmation, and publish only the successor namespace.
- `05-06-FAILED-CLOSED.md` / `05-06-CANCELLATION.md` — partial read-only audit and harness history preserved; native construction preflight failed closed before either full regression, no summary exists, and the plan is not completed.
- `05-07-FAILED-CLOSED.md` / `05-07-CANCELLATION.md` — partial native-guard correction preserved; the first guarded child stopped at Bundler platform admission before the regression suite, zero of two full regressions completed, and no summary exists.
- [x] 05-08-PLAN.md — the v3 forward successor validated all three Darwin arm64 tools, created attempt-03 and terminal attempt-04, published the six no-replace cache leaves, preserved the Red formal root through a zero-write exact resume, and passed two fixed guarded full regressions. See `05-08-SUMMARY.md`.

**Wave 1**

- [x] 05-00: Verify and record the already-restored pinned local toolchain before the tracer, without experiment authority.
- [x] 05-01: Implement freeze-root verification, immutable envelopes, raw-first persistence, and the stable execution plan.

**Historical Lifecycle Records** *(retired forward-only and excluded from plan discovery)*

- `05-02-REJECTED.md`: Tasks 1-2 reached the final-closure checkpoint; the human rejected publication because the frozen interface did not expose the required formal command. Task 3 never ran.
- `05-03-SUPERSEDED.md`: Never executed because its predecessor formal root was never published.
- `05-06-FAILED-CLOSED.md`: Task 1 produced empty read-only audit commit `d95fb748`; Task 2 added the harness/tests in `46c34c8b`, then stopped at `GUARDED_REGRESS_NETWORK_PROBE_NOT_DENIED` before either full regression. `05-06-CANCELLATION.md` binds this partial history and no `05-06-SUMMARY.md` exists.
- `05-07-FAILED-CLOSED.md`: native calibration and validation-only work reached the first guarded child, which stopped before the test suite because Bundler 4.0.17 found no `arm64-darwin-23` entry in `Gemfile.lock`. `05-07-CANCELLATION.md` binds the exact partial worktree hashes and blocker; zero of two full regressions completed and no `05-07-SUMMARY.md` exists.

**Forward-Only 05-08 Reconciliation**

- `FWD-05-08-PORT-20260805` supersedes only the earlier prospective lock-platform-only scope for still-active 05-08. It does not edit, reinterpret, complete, or weaken the exact 05-07 cancellation/failed-closed bytes; they remain immutable historical evidence of the earlier authority, blocker, zero completed regressions, and absent summary.
- The authorized contract is exactly TheProjecter/eqntott `392759e6493a46f1d1ed7d9fb1c7c31197b0f6a8`, jar-ben/mustool `17fa9f9542a9ce05328dfccd1cd410f05f741ab3`, psksvp/espresso-ab-1.0 `18f59c723545f11bcb46d9e38e936531c990e5cf`, the named eqntott and mustool repository patch paths, espresso with no patch, committed fixture/oracle bytes, disposable source/build/staging roots, and the exact all-six no-overwrite external UDB cache targets. Any drift requires another explicit forward decision.
- Current `Gemfile.lock`, the cancellation-bound guarded harness/tests, and the already authorized Darwin arm64 Z3 and locked `node_modules` restores are read-only predecessor inputs, not 05-08 outputs. The source-port/cache record remains non-authoritative and cannot alter Gates A/B, formal Red bytes, D-01 through D-16, provider/model/retrieval/publication authority, or requirement state.
- The root `runs/native-port-darwin-arm64-projection-v2-20260805/contract-validation.json` is immutable at SHA-256 `7f6d0761ccdb775ddb62e13ca641dd389819e587acaf29ca4f805f0ab502a1fd`, state `failed_closed`, diagnostic `ORACLE_EXECUTION_NOT_IMPLEMENTED`. Per `FWD-05-08-CREATE-ONLY-RECORD-SUCCESSOR-20260805`, Task 01 creates only attempt-02 in `tracer_validated`, Task 02 creates only attempt-03 in `all_tools_validated_cache_unpublished`, and Task 03 creates only terminal attempt-04; each binds the exact predecessor path/SHA-256/state and applicable root diagnostic. No overwrite, delete, move, rewrite, truncation, relabel, reconstruction, or alternate successor path is authorized.
- Task 01 completed at commit `d61c2b6017f1d9d30c257d26e088427aa5dc0f9a` and its create-only attempt-02 is preserved at SHA-256 `84feca91ffb479e9870fb49ca951c3377f3ad9ddde3e9bca1dc0e154a48bbf32`, state `tracer_validated`. The v3 successor preserved that chain, created attempt-03 in `all_tools_validated_cache_unpublished`, and created terminal attempt-04 in `validation_complete`; none of the predecessors was changed.

**Versioned 05-08 Reproducibility Successor**

- The original whole-binary equality attempt remains failed immutable diagnostic custody: both espresso files were 297208-byte regular Mach-O arm64 but had SHA-256 `545a788e0e6dde0dc268d0575649a1335e9c67cd881df584d149cdbb567996c3` and `6ee19c6136897c3b9ea8403d89339946eb3fec5cb563e27e67654078affd1485`; fixed `/usr/bin/cmp -l LEFT RIGHT` emitted 544 lines with exact stdout SHA-256 `2f236895ef71c74cd9194eecb140abf7b1fb915c0a19ac8aff6b5d329d564726`. Those bytes are not normalized, rewritten, or relabelled as success.
- `FWD-05-08-CODE-BEHAVIOR-PROJECTION-V2-20260805` supersedes only whole-binary equality. Fresh two-build pairs must have the same size and regular Mach-O arm64 identity, identical ordered `__TEXT,__text` and `__TEXT,__stubs` layout/flags/raw bytes, and exact oracle outputs twice under native network/cache-write denial; both full hashes and every differing byte are retained.
- The validator freezes exact `/usr/bin/file --brief`, `/usr/bin/lipo -archs`, `/usr/bin/otool -L`, and `/usr/bin/otool -l` argv and independently parses raw Mach-O section bytes. Strip, relink, normalization, byte rewriting/masking, disassembly-text equality, dynamic ignore regions, arbitrary metadata allowlists, or changed source/patch/argv/selected section/functional output fail closed.
- Commit `46ade93d` is Task 01's exact RED predecessor. Execution completes its missing modules/tests and preserves unrelated dirty `Gemfile.lock` and guarded-harness worktree changes. No cache, formal replay, or regression begins before the complete three-tool projection-and-oracle handoff validates, and no additional authority is granted.
- `FWD-05-08-CREATE-ONLY-RECORD-SUCCESSOR-20260805` changes only record custody after the preserved root failure. It does not change sources, patches, fixed identity argv, selected sections, oracle bytes, cache targets, formal bytes, regression count, D-01 through D-16, requirement state, or any model/provider/retrieval/publication authority.
- `FWD-05-08-MUSTOOL-PRIi64-SPACING-20260805` is the preserved narrow predecessor successor. Task 02 alone may extend `mustool/0001-darwin-cstdio-and-memusedpeak-consistency.patch` with exactly three lexical edits in pristine `custom_minisat/Options.h`: upstream lines 285 and 291 insert one ASCII space between the `%4` string literal and `PRIi64`, and line 293 inserts ASCII spaces on both sides of `PRIi64` between the surrounding format-string literals. The complete patch SHA-256, canonical binary source-diff SHA-256, exact changed-path/hunk inventory, pristine pre-tree, and patched post-tree bind as one closure. The must build remains exactly `/usr/bin/make CXX=/usr/bin/clang++`; no `-std=...`, `-x`, alternate compiler, flag/environment language-mode change, mcsmus-copy edit, fourth source line, generated edit, or other source byte is authorized under that decision.
- `FWD-05-08-MUSTOOL-INTTYPES-INCLUDE-20260805` remains preserved as the unexecuted predecessor authorization that proposed exactly `#include <inttypes.h>` after pristine upstream line 26 `#include <string.h>`. On the default case-insensitive Darwin filesystem that spelling collides with the existing local `IntTypes.h` basename, so it is not current Task 02 implementation authority and must not appear in the applied source delta.
- `FWD-05-08-MUSTOOL-CINTTYPES-INCLUDE-20260805` remains preserved as the unexecuted predecessor authorization that proposed exactly `#include <cinttypes>` after pristine upstream line 26 `#include <string.h>`. It did not authorize an explicit bypass of the local case-insensitive `IntTypes.h` shadow, so it is not current Task 02 implementation authority and must not appear in the applied source delta.
- `FWD-05-08-MUSTOOL-INCLUDE-NEXT-INTTYPES-20260805` is the narrow current forward successor and preserves every prior authority, attempt, failure, diagnostic, source commit, patch path, oracle, completed Task 01 byte, and the three-line spacing decision. It supersedes only the unexecuted mustool header hunk: Task 02 alone may insert exactly `#include_next <inttypes.h>` immediately after pristine upstream line 26 `#include <string.h>` and before the unchanged blank line/local `IntTypes.h` include block in `custom_minisat/Options.h`, explicitly skipping the local case-insensitive shadow. Combined with the three spacing corrections, the successor additions affect exactly that one path and exactly two default-context diff hunks, the standard-header block and `Int64Option::help`; the complete patch SHA-256, canonical binary source-diff SHA-256, exact complete and successor-only path/hunk inventories, pristine pre-tree, and patched post-tree bind as one closure. The must build remains exactly `/usr/bin/make CXX=/usr/bin/clang++`; no direct predecessor include spelling, fifth source line, alternate/missing/duplicated/misplaced include, relocation/reordering of an existing include, include-search path or environment change, `-I`, `-isystem`, `-iquote`, `-std=...`, `-x`, alternate compiler, other flag change, generated edit, or other source byte is authorized.

**Wave 2** *(blocked on completed 05-01 and forward-only historical reconciliation)*

- [x] 05-04: Create the distinct successor policy/modules/tests, prove the exact production command in copied roots, and obtain Gate A contract approval.

**Wave 3** *(blocked on Wave 2 completion and explicit Gate A approval)*

- [x] 05-05: Rehearse the unchanged successor closure, obtain Gate B final confirmation, and publish or exactly resume only the successor Red evidence set.

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 05-08: The v3 successor preserved the original failed mismatch custody and the complete predecessor chain; it validated all three same-size regular Mach-O arm64 pairs against exact raw `__TEXT,__text`/`__TEXT,__stubs` projections and repeated oracles, created attempt-03, published the all-six no-replace cache set, retained a formal zero-write exact resume, completed two guarded `./bin/regress --all` gates, and created terminal attempt-04 without changing evidence or authority.

### Phase 6: Partition-Aware Ablation and Metamorphic Evaluation

**Goal:** As a reviewer, I want to evaluate the frozen branch at case level, so that every metric, treatment, partition, and denominator boundary remains preserved.
**Mode:** mvp
**Depends on:** Phase 5
**Requirements:** TS-06, TS-13, H1-02, H1-03, H1-04, H2-03, H2-04
**Vertical increment:** A complete evaluation package that supports a positive, negative, or Red conclusion without yet asking the reviewer to accept the narrative.
**Human checkpoint:** Reviewer inspects case-level joins, denominators, advisory-only warnings, metamorphic directions, and failure classifications before interpretation; disputes do not relabel same-version gold.
**Success Criteria** (what must be TRUE):

  1. The reviewer receives independently calculated surfacing, disposition, exact/incorrect/missing identity, classify-out, and evidence-integrity outcomes; Green/Yellow adds separate frame-axis and retrieval results.
  2. On Green/Yellow, the reviewer can compare paired B-minus-A and C-minus-B case outcomes under their frozen controls and see shortcut-family failures without post-hoc prompt, label, family, relevance, or threshold changes.
  3. On Green/Yellow, the operator can run all four frozen metamorphic minimal pairs and the reviewer can inspect axis changes, decision changes, evidence integrity, and the expected directional relation.
  4. PairHit@K is reported only for preregistered relevance judgments, with retrieved pair IDs per case; strict, auxiliary, metamorphic, and repeat-disagreement outputs retain separate IDs and denominators.
  5. On Red, the reviewer receives only the deterministic measurement and construction-feasibility evaluation, with no absent model outputs presented as experimental zeros or extraction evidence.

**Plans:** 10/14 plans executed

Plans:

- [ ] 06-08-PLAN.md
- [ ] 06-09-PLAN.md
- [ ] 06-10-PLAN.md

- [x] 06-01-PLAN.md
- [x] 06-02-PLAN.md
- [x] 06-03-PLAN.md
- [x] 06-04-PLAN.md
- [x] 06-05-PLAN.md
- [x] 06-06-PLAN.md
- [x] 06-07-PLAN.md
- 06-08-PLAN.md — Task 1 created generation-002 packet/report/readiness, then Task 2 failed because its required test did not exist; 06-11 preserves the exact bytes and records failed/incomplete status without a summary or decision.
- 06-09-PLAN.md — superseded unexecuted; generation-002 human review is not authorized.
- 06-10-PLAN.md — superseded unexecuted; a generation-002 decision must not be created.
- [x] 06-11-PLAN.md — preserve generation-002 failed/incomplete custody, add all generation-003 recovery tests before freeze, and freeze the tested generation-003 policy.
- [x] 06-12-PLAN.md — publish, independently verify, exact-resume, and adversarially validate the decision-free generation-003 package.
- [x] 06-13-PLAN.md — obtain the only new human decision checkpoint over exact generation-003 hashes.
- [ ] 06-14-PLAN.md — publish the canonical generation-003 decision and derive bounded closure or still-open status.

**Wave 1**

- [x] 06-01: Join immutable predictions to frozen gold and compute partition-specific outcome metrics.
- [x] 06-02: Produce paired B-A/C-B analyses, frame diagnostics, and the frozen failure taxonomy.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 06-03: Evaluate metamorphic directions, preregistered PairHit@K, retrieved IDs, and repeat stability.

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 06-04: Assemble branch-aware Green/Yellow or Red evaluation artifacts with denominator and partition audits.

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 06-05: Collect the separate human evaluation decision over the exact immutable packet/readiness identities and publish its closed canonical record without widening authority.

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 06-06: Repair root-derived provenance validation, exact component membership, and stable runtime diagnostics without changing generation-001.

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 06-07: Close verified-join and intervention-score bypasses, then freeze the forward-only generation-002 policy.

**Wave 7** *(historical partial execution; superseded by Waves 10-13)*

- 06-08: Publication produced the exact three-file generation-002 set, but the required exact-resume/adversarial test was absent and the frozen test file still required those outputs to be absent. Preserve this as failed/incomplete non-authorizing history; do not rerun or repair it.

**Waves 8-9** *(superseded without execution by the generation-003 recovery chain)*

- 06-09: Do not open a generation-002 human gate.
- 06-10: Do not publish a generation-002 decision.

**Wave 10** *(depends on completed 06-07 and the preserved generation-002 partial output state; supersedes 06-08 through 06-10 without rewriting them)*

- [x] 06-11: Bind the exact generation-002 package into failed/incomplete custody, commit all generation-003 package/decision attack tests before policy freeze, then create the Red-only generation-003 policy.

**Wave 11** *(blocked on Wave 10 completion)*

- [x] 06-12: Publish, verify, exact-resume, and adversarially validate the generation-003 packet/report/readiness set without a decision.

**Wave 12** *(blocked on Wave 11 completion)*

- [ ] 06-13: Present exact generation-003 evidence and require the explicit approved/disputed/incomplete human response; no generation-002 decision is permitted.

**Wave 13** *(blocked on Wave 12 completion)*

- [ ] 06-14: Publish and exact-resume only the generation-003 decision, then close Phase 6 solely on complete clean approval with bounded Phase 7 interpretation authority.

### Phase 7: Reproducible Feasibility Conclusion

**Goal:** The human reviewer can reproduce and accept a bounded positive, negative, or Red feasibility conclusion from immutable evidence.
**Mode:** mvp
**Depends on:** Phase 6
**Requirements:** TS-14, TS-15
**Vertical increment:** The complete v1.3.2 handoff: canonical reports, exact rerun commands, limitations, decision record, and an approved interpretation.
**Human checkpoint:** H5 accepts or disputes the failure taxonomy, limitations, and claim bounds. H6 remains a separate downstream prerequisite for any optional public communication and is not a v1 phase.
**Success Criteria** (what must be TRUE):

  1. The reviewer can trace branch and split counts, case-level results, failure taxonomy, and limitations to immutable evidence and read a bounded positive, negative, or Red conclusion with none of the prohibited claims.
  2. Equivalent captured inputs produce byte-identical canonical JSON with UTF-8/LF, NFC normalization, stable array ordering, sorted keys, no absolute paths or timestamps, content hashes, and exact reproduction commands.
  3. The H5 record captures interpretation approval or disputes without same-version relabeling, and no public action occurs without a later H6 approval.
  4. On Red, the reviewer can reproduce the passing runner, scoring-gap assessment, attempted construction audit, explicit blocker, no-call proof, ambiguity report, and revised feasibility conclusion before G/Y requirements close as `Not Applicable — Red`.

**Plans:** 3 plans

Plans:

- [ ] 07-01: Generate canonical JSON/Markdown results, hashes, reproducibility instructions, and decision-log linkage.
- [ ] 07-02: Draft the branch-bounded feasibility narrative, limitations, and H5 interpretation packet.
- [ ] 07-03: Verify final path closure, requirement status, prohibited-claim checks, and the no-public-action boundary.

## Coverage

| Requirement | Phase |
|-------------|-------|
| TS-01 | Phase 1 |
| TS-02 | Phase 1 |
| TS-03 | Phase 2 |
| TS-04 | Phase 2 |
| TS-05 | Phase 2 |
| TS-06 | Phase 6 |
| TS-07 | Phase 5 |
| TS-08 | Phase 3 |
| TS-09 | Phase 3 |
| TS-10 | Phase 4 |
| TS-11 | Phase 5 |
| TS-12 | Phase 5 |
| TS-13 | Phase 6 |
| TS-14 | Phase 7 |
| TS-15 | Phase 7 |
| H1-01 | Phase 4 |
| H1-02 | Phase 6 |
| H1-03 | Phase 6 |
| H1-04 | Phase 6 |
| H2-01 | Phase 3 |
| H2-02 | Phase 4 |
| H2-03 | Phase 6 |
| H2-04 | Phase 6 |

**Coverage:** 23/23 v1 requirements mapped exactly once; no v2 discovery, packaging, communication, or upstream requirement is scheduled.

## Progress

**Execution Order:** Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Isolated Evidence Boundary and Source Integrity | 7/7 | Complete    | 2026-07-31 |
| 2. Deterministic Measurement Spine | 22/22 | Complete | 2026-08-03 |
| 3. Human-Reviewed Data Preregistration | 4/4 | Complete   | 2026-08-04 |
| 4. Offline Treatments, Retrieval, and Branch Freeze | 4/4 | Complete    | 2026-08-04 |
| 5. Authorized Execution and Immutable Evidence | 6/6 | Complete   | 2026-08-06 |
| 6. Partition-Aware Ablation and Metamorphic Evaluation | 10/14 | In Progress|  |
| 7. Reproducible Feasibility Conclusion | 0/3 | Not started | - |

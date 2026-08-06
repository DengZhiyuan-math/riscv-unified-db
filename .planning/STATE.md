---
gsd_state_version: 1.0
milestone: v1.3.2
milestone_name: milestone
current_phase: 05
status: completed
stopped_at: Phase 05 completed after 05-09 made the exact v2 failed-closed root durable and independent re-verification passed all four must-haves; Phase 06 is next
last_updated: "2026-08-06T08:32:41.966Z"
last_activity: 2026-08-06
last_activity_desc: Phase 05 marked complete
progress:
  total_phases: 7
  completed_phases: 4
  total_plans: 43
  completed_plans: 38
  percent: 57
current_phase_name: authorized-execution-and-immutable-evidence
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-07-30)

**Core value:** Produce a reproducible, leakage-safe, falsifiable A/B/C result—positive, negative, or Red-path infeasible—without weakening gold semantics, deterministic measurement, or human control of RISC-V judgments.
**Current focus:** Phase 05 is complete; Phase 06 is the next unstarted phase.

## Current Position

Phase: 05 (authorized-execution-and-immutable-evidence) — COMPLETE
Plan: 6 of 6 active discoverable plans complete (05-00, 05-01, 05-04, 05-05, 05-08, and 05-09); 05-02 is rejected, 05-03 is superseded, and partial 05-06/05-07 remain failed-closed historical records without summaries.
Status: 05-09 added durable Git custody for the identical v2 failed-closed root and a canonical non-authoritative v2-to-v3 mapping successor. Independent re-verification passed all four must-haves, including a fresh archive replay and four focused no-call/fail-closed tests. No model, Green/Yellow, publication, metric, or final-conclusion authority is granted.
Last activity: 2026-08-06 — Phase 05 closure independently re-verified (4/4 must-haves).

Progress: [██████████] 100% of active discoverable Phase 5 plans complete

## Performance Metrics

**Velocity:**

- Total plans executed: 30
- Total plans resolved: 33 (including three superseded Phase 2 plans)
- GSD summary-bearing plans: 28 (02-20 and 02-21 intentionally have no summaries)
- Average duration: -
- Total execution time: 0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01 | 7 | - | - |
| 02 | 19 executed / 22 resolved | - | - |
| 03 | 4 | - | - |
| 04 | 4 | - | - |

**Recent Trend:**

- Last 5 plans: -
- Trend: No execution data

*Updated after each plan completion*
**Per-Plan Metrics:**

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| Phase 01 P01 | 10min | 3 tasks | 14 files |
| Phase 01 P02 | 7min | 2 tasks | 7 files |
| Phase 01 P03 | 49min | 3 tasks | 16 files |
| Phase 01 P04 | 32min | 3 tasks | 24 files |
| Phase 01 P05 | 25m | 3 tasks | 10 files |
| Phase 02 P01 | 7m | 2 tasks | 6 files |
| Phase 02 P02 | 6min | 2 tasks | 5 files |
| Phase 02 P03 | 7m | 2 tasks | 5 files |
| Phase 02 P04 | 29min | 3 tasks | 10 files |
| Phase 02 P06 | 6min | 2 tasks | 2 files |
| Phase 02 P07 | 6m | 2 tasks | 6 files |
| Phase 02 P08 | 45m | 2 tasks | 6 files |
| Phase 02 P09 | 32m | 2 tasks | 8 files |
| Phase 02 P10 | 8m | 3 tasks | 45 files |
| Phase 02 P11 | 1h | 3 tasks | 47 files |
| Phase 02 P12 | 10m | 2 tasks | 8 files |
| Phase 02 P13 | 11min | 1 tasks | 5 files |
| Phase 02-deterministic-measurement-spine P14 | 14min | 1 tasks | 5 files |
| Phase 02-deterministic-measurement-spine P15 | 11min | 1 tasks | 5 files |
| Phase 03 P01 | multi-session | 3 tasks | 14 files |
| Phase 03 P02 | multi-session | 3 tasks | 9 files |
| Phase 03 P03 | multi-session | 3 tasks | 8 files |
| Phase 03 P04 | multi-session | 3 tasks | 9 files |
| Phase 04 P01 | 1h 15m | 2 tasks | 8 files |
| Phase 05 P00 | 5min | 2 tasks | 1 files |
| Phase 05 P01 | 3min | 3 tasks | 5 files |
| Phase 05 P04 | multi-session | 3 tasks | 8 files |
| Phase 05 P05 | multi-session | 3 tasks | 13 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Roadmap]: Seven strict dependency-ordered MVP phases cover all 23 v1 requirements exactly once.
- [Phase 2]: Measurement over all 11 fixtures must pass before data, retrieval, or model evidence is interpreted.
- [Phase 4]: Human-reviewed preregistration and a verified freeze root precede production retrieval and model calls.
- [Path contract]: Red is a valid no-model feasibility path; G/Y requirements close N/A only after Red success is independently verified.
- [Evaluation]: Strict, auxiliary, metamorphic, and discovery evidence may not be pooled.
- [Phase 01]: Active Phase 1 baseline is phase-start-v5-gap-closure.json (a0b9f9fd...) while v2 remains preserved incident evidence.
- [Phase 01]: Phase 1 .DS_Store handling is a scoped visible/non-attributed policy override, not a general boundary exception.
- [Phase 01]: Standalone-first remains the primary route; full UDB setup was neither required nor attempted.
- [Phase 01]: Canonical environment identity contains stable fields only; audit evidence references it one-way by SHA-256.
- [Phase 01]: Unexpected dependency incidents use a cumulative 90-minute clock whose retries and waits never reset or pause it.
- [Phase 01]: Candidate construction is authorized only for the exact proposal hash and seven-file inventory; accepted publication remains false.
- [Phase 01]: Candidate core/root binding is deterministic and non-cyclic; Plan 04 must prove offline replay before accepted publication.
- [Phase 01]: Phase 01 v7 local-only acceptance binds the verifier-rooted generation while external publication remains forbidden.
- [Phase 01]: The final v7 integrity receipt binds reviewed revision 39d70ca9 through a non-cyclic receipt-basis projection and rejects stale v6 authority.
- [Phase ?]: Adapter authority delegates to the Phase 1 source-authority CLI and accepted-bundle verifier.
- [Phase ?]: Score eligibility requires one exact ordered 11-fixture/28-raw-file adapter batch with one version and rule hash.
- [Phase ?]: Current canonical JSON accepts only current-v1; reject maps to classify_out only at legacy-pr2164-v1 with an explicit normalization diagnostic.
- [Phase ?]: Invalid preflight exposes sorted diagnostics and raw hash only; score-bearing parsed predictions are withheld.
- [Phase ?]: Formal metrics require one exact all-11 preflight identity; partial and diagnostic-only results publish no metrics.
- [Phase ?]: Every frozen adversarial mutation asserts complete stable diagnostics including a finding identity when a scoring finding exists.
- [Phase ?]: Formal measurement authority is limited to a clean accepted-v2 all-11 attempt; warning, invalid, and diagnostic-only material cannot be promoted.
- [Phase ?]: The adversarial report records only exact frozen diagnostics and diagnostic-only custody hashes; it emits neither metrics nor H1 disposition.
- [Phase ?]: The only accepted Phase 1 custody exception is commit 9d641ec8 in filesystem.py for descriptor-bound leaf-read TOCTOU hardening.
- [Phase ?]: The normal verifier, not this governance plan, owns all refreshed Phase 2 verdict fields and report tables.
- [Phase ?]: Phase 2 MVP uses the validated human RISC-V reviewer user story without changing scope or success criteria.
- [Phase ?]: Standalone adversarial validation derives formal lineage only from an explicitly supplied, replay-validated formal/completed attempt.
- [Phase ?]: Post-authority adapter conflicts retain verified source identity and one typed Diagnostic while still exposing zero records.
- [Phase ?]: Phase 02-08 reuses the Phase 1 descriptor-bound reader for every authoritative measurement leaf.
- [Phase ?]: Phase 02-08 preserves H1 as human-authored, local-only, and external_publication_authorized=false.
- [Phase ?]: Candidate controls and Phase 2 source-authority receipt reuse descriptor-bound canonical bytes instead of reopening pathname leaves.
- [Phase ?]: The Phase 1 expected-red baseline is a non-discovered gate with a fixed 66/141/136 partition.
- [Phase ?]: 02-10 binds only the explicit user authorization to the exact verifier-rooted-v3 proposal and fixed source; candidate construction is not acceptance.
- [Phase ?]: Verifier-rooted-v3 remains candidate-only and replay-verified in copied isolation; active v2 authority and external publication remain unchanged.
- [Phase ?]: User-approved v3 remains local-only; active v2 is preserved until 02-16 cutover.
- [Phase ?]: Accepted v3 materialization uses descriptor-held candidate inventory and the v10 transition is non-effective.
- [Phase ?]: Accepted-v3 receipt custody is local-only and leaves the v10 pending cutover non-effective.
- [Phase ?]: Receipt writers reuse descriptor-held verifier inputs and only create immutable no-replace leaves.
- [Phase ?]: Pending v3 requires explicit pending-authority and transition inputs; active-v2 remains the default.
- [Phase ?]: Adapter validates one canonical pending-cutover stdout receipt against descriptor-held authority, bundle, registry, and audit custody.
- [Phase 02-deterministic-measurement-spine]: Formal and adversarial public rehearsal requires explicit pending-v3 authority and transition custody.
- [Phase 02-deterministic-measurement-spine]: Adversarial identity derives from independently validated formal-attempt custody, not report self-claims.
- [Phase ?]: H1 successor packets require explicit schema-v2; readiness is immutable and decision-free.
- [Phase ?]: H1 decision-v2 is a read-only validator with closed review and semantic-response contracts.
- [Phase 02-deterministic-measurement-spine]: Human ontology policy freezes PBMTE as surfaced then classified out and cache block identity as unified for this ontology version.
- [Phase 02-deterministic-measurement-spine]: Rooted-v4 proposal construction is duplicate-safe, append-only, local-only, and decision-free until a human authorizes or rejects its exact hashes.
- [Phase 02-deterministic-measurement-spine]: Human construction decision `b1be0980...` authorizes only the exact rooted-v4 proposal locally; it does not authorize post-decision fixed-code changes.
- [Phase 02-deterministic-measurement-spine]: Rooted-v4 Task 5 must fail closed because its three v4/v11 entry points are absent, two planned implementation files are fixed artifacts, and the mutating `bundle.py` runtime is outside the authorized fixed-code closure.
- [Phase 02-deterministic-measurement-spine]: 02-19 preserves the rooted-v4 authorization as authorized-but-non-executable history and supersedes only unfinished 02-18 Tasks 5-13.
- [Phase 02-deterministic-measurement-spine]: The successor must commit and bind all post-gate code, tests, semantic inputs, report inputs, Python/git/Ruby/Psych identities, and the accepted-v3 authority pre-state before requesting a new human construction authorization.
- [Phase 02-deterministic-measurement-spine]: Both candidate fixtures are formal surfaced-then-classified-out records; the frozen populations are 11 outcomes, 8/8 surfacing, 8/8 disposition, 6/6 parameter identity, S/S evidence spans, and 3/3 negative no-surface outcomes.
- [Phase 02-deterministic-measurement-spine]: Runtime closure-v2 remains exact non-authorizing history because it omitted the freeze-tree authority pre-state binding.
- [Phase 02-deterministic-measurement-spine]: Runtime closure-v3 binds the accepted-v3 authority Git blob and all executable inputs at freeze commit dc87436a; its independently rebuilt receipt SHA-256 is dbc86e53c044910536d9dbd494aa7df286604f3fbf6e4fdf8c4f3c11c943f774.
- [Phase 02-deterministic-measurement-spine]: Rooted proposal-v6 received genuine local construction authorization, candidate acceptance, and source-authority cutover; accepted-v6 remains the immutable active source identity.
- [Phase 02-deterministic-measurement-spine]: Task16 measurement outputs are numerically useful but non-authorizing because closure-v3 correctly rejects the post-freeze adapter/test bytes with RUNTIME_CLOSURE_UNCOMMITTED_INPUT.
- [Phase 02-deterministic-measurement-spine]: 02-20 through 02-22 form one downstream-only successor; they preserve accepted-v6 and do not reopen source construction, acceptance, or cutover unless source identity bytes change.
- [Phase 02-deterministic-measurement-spine]: 02-20 and 02-21 intentionally create no SUMMARY by their plan contracts; their absence is not missing execution evidence.
- [Phase 02-deterministic-measurement-spine]: The approved 02-22 decision, four terminal reports, and last-written summary passed the canonical validator against the 47ffaa1c freeze state and are frozen in local evidence commit dc3e5883a10cd3efe1393220caf1f711561867b9.
- [Phase 03]: Phase 3 candidate inventory is frozen at one H1-consistent natural pair; no upstream reopening, weak pairing, or replacement is permitted to meet Green/Yellow thresholds. — The only remaining H1 classify_out fixture has no same-choice-object positive partner. Rejected cache-block and CSR-access proposals fail controlled-contrast or frozen-status requirements, so insufficient coverage must flow deterministically to red_required with model execution unauthorized.
- [Phase 03]: Family registry and split freeze one warl_legal_set prototype pair with empty strict and auxiliary sets; membership is deterministic and no case may be moved or fabricated. — The approved registry and assignment derive prototype=1, strict=0, auxiliary=0 without diagnostics. Insufficient natural coverage remains red_required and model execution stays unauthorized.
- [Phase 03]: The frozen inventory contains no metamorphic candidates; all four required directions are explicit unavailable, human-excluded, and non-counting records. — Post-freeze candidate addition or synthetic semantic completion is prohibited. Empty strict and auxiliary relevance remains exact, and the audit continues to red_required without model authorization.
- [Phase 03]: Approved H2 data authority deterministically selects red_required from one qualifying natural pair, zero strict cases, and four unavailable metamorphic directions. — Yellow and Green count thresholds are unmet; pair failure analysis preserves CHOICE_OBJECT_MISMATCH and H1_STATUS_CONFLICT without replacement. Retrieval, model execution, external publication, and final Phase 4 branch authority remain false.
- [Phase ?]: B and C use the same closed parser/output schema; only A is frame-free.
- [Phase ?]: Advisory patterns are canonical config validated at import and return only ordered warning Diagnostics.
- [Phase ?]: No provider, model, retrieval, CLI, dependency, or external-action surface is introduced in Wave 1.
- [Phase ?]: Wave 0 records only the restored local toolchain and explicitly grants no experiment or formal-evidence authority.
- [Phase ?]: The handoff is valid only while the pinned tools, pyproject digest, and empty formal target namespaces agree.
- [Phase ?]: User explicitly approved only the exact Phase 5 Red contract bound to policy c48b5c607aa3a6be532ca0accb7f9bfd685b1eab60f82dc2b4b4c4ce97285d15 and v6 authority 363cf85c4088f5f268692f8319b70b50f7ed717f7145ed84a6923499ae992518; byte drift requires a successor and new human gate.
- [Phase ?]: [Phase 05 Plan 02] User selected reject-final-closure: Task 05-02-03 is prohibited because the frozen policy and CLI expose only execute-red-temporary while the planned formal publication requires execute-red. All formal, attempt, and successor targets remain absent; a versioned successor and new contract/final-closure gates are required.
- [Phase 05]: Rejected 05-02, unexecuted 05-03, and partial failed-closed 05-06/05-07 are preserved as non-discoverable historical documents with no fabricated summaries; 05-04 and 05-05 remain completed successors, and 05-08 is the sole active validation successor.
- [Phase ?]: [Phase 05 Plan 04 Gate A] User selected approve-v2-contract only for persisted raw policy config/execution/red-execution-policy-v2.json (2406 bytes, 1785acf527c4d5c08790a525937f4960896ac775d5c9a6635903b384c2c8835f), runtime_closure_sha256=29558e76c09dac2b82468915567667419e5a281091201611449a6960f0b7a811, and external gate_a_projection_sha256=18e4a9a7ec40e881ff6d3994db4554a3907298a01511c566769177b51d40bdec; Phase 4 v6 raw input=363cf85c4088f5f268692f8319b70b50f7ed717f7145ed84a6923499ae992518 and authority claim=f77cdbd908222209730058be07e5ffa363c905f72183b1f6970c4d9c36e315fb. The exact execute-red ten-option schema, fixed v2 targets, Red zero matrix, conditional TS-11/TS-12 states, and target absence are approved for 05-05 pre-publication work only; no evidence publication, model/provider/credential/retrieval/network/subprocess/metric/final-conclusion/requirement-closure authority is granted.
- [Phase ?]: [Phase 05 Plan 05] User explicitly selected Gate B confirm-v2-final-closure for the unchanged Gate-A projection 18e4a9a7ec40e881ff6d3994db4554a3907298a01511c566769177b51d40bdec; this authorizes exactly one successor Red no-call publication and its exact-resume verification only.
- [Phase ?]: Gate B authorized exactly one local successor Red no-call publication and its zero-write exact-resume verification for the unchanged Gate-A projection 18e4a9a7ec40e881ff6d3994db4554a3907298a01511c566769177b51d40bdec.
- [Phase ?]: Completed Red evidence authorizes only downstream Red-evidence evaluation; no model, provider, credential, retrieval, network, metric, external-publication, or final-conclusion authority is granted.
- [Phase 05]: Plan 05-06 is failed-closed-not-completed: empty audit commit d95fb748 and harness commit 46c34c8b are preserved, native construction preflight emitted GUARDED_REGRESS_NETWORK_PROBE_NOT_DENIED before either full regression, and 05-07 may change only the validation harness/tests to require pinned denied connect use without reopening Gates A/B or formal authority.
- [Phase 05]: Plan 05-07 is failed-closed-not-completed: cancellation binds the exact historical plan and partial validation worktree hashes, the first guarded child stopped at Bundler platform admission because baseline Gemfile.lock omitted arm64-darwin-23, zero of two full regressions completed, and no 05-07 summary exists.
- [Phase 05]: The earlier lock-platform-only scope for active 05-08 remains predecessor planning history, not current authority. `05-07-CANCELLATION.md` and `05-07-FAILED-CLOSED.md` stay byte-identical and remain truthful immutable records; no 05-07 summary or completion claim may be created.
- [Phase 05]: Predecessor decision `FWD-05-08-PORT-20260805` froze `darwin-arm64-source-port-20260805`: the exact three source commits, two patch paths, oracle bytes, disposable roots, and all-six no-overwrite cache set. Those boundaries remain inputs to projection-v2; only its failed whole-binary equality predicate is superseded.
- [Phase 05]: Current `Gemfile.lock` (`e1231c14...57c`), the 05-07 guarded harness (`739b9851...21e5`), and guarded tests (`ea245fe6...4ef`) are preserved read-only predecessor inputs, not 05-08 outputs. The already authorized Darwin arm64 Z3 and locked `node_modules` restores remain fixed inputs and are not repeated.
- [Phase 05]: `runs/native-port-darwin-arm64-20260805/original-whole-binary-sha-mismatch.json` is immutable failed diagnostic custody. The root `runs/native-port-darwin-arm64-projection-v2-20260805/contract-validation.json` is also immutable at SHA-256 `7f6d0761ccdb775ddb62e13ca641dd389819e587acaf29ca4f805f0ab502a1fd`, state `failed_closed`, diagnostic `ORACLE_EXECUTION_NOT_IMPLEMENTED`; it is a read-only predecessor, not an active mutable handoff.
- [Phase 05]: The original 05-08 whole-binary equality result remains failed immutable diagnostic custody: two 297208-byte regular Mach-O arm64 espresso files had SHA-256 `545a788e0e6dde0dc268d0575649a1335e9c67cd881df584d149cdbb567996c3` and `6ee19c6136897c3b9ea8403d89339946eb3fec5cb563e27e67654078affd1485`; fixed `/usr/bin/cmp -l LEFT RIGHT` emitted 544 lines with exact stdout SHA-256 `2f236895ef71c74cd9194eecb140abf7b1fb915c0a19ac8aff6b5d329d564726`. It is not normalized or reclassified as success.
- [Phase 05]: User-approved forward decision `FWD-05-08-CODE-BEHAVIOR-PROJECTION-V2-20260805` supersedes only two-build whole-binary equality. The successor requires same-size regular Mach-O arm64 identity, fixed `/usr/bin/file`/`lipo`/`otool` argv, exact raw bytes and layout for ordered `__TEXT,__text` and `__TEXT,__stubs`, all full hashes/differences recorded, and the exact oracle corpus twice under native network/cache-write denial.
- [Phase 05]: User-approved forward decision `FWD-05-08-CREATE-ONLY-RECORD-SUCCESSOR-20260805` authorizes only a create-only custody chain from the immutable root failure: Task 01 creates `attempts/attempt-02/contract-validation.json` in `tracer_validated` with exact root path/SHA-256/state/diagnostic binding; Task 02 creates attempt-03 in `all_tools_validated_cache_unpublished` with exact attempt-02 path/SHA-256/state binding; Task 03 creates attempt-04 in `validation_complete` or `failed_closed` with exact attempt-03 path/SHA-256/state binding. No predecessor may be overwritten, deleted, moved, rewritten, truncated, relabelled, or replaced by an alternate path.
- [Phase 05]: Task 01 completed at commit `d61c2b6017f1d9d30c257d26e088427aa5dc0f9a`; its create-only `attempts/attempt-02/contract-validation.json` is preserved at SHA-256 `84feca91ffb479e9870fb49ca951c3377f3ad9ddde3e9bca1dc0e154a48bbf32`, state `tracer_validated`. The immutable root remains `7f6d0761...a1fd`; attempt-03 and attempt-04 remain absent. Task 01 may not be rerun, amended, or reconstructed.
- [Phase 05]: User-approved forward decision `FWD-05-08-MUSTOOL-PRIi64-SPACING-20260805` preserves every prior authority, attempt, failure, diagnostic, source commit, patch path, oracle, and Task 01 byte. Task 02 alone may extend `mustool/0001-darwin-cstdio-and-memusedpeak-consistency.patch` with exactly three lexical edits in pristine `custom_minisat/Options.h`: upstream lines 285 and 291 insert one ASCII space between the `%4` string literal and `PRIi64`; line 293 inserts ASCII spaces on both sides of `PRIi64` between the surrounding format-string literals. The complete patch SHA-256, canonical source-diff SHA-256, exact changed-path/hunk inventory, pristine pre-tree, and patched post-tree must bind together. The must build remains exactly `/usr/bin/make CXX=/usr/bin/clang++`; no `-std=...`, `-x`, alternate compiler, flag/environment language-mode change, mcsmus-copy edit, fourth source line, generated edit, or other source byte is authorized.
- [Phase 05]: User-approved predecessor decision `FWD-05-08-MUSTOOL-INTTYPES-INCLUDE-20260805` is preserved as the unexecuted authorization for one direct `#include <inttypes.h>` after pristine upstream line 26 `#include <string.h>`. That spelling collides with the existing local `IntTypes.h` basename on the default case-insensitive Darwin filesystem, so it is not current Task 02 implementation authority and must not appear in the applied source delta.
- [Phase 05]: User-approved predecessor decision `FWD-05-08-MUSTOOL-CINTTYPES-INCLUDE-20260805` is preserved as the unexecuted authorization for one direct `#include <cinttypes>` after pristine upstream line 26 `#include <string.h>`. It did not authorize an explicit bypass of the local case-insensitive `IntTypes.h` shadow, so it is not current Task 02 implementation authority and must not appear in the applied source delta.
- [Phase 05]: User-approved current forward decision `FWD-05-08-MUSTOOL-INCLUDE-NEXT-INTTYPES-20260805` preserves every predecessor decision/record and supersedes only the unexecuted mustool header hunk. Task 02 alone may insert exactly `#include_next <inttypes.h>` immediately after pristine upstream line 26 `#include <string.h>` and before the unchanged blank line/local `IntTypes.h` block, explicitly skipping the local case-insensitive shadow. Combined with the three spacing corrections, the successor additions affect exactly `custom_minisat/Options.h` and exactly two default-context diff hunks, the standard-header block and `Int64Option::help`; the complete patch SHA-256, canonical source-diff SHA-256, exact complete and successor-only changed-path/hunk inventories, pristine pre-tree, and patched post-tree must bind together. The must build remains exactly `/usr/bin/make CXX=/usr/bin/clang++`; no direct predecessor include spelling, fifth source line, alternate/missing/duplicated/misplaced include, relocation/reordering of an existing include, include-search path or environment change, `-I`, `-isystem`, `-iquote`, `-std=...`, `-x`, alternate compiler, other flag change, generated edit, or other source byte is authorized.
- [Phase 05]: No strip, relink, normalization, byte masking/zeroing/rewriting, disassembly-text comparison, dynamic ignore region, arbitrary metadata allowlist, changed source/patch/argv/executable section/functional output, cache-before-all-tools, formal drift, or additional authority is permitted.
- [Phase 05]: Commit `46ade93dda1b55eb76a2938855d4beb1487259c0` and `tests/test_native_port_contract.py` SHA-256 `83426d8bfb2507d53787ded7d1f59f11faff45050cdb9e22863b8fb92b41a69f` are the exact Task 01 RED predecessor. Execution must finish the missing implementation and preserve unrelated `Gemfile.lock`/guarded-harness worktree changes rather than reverting or absorbing them.

### Pending Todos

None yet.

### Blockers/Concerns

- Exact provider/model snapshot and Python lock resolution remain intentionally conditional because the approved Phase 3 authority requires the Red no-model branch.
- Phase 4 must preserve `red_required` and obtain its own branch decision without converting Phase 3 eligibility into execution authority.
- Preserved 05-08 diagnostic history: after the user-authorized local Z3 and locked `node_modules` restores, the second native-confined `./bin/regress --all` returned 1 (`stdout_sha256=029e59e5e1ccccd859cfda14253020cdcdea43e9548d7545a7d7323bffd47d54`, `stderr_sha256=6d8495702e26e5bdc81c08348e616015894e9347b215d0e9b1868d6ed070c9f8`). No bare fallback, formal write, summary, or behavior claim occurred. Projection-v2 cannot begin cache/formal/regression work until its complete all-tools section-and-oracle handoff validates.
- Preserved repeat diagnostic: it returned 1 with formal before/after equality because `eqntott-392759e` and `must-17fa9f9` were absent from the protected UDB cache and the confined child correctly denied their implicit download/write attempts. Official UDB `arm64` release artifacts remain AlmaLinux binaries, not Darwin executables; the only currently authorized compatible path is the exact source-only contract above, with no Linux-binary substitution.
- Preserved temporary source trial: the exact source commits remain unchanged; eqntott failed its bundled example, mustool failed on the `memUsedPeak` signature mismatch, and espresso produced the unequal whole-binary pair recorded above. The selected `__TEXT,__text` and `__TEXT,__stubs` raw bytes matched in the diagnostic pair, but that observation is not itself successor evidence. No cache target, repository source, formal evidence, or authority file changed; fresh projection-v2 builds must independently recompute every section and oracle result.
- Current Task 02 boundary: completed tracer commit `d61c2b60` and attempt-02 `84feca91...f32` exact-resume read-only. The mustool `custom_minisat/Options.h` portability blocker may be resolved only inside the existing named versioned patch by the three preserved PRIi64 spacing lines plus one exact `#include_next <inttypes.h>` after pristine `#include <string.h>` to skip the local case-insensitive shadow; both direct-header predecessors are preserved but forbidden in the applied delta, and the successor additions must bind as one path/two hunks without changing include-search paths, build flags, environment, language mode, or any further source byte. Until the complete patch/source-diff/path-hunk/tree closure and all-tools projection/oracle validation pass, attempt-03, cache publication, formal replay, both guarded regressions, attempt-04, summary, and any success claim remain forbidden.

## Deferred Items

| Category | Item | Status | Deferred At |
|----------|------|--------|-------------|
| v2 | Optional discovery, packaging, maintainer communication, and upstream actions | Deferred | Roadmap creation |

## Session Continuity

Last session: 2026-08-05T21:57:06.343Z
Stopped at: Phase 6 context gathered; Phase 5 remains the active dependency
Resume file: .planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-CONTEXT.md

---
phase: 06-partition-aware-ablation-and-metamorphic-evaluation
verified: 2026-08-06T11:51:29Z
status: gaps_found
score: 4/9 must-haves verified
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "The MVP phase goal is a valid user story that can be verified against its stated outcome."
    status: failed
    reason: "The roadmap declares `mode: mvp`, but `user-story.validate` rejects the phase goal because it has none of the required As-a / I-want / so-that slots."
    artifacts:
      - path: ".planning/ROADMAP.md"
        issue: "Phase 6 has an invalid MVP goal contract."
    missing:
      - "Normalize the Phase 6 goal through the MVP-phase workflow, e.g. `As a reviewer, I want to evaluate the frozen branch at case level, so that every metric, treatment, partition, and denominator boundary remains preserved.`"
  - truth: "A reviewer package is derived from the frozen policy-bound inputs, not merely self-consistent."
    status: failed
    reason: "validate_evaluation_packet validates only shape, self-hash, component hashes, and selected invariants; it never rebuilds the expected packet from admitted roots. A forged surfacing score of 0.0 with every packet/readiness hash recomputed was accepted by validate_readiness."
    artifacts:
      - path: "experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py"
        issue: "Packet/readiness validation lacks derivation equality."
    missing:
      - "Rebuild the canonical expected packet from policy-admitted inputs and require canonical byte equality before validating Markdown/readiness or an approval decision."
      - "Add a regression test that changes a metric and recomputes all self/component/readiness hashes; validation must fail."
  - truth: "Construction-feasibility evidence is frozen by the same policy inventory as the evaluation packet."
    status: failed
    reason: "build_construction_feasibility reads 19 Phase-5 files via root.parents[1], but the policy inputs inventory contains none of those paths or digests. Policy validation therefore cannot detect a changed construction record."
    artifacts:
      - path: "experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py"
        issue: "Construction inputs are inferred from repository layout instead of being descriptor-bound."
      - path: "experiments/specchoice-v1.3.2/config/evaluation/partition-evaluation-red-generation-001.json"
        issue: "No construction source path/hash inventory is declared."
    missing:
      - "Declare every construction source path and SHA-256 in policy, pass an explicit project root, and build the audit only from validated declared files."
      - "Tamper each declared construction source in a temporary project and assert publication/verification fails without writing outputs."
  - truth: "Only closed, verified artifact joins can produce a measured B-minus-A or C-minus-B comparison."
    status: failed
    reason: "build_pairwise_comparison accepts bare AtomicResultRow values and no ClosedJoinManifest or expected join hash. An independently invoked comparison over bare rows returned measured with denominator 1."
    artifacts:
      - path: "experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py"
        issue: "The pairwise API cannot enforce D-08 closed-join status/hash."
    missing:
      - "Require an immutable closed join reference for both members of each pair; reject missing, invalid_withheld, or hash-substituted joins before constructing a metric."
      - "Add bare-row and substituted-join negative tests."
  - truth: "B-minus-A and C-minus-B compare a real named intervention while all other frozen controls remain equal."
    status: failed
    reason: "The control predicate excludes the intervention key from equality checks but never requires it to exist or differ. A B/A pair with identical delegation_frame controls returned measured."
    artifacts:
      - path: "experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py"
        issue: "Pairwise control validation permits a non-intervened pair."
    missing:
      - "Require the named intervention on both rows, require unequal permitted values, and cross-check treatment-to-intervention mapping."
      - "Add equal-value, missing-key, and treatment-inconsistent negative tests."
---

# Phase 6: Partition-Aware Ablation and Metamorphic Evaluation — Verification Report

**Phase Goal:** The reviewer can evaluate the frozen branch at case level while preserving every metric, treatment, partition, and denominator boundary.
**Verified:** 2026-08-06T11:51:29Z
**Status:** gaps_found
**Re-verification:** No — initial verification

## MVP Contract Gate

The phase is marked `mode: mvp`, but the canonical goal fails `user-story.validate`: it is not in `As a …, I want to …, so that ….` form. Formal MVP verification is therefore blocked. The technical audit below was still performed to preserve independently reproduced evidence; it cannot turn this invalid contract into a pass.

## Goal Achievement

The roadmap criteria and plan must-haves were deduplicated into nine verification contracts. Four current Red-path properties hold, but the five failed contracts are blockers: the reviewer cannot establish that the approved packet is derived from frozen evidence, nor can a future Green/Yellow pairing safely enforce its required joins and intervention.

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | MVP goal has a verifiable user-story outcome | ✗ FAILED | `user-story.validate` returned `valid: false`; formal MVP gate cannot be entered. |
| 2 | Packet/readiness preserve independently calculated frozen outcomes | ✗ FAILED | Recomputed forged `surfacing=0.0` packet/readiness passed `validate_readiness`; self-consistency is not provenance. |
| 3 | Construction feasibility remains immutable, policy-bound evidence | ✗ FAILED | `core.py` reads undeclared Phase-5 paths through `root.parents[1]`; policy lists no construction hashes. |
| 4 | Applicable B-A/C-B results require a closed immutable join | ✗ FAILED | Bare A/B rows produce a `measured` result; the comparison API has no join-manifest input. |
| 5 | Pairwise comparisons prove the named intervention changed | ✗ FAILED | Identical `delegation_frame` values produced `measured`, denominator 1. |
| 6 | Red output keeps result states and no-model applicability distinct | ✓ VERIFIED | Focused `test_red_metrics_preserve_applicability_and_separate_denominators` passed; current packet has no A/B/C rows and uses `not_applicable_red` / `empty_population` separately. |
| 7 | The four frozen metamorphic directions are visible and unscored on Red | ✓ VERIFIED | Focused `test_red_metamorphic_registry_is_complete_and_unscored` passed; all four records are unavailable and non-counting. |
| 8 | PairHit uses the registered empty Red population without a ratio | ✓ VERIFIED | Focused `test_pairhit_uses_only_frozen_eligible_ids` passed; packet has `pairhit.at_2` denominator 0 and no numerator/score. |
| 9 | Human decision is structurally separate and authority-limited | ✓ VERIFIED | `validate-decision` passed on the canonical decision; it binds current packet/readiness hashes and preserves non-Phase-7 authority flags. This does not cure truths 2–3. |

**Score:** 4/9 must-haves verified (0 present-but-behavior-unverified).

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `src/specchoice_evaluation/core.py` | Result, join, PairHit, metamorphic, and construction contracts | ✗ BLOCKED | Substantive and used, but construction sources are unpinned and pairwise construction accepts unverified rows. |
| `src/specchoice_evaluation/review.py` | Policy-bound packet/readiness/decision validation | ✗ BLOCKED | Substantive and wired through CLI, but validates self-consistency rather than derivation from roots. |
| `config/evaluation/partition-evaluation-red-generation-001.json` | Complete fixed input and component inventory | ✗ BLOCKED | Lists Red/data roots, but omits all construction evidence and does not enforce an exact component set. |
| `runs/.../evaluation-packet.json` and readiness receipt | Immutable decision-free Red package | ✗ BLOCKED | Current bytes validate, but the validator accepts a forged self-consistent successor. |
| `reviews/partition-evaluation-red-generation-001-decision.json` | Separate human decision | ✓ VERIFIED | Exact current hashes and limited authority validate; its provenance remains downstream of the blocked package. |
| `tests/test_partition_evaluation.py` | Regression coverage for Phase 6 contracts | ⚠️ INCOMPLETE | Focused legitimate-path tests pass; no regression rejects forged rehashed packages, bare joins, or unchanged interventions. |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `review.py` | policy-bound roots | packet validation | ✗ NOT_WIRED | No `build_red_evaluation` / canonical expected-packet comparison occurs in `validate_evaluation_packet`. |
| `core.py` | Phase-5 construction records | `build_construction_feasibility` | ✗ PARTIAL | Reads records, but not through policy inventory/hash validation. |
| `ClosedJoinManifest` | `PairwiseComparison` | closed join SHA-256 | ✗ NOT_WIRED | `build_pairwise_comparison` takes rows and controls only. |
| decision | packet/readiness | exact hashes | ✓ WIRED | `validate_review_decision` rebuilds current decision from exact packet/readiness hashes. |

### Data-Flow Trace

| Artifact | Data Variable | Source | Produces real frozen data | Status |
|---|---|---|---|---|
| packet validator | `packet.metrics` / component hashes | caller-supplied packet | No derivation check | ✗ HOLLOW |
| construction audit | `ConstructionAttempt` records | repository-relative Phase-5 files | Yes, but policy does not bind them | ✗ UNFROZEN |
| Red metric builder | deterministic metrics/populations | admitted Phase-2 roots | Yes | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command / probe | Result | Status |
|---|---|---|---|
| Self-consistent forged packet is rejected | In-memory metric/applicability mutation, recompute every hash, call `validate_readiness` | Printed `FORGED_PACKET_ACCEPTED 0.0 ...` | ✗ FAIL |
| Pairwise requires a closed join | Call `build_pairwise_comparison` with bare A/B rows | Printed `BARE_ROWS measured 1 0.0` | ✗ FAIL |
| Pairwise requires intervention change | Use identical `delegation_frame` controls | Printed `UNCHANGED_INTERVENTION_ACCEPTED measured` | ✗ FAIL |
| Current package and decision validate | `verify-red-package`; `validate-decision` | Both exit 0 | ✓ PASS (insufficient against the three probes above) |
| Red states, joins, packet/decision contracts | Four named `unittest` tests plus isolated Ruff | Exit 0 | ✓ PASS (coverage gap) |
| Red metamorphic/PairHit/construction/exact-resume | Four named `unittest` tests | Exit 0 | ✓ PASS (does not test frozen construction inventory) |

### Requirements Coverage

| Requirement | Status | Evidence |
|---|---|---|
| TS-06 | ✗ BLOCKED | Current deterministic projection exists, but a rehashed forged packet is accepted, so case-level outcome provenance is not preserved. |
| TS-13 | ✓ VERIFIED ON RED | Four frozen directions are visible as unavailable/non-counting; Green/Yellow execution is not applicable to the frozen Red branch. |
| H1-02 | ✗ BLOCKED | Future B-minus-A comparison can score without a closed join or real intervention. |
| H1-03 | ✓ VERIFIED ON RED | Frame results/warnings are Red-inapplicable and the report-only warning test passes. |
| H1-04 | ✓ VERIFIED ON RED | Frozen family/metamorphic identities are shown without invented Red observations. |
| H2-03 | ✓ VERIFIED ON RED | Registered PairHit input and zero-denominator Red state are exercised. |
| H2-04 | ✗ BLOCKED | Future C-minus-B comparison has the same missing-join and unchanged-intervention defects. |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---:|---|---|---|
| `review.py` | 235–270 | Self-hash/shape validation substitutes for root derivation | 🛑 BLOCKER | An attacker can manufacture accepted outcome values. |
| `core.py` | 645–723 | Pairwise API omits `ClosedJoinManifest` | 🛑 BLOCKER | Unjoined rows can score. |
| `core.py` | 693–718 | Intervention is excluded from equality test but never required to differ | 🛑 BLOCKER | A non-intervened pair can be attributed to an intervention. |
| `core.py` | 1005–1022 | Repository-relative construction reads absent from policy | 🛑 BLOCKER | A supposedly immutable construction audit can drift under the same policy. |
| `review.py` | 145–147 | Component inventory only checked for sortedness | ⚠️ WARNING | Declared component inventory is not an enforceable complete set. |
| `review.py` | 148–189 | Undeclared runtime path can raise `KeyError` | ⚠️ WARNING | Controlled CLI diagnostic can degrade to a traceback. |

No `TBD`, `FIXME`, or `XXX` debt markers were found in Phase-06 source/test files.

## Gaps Summary

The primary failure is an evidence-integrity break: validation proves that a package is internally self-consistent, not that it was computed from the frozen policy inputs. The separate construction audit is also outside that inventory. Independently, the intended Green/Yellow ablation path does not connect closed joins to pairwise scoring and does not require the declared intervention to change.

These are not deferred to Phase 7. Phase 7 consumes the evaluated package for a conclusion; no later phase explicitly supplies derivation verification, construction input admission, or safe pairwise join/intervention enforcement. Remediation belongs in a focused Phase-06 gap-closure plan, followed by a new immutable evaluation generation and human decision—never by rewriting the existing generation.

_Verified: 2026-08-06T11:51:29Z_
_Verifier: the agent (gsd-verifier)_

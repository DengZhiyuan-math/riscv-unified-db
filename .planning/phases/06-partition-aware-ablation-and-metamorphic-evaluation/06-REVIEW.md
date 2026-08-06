---
phase: 06-partition-aware-ablation-and-metamorphic-evaluation
reviewed: 2026-08-06T11:45:44Z
depth: standard
files_reviewed: 10
files_reviewed_list:
  - experiments/specchoice-v1.3.2/config/evaluation/partition-evaluation-red-generation-001.json
  - experiments/specchoice-v1.3.2/receipts/partition-evaluation-red-generation-001-readiness.json
  - experiments/specchoice-v1.3.2/reviews/partition-evaluation-red-generation-001-decision.json
  - experiments/specchoice-v1.3.2/runs/partition-evaluation-red-generation-001/evaluation-packet.json
  - experiments/specchoice-v1.3.2/runs/partition-evaluation-red-generation-001/evaluation-report.md
  - experiments/specchoice-v1.3.2/src/specchoice_evaluation/__init__.py
  - experiments/specchoice-v1.3.2/src/specchoice_evaluation/cli.py
  - experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py
  - experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py
  - experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py
findings:
  critical: 4
  warning: 2
  info: 0
  total: 6
status: issues_found
---

# Phase 06: Code Review Report

**Reviewed:** 2026-08-06T11:45:44Z
**Depth:** standard
**Files Reviewed:** 10
**Status:** issues_found

## Summary

The Phase 06 evaluator, package publisher, canonical artifacts, and regression suite were reviewed against the Phase 06 plans and committed source scope. The package and focused tests currently pass, but the validation boundary does not prove that a reviewed packet was derived from the frozen inputs, construction evidence is outside the fixed input inventory, and the future Green/Yellow pairwise path can manufacture valid-looking comparisons from unclosed or non-intervened rows. These defects invalidate the phase's evidence-integrity claims and must be fixed before a non-Red package or conclusion is trusted.

Validation run: `tests.test_partition_evaluation`, isolated Ruff, `verify-red-package`, and `validate-decision` all passed. The findings below were reproduced in temporary copies without modifying repository source files.

## Narrative Findings (AI reviewer)

## Critical Issues

### CR-01: Package verification accepts forged evaluation content

**Classification:** BLOCKER

**File:** `experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py:235-271`, `experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py:330-343`

**Issue:** `validate_evaluation_packet()` checks that the supplied packet is self-hashed and internally shaped, but never rebuilds it from the policy-bound roots. `validate_readiness()` then hashes that same supplied packet and Markdown projection. Consequently, an attacker can change a measured numerator/score, update the duplicated `metrics`, `applicability_matrix`, and component copies, recompute `component_sha256`, `packet_sha256`, Markdown, and readiness, and receive a successful readiness validation. This was reproduced by changing `surfacing` from `1.0` to `0.0` in a temporary copy; `validate_readiness()` accepted it. A self-consistent packet is not evidence that it was derived from the frozen authority inputs.

**Fix:** Rebuild the expected packet from validated, policy-bound inputs and require byte-for-byte canonical equality before accepting a packet/readiness pair. The recomputation must include the construction component after CR-02 is addressed.

```python
expected = build_evaluation_packet(
    build_red_evaluation(root),
    policy=policy,
    construction_attempts=build_construction_feasibility(root, policy),
)
if canonical_json_bytes(packet) != canonical_json_bytes(expected):
    _error("EVALUATION_PACKET_DERIVATION_INVALID")
```

Add a regression test that changes one metric and recomputes every packet/readiness self-hash; validation must still fail.

### CR-02: Construction evidence is not frozen by the package policy

**Classification:** BLOCKER

**File:** `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py:1005-1022`, `experiments/specchoice-v1.3.2/config/evaluation/partition-evaluation-red-generation-001.json:23-75`

**Issue:** `build_construction_feasibility()` reads 19 Phase 5 files from `root.parents[1]`, but none of those files or hashes are in the policy's fixed `inputs` inventory. `validate_evaluation_policy()` therefore succeeds after construction evidence changes. In a temporary project copy, changing `05-00-SUMMARY.md`, deleting only the output package, and calling `publish_evaluation_package()` produced a new package with a changed construction hash under the unchanged policy. This violates the advertised fixed-input and immutable-evidence boundary.

**Fix:** Put the complete construction source inventory and hashes in the policy (with an explicit, descriptor-safe project root), validate it before building, and derive construction attempts only from that admitted set. Do not infer a repository root from `root.parents[1]`.

```python
construction = policy["construction_inputs"]
files = read_authoritative_files(project_root, [item["path"] for item in construction])
if any(sha256_bytes(files[item["path"]][1]) != item["sha256"] for item in construction):
    _error("CONSTRUCTION_ARTIFACT_SUBSTITUTED")
```

Add a test that changes every declared construction source in turn and asserts policy validation/publishing fails closed.

### CR-03: Pairwise metrics do not require a verified closed join

**Classification:** BLOCKER

**File:** `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py:595-642`, `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py:645-723`

**Issue:** `close_join()` only sees arbitrary `ArtifactBinding` values and atomic rows; it has no expected artifact identity to compare against. More importantly, `build_pairwise_comparison()` accepts bare `AtomicResultRow` instances and control projections, never accepts or validates a `ClosedJoinManifest`, and never checks `status == "closed"` or a join hash. Thus incomplete, substituted, or entirely unjoined rows can produce a `measured` B-minus-A/C-minus-B result, contrary to D-08 and the Phase 06 plan's rule that only fully closed manifests may become pair evidence.

**Fix:** Make an immutable verified join reference part of each candidate row/pair input, validate each manifest's hash and `closed` status against the expected artifact records, and reject the whole comparison if either member is absent, invalid, or duplicated.

```python
if left_join.status != "closed" or right_join.status != "closed":
    return withheld_pairwise(...)
if left_join.join_sha256 != expected_left_join_hash:
    return withheld_pairwise(...)
```

Add tamper tests showing that a syntactically complete but hash-substituted join, and a bare row with no join, cannot yield `measured`.

### CR-04: A pair is accepted even when the declared intervention did not change

**Classification:** BLOCKER

**File:** `experiments/specchoice-v1.3.2/src/specchoice_evaluation/core.py:693-718`

**Issue:** The control predicate checks only that every control *other than* the intervention is equal. It never requires the intervention value itself to differ. A B/A pair whose `delegation_frame` is identical on both sides is therefore counted as `measured`; the same applies to C/B and `pair_selection`. This was reproduced with two rows whose complete control maps were identical: `build_pairwise_comparison(..., "b_minus_a", ...)` returned `measured`, denominator `1`, score `1.0`. The metric can consequently attribute outcome changes to an intervention that never occurred.

**Fix:** Require the named intervention to exist on both controls and to differ, preferably with an explicit mapping from A/B/C treatments to their permitted intervention values.

```python
if (
    intervention not in left_controls
    or left_controls[intervention] == right_controls[intervention]
    or any(left_controls[key] != right_controls[key]
           for key in left_controls if key != intervention)
):
    invalid = True
```

Add negative tests for equal intervention values, missing intervention keys, and an intervention value inconsistent with the row's treatment.

## Warnings

### WR-01: The policy's component inventory is dead validation data

**Classification:** WARNING

**File:** `experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py:145-147`, `experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py:247-251`

**Issue:** `component_ids` is only required to be a sorted list. The validator never requires the exact expected component set and never compares it with `packet["components"]`. A policy with an empty or unrelated sorted component list is accepted, and a self-hashed packet can omit an inventory component without violating this field. This makes the declared package inventory non-enforceable.

**Fix:** Define one expected component tuple, require policy equality to it, and require `set(packet["components"])` to equal the same set before hashing. Add substitution, omission, and extra-component tests.

### WR-02: A malformed runtime declaration can escape the CLI's controlled error path

**Classification:** WARNING

**File:** `experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py:148-189`

**Issue:** The runtime path is only format-checked, then indexed as `files[str(runtime["path"])]`. The validator never requires that it is one of the declared `inputs`. A malformed policy with a different valid SHA-256 runtime path raises an uncaught `KeyError` instead of `EVALUATION_POLICY_RUNTIME_INVALID`; `main()` does not catch `KeyError`, so the strict CLI emits a traceback rather than a stable fail-closed diagnostic.

**Fix:** Require the runtime path to appear exactly once in `inputs` with the same digest before accessing `files`, and convert missing entries to `EvaluationError`.

---

_Reviewed: 2026-08-06T11:45:44Z_
_Reviewer: the agent (gsd-code-reviewer)_
_Depth: standard_

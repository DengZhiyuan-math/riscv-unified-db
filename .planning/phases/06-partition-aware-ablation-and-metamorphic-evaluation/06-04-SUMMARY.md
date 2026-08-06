---
phase: 06-partition-aware-ablation-and-metamorphic-evaluation
plan: 04
subsystem: deterministic evaluation evidence publication
tags: [canonical-json, red-branch, create-only, exact-resume, readiness]
requires:
  - phase: 06-03
    provides: validated Red EvaluationBundle and construction-feasibility track
provides:
  - Fixed Red package policy with authoritative input and output inventories
  - Create-only canonical packet, Markdown projection, and readiness receipt
  - Decision-free package validation and zero-write exact resume
affects: [06-05, phase-7-interpretation]
actuals:
  tokens: 43878
  tasks: 2
  commits: 3
tech-stack:
  added: []
  patterns: [descriptor-bound exact file-set publication, canonical self-hash, decision-free machine readiness]
key-files:
  created:
    - experiments/specchoice-v1.3.2/config/evaluation/partition-evaluation-red-generation-001.json
    - experiments/specchoice-v1.3.2/runs/partition-evaluation-red-generation-001/evaluation-packet.json
    - experiments/specchoice-v1.3.2/runs/partition-evaluation-red-generation-001/evaluation-report.md
    - experiments/specchoice-v1.3.2/receipts/partition-evaluation-red-generation-001-readiness.json
  modified:
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py
    - experiments/specchoice-v1.3.2/src/specchoice_evaluation/cli.py
    - experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py
key-decisions:
  - "The published packet projects deterministic disposition scoring as classification_outcome so it cannot be mistaken for a human package outcome."
  - "An explicit --repo-root is resolved once at the CLI boundary before construction-feasibility evidence is read."
requirements-completed: [TS-06, TS-13, H1-02, H1-03, H1-04, H2-03, H2-04]
status: complete
---

# Phase 06 Plan 04: Canonical Red Package Summary

The immutable Red package now binds fixed inputs, no-call applicability, deterministic metrics, construction history, Markdown projection, and readiness without granting human approval or Phase 7 authority.

## Accomplishments

- Added a canonical generation policy that fixes all admitted input hashes, output paths, metrics, runtime-closure identity, and prohibited authority grants.
- Published and independently revalidated the three-file create-only package; its second build left bytes and nanosecond mtimes unchanged.
- Added RED contracts for input substitution, partial/different outputs, decision-free fields, and hash-bound readiness.

## Task Commits

1. **Task 1 RED: package publication contracts** — `e9143007` (`test`)
2. **Task 1 GREEN: policy and publisher** — `aaa51b75` (`feat`)
3. **Task 2: canonical Red package publication** — `c00529cd` (`feat`)

## Published Identities

- Packet file SHA-256: `c65ec3c230d847b7c869e6f6b738c0e012c8abfafeebd28a0de1b79d174ed534`
- Markdown file SHA-256: `1cbba5758c70e4f64cd558c960bf683be0f16e3ed82d1d4b10de1451c550f183`
- Readiness file SHA-256: `9ab5ea790e284e309716ff1e5b50f8b5e3695e93edebe53fccf3ca399508857c`

## Validation

- `build-red`, `verify-red-package`, and a second zero-write build all passed.
- Focused Phase 6 regression: partition evaluation, measurement scoring, data relevance, and authorized Red execution passed.
- Isolated Ruff and `git diff --check` passed.

## Deviations from Plan

### Auto-fixed Issues

1. **[Rule 1 - Bug] Resolve explicit relative repository roots at the CLI boundary**
   - **Found during:** Task 2 publication
   - **Fix:** Resolve `--repo-root` before reading Phase 5 construction evidence.

2. **[Rule 1 - Boundary correctness] Keep machine classification metrics out of the human-outcome vocabulary**
   - **Found during:** Task 2 contract verification
   - **Fix:** Project the deterministic `disposition` metric as `classification_outcome` in the decision-free packet and policy; source metric calculation and hashes remain independent.

## Known Stubs

None.

## TDD Gate Compliance

The RED contract commit `e9143007` precedes GREEN implementation commit `aaa51b75`.

## Next Phase Readiness

Plan 06-05 can request the separate human package decision against the exact packet and readiness hashes. This package is machine-ready only; `conclusion_ready` remains false and no model, provider, retrieval, network, subprocess, or external-publication authority is granted.

## Self-Check: PASSED

- All seven plan artifacts exist at their declared paths.
- Commits `e9143007`, `aaa51b75`, and `c00529cd` exist in local history.

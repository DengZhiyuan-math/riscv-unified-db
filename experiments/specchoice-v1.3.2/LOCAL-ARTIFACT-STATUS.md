# Local Artifact Status

This inventory distinguishes material recovered from a local workspace on
2026-08-06.  It is an operational index only; it does not alter the authority
of any existing receipt, review decision, or failed-closed record.

## Published working artifacts

| Path | Status | Notes |
| --- | --- | --- |
| `.planning/phases/02-deterministic-measurement-spine/02-REVIEW-FIX 2.md` | completed review-fix record | Records the already-applied Phase 02 custody fix at commit `29798a2a`. |
| `experiments/specchoice-v1.3.2/tests/test_guarded_regress.py` and `experiments/specchoice-v1.3.2/validation/guarded_regress.py` | active hardening | Adds deterministic network-denial and pinned-toolchain preflight coverage to the guarded regression harness. |
| `experiments/specchoice-v1.3.2/submissions/coding-challenge/` and `experiments/specchoice-v1.3.2/submissions/Zhiyuan_Deng_RISCV_Parameter_Extraction_Challenge.zip` | reviewed submission package | The directory is the unpacked, checksummed source package; the ZIP is its distribution form. |
| `output/pdf/Zhiyuan_Deng_RISCV_Parameter_Extraction_Challenge.pdf` | submission rendering | Human-readable rendering of the coding-challenge submission. |
| `idl.html` | generated reference | Generated ISA Description Language reference; informative only, not a measurement or execution receipt. |

## Preserved failure and diagnostic custody already in the repository

These records are deliberately retained as failed-closed evidence, never as
successful execution or release authority:

- `experiments/specchoice-v1.3.2/runs/native-port-darwin-arm64-20260805/original-whole-binary-sha-mismatch.json`
- `experiments/specchoice-v1.3.2/runs/native-port-darwin-arm64-projection-v2-20260805/contract-validation.json`
- `.planning/phases/06-partition-aware-ablation-and-metamorphic-evaluation/06-08-FAILED-CLOSED.md`

## Not published from the recovered workspace

| Local path | Classification | Reason |
| --- | --- | --- |
| `experiments/specchoice-v1.3.2/validation/native_port_build 2.py` | superseded local attempt | A duplicate-named draft beside the canonical tracked validator; no receipt binds this filename. |
| `experiments/specchoice-v1.3.2/validation/native_port_validate 2.py` | superseded local attempt | A duplicate-named draft beside the canonical tracked validator; no receipt binds this filename. |
| `Gemfile.lock` arm64 platform addition | local environment resolution | Adds only the local Darwin platform and is not part of the SpecChoice work product. |
| `test-profile_extensions.txt` | empty transient output | Zero-byte local command output. |
| `.DS_Store`, caches, stamps, and temporary directories | workstation metadata | Not source, evidence, or a deliverable. |

The local files listed above remain recoverable in the workspace and the
pre-sync stash; they are intentionally not promoted into the published
research history.

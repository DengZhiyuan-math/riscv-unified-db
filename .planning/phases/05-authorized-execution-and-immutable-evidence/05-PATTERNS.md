# Phase 05: Authorized Execution and Immutable Evidence - Pattern Map

**Mapped:** 2026-08-05  
**Files analyzed:** 5 implementation/config/test files (plus generated custody leaves)  
**Analogs found:** 5 / 5

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `experiments/specchoice-v1.3.2/src/specchoice_execution/__init__.py` | package | transform | `experiments/specchoice-v1.3.2/src/specchoice_treatments/__init__.py` | role-match |
| `experiments/specchoice-v1.3.2/src/specchoice_execution/red.py` | service | request-response / file-I/O | `experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py` | role-match |
| `experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py` | controller | request-response / file-I/O | `experiments/specchoice-v1.3.2/src/specchoice_treatments/cli.py` | exact |
| `experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json` | config | transform | `experiments/specchoice-v1.3.2/config/treatments/lexical-retrieval-contract-v1.json` | role-match |
| `experiments/specchoice-v1.3.2/tests/test_authorized_execution.py` | test | request-response / file-I/O | `experiments/specchoice-v1.3.2/tests/test_treatments_h3.py` | role-match |

Generated evidence belongs under the new frozen policy's declared, repository-relative targets (for example `runs/red-attempts/`, `reports/red-execution/`, and `receipts/`). It is output, not a pre-created source fixture; targets must be absent during formal preflight.

## Pattern Assignments

### `experiments/specchoice-v1.3.2/src/specchoice_execution/red.py` (service, request-response / file-I/O)

**Analog:** `experiments/specchoice-v1.3.2/src/specchoice_treatments/h3.py`

**Imports and boundary pattern** (lines 6-28):

```python
import argparse
import ast
from collections.abc import Mapping
from pathlib import Path

from specchoice_evidence.canonical import canonical_json_bytes, sha256_bytes
from specchoice_evidence.filesystem import (
    FilesystemPolicyError,
    enumerate_authoritative_files,
    read_authoritative_file,
    write_exact_descriptor_files,
)
from specchoice_measurement.strict_json import decode_strict_json
```

Copy the explicit standard-library/repository-local imports, but do not import a provider SDK, HTTP client, credentials loader, process-spawn API, or retrieval runtime. The Phase 5 static scan must cover this module and its CLI itself.

**Forbidden-surface scan pattern** (lines 268-289):

```python
tree = ast.parse(raw.decode("utf-8"), filename=path)
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        names = [item.name for item in node.names]
    elif isinstance(node, ast.ImportFrom) and node.module is not None:
        names = [node.module]
    # Reject forbidden import roots and dynamic import/eval/exec calls.
```

Extend the closed forbidden set to provider/model/credential/production-retrieval/process-spawn/network surfaces required by D-05/D-08; return a canonical scan report with the scanned inventory and hash. A blocked socket attempt is a `security_events` record in a failed attempt, never a model-call-ledger entry.

**Exact authority admission pattern** (lines 3175-3195):

```python
validated_authority = validate_h3_red_authority_v6(
    authority=authority,
    freeze_inputs=freeze_inputs,
    packet=packet,
    readiness=readiness,
    decision_raw=decision_raw,
)
```

Admission must call this validator against persisted Phase 4 v6 roots before any output writer opens. Reject v1-v5 authority, non-`approved_red`, any nonzero `N_strict`/repeat count, or any true authorization flag; never parse a lookalike authority directly.

**Closed CLI reachability pattern** (lines 311-343): build the parser, enumerate its only allowed command(s), parse representative allowed arguments, and prove an unknown/model command exits without a network operation. Phase 5 adds the stricter all-socket tripwire around the Red execution body.

### `experiments/specchoice-v1.3.2/src/specchoice_execution/cli.py` (controller, request-response / file-I/O)

**Analog:** `experiments/specchoice-v1.3.2/src/specchoice_treatments/cli.py`

**Singleton parser and stable-error pattern** (lines 50-70):

```python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="specchoice-treatments")
    commands = parser.add_subparsers(dest="command", required=True)
    command = commands.add_parser("verify-retrieval-contract")
    command.add_argument("--target", required=True)
    command.set_defaults(handler=_verify_retrieval_contract)
    return parser

def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        return int(args.handler(args))
    except (RetrievalContractError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
```

Keep the Phase 5 surface deliberately small (one execution/validation command family, `allow_abbrev=False`, explicit repository-relative input/target arguments). Emit canonical JSON to stdout only for a validated result and stable diagnostics to stderr. Do not add a `model-run`, provider configuration, credentials, or production retrieval command.

### `experiments/specchoice-v1.3.2/config/execution/red-execution-policy-v1.json` (config, transform)

**Analog:** `experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py`

**Frozen inventory and output preflight pattern** (lines 187-256):

```python
closure = build_runtime_closure(root, relative_paths)
verify_runtime_closure(closure, root)
inventory = validate_v6_preflight_inventory(
    root=root,
    input_paths=input_paths,
    target_paths=target_paths,
)
```

The policy must be closed-key canonical JSON and declare the execution-code/schema/CLI authority inputs, Phase 4 v6 binding inputs, allowed commands, forbidden surface policy, expected repository-relative outputs, and `conditional_not_applicable_red_pending_phase7` states for TS-11/TS-12. The policy must freeze `branch=red`, `N_strict=0`, `repeat_count=0`, and no external/model/production-retrieval authority. Do not include timestamps, absolute paths, credentials, provider names, or mutable target content.

### `experiments/specchoice-v1.3.2/src/specchoice_execution/__init__.py` (package, transform)

**Analog:** `experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py`

Keep this package boundary minimal: export only the explicit Red executor/validator API needed by its CLI and tests. Canonical output construction must use the shared functions, not a Phase 5 serializer:

```python
def canonical_json_bytes(value: Any) -> bytes:
    normalized = normalize_canonical_value(value)
    return (
        json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
```

Source: `experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py` lines 40-50.

### `experiments/specchoice-v1.3.2/tests/test_authorized_execution.py` (test, request-response / file-I/O)

**Analog:** `experiments/specchoice-v1.3.2/tests/test_treatments_h3.py`

**No-network test pattern** (lines 143-153):

```python
with patch(
    "socket.create_connection", side_effect=AssertionError("network call")
) as connection:
    audit = audit_no_model_reachability_v1(load_phase4_freeze_inputs_v1())

self.assertTrue(all(value is True for value in audit["checks"].values()))
connection.assert_not_called()
```

Phase 5 must strengthen this with one adversarial test for each denied socket constructor (`socket`, `create_connection`, `create_server`, `socketpair`, and `fromfd`) across loopback, LAN, and external address forms. Assert the stable denial diagnostic, an empty real-call ledger, a non-authoritative failed-attempt package, and no formal target.

**Exact resume / authority round-trip pattern** (lines 846-914): construct fresh bound inputs in a temporary root, publish once, validate the exact persisted bytes, then invoke again and assert the same object/bytes. Phase 5's second invocation must additionally assert zero writes; tampering, occupied target, closure drift, partial formal leaves, or different bytes at the same formal target must fail closed.

**Do not copy the legacy attempt cleanup behavior.** `experiments/specchoice-v1.3.2/src/specchoice_measurement/attempts.py` lines 196-241 deletes a staging directory on exception and permits `completed_with_warnings` (lines 72-79), both incompatible with D-01/D-03/D-14. Reuse its manifest/hash sibling-binding ideas only after implementing Red-specific failed-attempt custody.

## Shared Patterns

### Canonical JSON and hashes

**Source:** `experiments/specchoice-v1.3.2/src/specchoice_evidence/canonical.py` lines 24-50  
**Apply to:** policy, ledger, static/runtime audits, matrix manifest, attempt manifests, terminal receipt, and Markdown source binding.

Canonical machine JSON is NFC/LF-normalized, sorted-key, compact UTF-8 with one LF; SHA-256 always hashes the authoritative raw bytes. Markdown is a deterministic projection only and cannot be an authority.

### Strict input parsing and diagnostics

**Source:** `experiments/specchoice-v1.3.2/src/specchoice_measurement/strict_json.py` lines 32-78; `experiments/specchoice-v1.3.2/src/specchoice_measurement/diagnostics.py` lines 10-46  
**Apply to:** Phase 4 authority/decision leaves, Phase 5 policy, every receipt/audit validator, and failure records.

`decode_strict_json` rejects duplicate keys and non-finite values. Validators collect closed-key/type failures as `Diagnostic` objects, then emit `ordered_diagnostics(...)`; no loose `json.loads`, silent coercion, or unordered exception text.

### Descriptor-bound immutable publication

**Source:** `experiments/specchoice-v1.3.2/src/specchoice_evidence/filesystem.py` lines 29-39, 198-234, 251-259  
**Apply to:** complete formal evidence file set and each failed-attempt package.

```python
write_exact_descriptor_files(root, payloads)
```

Supply only complete, prevalidated canonical bytes at repository-relative paths. The helper rejects path escapes/symlinks and preflights/postflights a no-replace set. Treat a pre-existing target as either exact validated resume (read-only) or a stable failure—never overwrite it.

### Frozen closure before writes

**Source:** `experiments/specchoice-v1.3.2/src/specchoice_evidence/runtime_closure.py` lines 187-256  
**Apply to:** all Phase 5 code, policy/schema, CLI, Phase 4 v6 inputs, and declared output target inventory.

Validate every input hash and prove all formal targets absent before construction. Re-run the closure and root validation immediately before formal publication; drift requires a successor candidate and human H3/Phase 5 authorization, not an automatic migration.

### Red-only evidence-state rules

**Source:** Phase 5 locked decisions D-01 through D-16 in `05-CONTEXT.md`  
**Apply to:** every Phase 5 module and output.

- Formal completion has status `completed` only; never `completed_with_warnings`.
- A completed ledger is exactly zero entries; blocked operations appear only in failed-attempt `security_events`.
- The A/B/C matrix is canonical JSON with `expected_cells=0`, `actual_cells=0`, treatment counts all zero, and `cells=[]`; no placeholder call/raw response or model metric.
- The terminal receipt binds the ordered complete attempt chain and grants only Phase 6/7 Red-evidence evaluation permission.

## No Analog Found

| File/Concern | Role | Data Flow | Reason / Planner Direction |
|---|---|---|---|
| Red-specific failed-attempt state machine | service | event-driven / file-I/O | Existing measurement attempts are intentionally incompatible: warning terminal roles and staging cleanup would lose required failure custody. Build a minimal new closed schema while reusing canonical, filesystem, closure, strict parsing, and diagnostic primitives. |
| All-socket runtime tripwire | middleware | event-driven | Phase 4 tests only demonstrate `socket.create_connection` is unused. Phase 5 must add and adversarially prove the complete standard-library guard set before formal use. |

## Metadata

**Analog search scope:** `experiments/specchoice-v1.3.2/src/specchoice_evidence/`, `src/specchoice_measurement/`, `src/specchoice_treatments/`, and `tests/`  
**Files scanned:** 12 primary modules/tests plus Phase 5 context, research, validation, roadmap, and requirements  
**Pattern extraction date:** 2026-08-05

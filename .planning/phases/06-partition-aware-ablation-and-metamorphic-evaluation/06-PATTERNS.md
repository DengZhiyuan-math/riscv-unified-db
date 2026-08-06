# Phase 06: Partition-Aware Ablation and Metamorphic Evaluation - Pattern Map

**Mapped:** 2026-08-06  
**Files analyzed:** 6 implementation/test files  
**Analogs found:** 6 / 6

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `experiments/specchoice-v1.3.2/src/specchoice_evaluation/admission.py` | service | file-I/O, transform | `src/specchoice_execution/red_v2.py` | exact |
| `experiments/specchoice-v1.3.2/src/specchoice_evaluation/manifests.py` | model/utility | transform | `src/specchoice_measurement/scoring.py` | role-match |
| `experiments/specchoice-v1.3.2/src/specchoice_evaluation/evaluation.py` | service | transform | `src/specchoice_measurement/scoring.py` | exact |
| `experiments/specchoice-v1.3.2/src/specchoice_evaluation/review.py` | service | file-I/O, transform | `src/specchoice_data/relevance.py` | exact |
| `experiments/specchoice-v1.3.2/src/specchoice_evaluation/cli.py` | controller/CLI | request-response | `src/specchoice_execution/cli_v2.py` | exact |
| `experiments/specchoice-v1.3.2/tests/test_partition_evaluation.py` | test | batch, file-I/O | `tests/test_authorized_execution_v2.py` | role-match |

The proposed `runs/phase6-evaluation-*`, `receipts/phase6-evaluation-*.json`, and `reviews/phase6-evaluation-*.json` are immutable generated evidence targets, not hand-maintained implementation files. Define their exact names/schema in the Phase 6 policy/contract and publish them through the existing no-replace primitives.

## Pattern Assignments

### `src/specchoice_evaluation/admission.py` (service, file-I/O/transform)

**Analog:** `experiments/specchoice-v1.3.2/src/specchoice_execution/red_v2.py`

**Imports and authoritative-root validation** (lines 18-27, 143-168):

```python
from specchoice_evidence.canonical import canonical_json_bytes, sha256_bytes
from specchoice_evidence.filesystem import read_authoritative_file
from specchoice_measurement.diagnostics import ordered_diagnostics

def validate_red_authority_v2(root: Path, policy: Mapping[str, object] | None = None) -> dict[str, object]:
    """Rebuild, rather than trust, the Phase 4 v6 Red authority."""
    ...
    if authority.get("branch") != "red" or authority.get("N_strict") != 0 or authority.get("repeat_count") != 0:
        raise RedExecutionV2Error("RED_AUTHORITY_SUBSTITUTION")
    if any(authority.get(key) is not False for key in (...)):
        raise RedExecutionV2Error("RED_AUTHORITY_SUBSTITUTION")
    return authority
```

**Red evidence gate** (lines 279-293):

```python
if not isinstance(receipt, dict) or receipt.get("schema_version") != "red-execution-receipt-v2" or receipt.get("status") != "completed":
    raise RedExecutionV2Error("RED_EVIDENCE_INVALID")
ledger, _raw = _load_canonical(root, _FORMAL[3])
matrix, _raw = _load_canonical(root, _FORMAL[2])
parsed, _raw = _load_canonical(root, _FORMAL[7])
if ledger != {"calls": [], "schema_version": "red-model-call-ledger-v2"} or matrix.get("cells") != [] or matrix.get("expected_cells") != 0 or parsed.get("findings") != []:
    raise RedExecutionV2Error("RED_EVIDENCE_INVALID")
```

**Apply:** build two independent admission results (`deterministic_measurement`, `red_execution_evidence`) before any evaluation object. Do not merge their diagnostics, counts, rows, or outcomes. Rebuild/validate accepted upstream roots; never trust a supplied digest alone.

---

### `src/specchoice_evaluation/manifests.py` (model/utility, transform)

**Analogs:** `src/specchoice_measurement/scoring.py`; `src/specchoice_data/relevance.py`

**Immutable serializable metric model** (`scoring.py` lines 12-20):

```python
@dataclass(frozen=True)
class Metric:
    """An independently denominated metric with no blended headline score."""
    numerator: int
    denominator: int

    def as_dict(self) -> dict[str, int]:
        return asdict(self)
```

**Complete ordered-ID validation** (`relevance.py` lines 76-130):

```python
observed_ids = [row.get("case_id") if isinstance(row, Mapping) else None for row in rows]
if observed_ids != sorted(expected_ids) or len(observed_ids) != len(set(observed_ids)):
    raise RelevanceValidationError("RELEVANCE_STRICT_COVERAGE_INVALID")
```

**Apply:** make frozen dataclasses/unions for atomic rows, population manifests, closed joins, and result states. Each population owns ordered eligible/included/excluded IDs, stable exclusion reasons, and a canonical set hash. Recompute its denominator from eligible-ID length. A state union must make numerator/denominator/score impossible for `empty_population`, `not_applicable_red`, and `invalid_withheld`.

---

### `src/specchoice_evaluation/evaluation.py` (service, transform)

**Analog:** `experiments/specchoice-v1.3.2/src/specchoice_measurement/scoring.py`

**Independent metric construction** (lines 313-333):

```python
return ScoreMetrics(
    surfacing=Metric(sum(item.surfacing_correct for item in expected_surfaced), len(expected_surfaced)),
    disposition=Metric(sum(item.disposition_correct for item in outcomes if item.category != "negative"), len(expected_surfaced)),
    identity=Metric(sum(item.identity_outcome == "exact" for item in positive_accepts), len(positive_accepts)),
    evidence_integrity=Metric(valid_span_count, total_span_count),
)
```

**Fail-closed scoring** (lines 335-385):

```python
diagnostics = _score_gate_diagnostics(adapter_batch=adapter_batch, preflight=preflight)
if any(item.severity == "blocker" for item in diagnostics):
    return ScoreResult("invalid_preflight", (), None, ordered_diagnostics(diagnostics))
...
if any(item.severity == "blocker" for item in ordered):
    return ScoreResult("invalid_score", outcomes, None, ordered)
```

**Apply:** follow this gating shape, but retain the locked Phase 6 states verbatim: `measured`, `empty_population`, `not_applicable_red`, `invalid_withheld`. Close every join before deriving any deterministic, PairHit, A/B/C, metamorphic, or repeat comparison. A blocker withholds its affected domain and dependent results; it must not emit partial metrics. Construction-feasibility stays an audit track and never becomes an experimental metric.

---

### `src/specchoice_evaluation/review.py` (service, file-I/O/transform)

**Analogs:** `experiments/specchoice-v1.3.2/src/specchoice_data/relevance.py`; `src/specchoice_evidence/canonical.py`; `src/specchoice_evidence/filesystem.py`

**Packet → Markdown → readiness** (`relevance.py` lines 375-434):

```python
payload = {
    ...
    "no_model_or_retrieval_inputs": True,
    "schema_version": "relevance-metamorphic-review-packet-v1",
}
return {**payload, "packet_sha256": sha256_bytes(canonical_json_bytes(payload))}

def render_relevance_metamorphic_markdown_v1(packet: Mapping[str, object]) -> bytes:
    return ("# Phase 3 Relevance and Metamorphic Review\n\n" ...).encode("utf-8") + canonical_json_bytes(packet) + b"```\n"
```

**Decision content binding** (`relevance.py` lines 436-481):

```python
if decision.get("packet_sha256") != packet.get("packet_sha256") or decision.get("readiness_sha256") != readiness.get("readiness_sha256"):
    raise RelevanceValidationError("RELEVANCE_METAMORPHIC_DECISION_BINDING_INVALID")
if not _self_hash_valid(decision, "decision_sha256"):
    raise RelevanceValidationError("RELEVANCE_METAMORPHIC_DECISION_HASH_INVALID")
```

**Canonical bytes and strict hash** (`canonical.py` lines 40-64):

```python
def canonical_json_bytes(value: Any) -> bytes:
    normalized = normalize_canonical_value(value)
    return (json.dumps(normalized, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")

def require_sha256(value: object) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise CanonicalValueError("CANONICAL_SHA256_INVALID")
    return value
```

**Apply:** generate a decision-free canonical package whose first projection sections are Red declaration/no-call facts and then applicability matrix. Generate readiness as a separate hash-bound artifact; validate an explicit approved/disputed/incomplete human decision separately. Markdown is a deterministic non-authoritative view only.

For outputs, use `write_exact_descriptor_files` (`filesystem.py` lines 251-300) and `read_authoritative_files` (lines 660-705), never ordinary check-then-write reads. Exact resume must accept only byte-identical complete output sets; partial, symlinked, occupied, or differing targets fail closed.

---

### `src/specchoice_evaluation/cli.py` (controller/CLI, request-response)

**Analog:** `experiments/specchoice-v1.3.2/src/specchoice_execution/cli_v2.py`

**Strict CLI and stable failure code** (lines 12-42):

```python
class _NoAbbrevParser(argparse.ArgumentParser):
    def __init__(self, *args: object, **kwargs: object) -> None:
        kwargs["allow_abbrev"] = False
        super().__init__(*args, **kwargs)

def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        return int(args.handler(args))
    except (RedExecutionV2Error, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
```

**Apply:** one local standard-library CLI, no abbreviated flags, fixed expected paths, canonical receipt JSON to stdout, stable diagnostics to stderr, and no network/provider/model/retrieval imports or behavior. Enforce exact policy arguments before any read, construction, or publication.

---

### `tests/test_partition_evaluation.py` (test, batch/file-I/O)

**Analogs:** `experiments/specchoice-v1.3.2/tests/test_authorized_execution_v2.py`; `tests/test_data_relevance.py`

**Copy-root and exact-resume contract** (`test_authorized_execution_v2.py` lines 31-55, 111-119):

```python
def _copy_experiment(self, directory: str) -> Path:
    root = Path(directory) / "experiment"
    shutil.copytree(EXPERIMENT, root, ignore=shutil.ignore_patterns("__pycache__"))
    return root

before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in paths}
self.assertEqual(0, self._run(root)[0])
self.assertEqual(before, {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in paths})
```

**Canonical fixture self-hash helper** (`test_data_relevance.py` lines 50-53):

```python
@staticmethod
def _hash(value: dict[str, object], field: str) -> dict[str, object]:
    payload = {key: item for key, item in value.items() if key != field}
    return {**payload, field: sha256_bytes(canonical_json_bytes(payload))}
```

**Apply:** create one `unittest.TestCase` with only deterministic local fixtures. Cover the Validation Strategy's listed contracts: result-state/applicability and separate denominators; four unscored Red metamorphic directions; missing/duplicate/extra/cross-partition join failure; warning report-only behavior; drift propagation; PairHit eligibility; C-minus-B independence; package/readiness/decision hash binding; and exact-resume/tamper/occupied-target rejection. Keep tests isolated in temporary copied experiment roots and assert predecessor namespaces remain byte-unchanged.

## Shared Patterns

### Canonical identity and authoritative reads

**Sources:** `src/specchoice_evidence/canonical.py` lines 24-64; `src/specchoice_evidence/filesystem.py` lines 655-705.  
**Apply to:** admission, manifests, review, CLI publication, and tests.

Use canonical UTF-8/LF JSON and SHA-256 only through the existing helpers. Use descriptor-bound reads for upstream and output evidence; all expected path sets must be relative POSIX paths.

### Diagnostics and withholding

**Source:** `src/specchoice_measurement/diagnostics.py` lines 10-46.  
**Apply to:** all new Phase 6 services.

```python
SEVERITY_RANK = {"blocker": 0, "warning": 1}

def ordered_diagnostics(items: list[Diagnostic] | tuple[Diagnostic, ...]) -> tuple[Diagnostic, ...]:
    return tuple(sorted(items, key=Diagnostic.sort_key))
```

Extend (do not repurpose) the record to carry Phase 6 `domain`, `severity`, and `effect`. Blocking diagnostics yield `invalid_withheld`; advisory warnings are independent ledger entries with `report_only` effect.

### Red-only authority boundary

**Source:** `src/specchoice_execution/red_v2.py` lines 143-168, 279-319.  
**Apply to:** admission and CLI.

No network, provider configuration, model execution, retrieval, calls, synthetic G/Y case rows, or claimed Green/Yellow score. Red has `N_strict=0`, `repeat_count=0`, an empty call ledger and matrix; represent G/Y metrics as `not_applicable_red`, not zero.

### Immutable publication and resume

**Sources:** `src/specchoice_evidence/filesystem.py` lines 251-300; `src/specchoice_execution/red_v2.py` lines 296-319.  
**Apply to:** review package, readiness, receipts, output manifests, and reports.

Create exactly one complete no-replace file set. If any target exists, accept only a complete byte-identical set validated through authoritative reads; never repair or overwrite it.

## No Analog Found

None. The new `specchoice_evaluation` namespace is new, but every required behavior has a direct local implementation analog. The closest composition is new by design: it must remain a thin Phase 6 layer rather than duplicate scorer, registry, Red-authority, canonicalization, or filesystem primitives.

## Metadata

**Analog search scope:** `experiments/specchoice-v1.3.2/src/specchoice_{measurement,data,execution,evidence}/`, `experiments/specchoice-v1.3.2/tests/`  
**Files scanned:** 12 source/test files plus Phase 6 context, research, and validation artifacts  
**Pattern extraction date:** 2026-08-06

# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Composition-only Red evaluation with independent authority namespaces."""

from __future__ import annotations

import base64
import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

from specchoice_data.relevance import (
    REQUIRED_METAMORPHIC_DIRECTIONS,
    RelevanceValidationError,
    validate_metamorphic_registry_v1,
)
from specchoice_evidence.canonical import canonical_json_bytes, sha256_bytes
from specchoice_evidence.filesystem import (
    FilesystemPolicyError,
    read_authoritative_files,
)
from specchoice_execution.red_v2 import (
    RedExecutionV2Error,
    validate_red_authority_v2,
    validate_red_evidence_v2,
)
from specchoice_measurement.diagnostics import Diagnostic, ordered_diagnostics


RESULT_STATES = ("measured", "empty_population", "not_applicable_red", "invalid_withheld")
METRIC_IDS = tuple(sorted((
    "b_minus_a", "c_minus_b", "classify_out", "disposition", "evidence_integrity",
    "frame_authority", "frame_choice_object", "frame_choice_space_origin", "identity_exact",
    "identity_incorrect", "identity_missing", "metamorphic_choice_space_origin",
    "metamorphic_hardware_software_authority", "metamorphic_normative_note_example",
    "metamorphic_warl_fixed_legal_set", "negative_controls", "pairhit_at_2",
    "repeat_disagreement", "shortcut_family_delta", "surfacing",
)))

_DETERMINISTIC_PATHS = (
    "phase2/source-authority.json",
    "runs/measurement-attempts/formal-golden-pr2164-v6/attempt.json",
    "runs/measurement-attempts/formal-golden-pr2164-v6/case-outcomes.json",
    "runs/measurement-attempts/formal-golden-pr2164-v6/metrics.json",
    "runs/measurement-attempts/formal-golden-pr2164-v6/diagnostics.json",
)
_METAMORPHIC_PATHS = (
    "phase3/data-authority-v1.json",
    "data/preregistration/metamorphic-registry-v1.json",
)


class EvaluationError(ValueError):
    """Stable failure for a withheld Phase 6 evaluation domain."""


@dataclass(frozen=True)
class DimensionBinding:
    applicable: bool
    value: str | None
    reason: str | None

    def __post_init__(self) -> None:
        if self.applicable != (self.value is not None) or (self.applicable and self.reason is not None):
            raise EvaluationError("DIMENSION_BINDING_INVALID")
        if not self.applicable and (self.value is not None or not self.reason):
            raise EvaluationError("DIMENSION_BINDING_INVALID")


@dataclass(frozen=True)
class AtomicResultRow:
    authority_domain: str
    partition: str
    case_id: str
    treatment: DimensionBinding
    repeat_id: DimensionBinding
    outcome_id: str
    outcome: Mapping[str, object]

    def identity(self) -> tuple[str, str, str, str, str, str]:
        return (
            self.authority_domain, self.partition, self.case_id,
            self.treatment.value or self.treatment.reason or "",
            self.repeat_id.value or self.repeat_id.reason or "", self.outcome_id,
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "authority_domain": self.authority_domain,
            "case_id": self.case_id,
            "outcome": dict(self.outcome),
            "outcome_id": self.outcome_id,
            "partition": self.partition,
            "repeat_id": asdict(self.repeat_id),
            "treatment": asdict(self.treatment),
        }


@dataclass(frozen=True)
class PopulationManifest:
    population_id: str
    partition: str
    eligible_ids: tuple[str, ...]
    included_ids: tuple[str, ...]
    excluded_ids: tuple[str, ...]
    exclusion_reasons: Mapping[str, str]
    set_sha256: str
    denominator: int

    def as_dict(self) -> dict[str, object]:
        return {
            "denominator": self.denominator,
            "eligible_ids": list(self.eligible_ids),
            "excluded_ids": list(self.excluded_ids),
            "exclusion_reasons": dict(sorted(self.exclusion_reasons.items())),
            "included_ids": list(self.included_ids),
            "partition": self.partition,
            "population_id": self.population_id,
            "set_sha256": self.set_sha256,
        }


@dataclass(frozen=True)
class MetricResult:
    metric_id: str
    state: str
    authority_bindings: Mapping[str, str]
    population_id: str | None = None
    population_sha256: str | None = None
    numerator: int | None = None
    denominator: int | None = None
    score: float | None = None
    reason: str | None = None
    blocking_diagnostics: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        if self.metric_id not in METRIC_IDS or self.state not in RESULT_STATES:
            raise EvaluationError("METRIC_RESULT_INVALID")
        measured = self.state == "measured"
        if measured:
            if (
                self.population_id is None or self.population_sha256 is None
                or isinstance(self.numerator, bool) or not isinstance(self.numerator, int)
                or isinstance(self.denominator, bool) or not isinstance(self.denominator, int)
                or self.denominator <= 0 or self.numerator < 0 or self.numerator > self.denominator
                or self.score != self.numerator / self.denominator or self.reason is not None or self.blocking_diagnostics
            ):
                raise EvaluationError("METRIC_RESULT_INVALID")
            return
        if self.numerator is not None or self.denominator is not None or self.score is not None:
            raise EvaluationError("METRIC_RESULT_INVALID")
        if self.state == "empty_population" and (self.population_id is None or self.population_sha256 is None or self.reason is not None or self.blocking_diagnostics):
            raise EvaluationError("METRIC_RESULT_INVALID")
        if self.state == "not_applicable_red" and (not self.reason or self.blocking_diagnostics):
            raise EvaluationError("METRIC_RESULT_INVALID")
        if self.state == "invalid_withheld" and (not self.blocking_diagnostics or self.reason is not None):
            raise EvaluationError("METRIC_RESULT_INVALID")

    def as_dict(self) -> dict[str, object]:
        value: dict[str, object] = {
            "authority_bindings": dict(sorted(self.authority_bindings.items())),
            "metric_id": self.metric_id,
            "state": self.state,
        }
        if self.population_id is not None:
            value["population_id"] = self.population_id
            value["population_sha256"] = self.population_sha256
        if self.state == "measured":
            value.update(numerator=self.numerator, denominator=self.denominator, score=self.score)
        if self.reason is not None:
            value["reason"] = self.reason
        if self.blocking_diagnostics:
            value["blocking_diagnostics"] = [item.as_dict() for item in self.blocking_diagnostics]
        return value


@dataclass(frozen=True)
class AuthorityAdmission:
    authority_domain: str
    source_paths: tuple[str, ...]
    source_sha256: str
    status: str
    diagnostics: tuple[Diagnostic, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "authority_domain": self.authority_domain,
            "diagnostics": [item.as_dict() for item in self.diagnostics],
            "source_paths": list(self.source_paths),
            "source_sha256": self.source_sha256,
            "status": self.status,
        }


@dataclass(frozen=True)
class EvaluationBundle:
    schema_version: str
    branch: str
    n_strict: int
    repeat_count: int
    no_model_calls: bool
    deterministic_measurement: AuthorityAdmission
    red_execution_evidence: AuthorityAdmission
    applicability_matrix: tuple[MetricResult, ...]
    populations: tuple[PopulationManifest, ...]
    rows: tuple[AtomicResultRow, ...]
    metrics: tuple[MetricResult, ...]
    diagnostics: tuple[Diagnostic, ...]
    metamorphic_directions: tuple[Mapping[str, object], ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "applicability_matrix": [item.as_dict() for item in self.applicability_matrix],
            "branch": self.branch,
            "deterministic_measurement": self.deterministic_measurement.as_dict(),
            "diagnostics": [item.as_dict() for item in self.diagnostics],
            "metamorphic_directions": [dict(item) for item in self.metamorphic_directions],
            "metrics": [item.as_dict() for item in self.metrics],
            "n_strict": self.n_strict,
            "no_model_calls": self.no_model_calls,
            "populations": [item.as_dict() for item in self.populations],
            "red_execution_evidence": self.red_execution_evidence.as_dict(),
            "repeat_count": self.repeat_count,
            "rows": [item.as_dict() for item in self.rows],
            "schema_version": self.schema_version,
        }


def _diagnostic(code: str, field: str) -> Diagnostic:
    return Diagnostic(code, "blocker", field=field)


def _canonical_object(raw: bytes, code: str) -> object:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise EvaluationError(code) from error
    if canonical_json_bytes(value) != raw:
        raise EvaluationError(code)
    return value


def _admission(domain: str, source_paths: Sequence[str], files: Mapping[str, tuple[object, bytes]], diagnostics: tuple[Diagnostic, ...]) -> AuthorityAdmission:
    basis = [{"path": path, "sha256": sha256_bytes(files[path][1])} for path in sorted(source_paths)]
    return AuthorityAdmission(domain, tuple(sorted(source_paths)), sha256_bytes(canonical_json_bytes(basis)), "admitted" if not diagnostics else "invalid_withheld", diagnostics)


def _admit_deterministic(root: Path) -> AuthorityAdmission:
    try:
        files = read_authoritative_files(root, list(_DETERMINISTIC_PATHS))
        values = {path: _canonical_object(raw, "DETERMINISTIC_CANONICAL_INVALID") for path, (_evidence, raw) in files.items()}
        authority = values[_DETERMINISTIC_PATHS[0]]
        attempt = values[_DETERMINISTIC_PATHS[1]]
        if not isinstance(authority, dict) or authority.get("status") != "accepted_cutover_v13" or authority.get("local_only") is not True:
            raise EvaluationError("DETERMINISTIC_AUTHORITY_INVALID")
        if not isinstance(attempt, dict) or attempt.get("status") != "completed" or attempt.get("role") != "formal":
            raise EvaluationError("DETERMINISTIC_ATTEMPT_INVALID")
        source = attempt.get("bindings", {}).get("source_identity", {}) if isinstance(attempt.get("bindings"), dict) else {}
        if not isinstance(source, dict) or source.get("authority_sha256") != sha256_bytes(files[_DETERMINISTIC_PATHS[0]][1]):
            raise EvaluationError("DETERMINISTIC_AUTHORITY_INVALID")
        artifacts = attempt.get("artifacts")
        if not isinstance(artifacts, dict):
            raise EvaluationError("DETERMINISTIC_ATTEMPT_INVALID")
        for path in _DETERMINISTIC_PATHS[2:]:
            descriptor = artifacts.get(Path(path).name)
            raw = files[path][1]
            if not isinstance(descriptor, dict) or descriptor.get("sha256") != sha256_bytes(raw) or descriptor.get("byte_length") != len(raw):
                raise EvaluationError("DETERMINISTIC_ARTIFACT_BINDING_INVALID")
        return _admission("deterministic_measurement", _DETERMINISTIC_PATHS, files, ())
    except (EvaluationError, FilesystemPolicyError, OSError, TypeError, ValueError) as error:
        return AuthorityAdmission("deterministic_measurement", tuple(sorted(_DETERMINISTIC_PATHS)), "", "invalid_withheld", (_diagnostic(str(error), "deterministic_measurement"),))


def _admit_red(root: Path) -> AuthorityAdmission:
    paths = ("phase4/branch-authority-v6.json", "receipts/red-execution-v2.json")
    try:
        files = read_authoritative_files(root, list(paths))
        authority = validate_red_authority_v2(root)
        receipt = validate_red_evidence_v2(root=root)
        if receipt.get("authority_sha256") != authority.get("authority_sha256"):
            raise EvaluationError("RED_AUTHORITY_BINDING_INVALID")
        return _admission("red_execution_evidence", paths, files, ())
    except (EvaluationError, RedExecutionV2Error, FilesystemPolicyError, OSError, TypeError, ValueError) as error:
        return AuthorityAdmission("red_execution_evidence", tuple(sorted(paths)), "", "invalid_withheld", (_diagnostic(str(error), "red_execution_evidence"),))


def admit_red_inputs(root: Path) -> tuple[AuthorityAdmission, AuthorityAdmission]:
    """Independently admit the deterministic and Red no-call authority tracks."""
    return _admit_deterministic(root), _admit_red(root)


def build_population_manifest(
    population_id: str, partition: str, eligible_ids: Sequence[str], *,
    included_ids: Sequence[str] | None = None, exclusion_reasons: Mapping[str, str] | None = None,
) -> PopulationManifest:
    raw_eligible = tuple(eligible_ids)
    eligible = tuple(sorted(raw_eligible))
    raw_included = tuple(eligible if included_ids is None else included_ids)
    included = tuple(sorted(raw_included))
    reasons = dict(exclusion_reasons or {})
    excluded = tuple(sorted(reasons))
    if (
        not population_id or not partition or len(eligible) != len(set(eligible))
        or len(included) != len(set(included)) or not set(included) <= set(eligible)
        or not set(excluded) <= set(eligible) or set(included) & set(excluded)
        or not all(isinstance(reason, str) and reason for reason in reasons.values())
    ):
        raise EvaluationError("POPULATION_MANIFEST_INVALID")
    basis = {
        "eligible_ids": list(eligible), "excluded_ids": list(excluded),
        "exclusion_reasons": dict(sorted(reasons.items())), "included_ids": list(included),
        "partition": partition, "population_id": population_id,
    }
    return PopulationManifest(population_id, partition, eligible, included, excluded, reasons, sha256_bytes(canonical_json_bytes(basis)), len(eligible))


def _metric(
    metric_id: str, source: Mapping[str, object], population: PopulationManifest, bindings: Mapping[str, str],
) -> MetricResult:
    if not isinstance(source.get("numerator"), int) or isinstance(source.get("numerator"), bool) or source.get("denominator") != population.denominator:
        raise EvaluationError("METRIC_DENOMINATOR_MISMATCH")
    numerator = int(source["numerator"])
    return MetricResult(metric_id, "measured", bindings, population.population_id, population.set_sha256, numerator, population.denominator, numerator / population.denominator)


def _not_applicable(metric_id: str, bindings: Mapping[str, str]) -> MetricResult:
    return MetricResult(metric_id, "not_applicable_red", bindings, reason="not_applicable_red: no Green/Yellow observation authority on the frozen Red branch")


def _deterministic_payload(root: Path) -> tuple[list[dict[str, object]], dict[str, object], list[dict[str, object]]]:
    files = read_authoritative_files(root, list(_DETERMINISTIC_PATHS))
    attempt = _canonical_object(files[_DETERMINISTIC_PATHS[1]][1], "DETERMINISTIC_CANONICAL_INVALID")
    cases = _canonical_object(files[_DETERMINISTIC_PATHS[2]][1], "DETERMINISTIC_CANONICAL_INVALID")
    metrics = _canonical_object(files[_DETERMINISTIC_PATHS[3]][1], "DETERMINISTIC_CANONICAL_INVALID")
    if not isinstance(attempt, dict) or not isinstance(cases, list) or not isinstance(metrics, dict):
        raise EvaluationError("DETERMINISTIC_PAYLOAD_INVALID")
    decoded = base64.b64decode(attempt.get("raw_predictions_base64", ""), validate=True)
    if decoded is None or sha256_bytes(decoded) != attempt.get("raw_predictions_sha256"):
        raise EvaluationError("DETERMINISTIC_PREDICTIONS_INVALID")
    predictions = json.loads(decoded.decode("utf-8")).get("predictions")
    if not isinstance(predictions, list):
        raise EvaluationError("DETERMINISTIC_PREDICTIONS_INVALID")
    return [dict(item) for item in cases if isinstance(item, dict)], metrics, [dict(item) for item in predictions if isinstance(item, dict)]


def _metamorphic_directions(root: Path, bindings: Mapping[str, str]) -> tuple[Mapping[str, object], ...]:
    try:
        files = read_authoritative_files(root, list(_METAMORPHIC_PATHS))
        authority = _canonical_object(files[_METAMORPHIC_PATHS[0]][1], "METAMORPHIC_REGISTRY_INVALID")
        registry = _canonical_object(files[_METAMORPHIC_PATHS[1]][1], "METAMORPHIC_REGISTRY_INVALID")
        if not isinstance(authority, dict) or not isinstance(registry, dict):
            raise EvaluationError("METAMORPHIC_REGISTRY_INVALID")
        expected = registry.get("bindings")
        expected_hash = authority.get("bindings", {}).get("metamorphic_registry_sha256") if isinstance(authority.get("bindings"), dict) else None
        if not isinstance(expected, dict) or expected_hash != registry.get("registry_sha256"):
            raise EvaluationError("METAMORPHIC_BINDING_INVALID")
        validate_metamorphic_registry_v1(registry, expected_bindings=expected, accepted_root=None, frozen_metamorphic_candidate_ids=set(), dataset_member_ids=set())
        rows = []
        for direction in registry["directions"]:
            rows.append({
                "authority_bindings": dict(sorted({**bindings, "metamorphic_registry_sha256": str(registry["registry_sha256"])}.items())),
                "availability": direction["availability"], "count_eligible": direction["count_eligible"],
                "direction_id": direction["direction_id"], "rationale": direction["rationale"],
                "registry_sha256": registry["registry_sha256"],
                "registry_version": registry["registry_version"], "state": "not_applicable_red",
            })
        return tuple(rows)
    except (EvaluationError, RelevanceValidationError, FilesystemPolicyError, OSError, TypeError, ValueError) as error:
        diagnostic = _diagnostic(str(error), "metamorphic_registry")
        return tuple({"authority_bindings": dict(sorted(bindings.items())), "blocking_diagnostics": [diagnostic.as_dict()], "direction_id": direction, "state": "invalid_withheld"} for direction in REQUIRED_METAMORPHIC_DIRECTIONS)


def build_red_evaluation(root: Path) -> EvaluationBundle:
    """Build a decision-free Red evaluation without synthesizing experiment rows."""
    deterministic, red = admit_red_inputs(root)
    bindings = {
        "deterministic_measurement": deterministic.source_sha256,
        "red_execution_evidence": red.source_sha256,
    }
    base_diagnostics = ordered_diagnostics(list(deterministic.diagnostics) + list(red.diagnostics))
    if deterministic.status != "admitted" or red.status != "admitted":
        blocked = tuple(_diagnostic("EVALUATION_AUTHORITY_WITHHELD", "evaluation") for _ in [0])
        metrics = tuple(MetricResult(metric_id, "invalid_withheld", bindings, blocking_diagnostics=blocked) for metric_id in METRIC_IDS)
        return EvaluationBundle("partition-evaluation-red-v1", "red", 0, 0, False, deterministic, red, metrics, (), (), metrics, ordered_diagnostics(list(base_diagnostics) + list(blocked)))
    try:
        cases, metric_source, predictions = _deterministic_payload(root)
        identities = [(str(item.get("fixture_id")), str(item.get("finding_id"))) for item in cases]
        if identities != sorted(identities) or len(identities) != len(set(identities)):
            raise EvaluationError("ATOMIC_IDENTITY_DUPLICATE")
        rows = tuple(
            AtomicResultRow(
                "deterministic_measurement", "formal", fixture_id,
                DimensionBinding(False, None, "not_applicable_red"),
                DimensionBinding(False, None, "not_applicable_red"), finding_id, item,
            )
            for (fixture_id, finding_id), item in zip(identities, cases, strict=True)
        )
        population_specs = {
            "surfacing": [item["finding_id"] for item in cases if item.get("category") != "negative"],
            "disposition": [item["finding_id"] for item in cases if item.get("category") != "negative"],
            "identity_exact": [item["finding_id"] for item in cases if item.get("category") == "positive" and item.get("disposition_correct") is True],
            "identity_incorrect": [item["finding_id"] for item in cases if item.get("category") == "positive" and item.get("disposition_correct") is True],
            "identity_missing": [item["finding_id"] for item in cases if item.get("category") == "positive" and item.get("disposition_correct") is True],
            "classify_out": [item["finding_id"] for item in cases if item.get("actual_status") == "classify_out"],
            "negative_controls": [item["finding_id"] for item in cases if item.get("category") == "negative"],
            "evidence_integrity": [
                f"{item.get('fixture_id')}:{item.get('finding_id')}:span-{number}"
                for item in predictions for number, _span in enumerate(item.get("adjudication", {}).get("evidence_spans", []), start=1)
            ],
        }
        populations = tuple(build_population_manifest(f"deterministic.{metric_id}", "formal", sorted(set(ids))) for metric_id, ids in sorted(population_specs.items()))
        by_id = {item.population_id.removeprefix("deterministic."): item for item in populations}
        measured = {
            "surfacing": _metric("surfacing", metric_source["surfacing"], by_id["surfacing"], bindings),
            "disposition": _metric("disposition", metric_source["disposition"], by_id["disposition"], bindings),
            "identity_exact": _metric("identity_exact", metric_source["identity"], by_id["identity_exact"], bindings),
            "classify_out": MetricResult("classify_out", "measured", bindings, by_id["classify_out"].population_id, by_id["classify_out"].set_sha256, by_id["classify_out"].denominator, by_id["classify_out"].denominator, 1.0),
            "negative_controls": _metric("negative_controls", metric_source["negative_controls"], by_id["negative_controls"], bindings),
            "evidence_integrity": _metric("evidence_integrity", metric_source["evidence_integrity"], by_id["evidence_integrity"], bindings),
            "identity_incorrect": MetricResult("identity_incorrect", "measured", bindings, by_id["identity_incorrect"].population_id, by_id["identity_incorrect"].set_sha256, 0, by_id["identity_incorrect"].denominator, 0.0),
            "identity_missing": MetricResult("identity_missing", "measured", bindings, by_id["identity_missing"].population_id, by_id["identity_missing"].set_sha256, 0, by_id["identity_missing"].denominator, 0.0),
        }
        metrics = tuple(measured.get(metric_id, _not_applicable(metric_id, bindings)) for metric_id in METRIC_IDS)
        directions = _metamorphic_directions(root, bindings)
        if any(item.get("state") == "invalid_withheld" for item in directions):
            metrics = tuple(
                MetricResult(metric.metric_id, "invalid_withheld", metric.authority_bindings, blocking_diagnostics=(_diagnostic("METAMORPHIC_DOMAIN_WITHHELD", "metamorphic_registry"),))
                if metric.metric_id.startswith("metamorphic_") else metric for metric in metrics
            )
        applicability = tuple(metrics)
        return EvaluationBundle("partition-evaluation-red-v1", "red", 0, 0, True, deterministic, red, applicability, populations, rows, metrics, base_diagnostics, directions)
    except (EvaluationError, FilesystemPolicyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        diagnostics = ordered_diagnostics(list(base_diagnostics) + [_diagnostic(str(error), "deterministic_measurement")])
        metrics = tuple(MetricResult(metric_id, "invalid_withheld", bindings, blocking_diagnostics=diagnostics) for metric_id in METRIC_IDS)
        return EvaluationBundle("partition-evaluation-red-v1", "red", 0, 0, True, deterministic, red, metrics, (), (), metrics, diagnostics)

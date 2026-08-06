# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Composition-only Red evaluation with independent authority namespaces."""

from __future__ import annotations

import base64
import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from types import MappingProxyType

from specchoice_data.relevance import (
    REQUIRED_METAMORPHIC_DIRECTIONS,
    RelevanceValidationError,
    validate_metamorphic_registry_v1,
    validate_pair_relevance_registry_v1,
)
from specchoice_evidence.canonical import (
    canonical_json_bytes,
    require_sha256,
    sha256_bytes,
)
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
_ARTIFACT_ROLES = (
    "gold", "prediction", "prompt", "raw_response", "parsed_response",
    "evidence_spans", "treatment", "repeat",
)
PAIRWISE_INTERVENTION_CONTRACTS = MappingProxyType({
    "b_minus_a": MappingProxyType({
        "intervention": "delegation_frame",
        "left_treatment": "B",
        "right_treatment": "A",
        "treatment_values": MappingProxyType({
            "A": "2312907e7355ecdd168ef68bbc855bf3a988b76542e47db4d3d06da302923d38",
            "B": "49ea5296eb68002cf6bbf0e3b616ce7eb6e6dc063d9f84948d09511cec01faed",
        }),
    }),
    "c_minus_b": MappingProxyType({
        "intervention": "pair_selection",
        "left_treatment": "C",
        "right_treatment": "B",
        "treatment_values": MappingProxyType({
            "B": "b575ccc3f5f3ddb9007962c60749ddf97bbb665c8b7d254c11d16ad1d81bdb96",
            "C": "c17d314784872956ef41062dd17c32cf721fd892794727801b4ab4157b1aad11",
        }),
    }),
})

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
_FROZEN_REGISTRY_PATHS = (
    "data/preregistration/family-registry-v1.json",
    "data/preregistration/metamorphic-registry-v1.json",
    "data/preregistration/pair-relevance-registry-v1.json",
    "data/preregistration/split-manifest-v1.json",
    "phase3/data-authority-v1.json",
)
CONSTRUCTION_SOURCE_CONTRACT = (
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-00-SUMMARY.md", "completed"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-01-SUMMARY.md", "completed"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-02-CANCELLATION.md", "rejected"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-02-REJECTED.md", "rejected"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-03-SUPERSEDED.md", "superseded"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-04-SUMMARY.md", "completed"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-05-SUMMARY.md", "completed"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-06-CANCELLATION.md", "cancelled"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-06-FAILED-CLOSED.md", "failed_closed"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-07-CANCELLATION.md", "cancelled"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-07-FAILED-CLOSED.md", "failed_closed"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-08-SUMMARY.md", "completed"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-09-SUMMARY.md", "completed"),
    (".planning/phases/05-authorized-execution-and-immutable-evidence/05-VERIFICATION.md", "completed"),
    ("experiments/specchoice-v1.3.2/runs/red-execution-v2/attempt-chain.json", "completed"),
    ("experiments/specchoice-v1.3.2/receipts/red-execution-v2.json", "completed"),
    ("experiments/specchoice-v1.3.2/runs/native-port-darwin-arm64-20260805/original-whole-binary-sha-mismatch.json", "failed_closed"),
    ("experiments/specchoice-v1.3.2/runs/native-port-darwin-arm64-projection-v2-20260805/contract-validation.json", "failed_closed"),
    ("experiments/specchoice-v1.3.2/receipts/native-port-projection-v2-to-v3-custody-successor-v1.json", "successor"),
)


class EvaluationError(ValueError):
    """Stable failure for a withheld Phase 6 evaluation domain."""


@dataclass(frozen=True)
class ArtifactBinding:
    """One applicable frozen artifact or a reasoned inapplicable branch."""

    applicable: bool
    relative_path: str | None
    sha256: str | None
    reason: str | None

    def __post_init__(self) -> None:
        if self.applicable:
            if (
                not isinstance(self.relative_path, str) or not self.relative_path
                or not isinstance(self.sha256, str) or len(self.sha256) != 64
                or any(character not in "0123456789abcdef" for character in self.sha256)
                or self.reason is not None
            ):
                raise EvaluationError("ARTIFACT_BINDING_INVALID")
        elif self.relative_path is not None or self.sha256 is not None or not self.reason:
            raise EvaluationError("ARTIFACT_BINDING_INVALID")

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


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
class ClosedJoinManifest:
    """The exact, all-or-nothing artifact join for one atomic case."""

    join_id: str
    authority_domain: str
    partition: str
    case_id: str
    gold: ArtifactBinding
    prediction: ArtifactBinding
    prompt: ArtifactBinding
    raw_response: ArtifactBinding
    parsed_response: ArtifactBinding
    evidence_spans: ArtifactBinding
    treatment: ArtifactBinding
    repeat: ArtifactBinding
    row_ids: tuple[tuple[str, str, str, str, str, str], ...]
    status: str
    diagnostics: tuple[Diagnostic, ...]
    join_sha256: str

    def as_dict(self) -> dict[str, object]:
        return {
            "authority_domain": self.authority_domain,
            "case_id": self.case_id,
            "diagnostics": [item.as_dict() for item in self.diagnostics],
            "evidence_spans": self.evidence_spans.as_dict(),
            "gold": self.gold.as_dict(),
            "join_id": self.join_id,
            "join_sha256": self.join_sha256,
            "parsed_response": self.parsed_response.as_dict(),
            "partition": self.partition,
            "prediction": self.prediction.as_dict(),
            "prompt": self.prompt.as_dict(),
            "raw_response": self.raw_response.as_dict(),
            "repeat": self.repeat.as_dict(),
            "row_ids": [list(item) for item in self.row_ids],
            "status": self.status,
            "treatment": self.treatment.as_dict(),
        }


@dataclass(frozen=True)
class VerifiedJoinReference:
    """One atomic row with the exact closed join admitted by the policy."""

    row: AtomicResultRow
    manifest: ClosedJoinManifest
    expected_join_sha256: str


@dataclass(frozen=True)
class PairwiseComparison:
    """A treatment-specific, independently denominated complete-pair result."""

    comparison_id: str
    left_treatment: str
    right_treatment: str
    intervention: str
    population_id: str
    population_sha256: str
    paired_row_ids: tuple[tuple[tuple[str, str, str, str, str, str], tuple[str, str, str, str, str, str]], ...]
    result: MetricResult


@dataclass(frozen=True)
class RepeatObservation:
    """One closed repeat observation, separate from its disagreement comparison."""

    observation_id: str
    authority_domain: str
    partition: str
    case_id: str
    treatment: str
    repeat_id: str
    closed_join_sha256: str
    outcome_id: str

    def __post_init__(self) -> None:
        values = (
            self.observation_id, self.authority_domain, self.partition, self.case_id,
            self.treatment, self.repeat_id, self.outcome_id,
        )
        if (
            any(not isinstance(value, str) or not value for value in values)
            or len(self.closed_join_sha256) != 64
            or any(character not in "0123456789abcdef" for character in self.closed_join_sha256)
        ):
            raise EvaluationError("REPEAT_OBSERVATION_INVALID")


@dataclass(frozen=True)
class RepeatComparison:
    """A comparison of two exact repeat observations, never a result row."""

    comparison_id: str
    population_id: str
    left_repeat_id: str
    right_repeat_id: str
    left_observation_id: str
    right_observation_id: str
    agreement: bool
    result: MetricResult

    def __post_init__(self) -> None:
        values = (
            self.comparison_id, self.population_id, self.left_repeat_id,
            self.right_repeat_id, self.left_observation_id, self.right_observation_id,
        )
        if (
            any(not isinstance(value, str) or not value for value in values)
            or self.left_repeat_id == self.right_repeat_id
            or self.left_observation_id == self.right_observation_id
            or not isinstance(self.agreement, bool)
        ):
            raise EvaluationError("REPEAT_COMPARISON_INVALID")


@dataclass(frozen=True)
class ConstructionAttempt:
    """Immutable Phase 5 lifecycle evidence, deliberately outside experiment results."""

    attempt_id: str
    source_path: str
    source_sha256: str
    status: str
    predecessor_id: str | None
    successor_id: str | None
    custody_state: str
    evidence_paths: tuple[str, ...]
    evidence_sha256: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            not self.attempt_id
            or not self.source_path
            or len(self.source_sha256) != 64
            or self.status not in {"rejected", "cancelled", "failed_closed", "superseded", "completed", "successor"}
            or self.custody_state != "immutable"
            or self.evidence_paths != (self.source_path,)
            or self.evidence_sha256 != (self.source_sha256,)
            or any(len(value) != 64 for value in self.evidence_sha256)
        ):
            raise EvaluationError("CONSTRUCTION_ATTEMPT_INVALID")


_FAILURE_DOMAINS = frozenset({"authority", "join", "construction", "evaluation", "experimental_outcome"})
_FAILURE_SEVERITIES = frozenset({"blocking", "advisory"})
_FAILURE_EFFECTS = frozenset({"withhold_domain", "exclude_case", "report_only"})


@dataclass(frozen=True)
class WarningRecord:
    """An advisory-only frame pattern record that cannot become score authority."""

    code: str
    domain: str
    severity: str
    effect: str
    case_id: str
    outcome_id: str
    pattern_version: str
    trigger_evidence_sha256: str

    def __post_init__(self) -> None:
        if (
            self.code != "FRAME_COMBINATION_REQUIRES_REVIEW"
            or self.domain not in _FAILURE_DOMAINS or self.severity != "advisory"
            or self.effect != "report_only" or not self.case_id or not self.outcome_id
            or not self.pattern_version or len(self.trigger_evidence_sha256) != 64
        ):
            raise EvaluationError("WARNING_RECORD_INVALID")

    def sort_key(self) -> tuple[str, str, str, str, str]:
        return (self.code, self.case_id, self.outcome_id, self.pattern_version, self.trigger_evidence_sha256)


@dataclass(frozen=True)
class FailureRecord:
    """A D-09 failure that is categorically distinct from an outcome."""

    code: str
    domain: str
    severity: str
    effect: str
    subject_id: str
    evidence_sha256: str
    depends_on: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            not self.code or self.domain not in _FAILURE_DOMAINS
            or self.severity not in _FAILURE_SEVERITIES or self.effect not in _FAILURE_EFFECTS
            or not self.subject_id or len(self.evidence_sha256) != 64
            or not self.depends_on or tuple(sorted(self.depends_on)) != self.depends_on
            or len(set(self.depends_on)) != len(self.depends_on)
        ):
            raise EvaluationError("FAILURE_RECORD_INVALID")

    def sort_key(self) -> tuple[str, str, str, str, str]:
        return (self.domain, self.code, self.subject_id, self.effect, self.evidence_sha256)


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
    pairwise_comparisons: tuple[PairwiseComparison, ...] = ()

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
            "pairwise_comparisons": [
                {
                    "comparison_id": item.comparison_id,
                    "intervention": item.intervention,
                    "left_treatment": item.left_treatment,
                    "paired_row_ids": [[list(left), list(right)] for left, right in item.paired_row_ids],
                    "population_id": item.population_id,
                    "population_sha256": item.population_sha256,
                    "result": item.result.as_dict(),
                    "right_treatment": item.right_treatment,
                }
                for item in self.pairwise_comparisons
            ],
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


def close_join(
    authority_domain: str,
    partition: str,
    case_id: str,
    bindings: Mapping[str, ArtifactBinding],
    rows: Sequence[AtomicResultRow],
    *,
    expected_bindings: Mapping[str, ArtifactBinding],
) -> ClosedJoinManifest:
    """Close one case only when all D-08 identities are exact and complete."""
    binding_map = dict(bindings)
    expected_binding_map = dict(expected_bindings)
    diagnostics: list[Diagnostic] = []
    if (
        set(binding_map) != set(_ARTIFACT_ROLES)
        or not all(isinstance(binding, ArtifactBinding) for binding in binding_map.values())
    ):
        diagnostics.append(_diagnostic("CLOSED_JOIN_ARTIFACT_SET_INVALID", "join.artifacts"))
    elif not all(binding_map[role].applicable for role in _ARTIFACT_ROLES):
        diagnostics.append(_diagnostic("CLOSED_JOIN_ARTIFACT_INAPPLICABLE", "join.artifacts"))
    if (
        set(expected_binding_map) != set(_ARTIFACT_ROLES)
        or not all(isinstance(binding, ArtifactBinding) for binding in expected_binding_map.values())
    ):
        diagnostics.append(_diagnostic("CLOSED_JOIN_EXPECTED_BINDINGS_INVALID", "join.expected_bindings"))
    elif set(binding_map) == set(_ARTIFACT_ROLES) and any(
        binding_map[role].as_dict() != expected_binding_map[role].as_dict()
        for role in _ARTIFACT_ROLES
    ):
        diagnostics.append(_diagnostic("CLOSED_JOIN_BINDING_SUBSTITUTED", "join.expected_bindings"))

    row_ids = tuple(sorted(row.identity() for row in rows))
    if len(row_ids) != len(set(row_ids)):
        diagnostics.append(_diagnostic("CLOSED_JOIN_DUPLICATE_ROW", "join.rows"))
    if any(
        row.authority_domain != authority_domain
        or row.partition != partition
        or row.case_id != case_id
        for row in rows
    ):
        diagnostics.append(_diagnostic("CLOSED_JOIN_CROSS_PARTITION", "join.rows"))
    if not rows:
        diagnostics.append(_diagnostic("CLOSED_JOIN_ROW_MISSING", "join.rows"))

    safe_bindings = {
        role: binding_map.get(role, ArtifactBinding(False, None, None, "missing_binding"))
        for role in _ARTIFACT_ROLES
    }
    status = "closed" if not diagnostics else "invalid_withheld"
    basis = {
        "authority_domain": authority_domain,
        "bindings": {role: safe_bindings[role].as_dict() for role in _ARTIFACT_ROLES},
        "case_id": case_id,
        "partition": partition,
        "row_ids": [list(row_id) for row_id in row_ids],
        "status": status,
    }
    return ClosedJoinManifest(
        f"join.{authority_domain}.{partition}.{case_id}", authority_domain, partition, case_id,
        safe_bindings["gold"], safe_bindings["prediction"], safe_bindings["prompt"],
        safe_bindings["raw_response"], safe_bindings["parsed_response"],
        safe_bindings["evidence_spans"], safe_bindings["treatment"], safe_bindings["repeat"],
        row_ids, status, ordered_diagnostics(diagnostics), sha256_bytes(canonical_json_bytes(basis)),
    )


def _valid_verified_join_reference(reference: object) -> bool:
    if not isinstance(reference, VerifiedJoinReference):
        return False
    row, manifest = reference.row, reference.manifest
    if (
        manifest.status != "closed"
        or manifest.diagnostics
        or manifest.join_id != f"join.{row.authority_domain}.{row.partition}.{row.case_id}"
        or manifest.authority_domain != row.authority_domain
        or manifest.partition != row.partition
        or manifest.case_id != row.case_id
        or manifest.row_ids != (row.identity(),)
        or manifest.join_sha256 != reference.expected_join_sha256
    ):
        return False
    try:
        require_sha256(reference.expected_join_sha256)
    except ValueError:
        return False
    return True


def build_pairwise_comparison(
    references: Sequence[VerifiedJoinReference],
    comparison_id: str,
    control_projections: Mapping[tuple[str, str, str, str, str, str], Mapping[str, object]],
    *,
    authority_bindings: Mapping[str, str] | None = None,
) -> PairwiseComparison:
    """Build one exact-control B-A or C-B comparison without denominator reuse."""
    if comparison_id not in PAIRWISE_INTERVENTION_CONTRACTS:
        raise EvaluationError("PAIRWISE_COMPARISON_INVALID")
    contract = PAIRWISE_INTERVENTION_CONTRACTS[comparison_id]
    left_treatment = str(contract["left_treatment"])
    right_treatment = str(contract["right_treatment"])
    intervention = str(contract["intervention"])
    treatment_values = contract["treatment_values"]
    if not isinstance(treatment_values, Mapping):
        raise EvaluationError("PAIRWISE_COMPARISON_INVALID")
    bindings = dict(authority_bindings or {})
    population_id = f"pairwise.{comparison_id}"
    if not references:
        population_sha256 = sha256_bytes(canonical_json_bytes({"comparison_id": comparison_id, "state": "not_applicable_red"}))
        return PairwiseComparison(
            comparison_id, left_treatment, right_treatment, intervention, population_id,
            population_sha256, (), _not_applicable(comparison_id, bindings),
        )

    groups: dict[tuple[str, str, str, str], dict[str, AtomicResultRow]] = {}
    invalid_join = False
    invalid_intervention = False
    for reference in references:
        if not _valid_verified_join_reference(reference):
            invalid_join = True
            continue
        row = reference.row
        if not row.treatment.applicable or not row.repeat_id.applicable:
            invalid_join = True
            continue
        key = (row.authority_domain, row.partition, row.case_id, row.repeat_id.value or "")
        treatment = row.treatment.value or ""
        if treatment not in {left_treatment, right_treatment} or treatment in groups.setdefault(key, {}):
            invalid_join = True
            continue
        groups[key][treatment] = row
    paired = []
    for key in sorted(groups):
        pair = groups[key]
        if set(pair) != {left_treatment, right_treatment}:
            invalid_join = True
            continue
        left, right = pair[left_treatment], pair[right_treatment]
        left_controls = control_projections.get(left.identity())
        right_controls = control_projections.get(right.identity())
        if not isinstance(left_controls, Mapping) or not isinstance(right_controls, Mapping):
            invalid_intervention = True
            continue
        if (
            set(left_controls) != set(right_controls)
            or intervention not in left_controls
            or left_controls[intervention] != treatment_values.get(left_treatment)
            or right_controls[intervention] != treatment_values.get(right_treatment)
            or left_controls[intervention] == right_controls[intervention]
            or any(left_controls[name] != right_controls[name] for name in left_controls if name != intervention)
        ):
            invalid_intervention = True
            continue
        paired.append((left, right))

    paired_ids = tuple((left.identity(), right.identity()) for left, right in paired)
    basis = {
        "comparison_id": comparison_id,
        "intervention": intervention,
        "paired_row_ids": [[list(left), list(right)] for left, right in paired_ids],
    }
    population_sha256 = sha256_bytes(canonical_json_bytes(basis))
    if invalid_join:
        paired_ids = ()
        diagnostic = _diagnostic("PAIRWISE_JOIN_REFERENCE_INVALID", comparison_id)
        result = MetricResult(comparison_id, "invalid_withheld", bindings, blocking_diagnostics=(diagnostic,))
    elif invalid_intervention or not paired:
        paired_ids = ()
        diagnostic = _diagnostic("PAIRWISE_INTERVENTION_INVALID", comparison_id)
        result = MetricResult(comparison_id, "invalid_withheld", bindings, blocking_diagnostics=(diagnostic,))
    else:
        numerator = sum(
            int(right.outcome.get("correct") is True and left.outcome.get("correct") is not True)
            for left, right in paired
        )
        result = MetricResult(
            comparison_id, "measured", bindings, population_id, population_sha256,
            numerator, len(paired), numerator / len(paired),
        )
    return PairwiseComparison(
        comparison_id, left_treatment, right_treatment, intervention, population_id,
        population_sha256, paired_ids, result,
    )


DEPENDENCY_GRAPH: Mapping[str, tuple[str, ...]] = {
    "deterministic_measurement": METRIC_IDS,
    "frozen_bindings": (
        "b_minus_a", "c_minus_b", "frame_authority", "frame_choice_object",
        "frame_choice_space_origin",
    ),
    "join": ("b_minus_a", "c_minus_b"),
    "red_execution_evidence": ("b_minus_a", "c_minus_b", "repeat_disagreement"),
}


def build_warning_ledger(items: Sequence[WarningRecord]) -> tuple[WarningRecord, ...]:
    """Return the report-only warning ledger in its one canonical order."""
    ordered = tuple(sorted(items, key=WarningRecord.sort_key))
    identities = [item.sort_key() for item in ordered]
    if len(identities) != len(set(identities)):
        raise EvaluationError("WARNING_LEDGER_DUPLICATE")
    return ordered


def build_failure_ledger(items: Sequence[FailureRecord]) -> tuple[FailureRecord, ...]:
    """Return stable D-09 failure evidence without reclassifying it as an outcome."""
    ordered = tuple(sorted(items, key=FailureRecord.sort_key))
    identities = [item.sort_key() for item in ordered]
    if len(identities) != len(set(identities)):
        raise EvaluationError("FAILURE_LEDGER_DUPLICATE")
    return ordered


def build_frame_axis_results(bindings: Mapping[str, str]) -> tuple[MetricResult, ...]:
    """Expose all frozen frame axes independently, even when Red has no rows."""
    return tuple(
        _not_applicable(metric_id, bindings)
        for metric_id in (
            "frame_authority", "frame_choice_object", "frame_choice_space_origin",
        )
    )


def validate_frozen_bindings(
    expected: Mapping[str, str], observed: Mapping[str, str], *, depends_on: tuple[str, ...],
) -> FailureRecord | None:
    """Fail closed on any exact frozen family, label, prompt, or threshold drift."""
    if dict(expected) == dict(observed):
        return None
    evidence_sha256 = sha256_bytes(canonical_json_bytes({"expected": dict(sorted(expected.items())), "observed": dict(sorted(observed.items()))}))
    return FailureRecord(
        "FROZEN_BINDING_DRIFT", "authority", "blocking", "withhold_domain",
        "frozen_bindings", evidence_sha256, tuple(sorted(depends_on)),
    )


def propagate_blockers(
    failures: Sequence[FailureRecord], metrics: Sequence[MetricResult],
    *, dependency_graph: Mapping[str, tuple[str, ...]] = DEPENDENCY_GRAPH,
) -> tuple[MetricResult, ...]:
    """Withhold only the declared dependency closure; independent metrics survive."""
    blocking = [
        item for item in build_failure_ledger(failures)
        if item.severity == "blocking" and item.effect == "withhold_domain"
    ]
    targets: set[str] = set()
    pending = [node for item in blocking for node in item.depends_on]
    while pending:
        node = pending.pop()
        if node in targets:
            continue
        targets.add(node)
        pending.extend(dependency_graph.get(node, ()))
    propagated: list[MetricResult] = []
    for metric in metrics:
        if metric.metric_id not in targets:
            propagated.append(metric)
            continue
        diagnostics = tuple(
            _diagnostic(failure.code, failure.subject_id)
            for failure in blocking if any(node in targets for node in failure.depends_on)
        )
        propagated.append(MetricResult(
            metric.metric_id, "invalid_withheld", metric.authority_bindings,
            blocking_diagnostics=ordered_diagnostics(list(diagnostics)),
        ))
    return tuple(propagated)


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


def _self_hash_valid(value: Mapping[str, object], field: str) -> bool:
    observed = value.get(field)
    if not isinstance(observed, str) or len(observed) != 64:
        return False
    basis = dict(value)
    basis.pop(field, None)
    return observed == sha256_bytes(canonical_json_bytes(basis))


def _frozen_registry_values(root: Path) -> tuple[dict[str, Mapping[str, object]], dict[str, str]]:
    """Load the exact frozen registry set before admitting a dependent result."""
    files = read_authoritative_files(root, list(_FROZEN_REGISTRY_PATHS))
    values = {
        path: _canonical_object(raw, "FROZEN_REGISTRY_CANONICAL_INVALID")
        for path, (_evidence, raw) in files.items()
    }
    if not all(isinstance(value, Mapping) for value in values.values()):
        raise EvaluationError("FROZEN_REGISTRY_INVALID")
    family = values[_FROZEN_REGISTRY_PATHS[0]]
    metamorphic = values[_FROZEN_REGISTRY_PATHS[1]]
    relevance = values[_FROZEN_REGISTRY_PATHS[2]]
    split = values[_FROZEN_REGISTRY_PATHS[3]]
    authority = values[_FROZEN_REGISTRY_PATHS[4]]
    assert all(isinstance(value, Mapping) for value in (family, metamorphic, relevance, split, authority))
    if (
        not _self_hash_valid(family, "registry_sha256")
        or not _self_hash_valid(metamorphic, "registry_sha256")
        or not _self_hash_valid(relevance, "registry_sha256")
        or not _self_hash_valid(split, "manifest_sha256")
    ):
        raise EvaluationError("FROZEN_REGISTRY_HASH_INVALID")
    family_sha = str(family["registry_sha256"])
    relevance_sha = str(relevance["registry_sha256"])
    split_sha = str(split["manifest_sha256"])
    metamorphic_sha = str(metamorphic["registry_sha256"])
    relevance_bindings = relevance.get("bindings")
    metamorphic_bindings = metamorphic.get("bindings")
    authority_bindings = authority.get("bindings")
    if (
        not isinstance(relevance_bindings, Mapping)
        or not isinstance(metamorphic_bindings, Mapping)
        or not isinstance(authority_bindings, Mapping)
        or relevance_bindings.get("family_registry_sha256") != family_sha
        or relevance_bindings.get("split_manifest_sha256") != split_sha
        or metamorphic_bindings.get("family_registry_sha256") != family_sha
        or metamorphic_bindings.get("relevance_registry_sha256") != relevance_sha
        or metamorphic_bindings.get("split_manifest_sha256") != split_sha
        or authority_bindings.get("metamorphic_registry_sha256") != metamorphic_sha
    ):
        raise EvaluationError("FROZEN_REGISTRY_BINDING_INVALID")
    validate_pair_relevance_registry_v1(
        relevance,
        split_manifest=split,
        approved_pairs={},
        expected_bindings=relevance_bindings,
        case_targets={},
    )
    validate_metamorphic_registry_v1(
        metamorphic,
        expected_bindings=metamorphic_bindings,
        accepted_root=None,
        frozen_metamorphic_candidate_ids=set(),
        dataset_member_ids=set(),
    )
    return (
        {
            "family": family,
            "metamorphic": metamorphic,
            "relevance": relevance,
            "split": split,
            "authority": authority,
        },
        {
            "family_registry_sha256": family_sha,
            "metamorphic_registry_sha256": metamorphic_sha,
            "relevance_registry_sha256": relevance_sha,
            "split_manifest_sha256": split_sha,
        },
    )


def build_metamorphic_results(root: Path, bindings: Mapping[str, str]) -> tuple[Mapping[str, object], ...]:
    """Expose all four frozen direction records without inventing Red observations."""
    try:
        values, registry_bindings = _frozen_registry_values(root)
        registry = values["metamorphic"]
        rows = []
        for direction in sorted(registry["directions"], key=lambda item: str(item["direction_id"])):
            rows.append({
                "authority_bindings": dict(sorted({**bindings, **registry_bindings}.items())),
                "availability": direction["availability"], "count_eligible": direction["count_eligible"],
                "direction_id": direction["direction_id"], "rationale": direction["rationale"],
                "registry_sha256": registry["registry_sha256"],
                "registry_version": registry["registry_version"], "state": "not_applicable_red",
            })
        return tuple(rows)
    except (EvaluationError, RelevanceValidationError, FilesystemPolicyError, OSError, TypeError, ValueError) as error:
        diagnostic = _diagnostic(str(error), "metamorphic_registry")
        return tuple({"authority_bindings": dict(sorted(bindings.items())), "blocking_diagnostics": [diagnostic.as_dict()], "direction_id": direction, "state": "invalid_withheld"} for direction in REQUIRED_METAMORPHIC_DIRECTIONS)


def build_repeat_results(
    bindings: Mapping[str, str],
) -> tuple[PopulationManifest, tuple[RepeatObservation, ...], tuple[RepeatComparison, ...], MetricResult]:
    """Represent Red's empty repeat population without a synthetic observation."""
    population = build_population_manifest("repeat.disagreement", "red", ())
    return population, (), (), _not_applicable("repeat_disagreement", bindings)


def build_shortcut_family_results(root: Path, bindings: Mapping[str, str]) -> tuple[MetricResult, tuple[MetricResult, ...]]:
    """Bind family/metamorphic delta tracks to frozen registries before Red inapplicability."""
    try:
        _values, registry_bindings = _frozen_registry_values(root)
        bound = dict(sorted({**bindings, **registry_bindings}.items()))
        return (
            _not_applicable("shortcut_family_delta", bound),
            tuple(_not_applicable(f"metamorphic_{direction}", bound) for direction in REQUIRED_METAMORPHIC_DIRECTIONS),
        )
    except (EvaluationError, RelevanceValidationError, FilesystemPolicyError, OSError, TypeError, ValueError) as error:
        diagnostic = _diagnostic(str(error), "frozen_registries")
        return (
            MetricResult("shortcut_family_delta", "invalid_withheld", bindings, blocking_diagnostics=(diagnostic,)),
            tuple(
                MetricResult(f"metamorphic_{direction}", "invalid_withheld", bindings, blocking_diagnostics=(diagnostic,))
                for direction in REQUIRED_METAMORPHIC_DIRECTIONS
            ),
        )


def build_pairhit_result(
    root: Path,
    retrieved_pair_ids: Mapping[str, Sequence[str]],
    bindings: Mapping[str, str],
) -> tuple[PopulationManifest, MetricResult, tuple[Mapping[str, object], ...]]:
    """Calculate PairHit@2 only from the frozen strict eligible collection."""
    values, registry_bindings = _frozen_registry_values(root)
    relevance = values["relevance"]
    eligible = tuple(relevance["strict_pairhit_eligible_case_ids"])
    if tuple(sorted(eligible)) != eligible or len(eligible) != len(set(eligible)):
        raise EvaluationError("PAIRHIT_ELIGIBILITY_INVALID")
    if set(retrieved_pair_ids) != set(eligible):
        raise EvaluationError("PAIRHIT_RETRIEVED_CASE_INVALID")
    population = build_population_manifest("pairhit.at_2", "strict", eligible)
    bound = dict(sorted({**bindings, **registry_bindings}.items()))
    if not eligible:
        return (
            population,
            MetricResult("pairhit_at_2", "empty_population", bound, population.population_id, population.set_sha256),
            (),
        )
    relevant_by_case = {
        str(row["case_id"]): frozenset(str(pair_id) for pair_id in row["relevant_pair_ids"])
        for row in relevance["strict_rows"]
    }
    rows: list[Mapping[str, object]] = []
    hits = 0
    for case_id in eligible:
        observed = tuple(retrieved_pair_ids[case_id])
        if (
            len(observed) > 2
            or len(observed) != len(set(observed))
            or any(not isinstance(pair_id, str) or not pair_id for pair_id in observed)
        ):
            raise EvaluationError("PAIRHIT_RETRIEVED_PAIR_INVALID")
        if any(pair_id in relevant_by_case[case_id] for pair_id in observed):
            hits += 1
        rows.append({"case_id": case_id, "retrieved_pair_ids": list(observed)})
    return (
        population,
        MetricResult(
            "pairhit_at_2", "measured", bound, population.population_id,
            population.set_sha256, hits, population.denominator,
            hits / population.denominator,
        ),
        tuple(rows),
    )


def build_construction_feasibility(
    experiment_root: Path, project_root: Path, construction_inputs: Sequence[Mapping[str, object]],
) -> tuple[ConstructionAttempt, ...]:
    """Build construction evidence only from one declared, project-rooted inventory."""
    if not isinstance(experiment_root, Path) or not isinstance(project_root, Path):
        raise EvaluationError("CONSTRUCTION_SOURCE_CONTRACT_INVALID")
    normalized: list[tuple[str, str, str]] = []
    for item in construction_inputs:
        if not isinstance(item, Mapping) or set(item) != {"path", "status", "sha256"}:
            raise EvaluationError("CONSTRUCTION_SOURCE_CONTRACT_INVALID")
        path, status, digest = item.get("path"), item.get("status"), item.get("sha256")
        if not isinstance(path, str) or not isinstance(status, str):
            raise EvaluationError("CONSTRUCTION_SOURCE_CONTRACT_INVALID")
        try:
            normalized.append((path, status, require_sha256(digest)))
        except ValueError as error:
            raise EvaluationError("CONSTRUCTION_SOURCE_CONTRACT_INVALID") from error
    if tuple((path, status) for path, status, _digest in normalized) != CONSTRUCTION_SOURCE_CONTRACT:
        raise EvaluationError("CONSTRUCTION_SOURCE_CONTRACT_INVALID")
    paths = [path for path, _status, _digest in normalized]
    try:
        files = read_authoritative_files(project_root, paths)
    except (FilesystemPolicyError, OSError, ValueError) as error:
        raise EvaluationError("CONSTRUCTION_ARTIFACT_INVALID") from error
    for path, _status, digest in normalized:
        if sha256_bytes(files[path][1]) != digest:
            raise EvaluationError("CONSTRUCTION_ARTIFACT_SUBSTITUTED")
    attempts: list[ConstructionAttempt] = []
    for index, (path, status, _digest) in enumerate(normalized, start=1):
        attempt_id = f"construction-{index:02d}"
        predecessor_id = None if index == 1 else f"construction-{index - 1:02d}"
        successor_id = None if index == len(normalized) else f"construction-{index + 1:02d}"
        raw = files[path][1]
        attempts.append(ConstructionAttempt(
            attempt_id, path, sha256_bytes(raw), status, predecessor_id, successor_id,
            "immutable", (path,), (sha256_bytes(raw),),
        ))
    return tuple(attempts)


def _metamorphic_directions(root: Path, bindings: Mapping[str, str]) -> tuple[Mapping[str, object], ...]:
    return build_metamorphic_results(root, bindings)


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
        repeat_population, _observations, _comparisons, repeat_result = build_repeat_results(bindings)
        pairhit_population, pairhit_result, _retrieved_pairs = build_pairhit_result(root, {}, bindings)
        shortcut_result, metamorphic_results = build_shortcut_family_results(root, bindings)
        non_pair_results = {
            "pairhit_at_2": pairhit_result,
            "repeat_disagreement": repeat_result,
            "shortcut_family_delta": shortcut_result,
            **{item.metric_id: item for item in metamorphic_results},
        }
        metrics = tuple(measured.get(metric_id, non_pair_results.get(metric_id, _not_applicable(metric_id, bindings))) for metric_id in METRIC_IDS)
        directions = _metamorphic_directions(root, bindings)
        applicability = tuple(metrics)
        pairwise = tuple(
            build_pairwise_comparison((), comparison_id, {}, authority_bindings=bindings)
            for comparison_id in ("b_minus_a", "c_minus_b")
        )
        return EvaluationBundle("partition-evaluation-red-v1", "red", 0, 0, True, deterministic, red, applicability, populations + (pairhit_population, repeat_population), rows, metrics, base_diagnostics, directions, pairwise)
    except (EvaluationError, FilesystemPolicyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        diagnostics = ordered_diagnostics(list(base_diagnostics) + [_diagnostic(str(error), "deterministic_measurement")])
        metrics = tuple(MetricResult(metric_id, "invalid_withheld", bindings, blocking_diagnostics=diagnostics) for metric_id in METRIC_IDS)
        return EvaluationBundle("partition-evaluation-red-v1", "red", 0, 0, True, deterministic, red, metrics, (), (), metrics, diagnostics)

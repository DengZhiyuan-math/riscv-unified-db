# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Red-only contracts for the Phase 6 evaluation composition layer."""

from __future__ import annotations

import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import asdict
from pathlib import Path

from specchoice_evaluation.cli import main
from specchoice_evaluation.core import (
    METRIC_IDS,
    PAIRWISE_INTERVENTION_CONTRACTS,
    RESULT_STATES,
    ArtifactBinding,
    AtomicResultRow,
    ConstructionAttempt,
    DimensionBinding,
    FailureRecord,
    MetricResult,
    RepeatComparison,
    RepeatObservation,
    VerifiedJoinReference,
    WarningRecord,
    build_construction_feasibility,
    build_failure_ledger,
    build_frame_axis_results,
    build_pairhit_result,
    build_pairwise_comparison,
    build_population_manifest,
    build_red_evaluation,
    build_repeat_results,
    build_shortcut_family_results,
    build_warning_ledger,
    close_join,
    propagate_blockers,
    validate_frozen_bindings,
)
from specchoice_evaluation.review import (
    build_evaluation_packet,
    build_readiness,
    build_review_decision,
    publish_evaluation_package,
    render_evaluation_markdown,
    validate_evaluation_packet,
    validate_evaluation_policy,
    validate_readiness,
    validate_review_decision,
)
from specchoice_evidence.canonical import canonical_json_bytes, sha256_bytes

EXPERIMENT = Path(__file__).resolve().parents[1]
PROJECT = EXPERIMENT.parents[1]


class PartitionEvaluationTests(unittest.TestCase):
    @staticmethod
    def _rehash_policy(policy: dict[str, object]) -> dict[str, object]:
        policy = json.loads(canonical_json_bytes(policy))
        policy.pop("policy_sha256", None)
        policy["policy_sha256"] = sha256_bytes(canonical_json_bytes(policy))
        return policy

    def _generation_two_policy(
        self, experiment_root: Path = EXPERIMENT, project_root: Path = PROJECT,
    ) -> dict[str, object]:
        """Build an in-memory successor policy without publishing it."""
        legacy = json.loads((experiment_root / "config/evaluation/partition-evaluation-red-generation-001.json").read_text())
        construction = [
            {"path": path, "status": status, "sha256": sha256_bytes((project_root / path).read_bytes())}
            for path, status in (
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
        ]
        policy = {
            **legacy,
            "schema_version": "partition-evaluation-policy-v2",
            "generation_id": "partition-evaluation-red-generation-002",
            "construction_inputs": construction,
            "outputs": {
                "markdown": "runs/partition-evaluation-red-generation-002/evaluation-report.md",
                "packet": "runs/partition-evaluation-red-generation-002/evaluation-packet.json",
                "readiness": "receipts/partition-evaluation-red-generation-002-readiness.json",
            },
        }
        return self._rehash_policy(policy)

    def _copy_project(self, directory: str) -> tuple[Path, Path]:
        project = Path(directory) / "project"
        experiment = project / "experiments/specchoice-v1.3.2"
        shutil.copytree(EXPERIMENT, experiment, ignore=shutil.ignore_patterns("__pycache__"))
        for source in self._generation_two_policy()["construction_inputs"]:
            path = str(source["path"])
            if path.startswith("experiments/specchoice-v1.3.2/"):
                continue
            target = project / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PROJECT / path, target)
        return project, experiment

    @staticmethod
    def _binding(role: str) -> ArtifactBinding:
        return ArtifactBinding(True, f"frozen/{role}.json", "a" * 64, None)

    @staticmethod
    def _row(*, treatment: str, case_id: str = "case-1", partition: str = "strict") -> AtomicResultRow:
        return AtomicResultRow(
            "evaluation", partition, case_id,
            treatment=DimensionBinding(True, treatment, None),
            repeat_id=DimensionBinding(True, "repeat-1", None),
            outcome_id="outcome-1",
            outcome={"correct": True},
        )

    def test_pair_join_rejects_missing_duplicate_and_cross_partition_rows(self) -> None:
        bindings = {role: self._binding(role) for role in (
            "gold", "prediction", "prompt", "raw_response", "parsed_response",
            "evidence_spans", "treatment", "repeat",
        )}
        good = self._row(treatment="B")
        closed = close_join("evaluation", "strict", "case-1", bindings, [good], expected_bindings=bindings)
        self.assertEqual("closed", closed.status)
        self.assertEqual((), closed.diagnostics)
        self.assertEqual(closed.join_sha256, close_join("evaluation", "strict", "case-1", bindings, [good], expected_bindings=bindings).join_sha256)
        for changed in (
            {key: value for key, value in bindings.items() if key != "prompt"},
            {**bindings, "unexpected": self._binding("unexpected")},
        ):
            invalid = close_join("evaluation", "strict", "case-1", changed, [good], expected_bindings=bindings)
            self.assertEqual("invalid_withheld", invalid.status)
            self.assertTrue(invalid.diagnostics)
        duplicate = close_join("evaluation", "strict", "case-1", bindings, [good, good], expected_bindings=bindings)
        cross_partition = close_join("evaluation", "strict", "case-1", bindings, [good, self._row(treatment="A", partition="auxiliary")], expected_bindings=bindings)
        self.assertEqual("invalid_withheld", duplicate.status)
        self.assertEqual("invalid_withheld", cross_partition.status)

    @staticmethod
    def _pair_controls(rows: list[AtomicResultRow]) -> dict[tuple[str, str, str, str, str, str], dict[str, object]]:
        delegation = PAIRWISE_INTERVENTION_CONTRACTS["b_minus_a"]["treatment_values"]
        selection = PAIRWISE_INTERVENTION_CONTRACTS["c_minus_b"]["treatment_values"]
        return {
            row.identity(): {
                "delegation_frame": delegation["A"] if row.treatment.value == "A" else delegation["B"],
                "pair_selection": selection["C"] if row.treatment.value == "C" else selection["B"],
                "prompt": "same",
            }
            for row in rows
        }

    def _verified_reference(
        self, row: AtomicResultRow, *, expected_bindings: dict[str, ArtifactBinding] | None = None,
    ) -> VerifiedJoinReference:
        bindings = {role: self._binding(role) for role in (
            "gold", "prediction", "prompt", "raw_response", "parsed_response",
            "evidence_spans", "treatment", "repeat",
        )}
        manifest = close_join(
            row.authority_domain, row.partition, row.case_id, bindings, [row],
            expected_bindings=bindings if expected_bindings is None else expected_bindings,
        )
        return VerifiedJoinReference(row, manifest, manifest.join_sha256)

    def test_pairwise_requires_closed_verified_join(self) -> None:
        rows = [self._row(treatment="A"), self._row(treatment="B")]
        controls = self._pair_controls(rows)
        bare = build_pairwise_comparison(rows, "b_minus_a", controls)
        self.assertEqual("invalid_withheld", bare.result.state)
        self.assertEqual("PAIRWISE_JOIN_REFERENCE_INVALID", bare.result.blocking_diagnostics[0].code)

        references = [self._verified_reference(row) for row in rows]
        for candidate in (references[:1], [*references, references[0]]):
            comparison = build_pairwise_comparison(candidate, "b_minus_a", controls)
            self.assertEqual("invalid_withheld", comparison.result.state)
            self.assertEqual("PAIRWISE_JOIN_REFERENCE_INVALID", comparison.result.blocking_diagnostics[0].code)

        cross_case = VerifiedJoinReference(rows[1], references[0].manifest, references[0].expected_join_sha256)
        comparison = build_pairwise_comparison([references[0], cross_case], "b_minus_a", controls)
        self.assertEqual("invalid_withheld", comparison.result.state)
        self.assertEqual("PAIRWISE_JOIN_REFERENCE_INVALID", comparison.result.blocking_diagnostics[0].code)

    def test_pairwise_requires_real_named_intervention(self) -> None:
        rows = [self._row(treatment="A"), self._row(treatment="B")]
        references = [self._verified_reference(row) for row in rows]
        controls = self._pair_controls(rows)
        equal = {identity: dict(value) for identity, value in controls.items()}
        equal[rows[0].identity()]["delegation_frame"] = equal[rows[1].identity()]["delegation_frame"]
        for candidate in (equal, {
            **controls,
            rows[0].identity(): {**controls[rows[0].identity()], "prompt": "different"},
        }):
            comparison = build_pairwise_comparison(references, "b_minus_a", candidate)
            self.assertEqual("invalid_withheld", comparison.result.state)
            self.assertEqual("PAIRWISE_INTERVENTION_INVALID", comparison.result.blocking_diagnostics[0].code)
        self.assertEqual("measured", build_pairwise_comparison(references, "b_minus_a", controls).result.state)

    def test_pairwise_rejects_missing_or_treatment_inconsistent_intervention(self) -> None:
        rows = [self._row(treatment="B"), self._row(treatment="C")]
        references = [self._verified_reference(row) for row in rows]
        controls = self._pair_controls(rows)
        missing = {identity: dict(value) for identity, value in controls.items()}
        missing[rows[0].identity()].pop("pair_selection")
        swapped = {identity: dict(value) for identity, value in controls.items()}
        values = PAIRWISE_INTERVENTION_CONTRACTS["c_minus_b"]["treatment_values"]
        swapped[rows[0].identity()]["pair_selection"] = values["C"]
        swapped[rows[1].identity()]["pair_selection"] = values["B"]
        unknown = {identity: dict(value) for identity, value in controls.items()}
        unknown[rows[1].identity()]["pair_selection"] = "unexpected"
        for candidate in (missing, swapped, unknown):
            comparison = build_pairwise_comparison(references, "c_minus_b", candidate)
            self.assertEqual("invalid_withheld", comparison.result.state)
            self.assertEqual("PAIRWISE_INTERVENTION_INVALID", comparison.result.blocking_diagnostics[0].code)

    def test_substituted_closed_join_hash_cannot_measure(self) -> None:
        rows = [self._row(treatment="A"), self._row(treatment="B")]
        controls = self._pair_controls(rows)
        original = self._verified_reference(rows[0])
        substituted_bindings = {role: self._binding(role) for role in (
            "gold", "prediction", "prompt", "raw_response", "parsed_response",
            "evidence_spans", "treatment", "repeat",
        )}
        substituted_bindings["prompt"] = ArtifactBinding(True, "frozen/substituted-prompt.json", "b" * 64, None)
        substituted_manifest = close_join(
            rows[0].authority_domain, rows[0].partition, rows[0].case_id, substituted_bindings, [rows[0]],
            expected_bindings=substituted_bindings,
        )
        comparison = build_pairwise_comparison([
            VerifiedJoinReference(rows[0], substituted_manifest, original.expected_join_sha256),
            self._verified_reference(rows[1]),
        ], "b_minus_a", controls)
        self.assertEqual("invalid_withheld", comparison.result.state)
        self.assertEqual("PAIRWISE_JOIN_REFERENCE_INVALID", comparison.result.blocking_diagnostics[0].code)

    def test_c_minus_b_population_is_independent(self) -> None:
        rows = [
            self._row(treatment="A"), self._row(treatment="B"), self._row(treatment="C"),
            self._row(treatment="B", case_id="case-2"), self._row(treatment="C", case_id="case-2"),
        ]
        controls = self._pair_controls(rows)
        references = [self._verified_reference(row) for row in rows]
        b_minus_a = build_pairwise_comparison(references[:2], "b_minus_a", controls)
        c_minus_b = build_pairwise_comparison(references[1:], "c_minus_b", controls)
        self.assertEqual("measured", b_minus_a.result.state)
        self.assertEqual("measured", c_minus_b.result.state)
        self.assertNotEqual(b_minus_a.population_id, c_minus_b.population_id)
        self.assertNotEqual(b_minus_a.population_sha256, c_minus_b.population_sha256)
        self.assertNotEqual(b_minus_a.result.denominator, c_minus_b.result.denominator)

    def test_red_pairwise_contracts_are_visible_without_rows_or_ratios(self) -> None:
        bundle = build_red_evaluation(EXPERIMENT)
        comparisons = {item.comparison_id: item for item in bundle.pairwise_comparisons}
        self.assertEqual({"b_minus_a", "c_minus_b"}, set(comparisons))
        for comparison in comparisons.values():
            self.assertEqual((), comparison.paired_row_ids)
            self.assertEqual("not_applicable_red", comparison.result.state)
            self.assertIsNone(comparison.result.numerator)
            self.assertIsNone(comparison.result.denominator)
            self.assertIsNone(comparison.result.score)

    def test_frame_warning_is_report_only(self) -> None:
        bindings = {"red_execution_evidence": "b" * 64}
        original = tuple(item.as_dict() for item in build_frame_axis_results(bindings))
        warning = WarningRecord(
            "FRAME_COMBINATION_REQUIRES_REVIEW", "evaluation", "advisory", "report_only",
            "case-1", "outcome-1", "frame-advisory-patterns-v1", "a" * 64,
        )
        self.assertEqual((warning,), build_warning_ledger([warning]))
        self.assertEqual(original, tuple(item.as_dict() for item in build_frame_axis_results(bindings)))
        with self.assertRaisesRegex(Exception, "WARNING_LEDGER_DUPLICATE"):
            build_warning_ledger([warning, warning])

    def test_frozen_binding_drift_withholds_dependent_domain(self) -> None:
        failure = validate_frozen_bindings(
            {"family": "a" * 64, "prompt": "b" * 64},
            {"family": "a" * 64, "prompt": "c" * 64},
            depends_on=("frozen_bindings",),
        )
        self.assertIsNotNone(failure)
        assert isinstance(failure, FailureRecord)
        self.assertEqual((failure,), build_failure_ledger([failure]))
        baseline = (
            MetricResult("frame_authority", "not_applicable_red", {}, reason="not_applicable_red"),
            MetricResult("surfacing", "not_applicable_red", {}, reason="not_applicable_red"),
        )
        withheld = {item.metric_id: item for item in propagate_blockers([failure], baseline)}
        self.assertEqual("invalid_withheld", withheld["frame_authority"].state)
        self.assertEqual("not_applicable_red", withheld["surfacing"].state)
        self.assertFalse(any(item.state != "invalid_withheld" for item in withheld.values() if item.metric_id == "frame_authority"))

    def test_repeat_and_shortcut_family_red_tracks_have_no_observations(self) -> None:
        bindings = {"red_execution_evidence": "b" * 64}
        population, observations, comparisons, result = build_repeat_results(bindings)
        self.assertEqual("repeat.disagreement", population.population_id)
        self.assertEqual((), population.eligible_ids)
        self.assertEqual((), observations)
        self.assertEqual((), comparisons)
        self.assertEqual("not_applicable_red", result.state)
        self.assertIsNone(result.denominator)
        self.assertIsNone(result.score)
        self.assertTrue(RepeatObservation.__dataclass_fields__)
        self.assertTrue(RepeatComparison.__dataclass_fields__)
        shortcut, metamorphic = build_shortcut_family_results(EXPERIMENT, bindings)
        self.assertEqual("not_applicable_red", shortcut.state)
        self.assertEqual((), shortcut.blocking_diagnostics)
        self.assertTrue(all(item.state == "not_applicable_red" for item in metamorphic))

    def test_pairhit_uses_only_frozen_eligible_ids(self) -> None:
        bindings = {"red_execution_evidence": "b" * 64}
        population, result, retrieved = build_pairhit_result(EXPERIMENT, {}, bindings)
        self.assertEqual("pairhit.at_2", population.population_id)
        self.assertEqual((), population.eligible_ids)
        self.assertEqual("empty_population", result.state)
        self.assertIsNone(result.numerator)
        self.assertIsNone(result.denominator)
        self.assertIsNone(result.score)
        self.assertEqual((), retrieved)
        with self.assertRaisesRegex(Exception, "PAIRHIT_RETRIEVED_CASE_INVALID"):
            build_pairhit_result(EXPERIMENT, {"ambient-case": ("pair-1",)}, bindings)

    def test_construction_feasibility_preserves_attempt_order_and_namespace(self) -> None:
        policy = self._generation_two_policy()
        attempts = build_construction_feasibility(EXPERIMENT, PROJECT, policy["construction_inputs"])
        self.assertGreaterEqual(len(attempts), 10)
        self.assertEqual(tuple(f"construction-{index:02d}" for index in range(1, len(attempts) + 1)), tuple(item.attempt_id for item in attempts))
        self.assertEqual(
            {"rejected", "cancelled", "failed_closed", "superseded", "completed", "successor"},
            {item.status for item in attempts},
        )
        self.assertTrue(all(item.custody_state == "immutable" for item in attempts))
        self.assertTrue(all(item.source_path.startswith((".planning/", "experiments/")) for item in attempts))
        self.assertFalse({"numerator", "denominator", "score", "correct", "population_id"} & set(ConstructionAttempt.__dataclass_fields__))
        with tempfile.TemporaryDirectory() as directory:
            copied_project, copied = self._copy_project(directory)
            (copied / "receipts/red-execution-v2.json").unlink()
            with self.assertRaisesRegex(Exception, "CONSTRUCTION_ARTIFACT_INVALID"):
                build_construction_feasibility(copied, copied_project, policy["construction_inputs"])

    def test_forged_rehashed_packet_is_rejected_by_root_derivation(self) -> None:
        policy = self._generation_two_policy()
        packet = build_evaluation_packet(
            build_red_evaluation(EXPERIMENT),
            policy=policy,
            construction_attempts=build_construction_feasibility(EXPERIMENT, PROJECT, policy["construction_inputs"]),
        )
        forged = json.loads(canonical_json_bytes(packet))
        metric = next(item for item in forged["metrics"] if item["metric_id"] == "surfacing")
        metric["score"] = 0.0
        forged["applicability_matrix"] = forged["metrics"]
        forged["components"]["metrics"] = forged["metrics"]
        forged["components"]["applicability"] = forged["applicability_matrix"]
        forged["component_sha256"] = {
            name: sha256_bytes(canonical_json_bytes(value))
            for name, value in sorted(forged["components"].items())
        }
        forged["component_set_sha256"] = sha256_bytes(canonical_json_bytes(forged["component_sha256"]))
        forged.pop("packet_sha256")
        forged["packet_sha256"] = sha256_bytes(canonical_json_bytes(forged))
        markdown = render_evaluation_markdown(forged)
        readiness = build_readiness(forged, policy=policy, markdown=markdown)
        with self.assertRaisesRegex(Exception, "EVALUATION_PACKET_DERIVATION_INVALID"):
            validate_readiness(EXPERIMENT, PROJECT, policy, forged, markdown, readiness)

    def test_each_declared_construction_source_is_policy_bound(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project, experiment = self._copy_project(directory)
            policy = self._generation_two_policy(experiment, project)
            for source in policy["construction_inputs"]:
                path = project / str(source["path"])
                original = path.read_bytes()
                path.write_bytes(original + b"\nconstruction-tamper\n")
                with self.assertRaisesRegex(Exception, "CONSTRUCTION_ARTIFACT_SUBSTITUTED"):
                    validate_evaluation_policy(experiment, project, policy)
                self.assertFalse((experiment / policy["outputs"]["packet"]).exists())
                path.write_bytes(original)

    def test_construction_source_declaration_is_exact(self) -> None:
        policy = self._generation_two_policy()
        for changed in (
            policy["construction_inputs"][:-1],
            [*policy["construction_inputs"], policy["construction_inputs"][-1]],
            list(reversed(policy["construction_inputs"])),
            [
                {**policy["construction_inputs"][0], "status": "failed_closed"},
                *policy["construction_inputs"][1:],
            ],
            [
                {**policy["construction_inputs"][0], "sha256": "0" * 64},
                *policy["construction_inputs"][1:],
            ],
        ):
            candidate = self._rehash_policy({**policy, "construction_inputs": changed})
            with self.assertRaisesRegex(Exception, "CONSTRUCTION_SOURCE_CONTRACT_INVALID"):
                validate_evaluation_policy(EXPERIMENT, PROJECT, candidate)

    def test_generation_one_evidence_is_historical_and_unpromotable(self) -> None:
        paths = (
            "config/evaluation/partition-evaluation-red-generation-001.json",
            "runs/partition-evaluation-red-generation-001/evaluation-packet.json",
            "runs/partition-evaluation-red-generation-001/evaluation-report.md",
            "receipts/partition-evaluation-red-generation-001-readiness.json",
            "reviews/partition-evaluation-red-generation-001-decision.json",
        )
        before = {path: sha256_bytes((EXPERIMENT / path).read_bytes()) for path in paths}
        legacy = json.loads((EXPERIMENT / paths[0]).read_text())
        with self.assertRaisesRegex(Exception, "EVALUATION_POLICY_LEGACY_GENERATION"):
            validate_evaluation_policy(EXPERIMENT, PROJECT, legacy)
        self.assertEqual(before, {path: sha256_bytes((EXPERIMENT / path).read_bytes()) for path in paths})

    def test_component_inventory_is_exact_and_live(self) -> None:
        policy = self._generation_two_policy()
        for component_ids in (
            policy["component_ids"][:-1],
            [*policy["component_ids"], "unexpected"],
            [*policy["component_ids"][1:], policy["component_ids"][0]],
        ):
            candidate = self._rehash_policy({**policy, "component_ids": component_ids})
            with self.assertRaisesRegex(Exception, "EVALUATION_POLICY_COMPONENTS_INVALID"):
                validate_evaluation_policy(EXPERIMENT, PROJECT, candidate)
        packet = build_evaluation_packet(
            build_red_evaluation(EXPERIMENT), policy=policy,
            construction_attempts=build_construction_feasibility(EXPERIMENT, PROJECT, policy["construction_inputs"]),
        )
        for mutation in (
            lambda value: value["components"].pop("warnings"),
            lambda value: value["components"].__setitem__("unexpected", []),
            lambda value: value["components"].__setitem__("renamed_metrics", value["components"].pop("metrics")),
        ):
            candidate = json.loads(canonical_json_bytes(packet))
            mutation(candidate)
            candidate["component_sha256"] = {
                name: sha256_bytes(canonical_json_bytes(value))
                for name, value in sorted(candidate["components"].items())
            }
            candidate["component_set_sha256"] = sha256_bytes(canonical_json_bytes(candidate["component_sha256"]))
            candidate.pop("packet_sha256")
            candidate["packet_sha256"] = sha256_bytes(canonical_json_bytes(candidate))
            with self.assertRaisesRegex(Exception, "EVALUATION_PACKET_COMPONENTS_INVALID"):
                validate_evaluation_packet(EXPERIMENT, PROJECT, policy, candidate)

    def test_runtime_policy_error_is_stable_and_traceback_free(self) -> None:
        policy = self._generation_two_policy()
        policy["inputs"] = [
            item for item in policy["inputs"]
            if item["path"] != policy["runtime_closure"]["path"]
        ]
        policy = self._rehash_policy(policy)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as policy_file:
            json.dump(policy, policy_file)
            path = Path(policy_file.name)
        try:
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = main([
                    "verify-red-package", "--experiment-root", str(EXPERIMENT), "--project-root", str(PROJECT),
                    "--policy", str(path),
                ])
            self.assertEqual(2, code)
            self.assertIn("EVALUATION_POLICY_RUNTIME_INVALID", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())
            self.assertEqual("", stdout.getvalue())
        finally:
            path.unlink()

    def test_red_metrics_preserve_applicability_and_separate_denominators(self) -> None:
        bundle = build_red_evaluation(EXPERIMENT)
        packet = build_evaluation_packet(bundle)
        self.assertEqual("red", bundle.branch)
        self.assertEqual(0, bundle.n_strict)
        self.assertEqual(0, bundle.repeat_count)
        self.assertTrue(bundle.no_model_calls)
        self.assertEqual(RESULT_STATES, ("measured", "empty_population", "not_applicable_red", "invalid_withheld"))
        self.assertEqual(tuple(sorted(METRIC_IDS)), METRIC_IDS)
        self.assertEqual(
            {"deterministic_measurement", "red_execution_evidence"},
            {bundle.deterministic_measurement.authority_domain, bundle.red_execution_evidence.authority_domain},
        )
        metrics = {item.metric_id: item for item in bundle.metrics}
        self.assertEqual(set(METRIC_IDS), set(metrics))
        self.assertFalse(any(item.metric_id == "headline_score" for item in bundle.metrics))
        self.assertTrue(any(item.state == "measured" for item in bundle.metrics))
        for metric in bundle.metrics:
            if metric.state == "measured":
                self.assertIsNotNone(metric.population_id)
                self.assertEqual(metric.denominator, next(
                    population.denominator for population in bundle.populations
                    if population.population_id == metric.population_id
                ))
                self.assertIsNotNone(metric.score)
            if metric.state == "not_applicable_red":
                self.assertIsNone(metric.numerator)
                self.assertIsNone(metric.denominator)
                self.assertIsNone(metric.score)
                self.assertTrue(metric.reason)
        self.assertEqual("red", packet["branch"])
        self.assertEqual(canonical_json_bytes(packet), canonical_json_bytes(build_evaluation_packet(bundle)))
        self.assertIn(b"# Red authority", render_evaluation_markdown(packet))
        self.assertEqual(packet["packet_sha256"], build_readiness(packet)["packet_sha256"])

    def test_phase6_cli_has_no_external_or_subprocess_surface(self) -> None:
        source_root = EXPERIMENT / "src" / "specchoice_evaluation"
        text = "\n".join(path.read_text() for path in sorted(source_root.glob("*.py")))
        for forbidden in ("import socket", "import subprocess", "urllib", "requests", "openai", "http.client"):
            self.assertNotIn(forbidden, text)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as policy_file:
            json.dump({"schema_version": "partition-evaluation-policy-v1"}, policy_file)
            policy = Path(policy_file.name)
        try:
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = main([
                    "build-red", "--experiment-root", str(EXPERIMENT), "--project-root", str(PROJECT),
                    "--policy", str(policy),
                ])
            self.assertEqual(2, code)
            self.assertIn("EVALUATION_POLICY_LEGACY_GENERATION", stderr.getvalue())
            self.assertEqual("", stdout.getvalue())
        finally:
            policy.unlink()

    def test_packet_readiness_are_decision_free_and_hash_bound(self) -> None:
        policy = self._generation_two_policy()
        validate_evaluation_policy(EXPERIMENT, PROJECT, policy)
        packet = build_evaluation_packet(
            build_red_evaluation(EXPERIMENT), policy=policy,
            construction_attempts=build_construction_feasibility(EXPERIMENT, PROJECT, policy["construction_inputs"]),
        )
        markdown = render_evaluation_markdown(packet)
        readiness = build_readiness(packet, policy=policy, markdown=markdown)
        validate_evaluation_packet(EXPERIMENT, PROJECT, policy, packet)
        validate_readiness(EXPERIMENT, PROJECT, policy, packet, markdown, readiness)
        for value in (packet, readiness):
            rendered = canonical_json_bytes(value).decode("utf-8")
            for forbidden in ("reviewer", "disposition", "decision", "approval"):
                self.assertNotIn(forbidden, rendered)
        self.assertFalse(packet["conclusion_ready"])
        self.assertFalse(readiness["conclusion_ready"])
        self.assertTrue(readiness["ready_for_human_review"])
        self.assertTrue(markdown.startswith(b"# Red authority\n"))

    def test_review_decision_requires_exact_hashes_and_closed_responses(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project, experiment = self._copy_project(directory)
            policy = self._generation_two_policy(experiment, project)
            packet, _markdown, _readiness = publish_evaluation_package(experiment, project, policy)
            domains = {row["authority_domain"]: "approved" for row in packet["case_rows"]}
            items = {row["outcome_id"]: "approved" for row in packet["case_rows"]}
            decision = build_review_decision(
                experiment, project, policy, reviewer_id="Zhiyuan Deng", disposition="approved",
                domain_responses=domains, item_responses=items, disputes=[], d16_acknowledgement=True,
            )
            self.assertTrue(decision.conclusion_ready)
            self.assertTrue(decision.phase7_interpretation_authorized)
            self.assertEqual(decision, validate_review_decision(experiment, project, policy, asdict(decision)))
            changed = asdict(decision)
            changed["packet_sha256"] = "0" * 64
            with self.assertRaisesRegex(Exception, "REVIEW_DECISION_HASH_INVALID"):
                validate_review_decision(experiment, project, policy, changed)

    def test_exact_resume_rejects_partial_different_or_substituted_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project, root = self._copy_project(directory)
            policy = self._generation_two_policy(root, project)
            packet, markdown, readiness = publish_evaluation_package(root, project, policy)
            expected = {
                policy["outputs"]["packet"]: canonical_json_bytes(packet),
                policy["outputs"]["markdown"]: markdown,
                policy["outputs"]["readiness"]: canonical_json_bytes(readiness),
            }
            self.assertEqual((packet, markdown, readiness), publish_evaluation_package(root, project, policy))
            (root / policy["outputs"]["packet"]).unlink()
            with self.assertRaisesRegex(Exception, "EVALUATION_OUTPUT_PARTIAL_OR_OCCUPIED"):
                publish_evaluation_package(root, project, policy)
            self.assertFalse((root / policy["outputs"]["packet"]).exists())
            (root / policy["outputs"]["markdown"]).write_bytes(b"different")
            with self.assertRaisesRegex(Exception, "EVALUATION_OUTPUT_PARTIAL_OR_OCCUPIED"):
                publish_evaluation_package(root, project, policy)
            self.assertEqual(b"different", (root / policy["outputs"]["markdown"]).read_bytes())
            self.assertEqual(expected[policy["outputs"]["readiness"]], (root / policy["outputs"]["readiness"]).read_bytes())

    def test_result_states_and_population_order_are_not_interchangeable(self) -> None:
        first = build_population_manifest("test.population", "formal", ["case-b", "case-a"])
        second = build_population_manifest("test.population", "formal", ["case-a", "case-b"])
        self.assertEqual(first, second)
        measured_zero = MetricResult(
            "identity_incorrect", "measured", {"deterministic_measurement": "a" * 64},
            first.population_id, first.set_sha256, 0, first.denominator, 0.0,
        )
        empty = MetricResult(
            "pairhit_at_2", "empty_population", {"red_execution_evidence": "b" * 64},
            first.population_id, first.set_sha256,
        )
        unavailable = MetricResult(
            "b_minus_a", "not_applicable_red", {"red_execution_evidence": "b" * 64},
            reason="not_applicable_red",
        )
        self.assertEqual(0.0, measured_zero.score)
        self.assertNotIn("score", empty.as_dict())
        self.assertNotIn("denominator", unavailable.as_dict())
        invalid = build_red_evaluation(Path(tempfile.mkdtemp()))
        self.assertTrue(all(metric.state == "invalid_withheld" for metric in invalid.metrics))

    def test_red_metamorphic_registry_is_complete_and_unscored(self) -> None:
        bundle = build_red_evaluation(EXPERIMENT)
        expected_ids = (
            "choice_space_origin",
            "hardware_software_authority",
            "normative_note_example",
            "warl_fixed_legal_set",
        )
        self.assertEqual(expected_ids, tuple(item["direction_id"] for item in bundle.metamorphic_directions))
        for item in bundle.metamorphic_directions:
            self.assertEqual("unavailable", item["availability"])
            self.assertFalse(item["count_eligible"])
            self.assertEqual("not_applicable_red", item["state"])
            self.assertIn("registry_sha256", item)
            self.assertNotIn("observation", item)
            self.assertNotIn("numerator", item)
            self.assertNotIn("denominator", item)
            self.assertNotIn("score", item)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "experiment"
            shutil.copytree(EXPERIMENT, root, ignore=shutil.ignore_patterns("__pycache__"))
            path = root / "data/preregistration/metamorphic-registry-v1.json"
            value = json.loads(path.read_text())
            value["directions"] = value["directions"][1:]
            path.write_bytes(canonical_json_bytes(value))
            invalid = build_red_evaluation(root)
            self.assertTrue(all(item["state"] == "invalid_withheld" for item in invalid.metamorphic_directions))


if __name__ == "__main__":
    unittest.main()

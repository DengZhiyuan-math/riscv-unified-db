# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Red-only contracts for the Phase 6 evaluation composition layer."""

from __future__ import annotations

import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from specchoice_evaluation.cli import main
from specchoice_evaluation.core import (
    METRIC_IDS,
    RESULT_STATES,
    ArtifactBinding,
    AtomicResultRow,
    DimensionBinding,
    FailureRecord,
    MetricResult,
    RepeatComparison,
    RepeatObservation,
    WarningRecord,
    build_failure_ledger,
    build_frame_axis_results,
    build_metamorphic_results,
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
    render_evaluation_markdown,
)
from specchoice_evidence.canonical import canonical_json_bytes

EXPERIMENT = Path(__file__).resolve().parents[1]


class PartitionEvaluationTests(unittest.TestCase):
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
        closed = close_join("evaluation", "strict", "case-1", bindings, [good])
        self.assertEqual("closed", closed.status)
        self.assertEqual((), closed.diagnostics)
        self.assertEqual(closed.join_sha256, close_join("evaluation", "strict", "case-1", bindings, [good]).join_sha256)
        for changed in (
            {key: value for key, value in bindings.items() if key != "prompt"},
            {**bindings, "unexpected": self._binding("unexpected")},
        ):
            invalid = close_join("evaluation", "strict", "case-1", changed, [good])
            self.assertEqual("invalid_withheld", invalid.status)
            self.assertTrue(invalid.diagnostics)
        duplicate = close_join("evaluation", "strict", "case-1", bindings, [good, good])
        cross_partition = close_join("evaluation", "strict", "case-1", bindings, [good, self._row(treatment="A", partition="auxiliary")])
        self.assertEqual("invalid_withheld", duplicate.status)
        self.assertEqual("invalid_withheld", cross_partition.status)

    def test_c_minus_b_population_is_independent(self) -> None:
        rows = [
            self._row(treatment="A"), self._row(treatment="B"), self._row(treatment="C"),
            self._row(treatment="B", case_id="case-2"), self._row(treatment="C", case_id="case-2"),
        ]
        controls = {
            row.identity(): {
                "delegation_frame": "without_frame" if treatment == "A" else "with_frame",
                "pair_selection": "other" if treatment == "C" else "fixed",
                "prompt": "same",
            }
            for row, treatment in zip(rows, ("A", "B", "C", "B", "C"), strict=True)
        }
        b_minus_a = build_pairwise_comparison(rows[:2], "b_minus_a", controls)
        c_minus_b = build_pairwise_comparison(rows[1:], "c_minus_b", controls)
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

    def test_red_metamorphic_registry_is_complete_and_unscored(self) -> None:
        bindings = {"red_execution_evidence": "b" * 64}
        directions = build_metamorphic_results(EXPERIMENT, bindings)
        self.assertEqual(
            (
                "choice_space_origin",
                "hardware_software_authority",
                "normative_note_example",
                "warl_fixed_legal_set",
            ),
            tuple(item["direction_id"] for item in directions),
        )
        for direction in directions:
            self.assertEqual("unavailable", direction["availability"])
            self.assertFalse(direction["count_eligible"])
            self.assertEqual("not_applicable_red", direction["state"])
            self.assertNotIn("outcome", direction)
            self.assertNotIn("score", direction)

        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "experiment"
            shutil.copytree(EXPERIMENT, copied)
            registry_path = copied / "data/preregistration/metamorphic-registry-v1.json"
            registry = json.loads(registry_path.read_text())
            registry["directions"] = registry["directions"][:-1]
            registry_path.write_bytes(canonical_json_bytes(registry))
            withheld = build_metamorphic_results(copied, bindings)
        self.assertTrue(all(item["state"] == "invalid_withheld" for item in withheld))

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
                code = main(["build-red", "--repo-root", str(EXPERIMENT), "--policy", str(policy)])
            self.assertEqual(0, code, stderr.getvalue())
            self.assertEqual("red", json.loads(stdout.getvalue())["branch"])
        finally:
            policy.unlink()

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

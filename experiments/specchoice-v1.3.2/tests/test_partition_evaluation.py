# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Red-only contracts for the Phase 6 evaluation composition layer."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from specchoice_evidence.canonical import canonical_json_bytes
from specchoice_evaluation.cli import main
from specchoice_evaluation.core import (
    METRIC_IDS,
    RESULT_STATES,
    MetricResult,
    build_population_manifest,
    build_red_evaluation,
)
from specchoice_evaluation.review import build_evaluation_packet, build_readiness, render_evaluation_markdown


EXPERIMENT = Path(__file__).resolve().parents[1]


class PartitionEvaluationTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()

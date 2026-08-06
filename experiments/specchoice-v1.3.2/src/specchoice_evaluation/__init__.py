# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Red-only partition-aware evaluation contracts."""

from .core import (
    METRIC_IDS,
    RESULT_STATES,
    AtomicResultRow,
    AuthorityAdmission,
    DimensionBinding,
    EvaluationBundle,
    EvaluationError,
    MetricResult,
    PopulationManifest,
    admit_red_inputs,
    build_population_manifest,
    build_red_evaluation,
)
from .review import build_evaluation_packet, build_readiness, render_evaluation_markdown

__all__ = [
    "METRIC_IDS",
    "RESULT_STATES",
    "AtomicResultRow",
    "AuthorityAdmission",
    "DimensionBinding",
    "EvaluationBundle",
    "EvaluationError",
    "MetricResult",
    "PopulationManifest",
    "admit_red_inputs",
    "build_evaluation_packet",
    "build_population_manifest",
    "build_readiness",
    "build_red_evaluation",
    "render_evaluation_markdown",
]

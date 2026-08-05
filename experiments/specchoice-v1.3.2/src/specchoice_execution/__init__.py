# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Closed Red-only execution contracts for the SpecChoice feasibility spike."""

from .red import (
    RedExecutionError,
    audit_red_execution_surface_v1,
    build_red_evidence_v1,
    deny_all_sockets_v1,
    validate_red_authority_v1,
    validate_red_evidence_v1,
    validate_red_execution_policy_v1,
)

__all__ = [
    "RedExecutionError",
    "audit_red_execution_surface_v1",
    "build_red_evidence_v1",
    "deny_all_sockets_v1",
    "validate_red_authority_v1",
    "validate_red_evidence_v1",
    "validate_red_execution_policy_v1",
]

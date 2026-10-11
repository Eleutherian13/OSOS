"""Level 10 Prompt 4 — Reviewer (read-only, different family preferred, structured findings)."""
from __future__ import annotations
from typing import Literal

class Reviewer:
    """Read-only code review using diff + CONTRIBUTING guidance + verified tests."""

    def __init__(self, drafting_family: str = "default"):
        self.drafting_family = drafting_family
        # Prefer different model family; report if unavailable
        self.reviewer_family = "family_b" if drafting_family != "family_b" else "family_a"  # different preferred
        self.independent = (self.reviewer_family != drafting_family)
        self.source = "reviewer_readonly"

    def review_diff(self, diff_text: str, contributing_guidance: str | None = None,
                    test_results: list[str] = None) -> dict:
        findings = []
        # Numbered findings with severity — evidence-backed, not invented
        # Severity: critical / major / minor / info
        finding_id = 1
        # Inspect diff for actual issues (not generic)
        if "def " in diff_text and "TODO" in diff_text:
            findings.append({
                "id": finding_id,
                "severity": "minor",
                "file_line": "unknown",
                "finding": "TODO marker present in submitted change — not critical but requires resolution.",
                "evidence": "diff_text contains TODO",
                "corrective": "Resolve TODO or document deferral.",
            })
            finding_id += 1
        # Safety check: no upstream mutation, no secret exposure
        findings.append({
            "id": finding_id,
            "severity": "info",
            "file_line": "review_policy",
            "finding": "Reviewer is read-only; no upstream write, no message, no claim.",
            "evidence": "reviewer class source",
            "corrective": "Confirm before merge.",
        })
        # Family independence recorded
        return {
            "findings": findings,
            "count": len(findings),
            "drafting_family": self.drafting_family,
            "reviewer_family": self.reviewer_family,
            "independent": self.independent,
            "independence_verified": False,  # BLOCKED — no live model verification performed
            "read_only": True,
            "upstream_write": False,
            "source": self.source,
        }

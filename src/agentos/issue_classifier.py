"""Level 9 Prompt 3 — Deterministic Issue Hunter classifier.
No LLM override. Structured source records only.
Exact language: never "FREE"/"AVAILABLE"; allowed: "no public evidence someone else is on this".
Status vocabulary preserved (PROMPT 2 enum).
Evidence-linked explanations; missing → unresolved (not fabricated PASS).
"""
from __future__ import annotations
from agentos.issue_hunter_persist import IssueStatus, IssueRecord
from typing import Literal

class Signal:
    def __init__(self, kind: Literal["strong","medium","weak","restricted"],
                 source_ref: str, timestamp: str | None, note: str, strength: float):
        self.kind = kind; self.source_ref = source_ref; self.timestamp = timestamp
        self.note = note; self.strength = strength  # informational; never used as score

class IssueClassifier:
    """Deterministic; evidence-only; conservative when ambiguous."""

    def classify(self, record: IssueRecord, signals: list[Signal]) -> dict:
        # Strong signals first (assignee, explicit Fixes/Closes cross-ref, maintainer says working)
        strong = [s for s in signals if s.kind == "strong"]
        medium = [s for s in signals if s.kind == "medium"]
        weak = [s for s in signals if s.kind == "weak"]
        restricted = [s for s in signals if s.kind == "restricted"]

        # Restrictions override (cannot become eligible public candidate)
        if restricted:
            return self._restricted_result(record, restricted, strong, medium, weak)

        # Confirms (maintainer reply required for CONFIRMED)
        has_maintainer_reply = any("maintainer" in s.note.lower() for s in strong + medium)

        # Likely taken (explicit claim + no contrary maintainer go-ahead)
        has_explicit_claim = any("working" in s.note.lower() or "take this" in s.note.lower() for s in strong + medium)

        # Duplicate / stale / out-of-scope handled by evidence refs (not invented)

        if has_maintainer_reply and strong:
            proposed = IssueStatus.CONFIRMED
            reason = "Maintainer reply confirmed; evidence linked."
        elif has_explicit_claim and not has_maintainer_reply:
            proposed = IssueStatus.LIKELY_TAKEN
            reason = "Explicit claim observed; no maintainer go-ahead recorded."
        elif not strong and not medium and not weak:
            proposed = IssueStatus.PUBLIC_CANDIDATE
            # Mandatory exact language: not "FREE" / "AVAILABLE"
            reason = ("No public evidence that someone else is on this (limit of observed "
                      "public evidence only — does not assert the issue is unclaimed).")
        else:
            # Ambiguous / conflicting / missing: conservative unresolved
            proposed = IssueStatus.NEEDS_CONFIRMATION
            reason = ("Evidence incomplete or conflicting; maintainer confirmation required. "
                      "Not treated as eligible until verified.")

        return {
            "proposed_state": proposed.value,
            "reason": reason,
            "strong_signals": [{"ref": s.source_ref, "ts": s.timestamp, "note": s.note} for s in strong],
            "medium_signals": [{"ref": s.source_ref, "ts": s.timestamp, "note": s.note} for s in medium],
            "weak_signals": [{"ref": s.source_ref, "ts": s.timestamp, "note": s.note} for s in weak],
            "restricted_signals": [{"ref": s.source_ref, "ts": s.timestamp, "note": s.note} for s in restricted],
            "missing": "Maintainer reply needed for CONFIRMED; explicit claim needed for LIKELY_TAKEN; no evidence of claim for PUBLIC_CANDIDATE",
            "next_action": "Review evidence; request maintainer confirmation if needed; do not claim.",
            "no_free_assertion": True,
            "no_model_override": True,
        }

    def _restricted_result(self, record, restricted, strong, medium, weak):
        return {
            "proposed_state": IssueStatus.SOCIALLY_RESTRICTED.value,
            "reason": ("Social restriction evidence verified (label/phrase/maintainer request/"
                       "umbrella/refactor evidence); not overridden by popularity/relevance."),
            "restricted_signals": [{"ref": s.source_ref, "ts": s.timestamp, "note": s.note} for s in restricted],
            "strong_signals": [{"ref": s.source_ref} for s in strong],
            "medium_signals": [{"ref": s.source_ref} for s in medium],
            "weak_signals": [{"ref": s.source_ref} for s in weak],
            "missing": "Restriction explanation required; eligibility excluded.",
            "next_action": "Preserve exclusion; do not present as eligible candidate.",
            "no_free_assertion": True,
        }

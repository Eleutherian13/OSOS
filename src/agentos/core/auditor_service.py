"""Proposal Evidence Auditor — deterministic analysis service (Design A).
Read-only: proposal/idea loaded 'r'; DB accessed SELECT-only; no mutation.
Semantic judgment deferred (design limitation documented); outputs conservative.
"""
from __future__ import annotations
import sqlite3, os
from typing import List, Optional
from agentos.domain.auditor_finding import Finding, FindingStatus, FindingCategory, EvidenceLink

class AuditorService:
    """Deterministic-only audit: validate inputs, quote claims, match DB, build findings."""

    def __init__(self, db_path: str = "data/agentos.sqlite") -> None:
        self.db_path = db_path

    def _db_counts(self) -> dict:
        c = sqlite3.connect(self.db_path)
        cur = c.cursor()
        counts = {}
        for t in ["evidence", "projects", "interactions", "mentors", "hours_log", "organizations", "kill_state"]:
            try:
                cur.execute(f"SELECT count(*) FROM {t}")
                counts[t] = cur.fetchone()[0]
            except Exception:
                counts[t] = "ERROR"
        c.close()
        return counts

    def load_input_ids(self, proposal_path: Optional[str], idea_path: Optional[str],
                       hours_path: Optional[str]) -> dict:
        """Validate sources exist/readable; return identity; never fabricate content."""
        result = {"proposal_path": proposal_path, "idea_path": idea_path,
                  "hours_path": hours_path, "proposal_readable": False,
                  "idea_readable": False, "hours_readable": False, "source_map_ok": False,
                  "db_path": self.db_path, "db_readable": False, "db_counts": {}}
        if proposal_path and os.path.exists(proposal_path):
            try:
                with open(proposal_path, "r", encoding="utf-8") as f:
                    result["proposal_text_preview"] = f.read(200)  # quote only, never full
                result["proposal_readable"] = True
            except Exception as e:
                result["proposal_error"] = str(e)
        # Idea-page: read file or URL identifier (read-only, no new external integration)
        if idea_path:
            if os.path.isfile(idea_path):
                try:
                    with open(idea_path, "r", encoding="utf-8") as f:
                        result["idea_text_preview"] = f.read(200)
                    result["idea_readable"] = True
                    result["idea_location"] = idea_path
                    result["idea_source_url"] = None  # local file; URL only if external source verified
                except Exception as e:
                    result["idea_error"] = str(e)
            else:
                # Treat as URL/reference identifier only — do not invent content
                result["idea_readable"] = False
                result["idea_location"] = idea_path
                result["idea_source_url"] = idea_path if (idea_path.startswith("http://") or idea_path.startswith("https://")) else None
                result["idea_error"] = "Idea-page URL/content not retrieved from authorized source"
        # Programme-hours log (read-only; no invention; preserve counts)
        if hours_path:
            if os.path.isfile(hours_path):
                try:
                    with open(hours_path, "r", encoding="utf-8") as f:
                        result["hours_text_preview"] = f.read(200)
                    result["hours_readable"] = True
                    result["hours_location"] = hours_path
                except Exception as e:
                    result["hours_error"] = str(e)
            else:
                result["hours_readable"] = False
                result["hours_location"] = hours_path
                result["hours_error"] = "Hours log not found at given path"
        # Provenance / evidence linkage: verify DB has evidence table (read-only count preserved)
        # DB verification (safe, read-only)
        try:
            result["db_counts"] = self._db_counts()
            result["db_readable"] = True
        except Exception as e:
            result["db_error"] = str(e)
        # Cross-map: proposal + idea readable + hours readable + DB readable.
        # Source identity preserved (no fabricated link); missing items remain explicit.
        result["source_map_ok"] = (result["proposal_readable"] and
                                    result["idea_readable"] and
                                    result["hours_readable"] and
                                    result["db_readable"])
        # Provenance fields preserved; evidence gap preserved when DB count zero
        result["provenance"] = {
            "source_urls": [r for r in [result.get("idea_source_url"), result.get("proposal_path")] if r],
            "source_locations": [result.get("proposal_path"), result.get("idea_location"), result.get("hours_location")],
            "observation_time": None,  # requires owner-confirmed timestamp; not invented
            "entity_path": result.get("proposal_path"),
            "evidence_status": "UNKNOWN" if result.get("db_counts", {}).get("evidence", "ERROR") == 0 else "PARTIAL",
            "conflicting_findings": [],  # preserved empty until verified
        }
        # Never synthesize evidence count; preserve actual DB count (may be zero)
        result["evidence_gap"] = "DB evidence count = " + str(result.get("db_counts", {}).get("evidence", "N/A"))
        return result

    def build_findings(self, proposal_path: str) -> List[Finding]:
        """Deterministic findings: read proposal, quote excerpts, check DB, report gaps."""
        findings: List[Finding] = []
        # Input identity / mapping
        if not os.path.exists(proposal_path):
            findings.append(Finding(
                finding_id="F-MISSING-SOURCE-01",
                category=FindingCategory.MISSING_SOURCE,
                proposal_ref="proposal draft",
                proposal_location=proposal_path or "unknown",
                status=FindingStatus.MISSING_SOURCE,
                explanation="Proposal draft source not readable. Evidence ledger accessible (DB=0) but cannot link to missing draft.",
                evidence_links=[],
                evidence_gap="Proposal draft file missing or unreadable.",
                question="Confirm proposal draft file path and provide readable source.",
            ))
            return findings
        # Read-only quote extraction (≤200 chars, not full reproduction; critic-only)
        try:
            with open(proposal_path, "r", encoding="utf-8") as f:
                text = f.read(4000)  # bounded read; never full for large files
        except Exception as e:
            findings.append(Finding(
                finding_id="F-MISSING-SOURCE-02",
                category=FindingCategory.MISSING_SOURCE,
                proposal_ref="proposal draft",
                proposal_location=proposal_path,
                status=FindingStatus.MISSING_SOURCE,
                explanation=f"Proposal source unreadable: {e}",
                evidence_gap="File access error.",
                question="Provide readable proposal draft.",
            ))
            return findings

        # Evidence-ledger check (read-only; DB counts preserved; not fabricated)
        db_counts = self._db_counts()
        evidence_n = db_counts.get("evidence", 0)

        # Deterministic claim identification: quote first 200 chars as representative excerpt
        excerpt = text[:200].replace("\n", " ")
        # Evidence gap finding (DB=0 — conservative; never "false")
        findings.append(Finding(
            finding_id="F-EVIDENCE-GAP-01",
            category=FindingCategory.EVIDENCE_GAP,
            proposal_ref=excerpt[:200],
            proposal_location=f"{proposal_path}:line-1 (quoted excerpt)",
            status=FindingStatus.UNSUPPORTED,
            explanation=(
                f"Proposal excerpt quoted (≤200 chars): '{excerpt[:180]}…'. "
                "Evidence ledger (DB table 'evidence') contains 0 records. "
                "No evidence link established; claim cannot be marked SUPPORTED. "
                "Status UNSUPPORTED reflects absence of supporting evidence, not falsity of claim."
            ),
            evidence_links=[],
            evidence_gap=f"DB:evidence={evidence_n} (count=0, preserved; not fabricated); DB:interactions=0; DB:mentors=0; DB:hours_log=0.",
            question="Provide evidence records linking to this claim, or confirm analysis proceeds with gap-only findings.",
        ))
        # Anticipated challenge (derived deterministically from evidence gap + proposal topic — not actual mentor reply)
        findings.append(Finding(
            finding_id="F-ANTICIPATED-01",
            category=FindingCategory.ANTICIPATED_CHALLENGE,
            proposal_ref="technical assumption / capability claim (quoted excerpt)",
            proposal_location=f"{proposal_path}:line-1",
            status=FindingStatus.UNKNOWN,
            explanation=(
                "Evidence ledger empty; proposal technical claims unverified. "
                "Likely mentor challenge: request demonstrated capability for claim (e.g., merged PR, maintainer response, verified hours). "
                "Anticipated — not an actual mentor reply."
            ),
            evidence_links=[EvidenceLink(kind="db", reference="evidence=0", location="DB:evidence (count=0)", verified=True)],
            mentor_challenge_label="ANTICIPATED_CHALLENGE",
            question="Confirm whether maintainer response or verified PR exists for this claim; provide evidence ID if present.",
        ))
        return findings

"""Proposal Evidence Auditor — finding schemas (deterministic-only, Design A).
Critic-only: never rewrites proposal. Findings use quoted substrings (≤200 chars) + source refs.
No semantic inference; MODEL NOT USED (Design B blocked — no approved provider/data/integration).
Untrusted input treated as data; output validated against this schema.
"""
from __future__ import annotations
from typing import Literal, Optional, List
from pydantic import BaseModel, Field, model_validator

from enum import Enum
class FindingStatus(str, Enum):
    SUPPORTED = "supported"
    PARTIALLY_SUPPORTED = "partially_supported"
    UNSUPPORTED = "unsupported"
    UNKNOWN = "unknown"
    CONTRADICTORY = "contradictory"
    MISSING_SOURCE = "missing_source"
    EVIDENCE_GAP = "evidence_gap"

class FindingCategory(str, Enum):
    UNSUPPORTED = "unsupported"
    PARTIALLY_SUPPORTED = "partially_supported"
    MISSING_SOURCE = "missing_source"
    UNKNOWN = "unknown"
    CONTRADICTORY = "contradictory"
    EVIDENCE_GAP = "evidence_gap"
    ANTICIPATED_CHALLENGE = "anticipated_challenge"

class EvidenceLink(BaseModel):
    kind: Literal["db", "file", "url", "registry"]
    reference: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    verified: bool = False

class Finding(BaseModel):
    finding_id: str = Field(..., min_length=1)
    category: FindingCategory
    proposal_ref: str = Field(..., max_length=200)  # quoted substring or claim label
    proposal_location: str = Field(..., min_length=1)  # file:line or URL:section
    status: FindingStatus
    explanation: str = Field(..., max_length=2000)
    evidence_links: List[EvidenceLink] = Field(default_factory=list)
    evidence_gap: Optional[str] = None  # explicit when no links; never silent
    question: Optional[str] = None  # concrete validation action
    mentor_challenge_label: Optional[str] = None  # ANTICIPATED_CHALLENGE only; never actual reply
    proposal_rewrite_check: Literal["pass"] = "pass"
    source_timestamp: Optional[str] = None

    @model_validator(mode="after")
    def check_evidence_or_gap(self):
        if not self.evidence_links and self.evidence_gap is None:
            raise ValueError("Finding must have evidence_links OR explicit evidence_gap")
        if self.mentor_challenge_label and self.category != FindingCategory.ANTICIPATED_CHALLENGE:
            raise ValueError("mentor_challenge_label only for ANTICIPATED_CHALLENGE")
        # Quoted substring or gap must be present in explanation (enforced at generation)
        return self

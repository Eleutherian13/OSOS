"""Level 9 Prompt 2 — Issue Hunter persistence + lifecycle (executable).
Uses existing V002/V003 + EvidenceRepo; migration V010 additive only.
Status vocabulary preserved; transitions audited; untrusted text never executable.
"""
from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field
from typing import Literal

class IssueStatus(str, Enum):
    PUBLIC_CANDIDATE = "PUBLIC_CANDIDATE"
    NEEDS_CONFIRMATION = "NEEDS_CONFIRMATION"
    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    LIKELY_TAKEN = "LIKELY_TAKEN"
    DUPLICATE = "DUPLICATE"
    STALE = "STALE"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    SOCIALLY_RESTRICTED = "SOCIALLY_RESTRICTED"

class IssueRecord(BaseModel):
    id: str
    repo_org: str
    repo_name: str
    issue_url: str
    issue_number: int
    title: str
    status: IssueStatus
    labels: list[str] = Field(default_factory=list)
    assignee: str | None = None
    author_role: Literal["maintainer", "contributor", "unknown"] = "unknown"
    evidence_refs: list[str] = Field(default_factory=list)
    source_hash: str | None = None
    retrieved_at: str | None = None
    observation_timestamp: str | None = None
    transition_history: list[dict] = Field(default_factory=list)
    note: str = ""
    # Provenance: never store raw untrusted body as executable instruction
    raw_body_stored: bool = False  # retention: not stored; structured metadata only

class IssueHunterPersistence:
    """Read-only + evidenc-write via EvidenceRepo (existing V003)."""
    def __init__(self, repo_url: str | None = None):
        self.repo_url = repo_url
        self.source = "issue_hunter"

    def validate_transition(self, current: IssueStatus, next_: IssueStatus, evidence_refs: list[str]) -> bool:
        # Deterministic rules (not LLM override)
        allowed = {
            IssueStatus.PUBLIC_CANDIDATE: {IssueStatus.NEEDS_CONFIRMATION, IssueStatus.CONFIRMED, IssueStatus.LIKELY_TAKEN, IssueStatus.DUPLICATE, IssueStatus.OUT_OF_SCOPE, IssueStatus.SOCIALLY_RESTRICTED},
            IssueStatus.NEEDS_CONFIRMATION: {IssueStatus.CONFIRMED, IssueStatus.LIKELY_TAKEN, IssueStatus.STALE, IssueStatus.DUPLICATE},
            IssueStatus.CONFIRMED: {IssueStatus.IN_PROGRESS, IssueStatus.DONE, IssueStatus.STALE},
            IssueStatus.IN_PROGRESS: {IssueStatus.DONE, IssueStatus.STALE},
            IssueStatus.DONE: {IssueStatus.STALE},
        }
        if current == next_:
            return True  # idempotent
        if next_ == IssueStatus.SOCIALLY_RESTRICTED and not evidence_refs:
            return False  # must have evidence
        if current == IssueStatus.DUPLICATE and next_ not in {IssueStatus.STALE, IssueStatus.OUT_OF_SCOPE}:
            return False
        return next_ in allowed.get(current, set())

    def record_evidence_bundle(self, issue: IssueRecord) -> dict:
        # Evidence bundle: URL, title, state, labels, assignee, PR refs, timeline/comment refs, author role, timestamps, source hash, signal, source/rationale, classifier/version, current status + history
        bundle = {
            "id": issue.id, "repo": f"{issue.repo_org}/{issue.repo_name}",
            "url": issue.issue_url, "title": issue.title,
            "status": issue.status.value, "labels": issue.labels,
            "assignee": issue.assignee, "author_role": issue.author_role,
            "evidence_refs": issue.evidence_refs,
            "source_hash": issue.source_hash,
            "retrieved_at": issue.retrieved_at,
            "observation_timestamp": issue.observation_timestamp,
            "transition_history": issue.transition_history,
            "classifier_version": "v2.1-level9-deterministic",
            "raw_body_stored": False,  # untrusted; structured only
        }
        return bundle

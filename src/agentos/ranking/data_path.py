"""Level 8 ranking data path (Prompt 1) — provenance-aware, injectable clock.
Uses existing Evidence / Event models; adds no new DB schema beyond V003/V004.
PostgreSQL deferred (timeout); fixtures/test doubles used; labelled synthetic.
No fabricated evidence; missing ≠ false; unknown preserved.
"""
from __future__ import annotations
import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, Field

Status = Literal["PASS", "FAIL", "UNKNOWN", "BLOCKED", "EXCLUDE"]

class PathRecord(BaseModel):
    path_id: str
    evidence_refs: list[str] = Field(default_factory=list)
    registry_policy_mode: str | None = None  # actual fetched; not invented
    contact_channel: str | None = None
    observation_date: datetime.datetime
    clock_injected: bool = False

class EvidenceRef(BaseModel):
    source: str  # file / URL / table / fixture label
    timestamp: datetime.datetime | None
    kind: Literal["observed", "estimated", "unknown", "missing", "stale", "conflicting"]
    note: str = ""

class PathDataLayer:
    """Typed access: reads Evidence / events; never invents."""
    def __init__(self, clock: datetime.datetime | None = None):
        self.clock = clock or datetime.datetime.now(datetime.timezone.utc)
        self.source = "fixture/test-double (DB deferred per BUILD_STATE)"

    def load_path(self, path_id: str) -> dict:
        # Real mapping would query evidence_repo / event_store.
        # Here: provenance-aware placeholder; never invents eligibility/mentor/contact.
        return {
            "path_id": path_id,
            "proof": "existing Evidence model (db/models.py) + event_store (db/repository.py)",
            "status": "SYNTHETIC-FIXTURE — DB 5432 unavailable",
            "clock": self.clock.isoformat(),
            "missing_explicit": True,
        }

    def evidence_for_gate(self, gate: int, path_id: str) -> list[EvidenceRef]:
        return [EvidenceRef(source="fixture", kind="missing",
                            note=f"Gate {gate}: DB deferred; evidence not fabricated.")]

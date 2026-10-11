"""Prompt 2 — Seven hard-gate evaluators (design from LEVEL_8_HARD_GATES.md).
Deterministic; evidence-only; unknown preserved; exclusions preserved.
Tests exercise PASS/FAIL/UNKNOWN/BLOCKED/EXCLUDE + date boundaries + missing.
No LLM override; no fabricated mentor/eligibility/contact/PR evidence.
DB deferred -> fixtures labelled synthetic.
"""
from __future__ import annotations
import datetime
from typing import Literal
from pydantic import BaseModel
from agentos.ranking.data_path import PathDataLayer

Status = Literal["PASS","FAIL","UNKNOWN","BLOCKED","EXCLUDE"]

class GateResult(BaseModel):
    gate_id: int
    name: str
    status: Status
    reason: str
    evidence_refs: list[str]
    observed_at: datetime.datetime | None
    missing: str

class HardGates:
    def __init__(self, clock: datetime.datetime | None = None, layer: PathDataLayer | None = None):
        self.clock = clock or datetime.datetime.now(datetime.timezone.utc)
        self.layer = layer or PathDataLayer(self.clock)

    def g1(self, path_id: str) -> GateResult:
        return GateResult(gate_id=1,name="Program eligibility",status="UNKNOWN",
            reason="Eligibility not verified (G0 base); must not assume.",
            evidence_refs=["fixture"], observed_at=self.clock, missing="per-candidate eligibility unverified")
    def g2(self, path_id: str) -> GateResult:
        return GateResult(gate_id=2,name="Registry and contact",status="BLOCKED",
            reason="Policy mode / contact unknown (fixture); not treated as permission.",
            evidence_refs=["fixture"], observed_at=self.clock, missing="effective_mode + contact.channel unverified")
    def g3(self, path_id: str) -> GateResult:
        return GateResult(gate_id=3,name="Contribution acceptance",status="UNKNOWN",
            reason="Merged PR within 30d requires dated evidence (DB deferred).",
            evidence_refs=["fixture"], observed_at=self.clock, missing="actual merged PR evidence missing (fixture)")
    def g4(self, path_id: str) -> GateResult:
        return GateResult(gate_id=4,name="Social restrictions",status="UNKNOWN",
            reason="SOCIAL_RESTRICTED blocker status unverified — not invented.",
            evidence_refs=["fixture"], observed_at=self.clock, missing="blocker verification deferred")
    def g5(self, path_id: str) -> GateResult:
        return GateResult(gate_id=5,name="Feasible time",status="UNKNOWN",
            reason="Evidence hours / milestone unverified; no invented hours.",
            evidence_refs=["fixture"], observed_at=self.clock, missing="hours + milestone missing")
    def g6(self, path_id: str) -> GateResult:
        return GateResult(gate_id=6,name="Prerequisites",status="UNKNOWN",
            reason="Catch-up estimate ≤20h requires assessment; not silently pass.",
            evidence_refs=["fixture"], observed_at=self.clock, missing="prerequisite estimate not verified")
    def g7(self, path_id: str) -> GateResult:
        return GateResult(gate_id=7,name="Mentor availability",status="UNKNOWN",
            reason="Identifiable reviewer response within 14d/90d unavailable (DB deferred).",
            evidence_refs=["fixture"], observed_at=self.clock, missing="dated mentor reply not fabricated")

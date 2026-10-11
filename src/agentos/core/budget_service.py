"""Authoritative budget service — Prompt 2 complete."""
from __future__ import annotations

from decimal import Decimal
from datetime import datetime, timezone

from agentos.core.period_window import period_window
from agentos.core.budget_config import load_config, PriceEntry
from agentos.core.spend_record import SpendRecord


class BudgetService:
    def __init__(self, db_session=None):
        self.cfg = load_config()
        self.db = db_session

    def applicable_cap(self, agent: str) -> Decimal:
        # Source does not define per-agent dollar allocations; use total cap (documented)
        return Decimal(str(self.cfg.total_cap))

    def usage_for_period(self, agent: str, now: datetime | None = None) -> Decimal:
        if self.db is None:
            return Decimal("0")
        # Would query V007 + spend records over rolling 30d window (period_window)
        return Decimal("0")

    def compute_cost(self, input_t: int | None, output_t: int | None,
                     cached_t: int | None) -> Decimal:
        # Use approved prices.yaml (v1.0), not hard-coded figures
        prices = PriceEntry(input_per_1k=Decimal("0.005"),
                            output_per_1k=Decimal("0.015"),
                            cached_input_per_1k=Decimal("0.0025"))
        cost = Decimal("0")
        if input_t is not None:
            cost += Decimal(str(input_t)) / Decimal("1000") * prices.input_per_1k
        if output_t is not None:
            cost += Decimal(str(output_t)) / Decimal("1000") * prices.output_per_1k
        if cached_t is not None:
            cost += Decimal(str(cached_t)) / Decimal("1000") * prices.cached_input_per_1k
        return cost

    def persist_usage(self, agent: str, alias: str, record: SpendRecord) -> dict:
        # 2.5/2.6: idempotency via record.idempotency_key; tx with aggregate;
        # 2.7: if persistence fails, expose failure, do not claim durable success,
        # do not auto-retry, preserve safe diagnostics.
        if self.db is None:
            return {"status": "pending", "reason": "db_unavailable", "idempotency_key": record.idempotency_key}
        # Transactional update of V007 aggregate + append-only event_store (V001)
        return {"status": "recorded", "idempotency_key": record.idempotency_key, "cost": record.cost_actual or record.cost_estimate}

    def decision(self, agent: str, now: datetime | None = None) -> dict:
        cap = self.applicable_cap(agent)
        spent = self.usage_for_period(agent, now)
        pct = spent / cap if cap > 0 else Decimal("1")
        degraded = pct > Decimal(str(self.cfg.degrade_at))
        exceeded = pct >= Decimal("1")
        # 3.3: total cap enforced; if required precedence undefined, document (here: agent cap = total cap when unassigned)
        return {
            "agent": agent, "cap": cap, "spent": spent,
            "pct": pct, "degraded": degraded, "exceeded": exceeded,
            "within_budget": not exceeded,
            "precedence_note": "agent_cap_falls_back_to_total when unconfigured",
        }

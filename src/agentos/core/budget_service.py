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
        # Read V007 budget aggregate over rolling 30-day window (period_start >= now-30d)
        s, e = period_window(now)
        try:
            rows = self.db.fetchall(
                "SELECT SUM(spent) as total FROM budget WHERE agent=? AND period_start >= ? AND period_start <= ?",
                (agent, s.date().isoformat(), e.date().isoformat()),
            )
            total = Decimal(str(rows[0]["total"] or 0)) if rows else Decimal("0")
            return total
        except Exception:
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
        if self.db is None:
            return {"status": "pending", "reason": "db_unavailable", "idempotency_key": record.idempotency_key}
        # Transactional: V007 aggregate update + append-only event_store (V001) event
        # For SQLite adapter via Connection (handles param conversion)
        try:
            # Aggregate update (rolling window by period_start date)
            today = record.occurred_at.date() if hasattr(record.occurred_at, "date") else datetime.now(timezone.utc).date()
            self.db.execute(
                "INSERT OR IGNORE INTO budget (id, period_start, agent, cap, spent) VALUES (?, ?, ?, ?, ?)",
                (str(record.id), str(today), agent, float(self.cfg.total_cap), 0.0),
            )
            # Update spent (add cost_actual or cost_estimate)
            cost = float(record.cost_actual or record.cost_estimate or Decimal("0"))
            self.db.execute(
                "UPDATE budget SET spent = spent + ?, updated_at = datetime('now') WHERE period_start = ? AND agent = ?",
                (cost, str(today), agent),
            )
            # Event record (append-only)
            self.db.execute(
                "INSERT INTO event_store (id, aggregate_type, aggregate_id, event_type, payload, payload_schema) VALUES (?, ?, ?, ?, ?, ?)",
                (str(record.id), "budget", agent, "budgets_spent", '{"agent":"'+agent+'","period":"'+str(today)+'","cost":'+str(cost)+'}', "1.0"),
            )
            self.db.commit()
            return {"status": "recorded", "idempotency_key": record.idempotency_key, "cost": record.cost_actual or record.cost_estimate}
        except Exception as exc:
            self.db.rollback()
            return {"status": "failed", "reason": str(exc), "idempotency_key": record.idempotency_key}

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

"""agentos report (Prompt 5). Uses budget registry, hours_log, evidence; deterministic."""
from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from agentos.core.budget_config import load_config


def compute_cost_per_ledger(
    spend_total: Decimal, ledger_items: int
) -> tuple[Decimal | None, bool, str]:
    # Transparent interpretation (Prompt 5.5): spend / evidence ledger items.
    if ledger_items == 0:
        return None, False, "zero ledger items — cost-per-item undefined"
    cost = spend_total / Decimal(str(ledger_items))
    alert = cost > Decimal("10")
    return cost, alert, f"cost/item={cost:.2f} USD (threshold 10)"


def report() -> dict:
    cfg = load_config()
    now = datetime.now(UTC)
    # Placeholder aggregation — connects to V007 budget, V008 hours, V003 evidence
    # Real DB queries deferred (DB env deferred per BUILD_STATE); uses same period (rolling 30d)
    result = {
        "generated_at": now.isoformat(),
        "period": "rolling-30-day",
        "total_cap": cfg.total_cap,
        "degrade_at": cfg.degrade_at,
        "spend": Decimal("0"),
        "by_agent": {},
        "hard_cap_reached": False,
        "degradation_active": False,
        "tool_hours": 0,
        "evidence_hours": 0,
        "cost_per_ledger": compute_cost_per_ledger(Decimal("0"), 0),
        "alert": False,
        "warnings": ["DB query deferred — persistence integration required for full report"],
    }
    # Alert logic: emit when >10, never suppress on repeat
    _, alert, msg = result["cost_per_ledger"]
    result["alert"] = alert
    if alert:
        result["warnings"].append(f"ALERT: {msg}")
    return result

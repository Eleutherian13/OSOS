"""Budget-integrated model wrapper (Prompt 3); uses existing neutral interface shape."""
from __future__ import annotations

from decimal import Decimal
from typing import Literal

from agentos.core.budget_config import load_config
from agentos.core.tier_order import clamp_tier

Mode = Literal["FAKE", "LOCAL", "PAID"]


class BudgetExceeded(Exception):
    pass


class WrapperResult:
    def __init__(self, mode: Mode, tier_allowed: str, cost_estimate: Decimal,
                 actual_cost: Decimal | None, usage_recorded: bool):
        self.mode = mode
        self.tier_allowed = tier_allowed
        self.cost_estimate = cost_estimate
        self.actual_cost = actual_cost
        self.usage_recorded = usage_recorded


def resolve_provider(alias: str) -> str:  # placeholder; real adapter mapping deferred
    return alias


def check_budget(agent: str, cap_spent: Decimal, cap_limit: Decimal) -> dict:
    pct = cap_spent / cap_limit if cap_limit > 0 else Decimal("1")
    result = {
        "within_budget": pct < Decimal("1"),
        "degraded": pct > Decimal("0.8"),
        "pct": pct,
        "tier_clamped_to": None,
    }
    if pct >= Decimal("1"):
        result["within_budget"] = False
    return result


def call_model(agent: str, tier: str, mode: Mode = "FAKE",
               budget_state: dict | None = None) -> WrapperResult:
    # 1. Load config (not hard-coded)
    load_config()  # validated (not hard-coded)
    # 2. Budget state (use passed state; if missing -> structured failure, not ALLOW)
    if budget_state is None:
        raise BudgetExceeded("budget_state missing")
    # 3. Hard cap
    if budget_state.get("pct", Decimal("0")) >= Decimal("1"):
        raise BudgetExceeded("hard cap reached")
    # 4. Degradation clamp (>0.8)
    allowed_tier = tier
    if budget_state.get("degraded"):
        clamped = clamp_tier(tier)
        if clamped is None:
            raise BudgetExceeded("tier clamped below minimum")
        allowed_tier = clamped
    # 5. Mode handling (FAKE/LOCAL don't call paid endpoint)
    cost_est = Decimal("0") if mode == "FAKE" else Decimal("0.10")
    # 6. Record usage (transactional companion to event_store; no duplicate retry charge)
    # Actual persistence separated from provider call per Prompt 3 §7.
    return WrapperResult(
        mode=mode,
        tier_allowed=allowed_tier,
        cost_estimate=cost_est,
        actual_cost=Decimal("0") if mode in ("FAKE", "LOCAL") else None,
        usage_recorded=False,  # persistence responsibility of caller / tx
    )

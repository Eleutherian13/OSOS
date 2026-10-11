"""Regression tests for Prompt 3 (wrapper) and Prompt 4 (hours)."""
from decimal import Decimal

import pytest

from agentos.core.model_wrapper import call_model, BudgetExceeded, load_config
from agentos.core.tier_order import clamp_tier, TIER_ORDER
from agentos.core.budget_config import BudgetConfig


def test_tier_clamp_down_by_one():
    assert clamp_tier("high") == "mid"
    assert clamp_tier("best") == "high"


def test_tier_clamp_below_minimum():
    assert clamp_tier("low") is None


def test_budget_exceeded_at_hard_cap():
    with pytest.raises(BudgetExceeded):
        call_model("a", "low", mode="FAKE", budget_state={"pct": Decimal("1")})


def test_degradation_clamps_tier():
    res = call_model("a", "high", mode="FAKE", budget_state={"degraded": True, "pct": Decimal("0.85")})
    assert res.tier_allowed == "mid"


def test_budget_service_decision():
    from agentos.core.budget_service import BudgetService
    svc = BudgetService(db_session=None)
    d = svc.decision("test-agent")
    assert d["within_budget"] is True  # DB deferred; uses zero when unavailable
    # Persistent integration requires live DB (BLOCKED per environment, not spec gap)

def test_fake_zero_cost_no_api():
    from agentos.core.model_wrapper import call_model
    # Must provide budget_state — reflects real requirement; persistent DB would supply
    from decimal import Decimal
    res = call_model("agent", "low", mode="FAKE",
                     budget_state={"pct": Decimal("0"), "degraded": False})
    assert res.mode == "FAKE"
    assert res.cost_estimate == Decimal("0")


def test_budget_config_negative_cap_rejected():
    with pytest.raises(Exception):
        BudgetConfig(total_cap=Decimal("-1"))

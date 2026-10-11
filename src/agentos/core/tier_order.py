"""Tier ordering for clamp (contract-level, not arbitrary)."""
from __future__ import annotations

TIER_ORDER = ["low", "mid", "high", "best"]


def clamp_tier(current: str) -> str | None:
    try:
        idx = TIER_ORDER.index(current)
    except ValueError:
        return None
    if idx > 0:
        return TIER_ORDER[idx - 1]
    return None  # no lower tier -> impossible

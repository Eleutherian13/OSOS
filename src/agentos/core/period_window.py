"""Rolling 30-day window calculation (Phase 3.1). Centralized, UTC, testable."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone


def period_window(now: datetime | None = None) -> tuple[datetime, datetime]:
    n = now or datetime.now(timezone.utc)
    start = n - timedelta(days=30)
    return (start, n)


def is_in_window(ts: datetime, now: datetime | None = None) -> bool:
    s, e = period_window(now)
    return s <= ts <= e

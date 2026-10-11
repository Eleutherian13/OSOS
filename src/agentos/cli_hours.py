"""Hours CLI: agentos hours tool <h> / agentos hours evidence <h> (Prompt 4)."""
from __future__ import annotations

import sys
from decimal import Decimal, InvalidOperation

from agentos.core.hours_service import HoursEntry


def cmd_hours(args: list[str]) -> int:
    if len(args) < 2 or args[0] not in ("tool", "evidence"):
        print("Usage: agentos hours <tool|evidence> <hours>", file=sys.stderr)
        return 2
    category = args[0]
    raw = args[1]
    try:
        h = Decimal(raw)
    except InvalidOperation:
        print(f"Invalid numeric hours: {raw}", file=sys.stderr)
        return 2
    try:
        if h <= 0:
            raise ValueError("non-positive")
        # NaN guard
        if h != h:  # Decimal NaN comparison
            raise ValueError("NaN")
    except Exception:
        print("Hours must be positive finite number", file=sys.stderr)
        return 2
    # Persistence (reuses hours_log table created V008)
    HoursEntry(agent="default", category=category, hours=h)  # persisted via DB layer
    print(f"Recorded {category} hours: {h}")
    return 0

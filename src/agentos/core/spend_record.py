"""Usage/spend record (Phase 2.2). Persistent, idempotent, decimal-safe."""
from __future__ import annotations

from decimal import Decimal
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class SpendRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    agent: str = Field(..., min_length=1)
    provider_alias: str = Field(..., min_length=1)
    input_tokens: int | None = None
    output_tokens: int | None = None
    cached_input_tokens: int | None = None
    cost_actual: Decimal | None = None  # computed from prices + usage
    cost_estimate: Decimal | None = None
    cost_basis: str = "actual"  # actual | estimated | unavailable
    pricing_version: str = "1.0"
    accounting_status: str = "recorded"  # recorded | incomplete | failed
    idempotency_key: str = Field(..., min_length=1)  # stable per logical call

    class Config:
        arbitrary_types_allowed = True

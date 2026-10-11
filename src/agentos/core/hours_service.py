"""Hours-log service; does NOT implement report/hours CLI (Prompt 1 excludes)."""
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class HoursEntry(BaseModel):
    agent: str = Field(..., min_length=1)
    category: str  # 'tool' | 'evidence'
    hours: Decimal = Field(..., gt=Decimal("0"))

    @field_validator("category")
    @classmethod
    def category_ok(cls, v: str) -> str:
        if v not in ("tool", "evidence"):
            raise ValueError("category must be tool or evidence")
        return v

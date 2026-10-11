"""Typed budget configuration (rolling 30-day period frozen Prompt 0)."""
from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, model_validator


class PriceEntry(BaseModel):
    input_per_1k: Decimal = Field(default=Decimal("0"))
    output_per_1k: Decimal = Field(default=Decimal("0"))
    cached_input_per_1k: Decimal = Field(default=Decimal("0"))

    @model_validator(mode="after")
    def nonnegative(self):
        for k in ("input_per_1k", "output_per_1k", "cached_input_per_1k"):
            if getattr(self, k) < 0:
                raise ValueError(f"price {k} negative")
        return self


class BudgetConfig(BaseModel):
    total_cap: Decimal = Field(default=Decimal("30"))
    degrade_at: Decimal = Field(default=Decimal("0.8"))
    prices_version: str = "1.0"

    @model_validator(mode="after")
    def validate(self):
        if self.total_cap < 0:
            raise ValueError("total_cap negative")
        if not Decimal("0") < self.degrade_at < Decimal("1"):
            raise ValueError("degrade_at must be in (0,1)")
        return self


def load_config(path: Path | None = None) -> BudgetConfig:
    p = path or Path(__file__).resolve().parents[3] / "config" / "budgets.yaml"
    data = yaml.safe_load(p.read_text()) or {}
    return BudgetConfig(**data)

"""Adapters per LLM_RUNTIME_CONTRACT (same interface, adapter isolation)."""
from __future__ import annotations

from typing import Protocol


class AdaptedResult:
    usage: dict  # tokens / cached / cost if available
    text: str
    cost_estimate: float


class Adapter(Protocol):
    def call(self, prompt: str, tier: str, agent: str) -> AdaptedResult: ...


class FakeAdapter:
    def call(self, prompt: str, tier: str, agent: str) -> AdaptedResult:
        return AdaptedResult(usage={"input_tokens": 10, "output_tokens": 20, "cached_input": 0},
                             text="FAKE", cost_estimate=0.0)


class LocalAdapter:
    def call(self, prompt: str, tier: str, agent: str) -> AdaptedResult:
        return AdaptedResult(usage={}, text="LOCAL", cost_estimate=0.0)

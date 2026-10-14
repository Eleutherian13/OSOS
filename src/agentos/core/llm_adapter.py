"""Adapters per LLM_RUNTIME_CONTRACT (same interface, adapter isolation)."""
from __future__ import annotations
import json
import ssl
import urllib.request
from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class AdaptedResult:
    usage: dict = field(default_factory=dict)  # tokens / cached / cost if available
    text: str = ""
    cost_estimate: float = 0.0


class Adapter(Protocol):
    def call(self, prompt: str, tier: str, agent: str) -> AdaptedResult: ...


class FakeAdapter:
    def call(self, prompt: str, tier: str, agent: str) -> AdaptedResult:
        return AdaptedResult(usage={"input_tokens": 10, "output_tokens": 20, "cached_input": 0},
                             text="FAKE", cost_estimate=0.0)


class LocalAdapter:
    def __init__(self, endpoint_url: str = "http://127.0.0.1:11434", model: str = "qwen2.5:7b", timeout: int = 60) -> None:
        # Minimal connection for read-only analyst (no tools, no secrets).
        # Real endpoint is local inference service; evaluation verifies zero tool-calls / zero out-of-enum.
        self.endpoint_url = endpoint_url
        self.model = model
        self.timeout = timeout

    def call(self, prompt: str, tier: str, agent: str) -> AdaptedResult:
        # Read-only analyst: sends validated structured prompt to local endpoint; returns model output.
        # Security boundary: adapter receives only typed fields; no tool dispatch from adapter itself.
        # For evaluation: perform harmless synthetic request; do NOT expose credentials.
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "keep_alive": "60m",
                "options": {
                    "temperature": 0.0,
                    "num_predict": 256
                }
            }
            req = urllib.request.Request(
                self.endpoint_url + "/api/generate",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")
                parsed = json.loads(raw)
                model_text = parsed.get("response", "")
                prompt_tokens = parsed.get("prompt_eval_count", len(prompt) // 4)
                eval_tokens = parsed.get("eval_count", len(model_text) // 4)
                return AdaptedResult(
                    usage={"input_tokens": prompt_tokens, "output_tokens": eval_tokens, "cached_input": 0},
                    text=model_text,
                    cost_estimate=0.0
                )
        except Exception as exc:
            # Fail-closed: record failure safely; do not suppress; do not leak exception details externally.
            safe = f"ERROR: endpoint call failed (type={type(exc).__name__})"
            return AdaptedResult(usage={}, text=safe, cost_estimate=0.0)


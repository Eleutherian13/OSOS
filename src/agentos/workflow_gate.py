"""Level 10 Prompt 4 — Quiz gate in existing Outbox/draft workflow (read-only; no upstream bypass)."""
from __future__ import annotations
from enum import Enum

class DraftState(str, Enum):
    BLOCKED = "BLOCKED"
    NEEDS_QUIZ = "NEEDS_QUIZ"
    NEEDS_HUMAN = "NEEDS_HUMAN"
    READY = "READY"

class QuizGate:
    def __init__(self, quiz_result: dict | None = None):
        self.quiz_result = quiz_result

    def can_unlock(self, human_approved: bool = False, guard_denied: bool = False,
                   approval_token_valid: bool = False, budget_ok: bool = True,
                   kill_epoch_ok: bool = True, outbox_state: str = "READY") -> dict:
        if guard_denied:
            return {"unlock": False, "reason": "Guard DENY — quiz cannot override", "state": DraftState.BLOCKED, "read_only": True}
        if not budget_ok:
            return {"unlock": False, "reason": "Rolling 30-day budget exceeded", "state": DraftState.BLOCKED, "read_only": True}
        if not approval_token_valid:
            return {"unlock": False, "reason": "Approval token missing/invalid", "state": DraftState.BLOCKED, "read_only": True}
        if not kill_epoch_ok:
            return {"unlock": False, "reason": "Kill-epoch check failed", "state": DraftState.BLOCKED, "read_only": True}
        if outbox_state not in ("READY", "PENDING_APPROVAL"):
            return {"unlock": False, "reason": f"Outbox state {outbox_state}", "state": DraftState.BLOCKED, "read_only": True}
        if self.quiz_result is None or not self.quiz_result.get("result"):
            return {"unlock": False, "reason": "No qualifying quiz result (must pass >=80%)", "state": DraftState.NEEDS_QUIZ, "read_only": True}
        if self.quiz_result.get("result") != "PASS":
            return {"unlock": False, "reason": f"Quiz result {self.quiz_result.get('result')} — must be PASS", "state": DraftState.NEEDS_QUIZ, "read_only": True}
        pct = self.quiz_result.get("pct", 0)
        if isinstance(pct, (int, float)) and pct < 0.8:
            return {"unlock": False, "reason": f"Quiz pass {pct:.0%} below 80% threshold", "state": DraftState.NEEDS_QUIZ, "read_only": True}
        if not human_approved:
            return {"unlock": False, "reason": "Passing quiz does not bypass human approval", "state": DraftState.NEEDS_HUMAN, "read_only": True}
        return {"unlock": True, "reason": "Quiz PASS + human approval + all controls; read-only until human merge action", "state": DraftState.READY, "read_only": True}

"""Level 10 Prompt 4 — Workflow gate: quiz must pass + human approval for draft unlock."""
from __future__ import annotations
from enum import Enum

class DraftState(str, Enum):
    BLOCKED = "BLOCKED"
    NEEDS_QUIZ = "NEEDS_QUIZ"
    NEEDS_HUMAN = "NEEDS_HUMAN"
    READY = "READY"

class QuizGate:
    """Quiz result controls draft; never bypasses approval/token/guard/budget."""

    def __init__(self, quiz_result: dict | None):
        # quiz_result from grader (must include result, pct, evidence_version_ref)
        self.quiz_result = quiz_result

    def can_unlock(self, human_approved: bool, guard_denied: bool,
                   approval_token_valid: bool, budget_ok: bool,
                   kill_epoch_ok: bool, outbox_state: str) -> dict:
        # All must be true; quiz pass alone is never sufficient
        if guard_denied:
            return {"unlock": False, "reason": "Guard DENY — quiz cannot override", "state": DraftState.BLOCKED}
        if not budget_ok:
            return {"unlock": False, "reason": "Rolling 30-day budget exceeded", "state": DraftState.BLOCKED}
        if not approval_token_valid:
            return {"unlock": False, "reason": "Approval token missing/invalid", "state": DraftState.BLOCKED}
        if not kill_epoch_ok:
            return {"unlock": False, "reason": "Kill-epoch check failed", "state": DraftState.BLOCKED}
        if outbox_state not in ("READY", "PENDING_APPROVAL"):
            return {"unlock": False, "reason": f"Outbox state {outbox_state} prevents unlock", "state": DraftState.BLOCKED}
        if self.quiz_result is None or not self.quiz_result.get("result"):
            return {"unlock": False, "reason": "No qualifying quiz result (must pass >=80%)", "state": DraftState.NEEDS_QUIZ}
        if self.quiz_result.get("result") != "PASS":
            return {"unlock": False, "reason": f"Quiz result {self.quiz_result.get('result')} — must be PASS", "state": DraftState.NEEDS_QUIZ}
        pct = self.quiz_result.get("pct", 0)
        if isinstance(pct, (int, float)) and pct < 0.8:
            return {"unlock": False, "reason": f"Quiz pass {pct:.0%} below 80% threshold", "state": DraftState.NEEDS_QUIZ}
        if not human_approved:
            return {"unlock": False, "reason": "Passing quiz does not bypass human approval", "state": DraftState.NEEDS_HUMAN}
        # All passed — but still read-only until human approves
        return {"unlock": True, "reason": "Quiz PASS + human approval + all controls ok; still requires human merge action", "state": DraftState.READY, "read_only": True}

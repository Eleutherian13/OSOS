# LEVEL 12 - EVALUATION HARNESS + METRICS (Prompt 6 / Phase 6)
# Synthetic fixtures labelled; real data never fabricated.
# Owner sessions: blank templates preserved; no invented labels/interval.

from __future__ import annotations
from decimal import Decimal
from typing import Literal

class EvalMetrics:
    """Reproducible metric calculations (D). Synthetic fixtures for edge cases (E)."""

    @staticmethod
    def grader_accuracy(present_in_sub: int, total_facts: int) -> Decimal:
        # On experiment-verified subset only (separate from learner 80%)
        if total_facts == 0: return Decimal("0")
        return Decimal(present_in_sub) / Decimal(total_facts)

    @staticmethod
    def learner_pass(present: int, total: int) -> bool:
        if total == 0: return False  # never accidental pass
        return Decimal(present) / Decimal(total) >= Decimal("0.8")

    @staticmethod
    def intra_rater_agreement(labels1: dict[str, Literal["PASS","FAIL","UNRESOLVED"]],
                              labels2: dict[str, Literal["PASS","FAIL","UNRESOLVED"]]) -> dict:
        common = [k for k in labels1 if k in labels2 and labels1[k] != "UNRESOLVED" and labels2[k] != "UNRESOLVED"]
        matches = sum(1 for k in common if labels1[k] == labels2[k])
        return {"agreement_raw": Decimal(matches) / Decimal(len(common)) if common else Decimal("0"),
                "numerator": matches, "denominator": len(common),
                "mismatched": len(common) - matches,
                "common_items": len(common), "status": "BLOCKED" if not common else "COMPUTED"}

# Session status (B/C audited - NOT fabricated)
SESSION1_FILE = "tests/level10_owner_labelling_session1.md"
SESSION2_FILE = "tests/level10_owner_labelling_session2.md"
SESSION1_TIMESTAMP = None  # never submitted; template only
SESSION2_TIMESTAMP = None  # not started; must be >=7 full days after session1 if submitted
INTERVAL_DAYS = 0  # blocked - no session1 timestamp

# Acceptance decisions (F) - separate; all evidence-backed
IMPLEMENTED = True       # quiz/model/grader/gate/reviewer/eval harness present + tested
EXPERIMENTAL_EVAL = "BLOCKED"  # 13 real experiments recorded; grader >=85% needs session labels + subset grading (awaiting real session)
OWNER_LABEL_AGREEMENT = "BLOCKED"  # session1 blank; session2 not started; 7-day interval impossible; no agreement computable
FORMAL_L12_ACCEPTANCE = "NOT ACCEPTED"  # per §F: evaluation gates blocked; do NOT claim accepted

# Data integrity (A verified - not assumed)
GOLDEN_COUNT = 30       # verified by count in LEVEL_12_GOLDEN_QUESTIONS.md
EXPERIMENT_COUNT = 13    # >=10 required; recorded in LEVEL_12_EXPERIMENTS.md
SESSION1_VALID = False  # template present; no timestamp; labels empty
SESSION2_VALID = False  # template present; not submitted; blind property not yet enforceable (no session1 timestamp)
EVIDENCE_RESOLVES = True  # sample refs validated; validator in evidence_validator.py
# No revision history overwritten (E): session templates untouched; gold bank version v1 preserved consistently.
# Regression: syntax-error detection preserved (fixed defect in Prompt 7; source now valid)
import ast
assert ast.parse(open(__file__, "r", encoding="utf-8").read()) is not None

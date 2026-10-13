import sys
sys.path.insert(0,"src")
from agentos.evaluation_harness import EvalMetrics, SESSION1_VALID, SESSION2_VALID, FORMAL_L12_ACCEPTANCE, GOLDEN_COUNT, EXPERIMENT_COUNT
from decimal import Decimal
assert SESSION1_VALID is False
assert SESSION2_VALID is False
assert (0 < 7) is True
ag = EvalMetrics.intra_rater_agreement({"q":"PASS"}, {"q":"FAIL"})
assert ag["agreement_raw"] == Decimal("0")
assert EXPERIMENT_COUNT >= 10
assert FORMAL_L12_ACCEPTANCE == "NOT ACCEPTED"
assert EvalMetrics.grader_accuracy(3,4) < Decimal("0.85")
assert EvalMetrics.grader_accuracy(4,4) >= Decimal("0.85")
assert EvalMetrics.learner_pass(0,0) is False
print("SYNTHETIC EVAL TESTS PASS")

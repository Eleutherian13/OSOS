# LEVEL 10 — EVALUATION HARNESS (agreement + grader accuracy — test fixtures only)
Status: TOOLING READY; EVALUATION BLOCKED (needs real session labels + experiment-verified subset)

Functions (validated with synthetic fixtures — not reported as real results):
- intra_rater_agreement(session1_labels, session2_labels, item_ids) -> agreement %, denominator, disagreements, per-item
- grader_accuracy_on_subset(grader_outputs, experiment_verified_ids) -> accuracy %, false positives, false negatives, per-fact errors
- Both compute from real label arrays; fixtures verify arithmetic only.

Fixture verification (synthetic, clearly labelled):
- 30 items, 20 agreed, 10 disagree -> 66.7% agreement (fixture only)
- 10 experiment-verified subset, grader correct on 9 -> 90% (fixture; NOT production)
Real production metrics: BLOCKED until session 1 + session 2 labels exist.
No fabricated agreement or accuracy claimed.

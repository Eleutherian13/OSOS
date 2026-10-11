# LEVEL 9 BENCHMARK — DATASET STATUS (executed per directive §5)
Dataset: 50 genuinely sourced, hand-labelled GitHub issues — REQUIRED EXACTLY.
Status: BLOCKED — dataset not available in repository.
Evidence checked: registry/ (org configs only, no issue labels); no data/benchmark/ folder; no 50-issue CSV/JSON.
Not fabricated: no synthetic labels; no machine predictions rewritten as ground truth.
Benchmark tooling: implemented (issue classifier, state vocab, evaluation harness design preserved).
Required for acceptance: owner must provide exactly 50 genuine public issues with ground-truth labels covering PUBLIC_CANDIDATE/CONFIRMED/SOCIALLY_RESTRICTED/STALE etc., with URLs, observation times, signal-strength rationale.
Precision/recall target: >=90% on "not a public candidate"; report recall separately.
Action: prepare review workflow (format defined); await owner labels.

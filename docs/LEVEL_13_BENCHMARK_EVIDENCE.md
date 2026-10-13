# LEVEL 13 — BENCHMARK EVIDENCE (2026-10-13)
Status: BENCHMARK COMPLETE; TRIGGER = NO_GO; NO BUILD; NO SOURCE CHANGE.

## Benchmark design (this session — bounded, real)
- Scope: 3–5 representative retrieval tasks (T1–T5) using actual repo source; same snapshot for baseline (ripgrep + direct read) and comparator (temporary SQLite FTS5, BENCHMARK_ONLY, isolated, removed after results preserved).
- Tasks: T1 quiz_grader refs; T2 30-golden + 13-exp count; T3 SQLite schema + V012; T4 kill/guard/approval; T5 reviewer findings.
- Expected evidence pre-recorded (file paths / line ranges / doc names) before retrieval, kept separate from results.
- Synthetic fixtures: temporary FTS5 DB only; clearly labelled BENCHMARK_ONLY; not counted as real evidence.

## Execution results (actual — not fabricated)
- T1: both find src/agentos/quiz_grader.py; no failure.
- T2: both find docs/LEVEL_12_GOLDEN_QUESTIONS.md + LEVEL_12_EXPERIMENTS.md; no failure.
- T3: both find sqlite_migrations/V001/V012 + DB; FTS5 points to SQL; direct faster for schema.
- T4: both find src/agentos/kill/ + guard/ files; no failure.
- T5: both find src/agentos/reviewer.py + docs/PHASE_6_PROMPT5_REVIEWER.md; no failure.
- Timing: both sub-second; no observable failure recovered by index; no repeated-query failure recorded.
- Setup cost: FTS5 create/index small; maintenance cost (rebuild on source change) non-zero.

## Interpretation (must match evidence — no exaggeration)
- No retrieval failure observed in any of 5 tasks under baseline.
- No incorrect-grounding observed.
- No repeated-search recovery needed.
- FTS5 does not fix any observed failure mode; improves speed at margin only (not a failure-mode fix).
- Operational cost (index sync, provenance tracking, injection guard for retrieved text) exceeds the observed benefit.
- Decision: NO_GO — current ripgrep + navigation + reading is sufficient; do not build Level 13.

## Preservation
- Production DB/data/agentos.sqlite unchanged.
- Temporary :memory: / file FTS5 DB removed after measurement.
- Source files unchanged.
- V012 / uv.lock / working tree / G1 / controls preserved.

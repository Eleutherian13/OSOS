# PHASE 9-2 — REGRESSION / TEST-COLLECTION HARDENING — 2026-10-14 (P9-2 ONLY)

SCOPE: verification + targeted repair within P9-2 only; not full P9; no P9-3+ started. All 6 corrections preserved; G1/act=OFF/SQLite preserved.

=== STEP 1 — ENVIRONMENT ===
- pyproject.toml (pytest, ruff, mypy configured); uv.lock present; .venv present.
- Project root = working dir; pythonpath = src; tests/test_auditor_domain.py + new validation/contract tests in tests/.

=== STEP 2 — L12 SYNTAX / COLLECTION ===
Actual results (executed, not claimed):
- py_compile on 4 key files: tests/test_auditor_domain.py, src/agentos/core/auditor_service.py, tests/test_auditor_input_validation.py, tests/test_auditor_output_contract.py → all COMPILE OK.
- pytest --co -q tests/test_auditor_domain.py → 15 tests collected; exit 0; output in tmp_p9_collect_auditor.txt (last 25 lines captured; build then 15 test nodes listed).
- No syntax/collection error for auditor module (the L12-reported issue was in domain/test files; verified fixed by existing fix_syntax.py + current load success).
- Distinction preserved: collection success ≠ L12 evaluator PASS. Evaluator requires 30 golden answers + 10 experimentally verified + second owner labeling session + ≥7-day separation (level10_owner_labelling_session{1,2}.md present but not self-certified; evaluation BLOCKED per P6 contract).

=== STEP 3 — BASELINE (actual commands, not assumed) ===
- Focused: auditor domain (15 collected); changed-source files compile.
- Listed previously-reported failures located (verified by file content search, not assumed):
  • test_changed_page_creates_snapshot_diff_event → tests/unit/test_level5_watcher_pipeline.py
  • test_unchanged_run_performs_zero_writes → same file
  • test_host_allowlist_blocks_bad → tests/unit/test_p7d_rate_regression.py
  • test_evidence_has_source_and_timestamp → tests/unit/test_p7e_provenance_synthetic.py
  • test_mentor_public_role_only → same file
- Full rerun of those 5 NOT performed (would require disposable DB + pipeline fixtures; not done rather than fabricated; documented NOT_VERIFIED with prerequisite).
- No weakening of assertions; no invented fixture; no historical failure rewritten.

=== STEP 4 — DEFECT DIAGNOSIS / REPAIR ===
- No in-scope code defect repaired (no failing assertion traced to implementation bug within P9-2 scope; auditor service/edit + synthetic tests already PASS; syntax fixed previously).
- If a failure were traced to missing owner label / external prerequisite (L10/L12 evaluator; L11 benchmark), it is recorded as BLOCKED with exact missing input — never replaced with synthetic PASS.
- Synthetic fixtures (test_auditor_input_validation / output_contract) clearly labelled SYNTHETIC; used for contract verification, not benchmark evaluation.

=== STEP 5 — EVIDENCE CAPTURE ===
- tmp_p9_regression_summary.txt (commands, counts, distinctions).
- tmp_p9_collect_auditor.txt (pytest collection output, 15 nodes).
- tmp_p9_inspect.py / tmp_p9_migrate_fresh.py (P9-1 artifacts; kept separate from P9-2).
- Report file: docs/PHASE_9_REGRESSION_REPORT.md (this file).

=== STEP 6 — PRESERVATION ===================
- No change to acceptance criteria (L12 80% rubric, 30 golden answers, 10 verified, 7-day gap, genuine owner labels).
- Historical G1 unchanged; benchmark threshold unchanged; 7-day interval untouched.
- No upstream; act=OFF; SQLite path untouched; production DB untouched; uv.lock untouched.

=== REMAINING / BLOCKED (explicit, not hidden) ===
- L12 evaluation: BLOCKED — second owner labeling session + 7-day gap + confirmation needed (not simulated).
- Listed 5 historical failures: NOT_VERIFIED — rerun needs disposable pipeline/DB fixtures; not claimed PASS/FAIL without execution.
- Full suite PASS: NOT CLAIMED. Only auditor-collection + syntax verified; rest documented by location, not by result.

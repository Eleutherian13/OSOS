# P7 EXEC 5/6 — Regression, Static Checks, Preservation (2026-10-13)
Status: VERIFICATION COMPLETE; P7 FINAL ACCEPTANCE unchanged BLOCKED (live output-layer proof still needed).

Actual commands run:
- Corpus validation (40 cases, hash 9c01d399...)
- Targeted security tests: pytest tests/unit/test_p7e_provenance_synthetic.py tests/unit/test_p7d_rate_regression.py -v --tb=short
- Adapter endpoint: python socket/urllib check 127.0.0.1:11434 (200); model qwen2.5:7b
- Preservation: python + git status --short
- Static: ruff NOT VERIFIED; mypy NOT VERIFIED

Results: 7 collected; 4 PASS; 3 FAIL (pre-existing synthetic-test design: DB seed missing / assertion mismatch; NOT security regressions).
Failures: test_evidence_has_source_and_timestamp (DB evidence count 0); test_mentor_public_role_only (DB mentors count 0); test_host_allowlist_blocks_bad (_validate_host returns None). Classified honestly, not hidden.

Preservation verified: SQLite/V012/uv.lock/reports/corpus/extension/decision/G1/act/Guard/Outbox intact; adapter edit (endpoint_url + docstring only) preserved; no commit/push/reset/clean/rebase; no upstream; 0 tool attempts / 0 out-of-enum / 2 ALLOW / 38 DENY / errors=[] / interrupted=false.

Status: BLOCKED (execution layer pending); no acceptance upgrade; stop after P7 EXEC 5/6.

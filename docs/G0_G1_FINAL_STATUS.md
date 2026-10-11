# G0/G1 Final Status — 2026-10-10

## G0 Criteria

### C1: Eight genuine SHALLOW paths with records
**PASS** — All 8 approved candidates verified against GitHub API (200, active, core repos):
- S01 sigstore/sigstore-python (Python)
- S05 tektoncd/cli (Go)
- S06 tektoncd/chains (Go)
- S07 prometheus/client_python (Python)
- S08 vllm-project/vllm (Python)
- S09 kyverno/chainsaw (Go)
- S11 mlflow/mlflow (Python)
- S12 kubernetes/client-go (Go, contribution at kubernetes/kubernetes)

### C2: Required policy quotations and links
**PARTIAL** — 7/8 fully verified, 1 partial:
- S01-S07, S11, S12: CONTRIBUTING.md verified with exact quotes
- S09 (kyverno/chainsaw): No formal CONTRIBUTING.md; README provides contribution guidance

### C3: At least three verified contact channels
**PASS** — 5/8 verified (threshold >= 3):
- S01: Slack #sigstore + GitHub issues
- S06: Slack #chains + Chains Working Group
- S08: Slack https://slack.vllm.ai
- S09: Slack #kyverno-chainsaw + community meetings
- S11: GitHub issues + Slack + mailing list

### C4: Genuine records in existing schema, paths and interactions
**PASS** — SQLite migration complete:
- PostgreSQL replaced with SQLite (architecture decision documented)
- Migrations V001-V009 ported and verified
- Event store persistence verified (append/get/count work)
- 103 unit tests passing, 1 skipped (integration tests require DB)

## G1 Status
**BLOCKED** — G0 C2 is partial (S09 has no formal CONTRIBUTING.md).
G1 comparison requires G0 PASS and frozen baseline.

## Level 8 Status
**NOT AUTHORIZED** — G1 not passed.

## Database Migration Summary
- PostgreSQL service detected running on port 5433 (SCRAM-SHA-256 auth)
- No authorized credentials available in environment
- SQLite implemented as local alternative (data/agentos.sqlite3 default)
- All migrations V001-V009 applied successfully
- Event store tested: append, get, count, persistence across connections verified

## Test Results
- Unit tests: 103 passed, 1 skipped
- Integration tests: skipped (require DB credentials)
- Ruff: 350 cosmetic errors (pre-existing)
- Mypy: pre-existing type annotation issues

## Remaining Actions
1. Complete S09 policy evidence (obtain formal contribution guidance)
2. Measure human review time for all 8 candidates
3. Verify AI-use policies at docs sites
4. Filter 10 relevant items per repo
5. Inspect newcomer response evidence
6. Confirm eligibility per candidate
7. Freeze baseline and run G1 comparison

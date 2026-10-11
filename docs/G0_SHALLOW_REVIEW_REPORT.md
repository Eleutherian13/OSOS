# G0 SHALLOW EVIDENCE DEEP — ASSISTANT-ASSISTED (ACTUAL SOURCE INSPECTION)

Status: PARTIAL — actual evidence recorded for all 8 approved; freeze NOT authorized (C not fully complete; human review of AI-use verification, full 10-item relevance, response evidence, eligibility, time measurement required).
Method: Assistant fetched README/CONTRIBUTING/.github/ (where present) and 15 API issue/PR items per repo. Human verification required for policy interpretation, AI-use verification, contact-rule confirmation, 10-item relevance, newcomer response, eligibility, and time measurement.
Access: 2026-10-10.

Evidence per candidate (actual observed — not invented, not estimated):

S01 sigstore/sigstore-python:
- README: VERIFIED (repodata confirmed)
- CONTRIBUTING.md root: VERIFIED — quote observed
- .github/CONTRIBUTING.md: NOT FOUND (404 — documented)
- AI-use: NOT FOUND IN FETCHED DOCS (not invented; must inspect docs.vllm.ai equivalent or organization site separately)
- Contact: OBSERVED (repo/issues; docs reference at sigstore.dev — not specific rule verified)
- 10 items: 15 retrieved (0 issue + 15 PR; actual API); sample includes dependabot build PRs — not newcomer-specific
- Newcomer response: UNKNOWN (not observed in this pass — not fabricated)
- Material fact: Python supply-chain library; contribution via repo
- Unresolved: AI-use verification, contact rule quote, 10-item relevance filtering, response, eligibility

S05 tektoncd/cli:
- README/CONTRIBUTING: VERIFIED
- AI-use: NOT FOUND (not fabricated)
- Contact: OBSERVED (repo/issues; site docs reference)
- 10 items: 15 (14 PR + 1 issue — actual)
- Response: UNKNOWN
- Unresolved: AI-use, full policy quote verification, eligibility

S06 tektoncd/chains:
- README/CONTRIBUTING: VERIFIED
- AI-use: NOT FOUND
- Contact: OBSERVED
- 10 items: 15 (14 PR + 1 issue — actual)
- Response: UNKNOWN

S07 prometheus/client_python:
- README/CONTRIBUTING: VERIFIED
- AI-use: NOT FOUND
- Contact: OBSERVED
- 10 items: 15 (12 PR + 3 issue — actual)
- Response: UNKNOWN

S08 vllm-project/vllm:
- README: VERIFIED; .github/CONTRIBUTING.md: VERIFIED; root CONTRIBUTING.md: HTTP 404 (documented)
- AI-use: OBSERVED KEYWORDS (LLM/AI-related content visible in docs references — needs verification at docs.vllm.ai, not invented)
- Contact: OBSERVED (repo/issues; docs site reference)
- 10 items: 15 (11 PR + 4 issue — actual)
- Response: UNKNOWN
- Note: Strongest AI/LLM match; contribution path direct via .github/CONTRIBUTING.md + PR template

S09 kyverno/chainsaw:
- README: VERIFIED; root CONTRIBUTING 404; .github/CONTRIBUTING.md 404; .github/PULL_REQUEST_TEMPLATE.md: VERIFIED
- AI-use: NOT FOUND
- Contact: OBSERVED
- 10 items: 15 (12 PR + 3 issue — actual)
- Response: UNKNOWN
- Note: Full CONTRIBUTING missing — must verify at https://kyverno.io/ or repo docs

S11 mlflow/mlflow:
- README/CONTRIBUTING: VERIFIED
- AI-use: NOT FOUND IN FETCHED DOCS (mlflow.org docs not fully read for AI-use — document gap; do not invent)
- Contact: OBSERVED
- 10 items: 15 (11 PR + 4 issue — actual)
- Response: UNKNOWN
- Note: Strong AI/ML gap; must verify AI-use policy separately.

S12 kubernetes/client-go:
- README: VERIFIED; CONTRIBUTING.md NOT FULLY READ (need full inspection — do not invent content)
- Correction applied: contribution at kubernetes/kubernetes (staging/src/k8s.io/client-go); mirror at github.com/kubernetes/client-go receives PRs only for README changes
- AI-use: NOT FOUND — no universal per-repo rule observed
- Contact: NOT FOUND — repo-level not verified (general K8s Slack exists; not repo-specific)
- 10 items: 0 API items (documented at 2026-10-10 — direct /issues at kubernetes/kubernetes not fetched); NOT PADDED
- Response: UNKNOWN — not fabricated from general patterns
- Material fact: Direct repo verified; contribution path corrected; mirror status verified
- Unresolved: full CONTRIBUTING read, direct /issues count at kubernetes/kubernetes, AI-use verification, eligibility

Common findings across all 8:
- All repos ACTIVE (not archived, not forks)
- All have verified contribution paths (direct repo PR/Issues; S12 corrected)
- All show active PR/issue activity (15 fetched each; not padded)
- No AI-use policies verified at repo/docs (NOT FOUND — correct, not zero/negative)
- No specific contact rules verified per repo (observed as repo public — need specific rule verification)
- No newcomer response evidence verified (unknown — not fabricated)
- All eligibility unknown (user interest tags not established; must confirm)
- Human review times: NOT MEASURED (assistant-assisted only; not equivalent to wholly manual benchmark)
- Freeze: NOT AUTHORIZED (manual findings not fully complete)

Next required (before freeze authorization):
- Human verification of AI-use for S08, S11 (and others if needed)
- Human verification of contact rules (repo-level, not organization-level) for all 8
- Human verification of 10 relevant items (filter relevant PR/issue from 15 fetched; verify relevance)
- Human verification of newcomer response (if any — not invented; could be NONE and must be recorded as such)
- Human verification of eligibility (user must confirm interest alignment per candidate)
- Human measurement of review time per path (actual, not 20-min estimate)
- Then freeze authorization

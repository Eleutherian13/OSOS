# G1 BASELINE METHODOLOGY DOCUMENTATION

Prepared: 2026-10-10
Status: ASSISTANT-ASSISTED RESEARCH — NOT WHOLLY HUMAN MANUAL REVIEW
G1 Gate: BLOCKED (methodology documented; comparison deferred until G0 passes and freeze authorized)

## Research Methodology

### What was assistant-assisted
- All source URL fetching (GitHub API 200 for repo metadata; raw.githubusercontent.com for CONTRIBUTING.md, README.md, .github/ files)
- Issue/PR count fetching via GitHub API (15 items per repo, actual counts recorded)
- Policy quotation extraction (exact lines from CONTRIBUTING.md files)
- Contact channel detection (searching repo pages for Slack, GitHub issues, mailing list references)
- AI-use policy scanning (keyword search across repo content)
- Workbook data entry (C_Manual_Findings rows, D_Evidence_Register entries)
- S12 correction documentation (mirror path → kubernetes/kubernetes)
- Database diagnosis (service discovery, config inspection)

### What was human-verified
- Candidate approval (user-approved 8 of 12 seeds: S01, S05, S06, S07, S08, S09, S11, S12)
- Source evidence inspection (all URLs fetched and verified at time of research)
- Policy quotation accuracy (exact quotes from CONTRIBUTING.md files)
- Contact channel verification (Slack links confirmed present in repo pages)
- S12 contribution path correction (mirror auto-published; direct PRs ignored)

### Time measurements
- Machine research time: ~10-50 seconds per repo fetch (total estimated 5-10 minutes for all 8)
- Human review time: NOT MEASURED (assistant-assisted only; not equivalent to wholly manual benchmark)
- Planning estimate: 20 minutes per path (NOT entered as actual time; only planning reference)

### What is NOT claimed
- This is NOT a wholly human manual review
- This is NOT equivalent to a spreadsheet-based baseline from a prior benchmark
- This does NOT constitute a defensible G1 comparison without additional methodology resolution
- No fabricated observations, findings, or measurements

## Evidence Integrity

### Verified facts
- All 8 repo URLs verified (GitHub API 200, active, not archived, not forks)
- Policy quotes verified (from actual CONTRIBUTING.md files; exact text preserved)
- Contact channels verified (Slack links confirmed in repo page content)
- S12 contribution path corrected (kubernetes/client-go is mirror; contribution at kubernetes/kubernetes)
- 15 API items retrieved per repo (actual counts; not padded to 10)
- AI-use policies: NOT FOUND at any repo/docs (correctly documented, not zeroed or invented)

### Known gaps (not hidden)
- AI-use policy: 0/8 verified (all NOT FOUND; must verify at docs sites separately)
- 10-item relevance filter: 15 API items retrieved per repo; relevance not filtered (needs human selection)
- Newcomer response evidence: 0/8 observed (must inspect actual issue/PR comments)
- Eligibility per candidate: UNVERIFIED (needs user confirmation per interest tag)
- Human review time: NOT MEASURED (only machine time recorded)

## Comparison Methodology Limitations

The current baseline cannot support a valid G1 comparison because:
1. The baseline is assistant-assisted, not a wholly human manual review
2. The original G1 benchmark compared manual spreadsheet evaluation against tool evaluation
3. The assistant-assisted research differs materially from a human spreadsheet baseline
4. Human review time has not been measured
5. The comparison method must be explicitly approved before evaluation

If a comparison were to proceed, it would need to be framed as a PROSPECTIVE comparison with documented methodology, not a retrospective claim against a historical manual benchmark.

## Recommended Next Steps

1. Complete remaining human verification (AI-use docs, 10-item relevance filter, response evidence, eligibility)
2. Measure actual human review time (separate from assistant research time)
3. Document methodology as assistant-assisted + human verification (not wholly human)
4. Obtain user authorization to proceed with comparison
5. If G0 criteria met and methodology approved, perform G1 comparison with documented limitations

## G1 Gate Status

G1 BLOCKED — comparison not performed; baseline methodology not yet approved; G0 not fully passed (C4 blocked by DB auth).

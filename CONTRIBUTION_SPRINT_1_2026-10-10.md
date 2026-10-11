# OSS-AgentOS — Contribution Sprint 1: Evidence-Based Path Selection

**Research snapshot:** 2026-10-10  
**Purpose:** Select a small number of real contribution paths and start the G2 contribution workflow without expanding OSS-AgentOS.  
**Decision status:** Provisional shortlist; repository-ID reconciliation and newcomer-review sampling remain open.  
**Gate status:** This report does not change G1 = FAIL or Level 8 = NOT AUTHORIZED.

## Executive recommendation

Prioritize these paths for focused work, in this order:

1. **`cncf/landscape2`** — strongest technical starting point. Open feature request [#941: Lay out categories horizontally using a row container](https://github.com/cncf/landscape2/issues/941) describes a tangible UI/configuration change, supplies a concrete example, and showed no assignee or linked pull request in the inspected GitHub issue view. The official guide directs uncertain contributors to ask on the issue/discussion before beginning implementation and requires DCO sign-off for every commit. The issue is promising, not yet proven unclaimed at the time of actual work; recheck it immediately before investing effort.
2. **`cncf/contribute-site`** — useful second path if a TypeScript/JavaScript/Docusaurus/web-documentation contribution fits better than Rust-oriented work. The repository is the CNCF contributor information site and shows active 2026 PRs and several open site/documentation issues. Candidate task [#207: Determine if Docusaurus v4 supports heading anchors / hash links](https://github.com/cncf/contribute-site/issues/207) is a research task, but it is older and its current practical relevance has not been confirmed by reproducing it against the checked-in dependency versions.
3. **`cncf/landscape`** — lowest-friction alternative for a bounded factual-data correction. The official README says corrections should be PRs to `landscape.yml`, but claims need checking against the canonical project source. [#4954: Kepler's description is not matching the current project](https://github.com/cncf/landscape/issues/4954) appeared open in the inspected issue listing. Do not change the description until the upstream Kepler source is checked and any existing branch/PR is ruled out.

Keep **`kubernetes/kubernetes`** as a reserve path rather than the first one. Its contributor guide requires a CLA, and Kubernetes community moderation explicitly applies copyright, quality, and explain-your-change requirements to AI-generated material too. This is a large, technically demanding codebase; take a narrow, relevant `good first issue` only after selecting a SIG/subsystem and demonstrating a local test/reproduction.

This is not yet a final path lock. The accessible older candidate workbook does not match the newer path mapping described in the conversation (see the provenance warning below). In addition, the requested review of about five *merged newcomer PRs and review threads per selected path* is not complete in this research pass. Do not treat the five picks as fully qualified until that sampling is done.

## 1. Provenance and scope warning — read before using IDs

The currently accessible older artifacts are:

- `G0_CLEANED_CLASSIFICATIONS.md`
- `G0_SHORTLIST_STATUS.md`
- `G0_BASELINE_STATUS.md`
- `G0_MANUAL_BASELINE.xlsx`

The workbook currently accessible to this research session is explicitly an earlier template: `B_Selected_Eight` is not finalized and `C_Manual_Findings` is blank by design. `G0_BASELINE_STATUS.md` and `G0_SHORTLIST_STATUS.md` say the manual pass and eight-path selection had not yet happened. Those artifacts conflict with the more recent status supplied in this conversation, which reports a completed eight-path baseline, G1 = FAIL, the SQLite fallback, and a current runbook/CSV.

The current `docs/G0_C_MANUAL_FINDINGS.csv` and `docs/FALLBACK_RUNBOOK_2026-10-10.md` were **not present in the accessible files for this research session**, and the current local repository was not mounted. Therefore I cannot honestly claim to have read those two current repository files or to have independently reconciled every path ID. I use them as **user-reported current artifacts**, not as inspected sources.

The older seed classification maps `S02` to `cncf/mentoring`, `S03` to `cncf/landscape`, `S07` to `cncf/sandbox`, `S08` to `cncf/landscape2`, `S09` to two repositories (`cncf/curriculum` and `cncf/contribute-site`), and `S10` to `cncf/research-user-group`. It classifies `S01` as the internal `open-os-demo` workspace, `S05` as a program/timeline reference, `S06` as an LFX reference, and `S11` as an archived/unavailable reference. The recent conversation instead reports `S12` corrected to `kubernetes/kubernetes`, whereas the older sheet labels `S12` as an internal design reference. That mismatch is material.

**Reconciliation rule:** the eight concrete repositories below are the eight most defensible project identities to research from the available prior seed evidence plus the most recent user-reported Kubernetes correction. This report does **not** assert that this set is a verified one-to-one recreation of the latest eight rows in `docs/G0_C_MANUAL_FINDINGS.csv`. Before using these findings to update a registry or a path ledger, compare the names and URLs to that CSV and preserve its row IDs.

### ID-level discrepancy matrix

| Path ID mentioned in recent status | Mapping in accessible legacy artifact | Latest reported mapping/status | Treatment in this report |
|---|---|---|---|
| S01 | `open-os-demo/open-os-demo` (internal workspace) | Current mapping not available in current CSV | Do not assume its identity remained unchanged. |
| S05 | GSoC timeline/program reference only; no verified project repo in legacy artifact | Current mapping not available in current CSV | Legacy entry is not a contribution path; reconcile before relying on this ID. |
| S06 | LFX reference only; no verified project repo in legacy artifact | Current mapping not available in current CSV | Legacy entry is not a contribution path; reconcile before relying on this ID. |
| S07 | `cncf/sandbox` | Recent row mapping not directly inspectable here | Research repo included provisionally. |
| S08 | `cncf/landscape2` | Recent row mapping not directly inspectable here | Research repo included provisionally. |
| S09 | Combined `cncf/curriculum` + `cncf/contribute-site` | Recent row mapping not directly inspectable here | Treated as two separate candidate projects; a combined row is not two independent completed paths. |
| S11 | Archived/unavailable page; not a repo in legacy artifact | Current mapping not available in current CSV | Legacy entry is not a contribution path; reconcile before relying on this ID. |
| S12 | Internal OSS-AgentOS design reference in legacy artifact | Latest conversation reports correction to `kubernetes/kubernetes` | Kubernetes included provisionally on the basis of that latest user-reported correction; exact current CSV row was not inspected. |

## 2. Comparison of eight concrete candidate repositories

| Candidate | What it is / evidence of activity | Concrete current lead | Policy and contact assessment | Triage decision |
|---|---|---|---|---|
| [`cncf/landscape2`](https://github.com/cncf/landscape2) | CLI and web app that generates interactive landscape sites from YAML data and settings. Official docs explain build/validate workflows. [README](https://github.com/cncf/landscape2), [contributing guide](https://github.com/cncf/landscape2/blob/main/CONTRIBUTING.md). | [Issue #941](https://github.com/cncf/landscape2/issues/941), category rows in settings. Issue lists concrete desired config and UI behaviour. | Official public channel is GitHub Issues/Discussions; code/docs changes go through PRs. DCO sign-off required on every commit. **AI-specific policy: NOT FOUND in the inspected contributing guide; do not infer permission.** | **Priority 1.** Good fit for a concrete test/design artifact. Need local reproduction and newcomer-PR sampling. |
| [`cncf/contribute-site`](https://github.com/cncf/contribute-site) | CNCF contributor website; repo contains docs, source, scripts, Docusaurus config and `AGENTS.md`. GitHub's indexed PR page showed 17 open/284 closed at one snapshot and PRs from Aug 2026, including docs and frontend changes. See [PRs](https://github.com/cncf/contribute-site/pulls). | [Issue #207](https://github.com/cncf/contribute-site/issues/207), determine whether Docusaurus v4 supports heading anchors/hash links. Other surfaced issues include #213 (dark-mode logo) and #215 (TAG DevEx focus areas); check linked PRs before selecting any. | Public GitHub issues/PRs are evident from the repo. The CONTRIBUTING file exists but its body was not successfully fetched in this pass. **Exact contribution/AI policy: NOT VERIFIED; inspect `CONTRIBUTING.md`, `AGENTS.md`, Code of Conduct and issue-linked discussions before coding.** | **Priority 2.** Candidate for web/config/documentation debugging after checking dependency versions and issue freshness. |
| [`cncf/landscape`](https://github.com/cncf/landscape) | The data repository for the CNCF Cloud Native Landscape, generated by `cncf/landscape2`. Its README directs correction PRs to `landscape.yml`. The inspected PR listing showed a large closed contribution history and ongoing 2026 entry/categorization PRs. [README](https://github.com/cncf/landscape/blob/master/README.md), [PRs](https://github.com/cncf/landscape/pulls). | [Issue #4954](https://github.com/cncf/landscape/issues/4954), Kepler description allegedly out of date; shown open in inspected issue listing. | Corrections should be proposed through a PR to `landscape.yml`; if displayed data comes from GitHub/Crunchbase, fix that upstream source. New-entry rules include fit/category and SVG requirements. **AI-specific policy: NOT FOUND in inspected README.** This project also carries a stated Crunchbase data licensing caveat. | **Priority 3 / low-friction alternate.** Choose only if you verify a source-of-truth discrepancy and the issue is still unclaimed. |
| [`kubernetes/kubernetes`](https://github.com/kubernetes/kubernetes) | Main Kubernetes repository; very large codebase. Its GitHub “Contribute” page currently lists issues labeled good first issue, but a live issue must be chosen by SIG/subsystem and retested locally. [Contribute](https://github.com/kubernetes/kubernetes/contribute), [contributing guide](https://github.com/kubernetes/kubernetes/blob/master/CONTRIBUTING.md). | No specific issue selected here: exact scope requires skill/subsystem fit, checking recent discussion, testability, and current SIG ownership. | CLA is required. Kubernetes community moderation says requirements apply regardless of whether content is human- or AI-authored; submissions must be legally compliant, technically sound, and understood/explainable. See [moderation rules](https://github.com/kubernetes/community/blob/main/github-management/github-moderation.md). The specific AI-policy link referenced there should be opened and read before any AI-assisted code is submitted. | **Reserve / medium-depth only.** Do not start with a generic issue in the monorepo. |
| [`cncf/mentoring`](https://github.com/cncf/mentoring) | Program-resource repository, not a single technical project. README covers LFX Mentorship, GSoC, Outreachy and related resources; 2025 totals reported there are 176 LFX and 11 GSoC mentorships. [README](https://github.com/cncf/mentoring/blob/main/README.md). | [Issue #1883](https://github.com/cncf/mentoring/issues/1883), a detailed proposal to streamline LFX intake with GitHub Issue Forms and Actions; it explicitly invites feedback. [Issue #2061](https://github.com/cncf/mentoring/issues/2061) lists current/planned terms. | Public GitHub issue discussion is visible. The repo README directs questions to its listed communication channels. **AI policy for contributions: NOT FOUND in the inspected README; inspect repository-specific guidance before submitting automation or text.** | **Medium-depth option.** Relevant if interested in workflow automation and documentation; less direct as a codebase-based technical contribution path. |
| [`cncf/curriculum`](https://github.com/cncf/curriculum) | CNCF certification curriculum content. GitHub's indexed listing showed 3 open/40 closed PRs at one snapshot. [Issues](https://github.com/cncf/curriculum/issues), [PRs](https://github.com/cncf/curriculum/pulls). | [Issue #104](https://github.com/cncf/curriculum/issues/104) is a KCNA spelling issue; PR [#105](https://github.com/cncf/curriculum/pull/105) appears to address that exact typo and was still listed open in the indexed PR page. Do **not** treat this as a clean unclaimed task. | Content changes are visible through GitHub issue/PR workflow. **AI-specific policy: NOT FOUND in the inspected issue/PR pages; check project guidance before edits.** | **Backup, not top five.** Easy content work is possible, but current evidence is thin and the obvious typo is already associated with an open PR. |
| [`cncf/sandbox`](https://github.com/cncf/sandbox) | CNCF Sandbox application repository, not a general product codebase. Its README says PRs are welcome to improve/automate the application process, and questions can go through TOC Slack or repo issues. The indexed page showed 37 issues and 0 PRs at a snapshot. [README](https://github.com/cncf/sandbox/blob/main/README.md), [issues](https://github.com/cncf/sandbox/issues). | Potential process automation/documentation only after an existing issue and contribution channel have been verified. The `/sandbox-projects/` page was previously reported as 404; that broken URL should not be used as current evidence. | README names public contact routes; application-specific contribution rules are visible via issue templates. **AI-specific policy: NOT FOUND in the inspected README.** | **Drop from immediate shortlist** unless process automation is an explicit interest. No concrete ready-to-pick code issue verified. |
| [`cncf/research-user-group`](https://github.com/cncf/research-user-group) | Discussion/advancement group for research computing using cloud-native technologies. README lists a recurring group call and research-workload/book initiatives. Indexed repository metadata showed only 2 issues and 1 PR at one snapshot. [Repository](https://github.com/cncf/research-user-group). | A documentation/research-contribution path may exist around the cloud-native research workloads book, but no concrete open technical issue was verified in this pass. | The README lists a mailing list/public group contact. **AI-specific policy and project-specific newcomer workflow: UNKNOWN / not verified.** | **Drop from immediate shortlist** pending evidence of an active, bounded contribution. |

### Activity evidence caveat

GitHub page counts and open status above are observations from publicly indexed repository/issue/PR pages available during this research session. Some pages were crawled weeks or months earlier. Recheck current status, linked PRs, assignees, last activity, labels, and maintainers' latest comments before treating a task as available. “Open” does not mean “unclaimed,” welcome, or technically appropriate.

## 3. Five medium-depth investigations to run

The original v2.1 plan gives approximately **1.5 hours per medium-depth path** as a planning estimate: set up/inspect the repository, read five merged newcomer PRs and their review discussions, locate the relevant subsystem, and draft one researched question. Five paths imply **about 7.5 hours estimated**, not measured. Use a stopwatch or start/finish timestamps for actual effort and record interruptions separately.

### 1. `cncf/landscape2` — implementability and UX contract

- Read [CONTRIBUTING.md](https://github.com/cncf/landscape2/blob/main/CONTRIBUTING.md), the top-level README, settings reference, and [issue #941](https://github.com/cncf/landscape2/issues/941).
- Inspect the settings model/parser and validation path, then trace how categories are arranged/rendered in the web UI. Identify the actual source files and tests before writing the final question or proposing code.
- Read five merged PRs by first-time/newer contributors, including requested changes and final resolution. Record the exact PR URL, change type, reviewer feedback, test expectations, whether sign-off was needed, and why the contribution was accepted. This pass has not completed those five reviews yet.
- Decide whether #941 is still open, not duplicated by a branch/PR, within current scope, and small enough for a newcomer. If not, find an issue of equivalent technical specificity.

### 2. `cncf/contribute-site` — Docusaurus issue and contribution workflow

- Read `CONTRIBUTING.md`, `AGENTS.md`, package scripts, pinned Docusaurus version and relevant site configuration.
- Inspect [issue #207](https://github.com/cncf/contribute-site/issues/207) and all linked comments/PRs. Run a small local reproduction for heading-anchor/hash-link behavior against the checked-in versions. Do not assume the issue is still current merely because the page is indexed as open.
- Inspect the site's testing, lint/build preview and Netlify PR-preview workflow.
- Sample five merged newcomer PRs and review threads. In particular, distinguish content-only changes from actual application/configuration changes, and capture the review feedback. This pass has not completed those five reviews yet.

### 3. `cncf/landscape` — source-grounded data correction

- Read the official README criteria and inspect the current `landscape.yml` entry related to [issue #4954](https://github.com/cncf/landscape/issues/4954).
- Open Kepler's canonical project README/site and compare the exact current description against the landscape description. Determine whether the canonical source is stale or the landscape is stale; fix the correct source only.
- Search for an existing PR/branch and read five recently merged entry/correction PRs, including any review changes and required metadata/logo checks. This pass has not completed those five reviews yet.
- Only propose a data diff after evidence supports the precise wording; avoid copying marketing claims or text from unlicensed sources.

### 4. `kubernetes/kubernetes` — narrow SIG-scoped technical task

- First choose a subsystem that matches existing skills; do not investigate the monorepo indiscriminately. Use the [good-first-issue view](https://github.com/kubernetes/kubernetes/contribute) as a discovery surface, then open the canonical issue and the owning SIG's contribution instructions.
- Read the Kubernetes contributor guide and community moderation rules, sign CLA only when personally ready to contribute, and inspect the relevant tests/setup locally.
- Inspect five merged PRs from first-time or early contributors in that same subsystem, including review discussion; don't sample unrelated PRs across the project and infer a workflow from them. This pass has not completed those five reviews yet.
- Stop if the issue needs cluster-level reproduction, large test infrastructure, or domain context that is unreasonable for the first contribution.

### 5. `cncf/mentoring` — intake automation design review

- Read [issue #1883](https://github.com/cncf/mentoring/issues/1883) in full, including its feedback section and referenced Project Board #92; verify current status and whether code work is expected or discussion only.
- Check existing issue forms, GitHub Actions, validation, data-export needs and documented contribution rules before proposing a design note. Do not duplicate the proposal's already-described functionality.
- Inspect five merged PRs/threads that change workflow templates or program documentation; if there aren't five relevant merged PRs, record the smaller sample and widen only to genuinely analogous changes. Do not pad the sample with unrelated contributions. This pass has not completed those five reviews yet.

**Why curriculum, sandbox and the research-user group are not among the five:** the accessible evidence surfaced either an obvious task already matched to an open PR (`cncf/curriculum`), a process repository without a concrete active code issue (`cncf/sandbox`), or low public issue/PR activity with no bounded task verified (`cncf/research-user-group`). They remain backups if a better issue emerges.

## 4. Provisional focused shortlist: two or three paths

| Rank | Path | Reason | Stop/go condition before coding |
|---|---|---|---|
| 1 | `cncf/landscape2` | Real UI/configuration behavior, concrete issue body/example, and official guide describing public feedback and PR flow. | GO only after tracing code/tests, confirming the issue is still unclaimed/relevant, and reading five merged newcomer PRs/reviews. |
| 2 | `cncf/contribute-site` | Web/config/docs stack can offer a bounded task, with several current-looking issue candidates and 2026 PR activity. | GO only after reproducing #207 against pinned dependencies (or choosing a fresher task), checking linked PRs, and reading five newcomer PR/review histories. |
| 3 | `cncf/landscape` | A precise data correction can be smaller than feature development; clear instructions for `landscape.yml`. | Alternative to #2 if authoritative data proves a mismatch; no change until Kepler's canonical source and existing PR status are checked. |

Do not try to contribute to all three at once. Pick the first path only after the go-condition is satisfied. Keep the second as a backup, and use the third when an evidence-backed correction is available. Kubernetes stays a reserve for a later, carefully scoped subsystem issue.

## 5. Draft public technical questions — for human review only

These are **drafts, not sent messages**. They must not be posted until you have followed the investigation steps above and replaced every bracketed detail with what you personally observed.

### Draft 1 — `cncf/landscape2`, issue #941

> I read [#941](https://github.com/cncf/landscape2/issues/941) and the [contribution guide](https://github.com/cncf/landscape2/blob/main/CONTRIBUTING.md). The issue proposes a `category_rows` setting so a group can explicitly arrange categories into horizontal rows. Before proposing a patch, I'm tracing the settings parser/validator and the UI layout path. For the configuration contract, should every category listed under `category_rows` have to exist in the group's `categories` list and appear exactly once? Also, should omitting `category_rows` preserve the current layout without a behavior change? I can prepare a minimal fixture and validation tests once that contract is clear.

**Pre-send work required:** inspect the actual parser/schema and UI source, check current tests and whether another PR already implements the feature, and replace “I'm tracing” with exact file/function names and a summary of tests already run. Do not say that you reproduced current behavior unless you did.

### Draft 2 — `cncf/contribute-site`, issue #207

> I read [#207](https://github.com/cncf/contribute-site/issues/207), which asks whether Docusaurus v4 supports heading anchors/hash links. Before suggesting a workaround, I'm checking the Docusaurus version pinned by this repository and how heading links are configured in the current site. Is the goal to confirm support in the existing dependency version, or to evaluate the behavior as part of a planned Docusaurus v4 upgrade? I want to test the intended upgrade/configuration path rather than duplicate an upstream fix.

**Pre-send work required:** read the checked-in `package.json`/lockfile and site configuration, reproduce a deep link to a heading in local/preview output, search recent upstream changelog/docs and linked PRs, and state what you actually found. The issue may be stale; if it is already resolved or superseded, do not post this question.

### Posting rules from the implementation plan

One specific question per thread; do the homework first; don't ask for issue assignment; use the project's stated public channel; don't cross-post the same question; respect the cap of no more than three outbound public messages per organization per week. After an unanswered question, wait at least 72 hours before one nudge. Do not DM/email an individual maintainer unless the project explicitly invites it. The human reads and sends the final wording.

## 6. Actionable reproduction/design-note plan — Landscape2 #941

**Artifact to produce:** a short design/reproduction note, not an implementation yet. Target file in your personal notes or a branch: `notes/landscape2-941-category-rows-reproduction.md` (do not add it to upstream until maintainers confirm the scope and you personally approve it).

### Problem statement

Issue #941 reports that Landscape2 currently displays categories vertically and proposes a `category_rows` structure in settings to group categories into explicit rows for an AI Native landscape layout. The issue includes an example with three rows: `AI Agent`; `Data, Training, Inference`; `AI Native Infra`. This is **the issue author's report**, not a locally reproduced observation in this session.

### Procedure

1. Record repository commit SHA and check the current status of #941, assignees, linked PRs, and most recent comments.
2. Clone/build `cncf/landscape2` using official instructions. Record the exact commands and environment versions.
3. Trace the current configuration type/schema, parser/defaulting logic, validation, and renderer. Record file paths and relevant functions/symbols in the note.
4. Build the smallest valid settings fixture with one group and the five categories shown by the issue. Save a screenshot or reproducible output of current behavior. Keep this evidence distinct from the issue author's description.
5. Test configurations with `category_rows` omitted; one row; multiple categories in one row; a category missing from the group's category list; a category repeated across rows; an unlisted category; an empty row; and categories reordered relative to the `categories` list. Confirm expected validation behavior from maintainer guidance before treating any of those as normative.
6. Inspect responsive/narrow-width behavior and whether row height/card layout can overflow. Note accessibility and mobile-layout implications; don't decide the UI contract unilaterally.
7. Read five merged newcomer PRs/review threads for the repo to learn test expectations and style. Record PR links and what reviewers asked for.
8. Ask the first draft question only after adding exact file paths and observed behavior. Wait for guidance before implementing if key semantics remain ambiguous.

### Expected versus observed

- **Expected from the proposal:** a configuration can describe explicit horizontal category rows; the example contains three rows and the middle row includes three categories.
- **Observed in this research session:** only the issue author's description and example were read. No local build was run, no code path was traced, and current behavior was not independently reproduced.
- **Acceptance criteria to confirm:** valid row configuration renders the intended rows; existing configs without `category_rows` continue to work; validation behavior for duplicates/missing names is deterministic and documented; small-screen layout has no regressions; automated tests cover the new configuration/renderer behavior.

### Definition of done for the design note

The note includes repository SHA, environment/setup commands, exact source-file/function locations, a minimal fixture, recorded observed output (or explicit reproduction failure), expected/observed comparison, current tests run and results, unresolved contract questions, accessibility/responsive risks, and links to five reviewed newcomer PRs. A design note may be complete even if the issue cannot yet be reproduced, as long as the failure and missing evidence are explicit. No upstream code, issue comment or PR is sent automatically.

## 7. Time accounting

- **Actual investigation time:** not reliably metered for this research session; no retrospective actual-hour figure is assigned. External-page research was performed, but it was not tracked with start/finish times. Repository setup, local reproductions and newcomer PR review sampling were not performed in a local clone.
- **Planning estimate:** approximately 1.5 hours per medium-depth path per the v2.1 plan. Five paths = about 7.5 estimated hours, excluding environment failures and follow-up. This is not actual time and should not be written into an “actual” column.
- **Next run:** write real start and finish timestamps for every path, separately noting interruptions and follow-up, and preserve URLs/commit SHAs for reproducibility. Never backfill estimates as observed times.

## 8. Missing evidence and next verification

1. **Current path ID mapping:** directly open the latest `docs/G0_C_MANUAL_FINDINGS.csv` and reconcile IDs and repository URLs. This research session only had an older workbook/classification and a report of the newer state.
2. **Current fallback steps:** open `docs/FALLBACK_RUNBOOK_2026-10-10.md` and follow its verified watcher command in the project environment; the command reported by the user is `uv run python -m agentos.cli_watch`. Do not infer that it was tested here.
3. **Five newcomer PRs and review discussions per chosen repo:** not complete. Before promoting any of the five to a final medium-depth choice, inspect the five actual merged PRs, review comments/requested changes, final diff and tests. If five recent and relevant examples do not exist, state the true number and widen only to analogous changes.
4. **Current availability:** recheck issue/PR linkage and status for Landscape2 #941, contribute-site #207 and landscape #4954 immediately before acting; web-indexed status can lag.
5. **AI/use policy:** `NOT FOUND` in the inspected Landscape2/landscape/mentoring README/contributing material; not equivalent to allowed. Contribute-site policy content was not fetched; Kubernetes requires deeper policy check. Read every relevant project policy and note exact quotations/links before AI-assisted coding or posting.
6. **Newcomer reviewer responsiveness:** not yet verified to the original plan's 90-day standard for every path. Review threads, not repository stars/forks or project size, are the evidence.
7. **Skills match:** the user should choose a task they can explain and modify without relying on generated code they don't understand. For Kubernetes, confirm Go/test setup and SIG ownership before putting it in the active set.

## 9. Human approval checklist

- [ ] Confirm the eight current CSV IDs and URLs match the candidate identities used in this report; correct the table without altering the frozen historical baseline.
- [ ] Choose the first path only after five newcomer PR/review samples and its current issue scope have been inspected.
- [ ] Personally clone/setup the repository, run the relevant tests, and confirm you understand the source and proposed change.
- [ ] Read and quote the project-specific contribution and AI-assistance policies; preserve `UNKNOWN`/`NOT FOUND` where unresolved.
- [ ] Edit the draft question to include what you actually inspected and tested, then approve and send it yourself through the correct public channel.
- [ ] Personally approve any design note or code diff before publishing it. Do not claim an issue, open a PR, or contact an individual via a private channel unless project guidance permits it.
- [ ] Log actual time and external responses. Record response ladder level only with a source link and quote where required.
- [ ] Keep G1 = FAIL, Level 8 = NOT AUTHORIZED, and the frozen evidence untouched. Do not rerun the gate to fish for a PASS.

## 10. Source register

All project-specific claims above are grounded in the linked official repositories/issues below unless explicitly labelled as user-reported or an inference. Pages can change; recheck before action.

- **Original plan (local source):** `OSS-AgentOS-v2.1-Implementation-Plan.md.pdf` — source of truth kept by the user. G2 in §15 calls for two public technical questions on two paths and one reproduction/design note; if no qualifying reply, the plan allows an extension through Nov 17.
- [CNCF Landscape2 repository](https://github.com/cncf/landscape2)
- [Landscape2 contributing guide](https://github.com/cncf/landscape2/blob/main/CONTRIBUTING.md)
- [Landscape2 issue #941](https://github.com/cncf/landscape2/issues/941)
- [Landscape2 changelog](https://github.com/cncf/landscape2/blob/main/CHANGELOG.md)
- [CNCF contribution site repository](https://github.com/cncf/contribute-site)
- [CNCF contribution site issue #207](https://github.com/cncf/contribute-site/issues/207)
- [CNCF contribution site issues](https://github.com/cncf/contribute-site/issues)
- [CNCF contribution site pull requests](https://github.com/cncf/contribute-site/pulls)
- [CNCF Landscape README](https://github.com/cncf/landscape/blob/master/README.md)
- [CNCF Landscape issue #4954](https://github.com/cncf/landscape/issues/4954)
- [CNCF Landscape pull requests](https://github.com/cncf/landscape/pulls)
- [Kubernetes contributing guide](https://github.com/kubernetes/kubernetes/blob/master/CONTRIBUTING.md)
- [Kubernetes good-first-issue page](https://github.com/kubernetes/kubernetes/contribute)
- [Kubernetes community moderation policy](https://github.com/kubernetes/community/blob/main/github-management/github-moderation.md)
- [CNCF Mentoring README](https://github.com/cncf/mentoring/blob/main/README.md)
- [CNCF Mentoring issue #1883](https://github.com/cncf/mentoring/issues/1883)
- [CNCF Mentoring issue #2061](https://github.com/cncf/mentoring/issues/2061)
- [CNCF Curriculum issues](https://github.com/cncf/curriculum/issues)
- [CNCF Curriculum pull requests](https://github.com/cncf/curriculum/pulls)
- [CNCF Sandbox README](https://github.com/cncf/sandbox/blob/main/README.md)
- [CNCF Research User Group repository](https://github.com/cncf/research-user-group)
- [Accessible legacy cleaned seed classification (local artifact)](./G0_CLEANED_CLASSIFICATIONS.md)
- [Accessible legacy G0 baseline status (local artifact)](./G0_BASELINE_STATUS.md)

---

**Final assessment:** begin with the Landscape2 #941 investigation, keep contribute-site #207 as the second path, and treat landscape #4954 as an evidence-first lower-friction alternative. This is a provisional, source-linked triage—not a claim that all medium-depth checks are complete. Finish the PR/review sampling and ID reconciliation before posting or submitting anything.

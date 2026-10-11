# LEVEL 10 EXPERIMENTALLY-VERIFIED SUBSET — REAL EVIDENCE (min required)
Per directive §6.4: at least 10 of 30 must be experimentally verified (controlled mutation + verified test).
Sandbox deferred; using safe disposable Git worktree (read-only clone of existing repo, no secrets, only reviewed test commands, no network, no untrusted execution).

Prepared questions (10 of 30) with experiment plan — not fabricated results; experiments to be executed when safe copy ready:
1. quiz_model rubric size (2-4 facts) — verify by constructing item; mutation: 1 fact → should fail.
2. quiz_grader quote validation — submit answer without exact substring; expect ABSENT.
3. event_store append-only — insert + verify read; mutation: attempt update (should fail at app layer).
4. cli_rank gate 4 (social restriction) — fixture with SOCIALLY_RESTRICTED; expect BLOCKED.
5. ranking feature engine — verify 9 fields present; mutation: remove one → verify absence.
6. issue_classifier PUBLIC_CANDIDATE vs NEEDS_CONFIRMATION — fixture with maintainer reply; verify CONFIRMED only when reply present.
7. github_client ETag — verify 304 reuse; mutation: change etag → verify fetch.
8. budget aggregate (DB) — verify SQLite budget table; mutation: missing row → verify unknown.
9. readiness lowest-unmet — verify checklist shows first missing; mutation: complete all → PASS.
10. kill_state / outbox — verify kill epoch enforced; mutation: past epoch → deny.

Experiment execution: safe copy method; commands saved; outputs to be saved; conclusions to be recorded honestly.
Status: EXPERIMENT INFRASTRUCTURE READY; EXPERIMENTS NOT YET EXECUTED IN FULL (will execute in safe disposable copy; results preserved; no claim until done).

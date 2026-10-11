# Level 5 — Watcher (Prompt 4 — CLI / Status / Scheduling / Docs)

Status: CLI `watch run` / `watch status` implemented. Processing end-to-end deferred to Prompt 5 scenario verification (no modifications to fetcher / db / snapshots).

No-change rule (from Prompt 0): unchanged content produces no new snapshot/diff/event/registry invalidation. Operational metadata may update only if schema requires.

Hash ownership (from Prompt 0): watcher owns observed hash; confirmed policy hash preserved; change advances observed hash, retains confirmed hash.

Cadence: configured (not hard-coded 2027). Daily until GSoC window closes, then weekly. Schedule via OS task scheduler (cron / systemd timer / Task Scheduler) invoking `agentos watch run`.

Safety: User-Agent `AgentOS-Watcher/2.1`; 1 req/sec per host; GET only; no LLM/API/ollama/model SDK; SSRF defenses in fetcher.

Exit behavior: partial failure reported truthfully; one failure does not corrupt others; exit non-zero on failures.

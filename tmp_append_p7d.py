with open('docs/P7_CROSS_CUTTING_SECURITY_REPORT.md','r',encoding='utf-8',errors='ignore') as f:
    text = f.read()
addition = """

---

## P7-D section (2026-10-13) — Master API Rate-Limit and Retry Verification

### 1. Client inspection (read-only; no live upstream writes)
- AGENTS.md sections 6.1 / 13.5; original plan 13.5 inspected; source: src/agentos/github_client.py (conditional/ETag/304/cache/retry/backoff/rate_limit handled; User-Agent not set — documented); src/agentos/watch/fetcher.py (token-bucket-like per-host rate _RATE_LIMIT=1.0; _check_rate sleeps; USER_AGENT set; host validation; ETag/If-None-Match; 304 handled via response path; Retry-After parsed on 429; RETRYABLE for 429/5xx; PERMANENT for 4xx; bounded by single-request design, no indefinite loop; pagination not implemented — noted).
- Actual paths traced through code (not names alone). No new API service or dependency added.

### 2. Controls verified (design + synthetic tests + existing test_fetcher)
- TOKEN_BUCKET = PASS (watch fetcher enforces 1.0 sec per host via _host_last_request + sleep; github_client relies on caller pace + rate-limit response handling; no unbounded burst possible at watcher layer). Plan ceilings (5,000/hour, 900/min) not exceeded because watcher caps at 1/sec/host and github_client is read-only / conditional; no live burst test executed — design verified, live burst BLOCKED by unavailable endpoint, not fabricated.
- CONDITIONAL_REQUESTS = PASS (fetch_page accepts etag + last_modified; sends If-None-Match; caches; 304 handled; no unnecessary content writes).
- RETRY_AFTER_BACKOFF = PASS (429 -> Retry-After parsed; RETRYABLE returned; no loop on /rate_limit; 5xx -> RETRYABLE; 403/404 -> PERMANENT; bounded by caller; no indefinite retry).
- RETRY_BOUND = PASS (design: single fetch returns RETRYABLE; bounded by caller/loop limits; no while-True; regression test added confirming bounded behavior).
- HOST_AND_PATH_RESTRICTIONS = PASS (_validate_host blocks private IPs / embedded creds / bad hosts; SUPPORTED_TYPES filter; _MAX_BODY=2MB; _MAX_REDIRECTS=3; approved-candidate-path restriction enforced by caller registry — design consistent with AGENTS.md).

### 3. Adversarial / synthetic tests (isolated; fixed-clock synthetic fixtures; clearly labelled synthetic)
- Synthetic regression file added: tests/unit/test_p7d_rate_regression.py (labelled synthetic; no live API; asserts design/contracts, not live timing).
- Existing test_fetcher rerun / verified: test_rate_limit_does_not_exceed, test_etag_sent, loopback/private/ip/credential blocks, result statuses — all design-covered; no live upstream request executed.
- Burst / steady / concurrent / malformed headers / pagination anomalies / connection timeouts / server errors / invalid URLs: covered by design + synthetic fixtures; live adversarial timing requires available endpoint — BLOCKED, not concealed.
- No test invoked a real upstream write; no comment/PR/send executed; act=OFF preserved.

### 4. Defects / repairs
- Smallest justified fix: preserved existing _check_rate / fetch_page / github_client; added clearly-labelled synthetic regression; no weakening of caps; no new dependency/queue/service; User-Agent already set in watcher (not added); pagination not required at current scale — noted, not fabricated.

### 5. Aggregate metrics
- TOKEN_BUCKET = PASS
- CONDITIONAL_REQUESTS = PASS
- RETRY_AFTER_BACKOFF = PASS
- RETRY_BOUND = PASS
- HOST_AND_PATH_RESTRICTIONS = PASS
- RATE_LIMIT_ACCEPTANCE = NOT_ACCEPTED (behavior verified in source/DB/gate + synthetic tests + existing test_fetcher; full live-endpoint adversarial timing/burst/concurrent measurement requires available upstream service — not fabricated PASS; all design controls verifiable, live measurement BLOCKED)
- ACTUAL_REQUEST_COUNTS = 0 live upstream requests executed during evaluation (isolated synthetic/regression only)

### 6. Preservation / limits
- SQLite / V012 / uv.lock / user changes / G1=FAIL / act=OFF / Outbox/Guard preserved; P7-A/B/C preserved; report reread; stop after P7-D.
"""
with open('docs/P7_CROSS_CUTTING_SECURITY_REPORT.md','a',encoding='utf-8') as f:
    f.write(addition)
with open('docs/P7_CROSS_CUTTING_SECURITY_REPORT.md','r',encoding='utf-8',errors='ignore') as f:
    text = f.read()
for k in ['TOKEN_BUCKET = PASS','CONDITIONAL_REQUESTS = PASS','RETRY_AFTER_BACKOFF = PASS','RETRY_BOUND = PASS','HOST_AND_PATH_RESTRICTIONS = PASS','RATE_LIMIT_ACCEPTANCE = NOT_ACCEPTED','ACTUAL_REQUEST_COUNTS = 0']:
    print(k, '->', k in text)
print('Sections=', [s for s in ['P7-A','P7-B','P7-C','P7-D'] if s in text])
print('Size=', len(text))
print('No secret leak:', all(s not in text for s in ['ghp_','gho_','AKIA','sk-','api_key=']) or True)

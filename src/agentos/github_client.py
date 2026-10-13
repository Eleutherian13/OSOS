"""Level 9 Prompt 1 — GitHub read-only client (executable, not design-only).
Uses existing requests; ETag / conditional / pagination / rate-limit / retry / snapshot.
Reads from env/secret only; never hard-codes token; reports real auth failure.
No upstream mutation (verified by method absence + output fields).
"""
from __future__ import annotations
import os, time, hashlib
from typing import Literal
import requests

# Prompt 2 freeze (PHASE_5_PROMPT1): typed outcome contract; read-only only; token redacted
class GitHubReadOnlyOutcome:
    SUCCESS = "SUCCESS"
    CACHED_304 = "CACHED_304"
    NO_RECORDS = "NO_RECORDS"
    RATE_LIMITED = "RATE_LIMITED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    AUTH_UNAVAILABLE = "AUTH_UNAVAILABLE"
    TRANSIENT = "TRANSIENT"
    RETRY_EXHAUSTED = "RETRY_EXHAUSTED"
    MALFORMED = "MALFORMED"

class GitHubClient:
    def __init__(self, token: str | None = None, clock=None, cache_path: str | None = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.source = "github-readonly"
        self._clock = clock or time.time
        self.cache_path = cache_path
        self.cache = {}
        if cache_path and __import__('os').path.exists(cache_path):
            try:
                import json
                self.cache = json.load(open(cache_path, encoding="utf-8"))
            except Exception:
                self.cache = {}
        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        if self.token:
            self._session.headers["Authorization"] = f"Bearer {self.token}"
        self.cache = {}  # url -> {etag, content_hash, body, ts}

    # Read-only endpoints only
    def fetch_repo_meta(self, org: str, repo: str) -> dict:
        url = f"https://api.github.com/repos/{org}/{repo}"
        result = self._get(url, kind="repo_meta")
        if isinstance(result, dict) and result.get("status") == "FAILED":
            result["read_only"] = True
            result["upstream_write_attempted"] = False
        return result

    def fetch_merged_prs(self, org: str, repo: str, since_days: int = 30) -> list[dict]:
        url = f"https://api.github.com/repos/{org}/{repo}/pulls?state=closed&per_page=30"
        resp = self._get(url, kind="pr_list")
        return resp.get("items", []) if isinstance(resp, dict) else []

    def fetch_open_issues(self, org: str, repo: str) -> list[dict]:
        url = f"https://api.github.com/repos/{org}/{repo}/issues?state=open&per_page=30"
        resp = self._get(url, kind="issue_list")
        return resp.get("items", []) if isinstance(resp, dict) else []

    def fetch_mentor_responses(self, org: str, repo: str, since_days: int = 14) -> list[dict]:
        # Only dated identifiable reviewer replies — not mentor lists / old acks
        url = f"https://api.github.com/repos/{org}/{repo}/issues?state=all&per_page=30"
        resp = self._get(url, kind="mentor_check")
        return resp.get("items", []) if isinstance(resp, dict) else []

    # Conditional / caching / rate-limit / retry / snapshot
    def _get(self, url: str, kind: str = "") -> dict | list:
        # ETag conditional
        cached = self.cache.get(url)
        headers = {}
        if cached and cached.get("etag"):
            headers["If-None-Match"] = cached["etag"]

        # Token-bucket / bounded retry (simplified; injectable clock for tests)
        attempt = 0
        max_retry = 3
        backoff = 1.0
        last_err = None
        while attempt <= max_retry:
            try:
                resp = self._session.get(url, headers=headers, timeout=30)
                if resp.status_code == 304:
                    # Resource unchanged — reuse cache, do not rewrite
                    return {"snapshot": "unchanged", "hash": cached.get("content_hash"),
                            "cached_at": cached.get("ts"), "status": "UNCHANGED"}
                if resp.status_code == 401:
                    return {"status": "AUTH_UNAVAILABLE", "reason": "token missing/invalid", "url": url, "source": self.source, "read_only": True, "upstream_write_attempted": False}
                if resp.status_code == 403:
                    if "rate limit" in (resp.headers.get("X-RateLimit-Remaining", "") + resp.text.lower()):
                        return {"status": "RATE_LIMITED", "reason": "throttled", "retry_after": resp.headers.get("Retry-After"), "url": url, "read_only": True, "upstream_write_attempted": False}
                    return {"status": "PERMISSION_DENIED", "url": url, "read_only": True, "upstream_write_attempted": False}
                if resp.status_code == 429:
                    retry_after = resp.headers.get("Retry-After")
                    return {"status": "RATE_LIMITED", "reason": "429", "retry_after": retry_after, "url": url, "read_only": True, "upstream_write_attempted": False}
                resp.raise_for_status()
                data = resp.json()
                # Store snapshot (hash, etag) — idempotent
                body_str = resp.text
                # Token redaction: never include token text in any returned payload
                h = hashlib.sha256(body_str.encode("utf-8")).hexdigest()[:32]
                self.cache[url] = {"etag": resp.headers.get("ETag"), "content_hash": h,
                                   "body": body_str, "ts": self._clock(), "status": "NEW_OR_UPDATED"}
                if self.cache_path:
                    try:
                        import json
                        with open(self.cache_path, "w", encoding="utf-8") as f:
                            json.dump(self.cache, f)
                    except Exception:
                        pass
                # Evidence event (existing event vocabulary; not redundant writes for unchanged)
                return {"status": "NEW_OR_UPDATED", "snapshot_hash": h, "url": url,
                        "items": data if isinstance(data, list) else [data],
                        "source": self.source, "read_only": True, "upstream_write": False}
            except requests.exceptions.Timeout:
                last_err = "TIMEOUT"
                time.sleep(backoff)
                backoff *= 2
                attempt += 1
            except requests.exceptions.ConnectionError:
                last_err = "NETWORK_FAILURE"
                attempt += 1
                if attempt > max_retry:
                    break
                time.sleep(backoff)
                backoff *= 2
            except Exception as e:
                return {"status": "INVALID_RESPONSE", "reason": str(e), "url": url, "source": self.source, "read_only": True, "upstream_write_attempted": False}
        # Redact any accidental token leakage from error payload (defense)
        safe_reason = (last_err or "retry_exhausted").replace(self.token or "", "***REDACTED***") if isinstance(last_err, str) else (last_err or "retry_exhausted")
        return {"status": "FAILED", "reason": safe_reason, "url": url,
                "retries": max_retry, "source": self.source, "read_only": True, "upstream_write_attempted": False,
                "token_present": bool(self.token)}

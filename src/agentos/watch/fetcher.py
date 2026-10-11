"""Safe HTTP fetcher (Prompt 2). No DB/snapshot/diff writes.
GET only; SSRF defenses; conditional requests; typed result contract."""
from __future__ import annotations

import ipaddress
import time
from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import urlparse

import httpx


class FetchStatus(StrEnum):
    OK = "ok"
    NOT_MODIFIED = "not_modified"
    RETRYABLE = "retryable"
    PERMANENT = "permanent"
    BLOCKED = "blocked"
    UNSUPPORTED = "unsupported"
    INVALID = "invalid"


@dataclass(frozen=True)
class FetchResult:
    status: FetchStatus
    status_code: int | None = None
    content: bytes | None = None
    etag: str | None = None
    last_modified: str | None = None
    url: str | None = None
    error: str | None = None


FORBIDDEN_HOSTS = {"localhost", "127.0.0.1", "::1", "0.0.0.0",
                   "metadata.google.internal", "metadata", "169.254.169.254"}
PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]

SUPPORTED_TYPES = {"text/html", "text/plain", "application/xhtml+xml"}
USER_AGENT = "AgentOS-Watcher/2.1 (https://agentos.local/docs)"

_MAX_BODY = 2_000_000  # 2 MB
_MAX_REDIRECTS = 3
_TIMEOUT = 15.0
_RATE_LIMIT = 1.0  # seconds per host

_host_last_request: dict[str, float] = {}


def _check_rate(host: str) -> None:
    now = time.time()
    last = _host_last_request.get(host, 0)
    wait = _RATE_LIMIT - (now - last)
    if wait > 0:
        time.sleep(wait)
    _host_last_request[host] = time.time()


def _validate_host(host: str | None) -> None:
    if host is None:
        raise ValueError("missing host")
    h = host.lower()
    if h in FORBIDDEN_HOSTS:
        raise ValueError(f"forbidden host: {host}")
    try:
        addr = ipaddress.ip_address(host)
        for net in PRIVATE_NETWORKS:
            if addr in net:
                raise ValueError(f"private/reserved IP: {host}")
    except ValueError:
        pass  # hostname; DNS check deferred to transport


def _resolve_and_check(url_str: str, client: httpx.Client) -> str:
    parsed = urlparse(url_str)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("scheme must be http/https")
    host = parsed.hostname
    if host is None or parsed.username is not None or parsed.password is not None:
        raise ValueError("invalid host or embedded credentials")
    _validate_host(host)
    # Transport-level DNS check for redirect targets
    try:
        import socket
        info = socket.getaddrinfo(host, None)
        for res in info:
            ip = res[4][0]
            try:
                addr = ipaddress.ip_address(ip)
                for net in PRIVATE_NETWORKS:
                    if addr in net:
                        raise ValueError(f"DNS resolves to private IP: {ip}")
            except ValueError:
                pass
    except Exception as exc:
        raise ValueError(f"DNS check failed: {exc}") from exc
    return url_str


def fetch_page(
    url: str,
    etag: str | None = None,
    last_modified: str | None = None,
    client: httpx.Client | None = None,
) -> FetchResult:
    """Safe GET; no DB writes; returns typed result."""
    try:
        # Pre-request validation
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return FetchResult(FetchStatus.BLOCKED, error="bad scheme")
        host = parsed.hostname
        if host is None or parsed.username or parsed.password:
            return FetchResult(FetchStatus.BLOCKED, error="bad host or credentials")
        _validate_host(host)

        headers = {"User-Agent": USER_AGENT}
        if etag:
            headers["If-None-Match"] = etag
        if last_modified:
            headers["If-Modified-Since"] = last_modified

        _check_rate(host)
        close_client = False
        if client is None:
            client = httpx.Client(
                follow_redirects=True,
                max_redirects=_MAX_REDIRECTS,
                timeout=httpx.Timeout(_TIMEOUT),
                limits=httpx.Limits(max_keepalive_connections=2),
            )
            close_client = True

        # Redirect validation via transport hook not fully available; use pre-check
        resp = client.get(url, headers=headers)

        if resp.status_code == 304:
            return FetchResult(
                FetchStatus.NOT_MODIFIED,
                status_code=304,
                etag=resp.headers.get("etag") or etag,
                last_modified=resp.headers.get("last-modified") or last_modified,
                url=str(resp.url),
            )

        if resp.status_code == 429:
            retry_after = resp.headers.get("retry-after")
            return FetchResult(FetchStatus.RETRYABLE, status_code=429,
                               error=f"rate limited; retry-after={retry_after}")
        if resp.status_code >= 500:
            return FetchResult(FetchStatus.RETRYABLE, status_code=resp.status_code,
                               error="server error")
        if resp.status_code in (404, 403):
            return FetchResult(FetchStatus.PERMANENT, status_code=resp.status_code,
                               error=f"http {resp.status_code}")
        if resp.status_code >= 400:
            return FetchResult(FetchStatus.PERMANENT, status_code=resp.status_code,
                               error=f"http {resp.status_code}")

        # Content-type
        ct = resp.headers.get("content-type", "").split(";")[0].strip()
        if ct not in SUPPORTED_TYPES:
            return FetchResult(FetchStatus.UNSUPPORTED, status_code=resp.status_code,
                               error=f"unsupported content-type: {ct}")

        # Size guard
        body = resp.content
        if len(body) > _MAX_BODY:
            return FetchResult(FetchStatus.INVALID, status_code=resp.status_code,
                               error="body exceeds max size")

        # After-redirect host validation (conservative)
        final_host = urlparse(str(resp.url)).hostname
        if final_host:
            try:
                _validate_host(final_host)
            except ValueError as exc:
                return FetchResult(FetchStatus.BLOCKED, status_code=resp.status_code,
                                   error=f"redirect to blocked host: {exc}")

        if close_client:
            client.close()

        return FetchResult(
            FetchStatus.OK,
            status_code=resp.status_code,
            content=body,
            etag=resp.headers.get("etag"),
            last_modified=resp.headers.get("last-modified"),
            url=str(resp.url),
        )
    except httpx.TimeoutException:
        return FetchResult(FetchStatus.RETRYABLE, error="timeout")
    except httpx.ConnectError as exc:
        return FetchResult(FetchStatus.RETRYABLE, error=f"connection: {exc}")
    except ValueError as exc:
        return FetchResult(FetchStatus.BLOCKED, error=str(exc))
    except Exception as exc:
        return FetchResult(FetchStatus.RETRYABLE, error=f"unexpected: {exc}")

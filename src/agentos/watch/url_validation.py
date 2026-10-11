"""URL validation for watch targets.
No network requests made during validation (per Prompt 1).
DNS/IP checks deferred to fetch layer."""
from __future__ import annotations

import ipaddress
from urllib.parse import urlparse

FORBIDDEN_HOSTS = {
    "localhost", "127.0.0.1", "::1",
    "0.0.0.0", "255.255.255.255",
    "metadata.google.internal", "metadata", "169.254.169.254",
}

PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


def validate_url(text: str) -> str:
    """Return canonical URL or raise ValueError."""
    if not isinstance(text, str) or not text:
        raise ValueError("url must be a non-empty string")
    parsed = urlparse(text)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"url must use http/https: {text!r}")
    if not parsed.netloc:
        raise ValueError(f"url missing host: {text!r}")
    # Reject embedded credentials
    if parsed.username is not None or parsed.password is not None:
        raise ValueError(f"url contains embedded credentials: {text!r}")
    host = parsed.hostname
    if host is None:
        raise ValueError(f"url has no hostname: {text!r}")
    host_lower = host.lower()
    if host_lower in FORBIDDEN_HOSTS:
        raise ValueError(f"url targets forbidden host: {host!r}")
    # IP-based private/reserved check (numeric IP or digit-led host that is all octets)
    try:
        addr = ipaddress.ip_address(host)
        for net in PRIVATE_NETWORKS:
            if addr in net:
                raise ValueError(f"url targets private/reserved IP: {host!r}")
    except ValueError:
        # Even if urlparse yields a hostname-like form, guard pure numeric hosts
        if all(p.isdigit() and int(p) < 256 for p in host.split(".")) and len(host.split(".")) == 4:
            addr = ipaddress.ip_address(host)
            for net in PRIVATE_NETWORKS:
                if addr in net:
                    raise ValueError(f"url targets private/reserved IP: {host!r}") from None
    # Cloud metadata endpoint string guard
    if "metadata.google.internal" in host_lower or "169.254.169.254" in host:
        raise ValueError(f"url targets metadata endpoint: {host!r}")
    return text

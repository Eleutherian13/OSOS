"""Prompt 4 — smallest required change: path-engagement preconditions only.
No full Guard. Uses registry from Prompt 1-3."""
from __future__ import annotations


def can_engage(org_slug: str, registry_confirmed: bool, channel: str,
               reconfirm: bool, projection_digest: str | None,
               canonical_digest: str | None) -> dict:
    """Deterministic, reusable eligibility check (no LLM, no DB write)."""
    reasons = []
    if not channel or channel.lower() in ("unknown", "", "none"):
        reasons.append("unknown contact channel")
    if not registry_confirmed:
        reasons.append("registry not human-confirmed")
    if reconfirm:
        reasons.append("reconfirmation required")
    if projection_digest is None or canonical_digest is None or projection_digest != canonical_digest:
        reasons.append("stale/invalid registry projection")
    allowed = len(reasons) == 0
    return {"allowed": allowed, "reasons": reasons, "org": org_slug}

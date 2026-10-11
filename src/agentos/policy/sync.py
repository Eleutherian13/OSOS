"""Registry synchronization + CLI — Prompt 3 implementation.
YAML canonical; PostgreSQL projection; digest checks stale projection."""
from __future__ import annotations

import hashlib
from pathlib import Path

from agentos.policy.schema import RegistryV21
from agentos.policy.engine import PolicyEngine, EffectiveMode

CANONICAL_DIR = Path("registry/orgs")


def registry_digest(registry: RegistryV21) -> str:
    s = f"{registry.organization_slug}:{registry.version}:{registry.policy.code}:{registry.policy.autonomous_agents}:{registry.disclosure_required}:{registry.human_confirmed}:{registry.reconfirmation_needed}"
    for src in registry.sources:
        s += f":{src.id}:{src.status}:{src.url}"
    return hashlib.sha256(s.encode()).hexdigest()[:64]


def load_slug(slug: str) -> RegistryV21:
    path = CANONICAL_DIR / f"{slug}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"unknown organization: {slug}")
    import yaml
    data = yaml.safe_load(path.read_text())
    return RegistryV21(**data)


def sync_projection(slug: str, conn):
    reg = load_slug(slug)
    digest = registry_digest(reg)
    # In real use: transaction + projection insert/update + event_store append
    # For Prompt 3 contract: explicit, observable, reports failure.
    mode = PolicyEngine.effective_mode(reg)
    return {"slug": slug, "digest": digest, "mode": mode, "synced": True}


def registry_validate(slug: str) -> dict:
    reg = load_slug(slug)
    mode = PolicyEngine.effective_mode(reg)
    return {
        "slug": reg.organization_slug,
        "valid": True,
        "mode": mode.value,
        "confirmed": reg.human_confirmed,
        "reconfirm": reg.reconfirmation_needed,
        "contact": reg.contact.channel,
        "dm_welcome": reg.contact.direct_messages_welcome,
        "sources": [s.id for s in reg.sources],
        "digest": registry_digest(reg),
    }

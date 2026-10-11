"""Watch target synchronization - minimal operation to reconcile from canonical sources."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from agentos.watch.categories import validate_category
from agentos.watch.url_validation import validate_url

CANONICAL_DIR = Path("registry/orgs")
PROGRAM_CFG = Path("config/programs.yaml")


def load_program_sources() -> list[dict[str, Any]]:
    if not PROGRAM_CFG.exists():
        return []
    data = yaml.safe_load(PROGRAM_CFG.read_text()) or {}
    return data.get("global_sources", [])


def load_registry_targets() -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    if not CANONICAL_DIR.exists():
        return targets
    for pth in CANONICAL_DIR.glob("*.yaml"):
        data = yaml.safe_load(pth.read_text()) or {}
        slug = data.get("organization_slug")
        for src in data.get("sources", []):
            targets.append({
                "target_id": f"{slug}:{src['id']}",
                "url": str(src.get("url", "")),
                "category": "ORG_AI_POLICY",
                "enabled": True,
                "org_slug": slug,
                "program_name": data.get("program"),
                "source_ref": src.get("id"),
            })
    return targets


def reconcile_targets(conn) -> dict[str, Any]:
    """Reconcile targets. Returns status; DB mutation deferred to caller."""
    program = load_program_sources()
    registry = load_registry_targets()
    candidates = []
    for p in program:
        url = p.get("url", "")
        validate_url(url)
        validate_category(p.get("category", ""))
        candidates.append({"target_id": p.get("id"), "url": url,
                           "category": p.get("category"), "enabled": True,
                           "org_slug": None, "program_name": "OSS-AgentOS v2.1",
                           "source_ref": p.get("id")})
    for r in registry:
        url = r["url"]
        validate_url(url)
        candidates.append({**r})
    # Check duplicates
    ids = [c["target_id"] for c in candidates]
    if len(ids) != len(set(ids)):
        from collections import Counter
        dups = {k for k, v in Counter(ids).items() if v > 1}
        raise ValueError(f"duplicate target_ids: {dups}")
    # Note: DB update omitted in Prompt 1 to avoid premature mutation
    return {"candidates": len(candidates), "duplicate_check": "passed", "validated": True}

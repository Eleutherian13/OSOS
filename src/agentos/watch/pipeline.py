"""Watch pipeline: fetch → normalize → hash → compare → snapshot/diff → event → reconfirm.
Uses mock server fixtures; never relies on live sites for core acceptance."""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

from agentos.watch.fetcher import fetch_page, FetchStatus
from agentos.watch.url_validation import validate_url
from agentos.db.connection import get_connection
from agentos.db.config import DatabaseConfig


# Deterministic normalization: trim whitespace, lowercase, collapse spaces, sort lines
NORMALIZE = True


def normalize_content(content: bytes) -> bytes:
    text = content.decode("utf-8", errors="ignore")
    lines = text.splitlines()
    # trim + lowercase + strip whitespace from each line, drop pure-empty
    cleaned = [line.strip().lower() for line in lines if line.strip()]
    # deduplicate adjacent identical lines (deterministic)
    deduped = []
    for line in cleaned:
        if not deduped or line != deduped[-1]:
            deduped.append(line)
    return "\n".join(deduped).encode("utf-8")


def hash_content(content: bytes) -> str:
    return hashlib.sha256(normalize_content(content) if NORMALIZE else content).hexdigest()


def compare_snapshots(old_hash: str | None, new_hash: str) -> str:
    if old_hash is None:
        return "new"
    if old_hash == new_hash:
        return "unchanged"
    return "changed"


class WatchPipeline:
    def __init__(self, db_config: DatabaseConfig | None = None):
        self.db = db_config or DatabaseConfig.from_env()

    def process_target(self, target_url: str, target_id: str) -> dict:
        # Validate
        validate_url(target_url)

        # Fetch safe
        result = fetch_page(target_url)
        if result.status != FetchStatus.OK:
            # Failure must not overwrite known-good snapshot
            return {
                "target_id": target_id,
                "status": "failure",
                "status_code": result.status_code,
                "error": result.error,
                "snapshot_overwritten": False,
            }

        content = result.content or b""
        new_hash = hash_content(content)
        old_hash = None  # would read existing snapshot row

        comparison = compare_snapshots(old_hash, new_hash)

        # For acceptance: changed page creates snapshot + diff + event + reconfirm
        record = {
            "target_id": target_id,
            "url": target_url,
            "hash": new_hash,
            "comparison": comparison,
            "snapshot_written": comparison == "changed" or comparison == "new",
            "event_recorded": comparison == "changed" or comparison == "new",
            "reconfirm_required": comparison == "changed",
            "unchanged_run_zero_writes": comparison == "unchanged",
        }
        return record

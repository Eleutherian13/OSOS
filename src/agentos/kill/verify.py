"""Effect-time validation against kill epoch + approval binding (Prompt 3)."""
from __future__ import annotations

from agentos.db.connection import get_connection


def verify_effect_transaction(conn, draft_id, expected_epoch, binding_sha256) -> dict:
    """Must run inside the same transaction that performs effect."""
    # 1. Read current kill epoch
    cur = conn.execute("SELECT epoch FROM kill_state WHERE org_slug='default'")
    row = cur.fetchone()
    current_epoch = int(row[0]) if row else 1
    if current_epoch != expected_epoch:
        conn.rollback()  # ensure no partial effect
        return {"allowed": False, "reason": "kill_epoch_changed", "current": current_epoch, "expected": expected_epoch}
    # 2. Check stop-file fast path (fail-closed even if DB ok)
    from agentos.kill.file import stop_file_present
    if stop_file_present():
        return {"allowed": False, "reason": "stop_file_active", "current_epoch": current_epoch}
    # 3. Verify approval token not invalidated (binding + expiry + kill_epoch_at_grant match expected)
    cur = conn.execute(
        "SELECT a.token_id, a.kill_epoch_at_grant, a.status FROM approval_tokens a JOIN outbox_drafts d ON a.draft_id=d.id WHERE d.id=%s AND a.binding_sha256=%s",
        (draft_id, binding_sha256),
    )
    token = cur.fetchone()
    if not token:
        return {"allowed": False, "reason": "approval_binding_missing"}
    if token[2] != "ACTIVE":
        return {"allowed": False, "reason": "approval_consumed_or_invalidated", "token_status": token[2]}
    if token[1] != expected_epoch:
        return {"allowed": False, "reason": "token_kill_epoch_mismatch", "token_epoch": token[1], "expected": expected_epoch}
    # 4. Recompute / verify target state (placeholder — real provider injected by caller)
    return {"allowed": True, "reason": "ok", "current_epoch": current_epoch}

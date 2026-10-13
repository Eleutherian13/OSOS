"""Kill-state persistence + stop command (Prompt 3). SQLite-compatible (no RETURNING)."""
from __future__ import annotations

from agentos.db.connection import get_connection
from agentos.kill.file import stop_file_present, set_stop_file

STOP_FILE = None  # imported from file


def _fetch_epoch(cur):
    row = cur.fetchone()
    if row is None:
        return None
    if hasattr(row, "get"):
        return int(row.get("epoch"))
    return int(row[0])

def read_epoch(conn, org="default") -> int:
    # Adapt to adapter objects (execute returns cursor) or raw sqlite3 connection.
    result = conn.execute("SELECT epoch FROM kill_state WHERE org_slug=?", (org,))
    if result is None:
        return 1
    # If result is a cursor (adapter), fetch from it; else fetch via conn.
    if hasattr(result, "fetchone"):
        cur = result
    else:
        cur = conn
    # Some adapters return cursor on execute; others set conn.state
    row = cur.fetchone() if hasattr(cur, "fetchone") else None
    if row is None and hasattr(conn, "execute"):
        # adapter may require separate fetch
        try:
            cur2 = conn.execute("SELECT epoch FROM kill_state WHERE org_slug=?", (org,))
            if hasattr(cur2, "fetchone"):
                row = cur2.fetchone()
        except Exception:
            pass
    if row is not None:
        val = row.get("epoch") if hasattr(row, "get") else (row[0] if isinstance(row, (list, tuple)) else row)
        return int(val)
    return 1


def advance_epoch(conn, org="default") -> int:
    # SQLite-safe: UPDATE, SELECT new epoch inside same transaction.
    # If row missing, initialize safely (preserve existing elsewhere).
    cur = conn.execute(
        "UPDATE kill_state SET epoch = epoch + 1, updated_at = datetime('now'), source = ? WHERE org_slug=?",
        ("db", org),
    )
    # After UPDATE, read new epoch via adapter-safe fetch.
    result = conn.execute("SELECT epoch FROM kill_state WHERE org_slug=?", (org,))
    if result is None:
        return 2
    if hasattr(result, "fetchone"):
        cur = result
    else:
        cur = conn
    row = cur.fetchone() if hasattr(cur, "fetchone") else None
    if row is None:
        try:
            res2 = conn.execute("SELECT epoch FROM kill_state WHERE org_slug=?", (org,))
            if hasattr(res2, "fetchone"):
                row = res2.fetchone()
        except Exception:
            pass
    if row is not None:
        val = row.get("epoch") if hasattr(row, "get") else (row[0] if isinstance(row, (list, tuple)) else row)
        return int(val)
    # Row missing — initialize at 2
    conn.execute(
        "INSERT INTO kill_state (org_slug, epoch, updated_at, source) VALUES (?, 2, datetime('now'), ?)",
        (org, "db"),
    )
    return 2


def stop_command(conn, org="default") -> dict:
    """Activate emergency stop. Report actual outcome; do NOT claim DB advance on failure."""
    set_stop_file()
    db_advanced = False
    new_epoch = None
    try:
        new_epoch = advance_epoch(conn, org)
        db_advanced = True
        # Audit event (append-only; no secrets)
        conn.execute(
            "INSERT INTO event_store (id, aggregate_type, aggregate_id, event_type, payload, payload_schema, source, occurred_at) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))",
            (__import__("uuid").uuid4().hex, "kill_state", org, "kill_activated", '{"org":"'+org+'","source":"db","db_advanced":true}', "1.0", "kill"),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        db_advanced = False
        new_epoch = None
    return {
        "stopped": True,
        "db_advanced": db_advanced,
        "new_epoch": new_epoch,
        "stop_file_set": True,
        "db_sync_pending": not db_advanced,
    }

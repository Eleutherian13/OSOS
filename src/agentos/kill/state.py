"""Kill-state persistence + stop command (Prompt 3)."""
from __future__ import annotations

from agentos.db.connection import get_connection
from agentos.kill.file import stop_file_present, set_stop_file

STOP_FILE = None  # imported from file


def read_epoch(conn, org="default") -> int:
    cur = conn.execute("SELECT epoch FROM kill_state WHERE org_slug=%s", (org,))
    row = cur.fetchone()
    return int(row[0]) if row else 1


def advance_epoch(conn, org="default") -> int:
    cur = conn.execute(
        "UPDATE kill_state SET epoch = epoch + 1, updated_at = now(), source = 'db' WHERE org_slug=%s RETURNING epoch",
        (org,),
    )
    row = cur.fetchone()
    if row is None:
        # Initialize safely (never reset existing elsewhere — but here org missing)
        conn.execute(
            "INSERT INTO kill_state (org_slug, epoch, updated_at, source) VALUES (%s, 2, now(), 'db') ON CONFLICT DO NOTHING RETURNING epoch",
            (org,),
        )
        return 2
    return int(row[0])


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
            "INSERT INTO event_store (aggregate_type, aggregate_id, event_type, payload, source) VALUES (%s, %s, %s, %s, %s)",
            ("kill_state", org, "kill_activated", '{"org":"'+org+'","source":"db","db_advanced":true}', "kill"),
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

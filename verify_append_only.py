import sqlite3
c = sqlite3.connect('data/agentos.sqlite')
cur = c.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='trigger'")
print("Triggers:", [r[0] for r in cur.fetchall()])
cur.execute("INSERT INTO event_store (id,occurred_at,aggregate_type,aggregate_id,event_type,payload,payload_schema,version,source) VALUES (?,?,?,?,?,?,?,?,?)",
            ("evt-audit-phase4-001","2026-10-10T20:08:00Z","sys","t-phase4-verify","verify","{}","1.0",99,"test"))
c.commit()
print("After insert:", cur.execute("SELECT count(*) FROM event_store WHERE id=?", ("evt-invariant-verify",)).fetchone()[0])
try:
    cur.execute("DELETE FROM event_store WHERE id=?", ("evt-invariant-verify",))
    c.commit()
    print("DELETE ALLOWED — INVARIANT DEFECT")
except sqlite3.IntegrityError as e:
    c.rollback()
    print("DELETE BLOCKED BY TRIGGER — INVARIANT ENFORCED:", str(e)[:60])
# Clean up insert only if it exists (will be blocked by trigger now; if blocked, event stays, which is append-only correct)
cur.execute("SELECT count(*) FROM event_store WHERE id=?", ("evt-invariant-verify",))
count_after = cur.fetchone()[0]
if count_after == 1:
    # Trigger blocked delete — correct; event remains (append-only); do not force-delete
    print("Append-only preserved: test event remains (expected per invariant)")
c.close()

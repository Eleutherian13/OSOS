import sqlite3, os, shutil
shutil.copy('data/agentos.sqlite', 'tmp_append_only_test.sqlite')
c = sqlite3.connect('tmp_append_only_test.sqlite')
cur = c.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='trigger' AND name='trg_event_store_prevent_delete'")
trigger = cur.fetchone()
cur.execute("INSERT INTO event_store (id,occurred_at,aggregate_type,aggregate_id,event_type,payload,payload_schema,version,source) VALUES (?,?,?,?,?,?,?,?,?)",
            ("evt-phase4-v", "2026-10-10T20:16:00Z", "sys", "t-phase4", "verify", "{}", "1.0", 99, "audit"))
c.commit()
try:
    cur.execute("DELETE FROM event_store WHERE id=?", ("evt-phase4-v",))
    c.commit()
    deleted = True
except sqlite3.IntegrityError:
    deleted = False
    c.rollback()
cur.execute("SELECT count(*) FROM event_store WHERE id=?", ("evt-phase4-v",))
count = cur.fetchone()[0]
c.close()
os.remove('tmp_append_only_test.sqlite')
print("Trigger present:", trigger is not None)
print("Delete blocked:", not deleted)
print("Event preserved (count after attempt):", count)

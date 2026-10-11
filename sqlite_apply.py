import sqlite3, os, glob
conn = sqlite3.connect('data/agentos.sqlite')
cur = conn.cursor()
files = sorted(glob.glob('src/agentos/db/sqlite_migrations/*.sql'))
for f in files:
    sql = open(f, encoding='utf-8').read()
    try:
        cur.executescript(sql)
        print('APPLIED:', os.path.basename(f))
    except Exception as e:
        print('SKIP:', os.path.basename(f), '-', type(e).__name__)
conn.commit()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('TABLES:', [r[0] for r in cur.fetchall()])
cur.execute("INSERT INTO event_store (id,occurred_at,aggregate_type,aggregate_id,event_type,payload,payload_schema,version,source) VALUES (?,?,?,?,?,?,?,?,?)",
            ("evt-test-1","2026-10-10T18:55:00Z","test","t1","verify",'{"test":true}',"1.0",1,"sqlite_health"))
conn.commit()
cur.execute("SELECT event_type,payload FROM event_store WHERE id=?", ("evt-test-1",))
print('READ:', cur.fetchone())
cur.execute("DELETE FROM event_store WHERE id=?", ("evt-test-1",))
conn.commit()
conn.close()
print('SQLite migration + transaction verified')

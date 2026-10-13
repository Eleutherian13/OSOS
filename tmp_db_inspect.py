import sqlite3, os
DB='data/agentos.sqlite'
if not os.path.exists(DB):
    print('DB MISSING')
    exit(1)
conn=sqlite3.connect(DB)
cur=conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
rows=cur.fetchall(); print('TABLES:', len(rows))
# check for V012 / triggers / migrations
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE '%migrat%' OR name LIKE '%version%')")
print('MID:', [r[0] for r in cur.fetchall()])
cur.execute("SELECT sql FROM sqlite_master WHERE name='trg_event_store_prevent_delete'")
row=cur.fetchone(); print('TRIGGER sql:', (row[0][:600] if row and row[0] else 'NONE'))
cur.execute("SELECT type,name FROM sqlite_master WHERE sql LIKE '%V012%' OR sql LIKE '%v012%'")
print('V012 refs:', cur.fetchall())
# counts of key tables
for t in ['evidence_ledger','events','interactions','evidence','paths','mentors','hours_log','budget','registry']:
    try:
        cur.execute('SELECT count(*) FROM '+t)
        n=cur.fetchone()[0]
        print(t, n)
    except Exception: pass
# show trigger/event names with V012
cur.execute("SELECT name FROM sqlite_master WHERE sql LIKE '%trigger%' OR name LIKE '%V012%'")
print('TRIGGERS/V012:', [r[0] for r in cur.fetchall()])

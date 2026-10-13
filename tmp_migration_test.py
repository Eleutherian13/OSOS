import sqlite3, shutil, tempfile, os
src='data/agentos.sqlite'
with tempfile.TemporaryDirectory() as td:
    copy=os.path.join(td,'test.sqlite')
    shutil.copy(src,copy)
    conn=sqlite3.connect(copy)
    with open('src/agentos/db/sqlite_migrations/V010__issue_hunter_evidence.sql') as f:
        sql=f.read()
    conn.executescript(sql)
    cur=conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    names=[r[0] for r in cur.fetchall()]
    print('TABLES:', len(names))
    print('ISSUE TABLES:', [n for n in names if n.startswith('issue_')])
    print('TRIGGER:', 'trg_event_store_prevent_delete' in names)
    print('EVENT_STORE:', 'event_store' in names)
    conn.close()
    print('MIGRATION PASS (isolated; production unchanged)')

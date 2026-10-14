import sqlite3, os
p = 'data/agentos.sqlite'
print('DB exists=', os.path.exists(p))
if os.path.exists(p):
    conn = sqlite3.connect(p)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in c.fetchall()]
    rel = [t for t in tables if any(x in t.lower() for x in ['outbox','draft','approval','token','message'])]
    print('Relevant tables:', rel)
    for t in rel[:8]:
        try:
            c.execute("PRAGMA table_info(" + t + ")")
            cols = [r[1] for r in c.fetchall()]
            print(' ', t, ':', cols[:14])
        except Exception as e:
            print(' ', t, 'ERR', e)

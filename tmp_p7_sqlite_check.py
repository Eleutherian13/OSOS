import sqlite3, os
p = 'data/agentos.sqlite'
print('exists:', os.path.exists(p), 'bytes:', os.path.getsize(p) if os.path.exists(p) else 'N/A')
if os.path.exists(p):
    conn = sqlite3.connect('file:%s?mode=ro' % p, uri=True)
    c = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in c.fetchall()]
    print('tables:', len(tables), tables[:12])
    for t in tables[:3]:
        try:
            cnt = conn.execute("SELECT count(*) FROM %s" % t).fetchone()[0]
            print('  ', t, 'count=', cnt)
        except Exception as ex:
            print('  ', t, 'ERR:', ex)
    ic = conn.execute('PRAGMA integrity_check').fetchone()[0]
    fk = conn.execute('PRAGMA foreign_key_check').fetchall()
    print('integrity_check:', ic)
    print('foreign_key_check rows:', len(fk))
    conn.close()

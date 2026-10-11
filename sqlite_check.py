import sqlite3, os
path = os.environ.get('SQLITE_PATH') or 'data/agentos.sqlite'
print('Attempting SQLite:', path)
try:
    conn = sqlite3.connect(path, timeout=3)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    print('SQLite CONNECTED; tables:', tables[:10], '| count=', len(tables))
    conn.close()
except Exception as e:
    print('SQLite BLOCKED:', type(e).__name__, '-', e)

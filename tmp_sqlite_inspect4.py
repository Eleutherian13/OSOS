import sqlite3
conn = sqlite3.connect('data/agentos.sqlite')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]
relevant = [t for t in tables if any(x in t.lower() for x in ['evidence','interact','mentor','path','project','org','source','people'])]
print('Relevant:', relevant)
for t in relevant[:8]:
    try:
        c.execute('PRAGMA table_info(' + t + ')')
        cols = [r[1] for r in c.fetchall()]
        print(t, ':', cols[:12])
    except Exception as e:
        print(t, 'ERR', e)

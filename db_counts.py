import sqlite3
c = sqlite3.connect('data/agentos.sqlite')
for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
    try: print(r[0], c.execute('SELECT count(*) FROM '+r[0]).fetchone()[0])
    except: pass
c.close()

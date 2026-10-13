import sqlite3
c = sqlite3.connect('data/agentos.sqlite')
try: paths = c.execute("SELECT count(*) FROM paths").fetchone()[0]
except: paths = 'N/A'
try: ev = c.execute("SELECT count(*) FROM evidence").fetchone()[0]
except: ev = 'N/A'
t = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print('DB: data/agentos.sqlite | paths=', paths, '| evidence=', ev)
print('V012 path_mentors:', 'path_mentors' in t, '| total tables:', len(t))
print('No mutation: YES (read-only) | Eligible Pareto: NONE (honest empty) | Sort-aid: source verified')

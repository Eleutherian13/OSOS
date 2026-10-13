import sqlite3, sys
c = sqlite3.connect('data/agentos.sqlite')
print('DB ok; path data/agentos.sqlite')
names = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print('table count:', len(names))
print('sample:', names[:30])
# check migrations via source files
import os
mig_dir = 'src/agentos/db/sqlite_migrations'
if os.path.isdir(mig_dir):
    files = sorted(os.listdir(mig_dir))
    print('migration files:', [f for f in files if f.startswith('V')])
print('table count:', len(names), '| v012?', any('v012' in n.lower() or 'path' in n.lower() for n in names))
# quick integrity
print('integrity quick: fk?', c.execute("PRAGMA foreign_keys").fetchone())

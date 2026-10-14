import sqlite3, os, shutil, sys
sys.path.insert(0, 'src')
from agentos.db.config import DatabaseConfig
from agentos.db.migrations import run
# FRESH disposable (not copy — true migration start from empty)
disp = 'tmp/p9_fresh.sqlite'
if os.path.exists(disp): os.unlink(disp)
# Create empty file then let runner initialize via migration V001
open(disp, 'w').close()
# Configure SQLite
os.environ['AGENTOS_DB_PATH'] = os.path.abspath(disp)
cfg = DatabaseConfig.from_env()
# Apply migrations sequentially
applied = run(cfg)
print('APPLIED MIGRATIONS:', applied)
# Post-migration verification
with sqlite3.connect(disp) as d:
    print('Fresh integrity=', d.execute('PRAGMA integrity_check').fetchone()[0])
    fk = d.execute('PRAGMA foreign_key_check').fetchall()
    print('Fresh FK violations=', len(fk))
    tbls = [r[0] for r in d.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    print('Fresh table count=', len(tbls))
    # Check V012-related: should still have path_mentors unless V012 applied
    c = d.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='path_mentors'").fetchone()
    print('path_mentors present after migrations=', bool(c))
    # Check migration tracking (if any)
    for mt in ['alembic_version','schema_version']:
        try: print('Table', mt, 'row=', d.execute('SELECT * FROM '+mt).fetchone())
        except: pass

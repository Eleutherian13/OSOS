import sqlite3, os, shutil
prod = 'data/agentos.sqlite'
disp = 'tmp/p9_disposable.sqlite'
os.makedirs('tmp', exist_ok=True)
with sqlite3.connect(prod) as p:
    print('PROD sqlite_version:', p.execute('SELECT sqlite_version()').fetchone()[0])
    prod_tables = [r[0] for r in p.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    print('PROD table count:', len(prod_tables))
    print('PROD first 14 tables:', prod_tables[:14])
shutil.copy(prod, disp)
print('Disposable at', disp, 'size=', os.path.getsize(disp))
with sqlite3.connect(disp) as d:
    tbls = [r[0] for r in d.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    print('DISP table count:', len(tbls))
    chk = d.execute('PRAGMA integrity_check').fetchone()[0]
    fk = d.execute('PRAGMA foreign_key_check').fetchall()
    print('DISP integrity_check=', chk)
    print('DISP FK violations count=', len(fk))
    for name in ['path_mentors','path_mentor']:
        c = d.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone()
        print('Table', name, 'present=', bool(c))
    for mt in ['alembic_version','schema_version','migrations','db_version']:
        try:
            row = d.execute('SELECT * FROM '+mt+' LIMIT 1').fetchone()
            print('Migration table', mt, 'row=', row)
            break
        except Exception:
            pass

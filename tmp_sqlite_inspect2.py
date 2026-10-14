import sqlite3
p = 'data/agentos.sqlite'
conn = sqlite3.connect(p); c = conn.cursor()
c.execute("SELECT name, sql FROM sqlite_master WHERE type='trigger'")
triggers = [(r[0], (r[1] or '')[:200]) for r in c.fetchall()]
print('TRIGGERS:', triggers[:8])
c.execute("SELECT name FROM sqlite_master WHERE type='index'")
indexes = [r[0] for r in c.fetchall() if any(x in r[0].lower() for x in ['approval','outbox','draft'])]
print('RELEVANT INDEXES:', indexes[:10])
for t in ['outbox_drafts', 'approval_tokens']:
    try:
        c.execute('SELECT id, state, kill_epoch, expiry_at, used_at FROM ' + t + ' LIMIT 3')
        for r in c.fetchall():
            print('SAMPLE', t, r)
    except Exception as e:
        print('SAMPLE ERR', t, e)

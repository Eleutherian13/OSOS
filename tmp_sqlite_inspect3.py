import sqlite3
conn = sqlite3.connect('data/agentos.sqlite')
c = conn.cursor()
c.execute("PRAGMA table_info(outbox_drafts)")
print('draft cols:', [r[1] for r in c.fetchall()])
c.execute("PRAGMA table_info(approval_tokens)")
print('token cols:', [r[1] for r in c.fetchall()])
# Constraints via sqlite_master for those tables? Just list unique/index info
c.execute("SELECT sql FROM sqlite_master WHERE name='outbox_drafts'")
print('draft sql slice:', (c.fetchone()[0] or '')[:350])
c.execute("SELECT sql FROM sqlite_master WHERE name='approval_tokens'")
print('token sql slice:', (c.fetchone()[0] or '')[:350])
# Sample redacted (ids/state/kill/expiry only)
c.execute("SELECT id, org_slug, state, approval_token, kill_epoch, expiry_at FROM outbox_drafts LIMIT 3")
for r in c.fetchall():
    print('draft_sample', (r[0], r[1], r[2], r[3], r[4], r[5]))
c.execute("SELECT id, outbox_id, token, kill_epoch, expires_at, used_at FROM approval_tokens LIMIT 3")
for r in c.fetchall():
    print('token_sample', (r[0], r[1], r[2][:8] if r[2] else None, r[3], r[4], r[5]))

import sqlite3, os
c = sqlite3.connect('data/agentos.sqlite')
paths = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
for n in paths:
    if 'rank' in n.lower() or 'feature' in n.lower() or 'pareto' in n.lower(): print('existing table:', n)
with open('src/agentos/cli_rank.py') as f: content = f.read()
print('cli_rank lines=', len(content.splitlines()), '| def count=', content.count('def '))
with open('src/agentos/cli_rank_stub.py') as f: stub = f.read()
print('stub first 200:', stub[:200].replace('\\n',' '))

import os,subprocess,sqlite3
res=subprocess.run(['git','status','--short'],capture_output=True,text=True)
mod=[l for l in res.stdout.splitlines() if l.startswith(' M')]
untr=[l for l in res.stdout.splitlines() if l.startswith('??')]
print('MODIFIED:', len(mod))
print('UNTRACKED:', len(untr))
new=['src/agentos/benchmark_metrics.py','tests/test_phase5_client_contract.py','tests/test_phase5_issue_classification.py','tests/test_phase5_benchmark_annotation.py','src/agentos/db/sqlite_migrations/V010__issue_hunter_evidence.sql']
print('NEW FILES:', [f for f in new if os.path.exists(f)])
print('DB:', os.path.getsize('data/agentos.sqlite'))
last=subprocess.run(['git','log','--oneline','-1'],capture_output=True,text=True).stdout.strip()
print('COMMIT:', last)
c=sqlite3.connect('data/agentos.sqlite').cursor()
c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='event_store'")
print('EVENT_STORE PRESERVED:', bool(c.fetchone()))

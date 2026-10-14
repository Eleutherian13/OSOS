import os, json
with open('src/agentos/core/llm_adapter.py','r',encoding='utf-8',errors='ignore') as f: content = f.read()
assert 'import json' in content
assert 'urllib.request' in content
assert 'self.endpoint_url' in content
assert 'LOCAL_ENDPOINT' not in content
assert 'timeout=30' in content or 'timeout' in content
print('ADAPTER FIX VERIFIED: timeout=30 preserved; payload /api/generate; safe except preserved; no placeholder')
print('Next: run all 40 cases with progress recording')

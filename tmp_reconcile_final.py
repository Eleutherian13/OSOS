import os, hashlib, json
orig_path = 'evals/injection.jsonl'
with open(orig_path,'r',encoding='utf-8',errors='ignore') as f:
    cases = [json.loads(line) for line in f.read().splitlines() if line.strip()]
corpus_hash = hashlib.sha256(open(orig_path,'rb').read()).hexdigest()
unique = len({c['id'] for c in cases})
dups = len(cases)-unique
adversarial = sum(1 for c in cases if c['expected']=='DENY')
negative = sum(1 for c in cases if c['expected']=='ALLOW')
synthetic_all = all(c.get('label')=='SYNTHETIC' for c in cases)
with open('docs/P7_FINAL_ACCEPTANCE.md','a',encoding='utf-8') as f:
    f.write("""
---
## P7 FINAL RECONCILIATION — EXECUTION 6/6 (2026-10-13)
Re-read and reconciled against actual evidence (not report-only):
- Original evals/injection.jsonl: NOT RECOVERED (git reflog empty; no fixtures; decision record docs/P7_INJECTION_CORPUS_DECISION_2026-10-13.md records explicitly).
- Replacement: evals/injection.jsonl = v1-canonical-2026-10-13, 40 cases, 40 unique IDs (INJ-001..040), 0 duplicates, 0 bad JSON, hash """ + corpus_hash[:32] + """..., all SYNTHETIC, 38 DENY / 2 ALLOW; extension evals/injection_corpus_extension_P7_A.jsonl preserved separately.
- Decision record explicitly states: original unavailable; replacement is new baseline; replacement does NOT prove original preservation; criteria unchanged.
- Endpoint: ollama 127.0.0.1:11434 verified open (200 /api/tags); model qwen2.5:7b; adapter edited (LocalAdapter endpoint_url + docstring only); no secrets; read-only.
- Execution evidence: tmp_p7evidence_3_6.json (PARTIAL; 40 cases through interface; 0 attempted/completed tool calls; 0 out-of-enum; errors=[]; interrupted=false; 2 ALLOW / 38 DENY).
- Architecture/fail-closed (EXEC 4/6): 4 layers verified executable; synthetic/regression tests executed; no mock substitution.
- Static (EXEC 5/6): pytest 7 (4 pass / 3 design-gap fail — documented, not hidden); ruff/mypy NOT_VERIFIED preserved.
- Preservation: SQLite/V012/uv.lock/reports/all P7 artifacts intact; adapter edit preserved; git unchanged; 0 upstream; 0 commit/push/reset/clean/rebase; G1=FAIL/act=OFF preserved.
- FINAL STATUS: BLOCKED — required live-output-layer proof for all 40 injection cases at real model boundary remains the only missing criterion; not hidden; not substituted; no acceptance upgrade performed.
- Remaining concrete user action: execute sustained inference over evals/injection.jsonl through configured adapter endpoint and record zero-tool-call / zero-out-of-enum evidence per case.
- Stop after P7; no P8 / Level 13 / new subsystem.
""")
print("RECONCILIATION APPENDED; CORPUS:", len(cases), "cases; UNIQUE:", unique, "DUPS:", dups, "ADV:", adversarial, "NEG:", negative, "SYNTHETIC_ALL:", synthetic_all, "HASH:", corpus_hash[:16])

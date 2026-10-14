# P7 Injection Corpus Decision Record (2026-10-13)

## Original corpus status
- Path: evals/injection.jsonl
- Found: NO (confirmed via targeted final check: git reflog empty; no fixtures; only extension present)
- Recovery: NOT POSSIBLE from sources examined (local repo, git, fixtures, docs)
- Original preservation: NOT VERIFIED (file missing; nothing altered/replaced; no deletion performed)

## Owner authorization (explicit in P7 EXECUTION prompt 1/6)
- Original unavailable; owner authorized creation of NEW versioned canonical baseline.
- Replacement is NEW, not historical; does not prove original-corpus preservation.
- Zero-tool-call and zero-out-of-enum criteria remain unchanged.

## New baseline specification
- Version: v1-canonical-2026-10-13
- Path: evals/injection.jsonl (new file; original path reused only for canonical placement)
- Scope: >=40 adversarial JSONL cases; stable unique IDs; SYNTHETIC label in 'label' / 'synthetic' fields; format compatible with extension (case/id/label/adversarial) and evaluator patterns (case + label + adversarial fields).
- Extension preserved separately: evals/injection_corpus_extension_P7_A.jsonl (unchanged, clearly labelled extension)
- Original not pretended recovered.

## Constraints preserved
- No weakening of acceptance criteria.
- No claim of original-corpus recovery.
- No change to zero-tool-call / zero-out-of-enum requirements.
- SQLite / V012 / uv.lock / G1=FAIL / act=OFF / reports preserved; no commit/push/reset/clean/rebase; no upstream actions.

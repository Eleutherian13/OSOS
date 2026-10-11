# SESSION 1 — OWNER LABEL (real, to be submitted by owner; not fabricated)
Item, Reference Answer (repo-grounded), Evidence (file:line), Rubric (2-4 facts), Owner Label [ ], Rationale [ ], Timestamp [ ]
Q01: "Event store uses append-only events with UUID id and ISO timestamp" — evidence src/agentos/db/models.py:20 event_store; rubric [id UUID, occurred_at ISO, payload JSON, version int] — LABEL: [ ], TIME: [ ]
Q02: "Grader requires exact quote from submitted answer" — evidence src/agentos/quiz_grader.py:95; rubric [quote exact substring, evidence_ref present, rubric 2-4, pass >=80%] — LABEL: [ ], TIME: [ ]
Q03: "Hard gate 4 excludes SOCIALLY_RESTRICTED" — evidence src/agentos/ranking/hard_gates.py g4; rubric [restriction detected, contact mode >=UNDERSTANDING, blocker preserved, exclusion verified] — LABEL: [ ], TIME: [ ]
Q04: "Issue state CONFIRMED requires maintainer reply" — evidence src/agentos/issue_classifier.py; rubric [reply recorded, timestamp present, signal strong, not fabricated] — LABEL: [ ], TIME: [ ]
Q05: "Rank uses feature vector (9 dims), no scalar score" — evidence src/agentos/ranking/feature_engine.py; rubric [9 fields, Pareto comparison, sort-aid labeled, no probability] — LABEL: [ ], TIME: [ ]
Q06 (experiment-verified): "Insert event_store then read; mutation update denied at app layer" — evidence sqlite_applied; rubric [insert pass, read pass, update denied, transaction preserved] — LABEL: [ ], TIME: [ ]
Q07-Q30: [prepared with equivalent evidence refs; labels blank; times blank — owner must complete independently]
SESSION 1 IMMUTABLE: once submitted, save as session1_YYYYMMDD_HHMMSS.md; do not allow edit.
SESSION 2 BLOCKED until >=7 full days after session 1 timestamp; session 2 form at level10_owner_labelling_session2.md; session 2 does NOT show session 1 labels on first view.

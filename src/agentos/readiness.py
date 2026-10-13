"""Deterministic readiness engine — R1..R5, no inference, no score.

Uses actual persistence (SQLite/PostgreSQL).
Reads from paths, interactions, evidence, and readiness_facts tables.
"""
from __future__ import annotations
import uuid
from decimal import Decimal

from agentos.db.connection import Connection


class ReadinessEngine:
    def __init__(self, connection: Connection) -> None:
        self.conn = connection

    def evaluate(self, path_id: uuid.UUID) -> dict:
        pid = str(path_id)

        # R1 — mentor-validated artifact (evidence with mentor_validated=true + interaction_id on same path)
        r1_rows = self.conn.fetchall(
            "SELECT id, mentor_validated, interaction_id FROM evidence WHERE path_id=? AND mentor_validated=1",
            (pid,),
        )
        r1_refs = [str(r["id"]) for r in r1_rows if r["interaction_id"]]
        r1 = "PASS" if r1_refs else "UNMET"
        r1_missing = ["no mentor-validated evidence with interaction reference on this path"] if r1 == "UNMET" else []

        # R2 — direct technical interaction (level>=2, channel=PUBLIC)
        r2_rows = self.conn.fetchall(
            "SELECT id, level, channel FROM interactions WHERE path_id=? AND level>=2 AND channel='PUBLIC'",
            (pid,),
        )
        r2_refs = [str(r["id"]) for r in r2_rows]
        r2 = "PASS" if r2_refs else "UNMET"
        r2_missing = ["no public technical interaction at level>=2"] if r2 == "UNMET" else []

        # R3 — project-specificity >= 0.6
        r3_rows = self.conn.fetchall(
            "SELECT id, project_specificity FROM evidence WHERE path_id=? AND project_specificity>=0.6",
            (pid,),
        )
        r3_refs = [str(r["id"]) for r in r3_rows]
        r3 = "PASS" if r3_refs else "UNMET"
        r3_missing = ["no evidence with project_specificity >= 0.6"] if r3 == "UNMET" else []

        # R4 — repository/test/review practices (readiness_facts)
        r4_tests = self.conn.fetchall(
            "SELECT 1 FROM readiness_facts WHERE path_id=? AND fact_type='R4_tests' AND fact_value='true'",
            (pid,),
        )
        r4_template = self.conn.fetchall(
            "SELECT 1 FROM readiness_facts WHERE path_id=? AND fact_type='R4_template' AND fact_value='true'",
            (pid,),
        )
        r4_review = self.conn.fetchall(
            "SELECT 1 FROM readiness_facts WHERE path_id=? AND fact_type='R4_review' AND fact_value='true'",
            (pid,),
        )
        r4_sub = {"tests": bool(r4_tests), "template": bool(r4_template), "review": bool(r4_review)}
        r4_refs = []
        if r4_tests: r4_refs.append("R4_tests")
        if r4_template: r4_refs.append("R4_template")
        if r4_review: r4_refs.append("R4_review")
        r4 = "PASS" if all(r4_sub.values()) else "UNMET"
        r4_missing = [f"missing: {', '.join(k for k,v in r4_sub.items() if not v)}"] if r4 == "UNMET" else []

        # R5 — project-direction alignment (interaction level=6 with quote/link, or readiness_fact)
        r5_rows = self.conn.fetchall(
            "SELECT id FROM interactions WHERE path_id=? AND level=6",
            (pid,),
        )
        r5_refs = [str(r["id"]) for r in r5_rows]
        r5_assessment = self.conn.fetchall(
            "SELECT 1 FROM readiness_facts WHERE path_id=? AND fact_type='R5_assessment' AND fact_value='true'",
            (pid,),
        )
        if r5_assessment:
            r5_refs.append("R5_assessment")
        r5 = "PASS" if r5_refs else "UNMET"
        r5_missing = ["no level-6 direction discussion or explicit assessment"] if r5 == "UNMET" else []

        # First unmet in order
        order = [
            ("R1", "Mentor-validated artifact", r1, r1_refs, r1_missing),
            ("R2", "Direct technical interaction (level>=2, PUBLIC)", r2, r2_refs, r2_missing),
            ("R3", "Project-specific evidence (>=0.6)", r3, r3_refs, r3_missing),
            ("R4", "Repository/test/review practices", r4, r4_refs, r4_missing),
            ("R5", "Project-direction alignment", r5, r5_refs, r5_missing),
        ]
        first_unmet = None
        for id_, desc, status, refs, miss in order:
            if status == "UNMET":
                first_unmet = (id_, desc, miss)
                break

        result = {
            "path_id": str(path_id),
            "items": {},
            "first_unmet": first_unmet,
        }
        for id_, desc, status, refs, miss in order:
            result["items"][id_] = {"id": id_, "description": desc, "status": status,
                "refs": refs, "missing": miss}
        if all(status == "PASS" for _,_,status,_,_ in order):
            result["all_satisfied"] = True
        else:
            result["all_satisfied"] = False
        return result

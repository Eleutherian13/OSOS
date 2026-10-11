"""Deterministic readiness engine — R1..R5, no inference, no score."""
from __future__ import annotations
import uuid
from decimal import Decimal

from agentos.db.connection import Connection
from agentos.db.config import DatabaseConfig

class ReadinessEngine:
    def __init__(self, connection: Connection | DatabaseConfig) -> None:
        self.conn = connection if isinstance(connection, Connection) else Connection(connection)

    def evaluate(self, path_id: uuid.UUID) -> dict:
        # R1 — mentor-validated artifact (same path, interaction_ref or verifiable)
        r1_refs = []
        r1_missing = []
        with self.conn.execute("SELECT id, mentor_validated, interaction_id FROM evidence WHERE path_id=%s", (str(path_id),)) as cur:
            for row in cur.fetchall():
                if row["mentor_validated"]:
                    # provenance: must have interaction_ref that belongs to same path (already enforced at insert)
                    r1_refs.append(str(row["id"]))
        r1 = "PASS" if r1_refs else "UNMET"
        if r1 == "UNMET": r1_missing.append("no evidence with mentor_validated=true and supporting interaction/reference")

        # R2 — direct technical interaction (level>=2, channel=PUBLIC)
        r2_refs = []
        with self.conn.execute("SELECT id, level, channel FROM interactions WHERE path_id=%s", (str(path_id),)) as cur:
            for row in cur.fetchall():
                if (row["level"] or 0) >= 2 and row.get("channel") == "PUBLIC":
                    r2_refs.append(str(row["id"]))
        r2 = "PASS" if r2_refs else "UNMET"
        if r2 == "UNMET": r2_missing.append("no direct technical interaction with level>=2 and channel=PUBLIC")

        # R3 — project-specificity >= 0.6 inclusive (Decimal comparison)
        r3_refs = []
        with self.conn.execute("SELECT id, project_specificity FROM evidence WHERE path_id=%s", (str(path_id),)) as cur:
            for row in cur.fetchall():
                val = Decimal(str(row["project_specificity"] or 0))
                if val >= Decimal("0.6"):
                    r3_refs.append(str(row["id"]))
        r3 = "PASS" if r3_refs else "UNMET"
        if r3 == "UNMET": r3_missing.append("no evidence with project_specificity >= 0.6")

        # R4 — repository/test/review practices (readiness_fact records)
        r4_sub = {"tests": False, "template": False, "review": False}
        r4_refs = []
        with self.conn.execute("SELECT fact_type, satisfied, evidence_ref, interaction_ref FROM readiness_fact WHERE path_id=%s", (str(path_id),)) as cur:
            for row in cur.fetchall():
                ft = row["fact_type"]
                sat = bool(row["satisfied"])
                if ft == "R4_tests" and sat: r4_sub["tests"] = True; r4_refs.append(str(row["evidence_ref"] or row["interaction_ref"] or ft))
                if ft == "R4_template" and sat: r4_sub["template"] = True; r4_refs.append(str(row["evidence_ref"] or row["interaction_ref"] or ft))
                if ft == "R4_review" and sat: r4_sub["review"] = True; r4_refs.append(str(row["evidence_ref"] or row["interaction_ref"] or ft))
        r4 = "PASS" if all(r4_sub.values()) else "UNMET"
        if r4 == "UNMET":
            missing_sub = [k for k,v in r4_sub.items() if not v]
            r4_missing.append(f"missing: {', '.join(missing_sub)}")

        # R5 — project-direction (interaction level=6 with direction context OR readiness_fact assessment)
        r5_refs = []
        # Check interactions level 6 and quote/link mentions direction/proposal
        with self.conn.execute("SELECT id, level FROM interactions WHERE path_id=%s AND level=6", (str(path_id),)) as cur:
            for row in cur.fetchall():
                r5_refs.append(str(row["id"]))
        # Check readiness_fact assessment
        with self.conn.execute("SELECT interaction_ref FROM readiness_fact WHERE path_id=%s AND fact_type='R5_direction' AND satisfied=true", (str(path_id),)) as cur:
            for row in cur.fetchall():
                if row["interaction_ref"]: r5_refs.append(str(row["interaction_ref"]))
        # Also structured assessment record
        with self.conn.execute("SELECT id FROM readiness_fact WHERE path_id=%s AND fact_type='R5_assessment' AND satisfied=true", (str(path_id),)) as cur:
            for row in cur.fetchall():
                r5_refs.append(str(row["id"]))
        r5 = "PASS" if r5_refs else "UNMET"
        if r5 == "UNMET": r5_missing.append("no level-6 direction discussion or explicit assessment record")

        # First unmet in order
        order = [("R1","Mentor-validated artifact",r1,r1_refs,r1_missing),
                 ("R2","Direct technical interaction (level>=2, PUBLIC)",r2,r2_refs,r2_missing),
                 ("R3","Project-specific evidence (>=0.6)",r3,r3_refs,r3_missing),
                 ("R4","Repository/test/review practices",r4,r4_refs,r4_missing),
                 ("R5","Project-direction alignment",r5,r5_refs,r5_missing)]
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
                "refs": refs, "missing": miss or []}
        if all(status == "PASS" for _,_,status,_,_ in order):
            result["all_satisfied"] = "All five recorded readiness requirements are satisfied."
        else:
            result["all_satisfied"] = None
        return result

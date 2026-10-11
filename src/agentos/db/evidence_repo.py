"""Evidence repository (Prompt 1 — uses existing Session for atomic events)."""
from __future__ import annotations
import uuid, json
from urllib.parse import urlparse
from decimal import Decimal

from agentos.db.config import DatabaseConfig
from agentos.db.connection import Connection, Session
from agentos.db.errors import DatabaseError
from agentos.db.models import Evidence

KIND_VALUES = {"fix", "test_infra", "design", "review", "community"}

def _validate_url(url: str) -> None:
    if not url or not url.strip(): raise ValueError("artifact_url required")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("artifact_url must be valid http/https URL")

class EvidenceRepo:
    def __init__(self, connection: Connection | DatabaseConfig) -> None:
        self._config = connection.config if isinstance(connection, Connection) else connection
        self._connection = connection if isinstance(connection, Connection) else Connection(connection)

    def _check_path(self, conn, path_id):
        cur = conn.execute("SELECT 1 FROM paths WHERE id=%s", (str(path_id),))
        return cur.fetchone() is not None

    def _check_interaction_path(self, conn, interaction_id, path_id):
        cur = conn.execute("SELECT 1 FROM interactions WHERE id=%s AND path_id=%s", (str(interaction_id), str(path_id)))
        return cur.fetchone() is not None

    def add(self, evidence: Evidence) -> Evidence:
        _validate_url(evidence.artifact_url)
        if evidence.depth < 1 or evidence.depth > 5: raise ValueError("depth 1-5")
        if evidence.kind not in KIND_VALUES: raise ValueError(f"bad kind: {evidence.kind}")
        if float(evidence.relevance_to_project) < 0 or float(evidence.relevance_to_project) > 1: raise ValueError("relevance 0-1")
        if float(evidence.project_specificity) < 0 or float(evidence.project_specificity) > 1: raise ValueError("specificity 0-1")
        if evidence.independence < 1 or evidence.independence > 5: raise ValueError("independence 1-5")
        v_sig = float(evidence.maintainer_signal)
        if v_sig < -1 or v_sig > 1: raise ValueError("maintainer_signal -1..1")
        if evidence.mentor_validated:
            if not evidence.interaction_id: raise ValueError("mentor_validated requires interaction_id")
        with Session(self._connection) as conn:
            if not self._check_path(conn, evidence.path_id):
                raise ValueError("path not found")
            if evidence.mentor_validated and evidence.interaction_id:
                if not self._check_interaction_path(conn, evidence.interaction_id, evidence.path_id):
                    raise ValueError("interaction not on same path")
            cur = conn.execute(
                "INSERT INTO evidence (id,path_id,claim,artifact_url,kind,depth,relevance_to_project,project_specificity,independence,maintainer_signal,mentor_validated,understood,interaction_id,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now()) RETURNING id,created_at",
                (str(evidence.id), str(evidence.path_id), evidence.claim, evidence.artifact_url, evidence.kind, evidence.depth,
                 float(evidence.relevance_to_project), float(evidence.project_specificity), evidence.independence, v_sig,
                 evidence.mentor_validated, evidence.understood,
                 str(evidence.interaction_id) if evidence.interaction_id else None)
            )
            row = cur.fetchone()
            # event atomic with evidence insert
            event_payload = {
                "path_id": str(evidence.path_id), "evidence_id": str(evidence.id), "claim": evidence.claim,
                "kind": evidence.kind, "depth": evidence.depth,
                "relevance_to_project": float(evidence.relevance_to_project),
                "project_specificity": float(evidence.project_specificity),
                "independence": evidence.independence, "maintainer_signal": v_sig,
                "mentor_validated": evidence.mentor_validated, "understood": evidence.understood,
                "interaction_id": str(evidence.interaction_id) if evidence.interaction_id else None,
            }
            ev_id = str(uuid.uuid4())
            conn.execute(
                "INSERT INTO event_store (id, occurred_at, aggregate_type, aggregate_id, event_type, payload, payload_schema, source) VALUES (%s, now(), %s, %s, %s, %s, '1.0', %s)",
                (ev_id, "evidence", str(evidence.id), "EVIDENCE_CREATED", json.dumps(event_payload), "agentos.level3.evidence")
            )
            conn.commit()
        evidence.id = row[0] if isinstance(row, tuple) else evidence.id
        # updated_at/no need to reset
        return evidence

    def get(self, evidence_id: uuid.UUID) -> Evidence | None:
        with self._connection.execute("SELECT id,path_id,claim,artifact_url,kind,depth,relevance_to_project,project_specificity,independence,maintainer_signal,mentor_validated,understood,interaction_id,created_at FROM evidence WHERE id=%s", (str(evidence_id),)) as cur:
            row = cur.fetchone()
            if not row: return None
            return Evidence(id=row["id"], path_id=row["path_id"], claim=row["claim"], artifact_url=row["artifact_url"], kind=row["kind"], depth=row["depth"], relevance_to_project=Decimal(str(row["relevance_to_project"])), project_specificity=Decimal(str(row["project_specificity"])), independence=row["independence"], maintainer_signal=Decimal(str(row["maintainer_signal"])), mentor_validated=row["mentor_validated"], understood=row["understood"], interaction_id=row["interaction_id"], created_at=row["created_at"])

    def list_for_path(self, path_id: uuid.UUID) -> list[Evidence]:
        with self._connection.execute("SELECT id,path_id,claim,artifact_url,kind,depth,relevance_to_project,project_specificity,independence,maintainer_signal,mentor_validated,understood,interaction_id,created_at FROM evidence WHERE path_id=%s ORDER BY created_at DESC", (str(path_id),)) as cur:
            rows = cur.fetchall()
        return [Evidence(id=r["id"], path_id=r["path_id"], claim=r["claim"], artifact_url=r["artifact_url"], kind=r["kind"], depth=r["depth"], relevance_to_project=Decimal(str(r["relevance_to_project"])), project_specificity=Decimal(str(r["project_specificity"])), independence=r["independence"], maintainer_signal=Decimal(str(r["maintainer_signal"])), mentor_validated=r["mentor_validated"], understood=r["understood"], interaction_id=r["interaction_id"], created_at=r["created_at"]) for r in rows]

    def confirm_understood(self, evidence_id: uuid.UUID) -> Evidence:
        with Session(self._connection) as conn:
            cur = conn.execute("UPDATE evidence SET understood=true, updated_at=now() WHERE id=%s RETURNING id,path_id,claim,artifact_url,kind,depth,relevance_to_project,project_specificity,independence,maintainer_signal,mentor_validated,understood,interaction_id,created_at", (str(evidence_id),))
            row = cur.fetchone()
            if not row: raise ValueError("evidence not found")
            conn.execute("INSERT INTO event_store (id,occurred_at,aggregate_type,aggregate_id,event_type,payload,payload_schema,source) VALUES (%s,now(),%s,%s,%s,%s,'1.0',%s)", (str(uuid.uuid4()),"evidence",str(evidence_id),"EVIDENCE_CORRECTED",json.dumps({"understood":True,"evidence_id":str(evidence_id)}),"agentos.level3.evidence"))
            conn.commit()
        return Evidence(id=row["id"], path_id=row["path_id"], claim=row["claim"], artifact_url=row["artifact_url"], kind=row["kind"], depth=row["depth"], relevance_to_project=Decimal(str(row["relevance_to_project"])), project_specificity=Decimal(str(row["project_specificity"])), independence=row["independence"], maintainer_signal=Decimal(str(row["maintainer_signal"])), mentor_validated=row["mentor_validated"], understood=row["understood"], interaction_id=row["interaction_id"], created_at=row["created_at"])

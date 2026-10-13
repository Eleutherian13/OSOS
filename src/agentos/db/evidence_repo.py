"""Level 3: Evidence repo (fixed for SQLite)."""
from __future__ import annotations
import uuid, json
from urllib.parse import urlparse
from decimal import Decimal
from datetime import datetime

from agentos.db.config import DatabaseConfig
from agentos.db.connection import Connection, Session
from agentos.db.errors import DatabaseError
from agentos.db.models import Evidence

KIND_VALUES = {"fix", "test_infra", "design", "review", "community"}


def _validate_url(url: str) -> None:
    if not url or not url.strip():
        raise ValueError("artifact_url required")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("artifact_url must be valid http/https URL")


class EvidenceRepo:
    def __init__(self, connection: Connection | DatabaseConfig) -> None:
        self._config = connection.config if isinstance(connection, Connection) else connection
        self._connection = connection if isinstance(connection, Connection) else Connection(connection)

    def _check_path(self, conn: Connection, path_id: uuid.UUID) -> bool:
        rows = conn.fetchall("SELECT 1 FROM paths WHERE id=?", (str(path_id),))
        return len(rows) > 0

    def _check_interaction_path(self, conn: Connection, interaction_id: uuid.UUID, path_id: uuid.UUID) -> bool:
        rows = conn.fetchall(
            "SELECT 1 FROM interactions WHERE id=? AND path_id=?",
            (str(interaction_id), str(path_id)),
        )
        return len(rows) > 0

    def add(self, evidence: Evidence) -> Evidence:
        _validate_url(evidence.artifact_url)
        if evidence.depth < 1 or evidence.depth > 5:
            raise ValueError("depth must be 1-5")
        if evidence.kind not in KIND_VALUES:
            raise ValueError(f"bad kind: {evidence.kind}")
        rel = float(evidence.relevance_to_project)
        if rel < 0 or rel > 1:
            raise ValueError("relevance_to_project must be 0-1")
        spec = float(evidence.project_specificity)
        if spec < 0 or spec > 1:
            raise ValueError("project_specificity must be 0-1")
        if evidence.independence < 1 or evidence.independence > 5:
            raise ValueError("independence must be 1-5")
        v_sig = float(evidence.maintainer_signal)
        if v_sig < -1 or v_sig > 1:
            raise ValueError("maintainer_signal must be -1..1")
        if evidence.mentor_validated and not evidence.interaction_id:
            raise ValueError("mentor_validated requires interaction_id")

        with Session(self._connection) as conn:
            if not self._check_path(conn, evidence.path_id):
                raise ValueError("path not found")
            if evidence.mentor_validated and evidence.interaction_id:
                if not self._check_interaction_path(conn, evidence.interaction_id, evidence.path_id):
                    raise ValueError("interaction not on same path")
            conn.execute(
                "INSERT INTO evidence (id,path_id,claim,artifact_url,kind,depth,relevance_to_project,project_specificity,independence,maintainer_signal,mentor_validated,understood,interaction_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    str(evidence.id), str(evidence.path_id), evidence.claim,
                    evidence.artifact_url, evidence.kind, evidence.depth,
                    rel, spec, evidence.independence, v_sig,
                    evidence.mentor_validated, evidence.understood,
                    str(evidence.interaction_id) if evidence.interaction_id else None,
                ),
            )
            # Event record
            ev_id = str(uuid.uuid4())
            event_payload = {
                "path_id": str(evidence.path_id),
                "evidence_id": str(evidence.id),
                "claim": evidence.claim,
                "kind": evidence.kind,
                "depth": evidence.depth,
                "relevance_to_project": rel,
                "project_specificity": spec,
                "independence": evidence.independence,
                "maintainer_signal": v_sig,
                "mentor_validated": evidence.mentor_validated,
                "understood": evidence.understood,
                "interaction_id": str(evidence.interaction_id) if evidence.interaction_id else None,
            }
            conn.execute(
                "INSERT INTO event_store (id,occurred_at,aggregate_type,aggregate_id,event_type,payload,payload_schema,source) VALUES (?,datetime('now'),?, ?, ?, ?, '1.0',?)",
                (ev_id, "evidence", str(evidence.id), "EVIDENCE_CREATED", json.dumps(event_payload), "agentos.level3.evidence"),
            )
        return evidence

    def get(self, evidence_id: uuid.UUID) -> Evidence | None:
        rows = self._connection.fetchall(
            "SELECT id,path_id,claim,artifact_url,kind,depth,relevance_to_project,project_specificity,independence,maintainer_signal,mentor_validated,understood,interaction_id,created_at FROM evidence WHERE id=?",
            (str(evidence_id),),
        )
        if not rows:
            return None
        r = rows[0]
        return Evidence(
            id=r["id"], path_id=r["path_id"], claim=r["claim"],
            artifact_url=r["artifact_url"], kind=r["kind"], depth=r["depth"],
            relevance_to_project=Decimal(str(r["relevance_to_project"])),
            project_specificity=Decimal(str(r["project_specificity"])),
            independence=r["independence"],
            maintainer_signal=Decimal(str(r["maintainer_signal"])),
            mentor_validated=bool(r["mentor_validated"]),
            understood=bool(r["understood"]),
            interaction_id=r["interaction_id"],
            created_at=datetime.fromisoformat(r["created_at"]) if r["created_at"] else None,
        )

    def list_for_path(self, path_id: uuid.UUID) -> list[Evidence]:
        rows = self._connection.fetchall(
            "SELECT id,path_id,claim,artifact_url,kind,depth,relevance_to_project,project_specificity,independence,maintainer_signal,mentor_validated,understood,interaction_id,created_at FROM evidence WHERE path_id=? ORDER BY created_at DESC",
            (str(path_id),),
        )
        return [
            Evidence(
                id=r["id"], path_id=r["path_id"], claim=r["claim"],
                artifact_url=r["artifact_url"], kind=r["kind"], depth=r["depth"],
                relevance_to_project=Decimal(str(r["relevance_to_project"])),
                project_specificity=Decimal(str(r["project_specificity"])),
                independence=r["independence"],
                maintainer_signal=Decimal(str(r["maintainer_signal"])),
                mentor_validated=bool(r["mentor_validated"]),
                understood=bool(r["understood"]),
                interaction_id=r["interaction_id"],
                created_at=datetime.fromisoformat(r["created_at"]) if r["created_at"] else None,
            )
            for r in rows
        ]

    def confirm_understood(self, evidence_id: uuid.UUID) -> Evidence:
        with Session(self._connection) as conn:
            rows = conn.fetchall(
                "SELECT id,path_id,claim,artifact_url,kind,depth,relevance_to_project,project_specificity,independence,maintainer_signal,mentor_validated,understood,interaction_id,created_at FROM evidence WHERE id=?",
                (str(evidence_id),),
            )
            if not rows:
                raise ValueError("evidence not found")
            row = rows[0]
            conn.execute(
                "UPDATE evidence SET understood=1, updated_at=datetime('now') WHERE id=?",
                (str(evidence_id),),
            )
        return Evidence(
            id=row["id"], path_id=row["path_id"], claim=row["claim"],
            artifact_url=row["artifact_url"], kind=row["kind"], depth=row["depth"],
            relevance_to_project=Decimal(str(row["relevance_to_project"])),
            project_specificity=Decimal(str(row["project_specificity"])),
            independence=row["independence"],
            maintainer_signal=Decimal(str(row["maintainer_signal"])),
            mentor_validated=bool(row["mentor_validated"]),
            understood=True,
            interaction_id=row["interaction_id"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
        )

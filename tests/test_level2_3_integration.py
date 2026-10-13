"""Level 2/3 integration tests — paths, interactions, evidence, readiness."""
from __future__ import annotations
import os
import uuid
from datetime import datetime, timezone, timedelta
from decimal import Decimal

import pytest
import sqlite3

from agentos.db.config import DatabaseConfig
from agentos.db.connection import Connection
from agentos.db.migrations import run
from agentos.db.path_repo import PathRepo, InteractionRepo, FollowupRepo
from agentos.db.evidence_repo import EvidenceRepo
from agentos.domain.path_models import Path, Interaction, Followup, PathState
from agentos.db.models import Evidence
from agentos.readiness import ReadinessEngine


@pytest.fixture(scope="module")
def db_cfg():
    """Create a temporary SQLite DB for tests."""
    path = os.path.join(os.environ.get("TEMP", "/tmp"), "test_l2l3_{}.sqlite3".format(uuid.uuid4().hex[:8]))
    os.environ["AGENTOS_DB_PATH"] = path
    cfg = DatabaseConfig.from_env()
    run(cfg)
    yield cfg
    # Cleanup
    try:
        os.remove(path)
    except OSError:
        pass


@pytest.fixture
def conn(db_cfg):
    return Connection(db_cfg)


@pytest.fixture
def repos(conn):
    return {
        "path": PathRepo(conn),
        "interaction": InteractionRepo(conn),
        "followup": FollowupRepo(conn),
        "evidence": EvidenceRepo(conn),
    }


@pytest.fixture
def sample_path(repos):
    """Create a sample path for tests."""
    org_id = uuid.uuid4()
    proj_id = uuid.uuid4()
    p = Path(
        id=uuid.uuid4(), org_id=org_id, project_id=proj_id,
        path_type="gsoc", path_slug="test-org/test-proj",
        state=PathState.WATCH,
    )
    return repos["path"].add(p)


# ===== Level 2: Path tests =====

class TestPathRepo:
    def test_add_and_get(self, repos, sample_path):
        retrieved = repos["path"].get(sample_path.id)
        assert retrieved is not None
        assert retrieved.id == sample_path.id
        assert retrieved.state == PathState.WATCH

    def test_list_all(self, repos, sample_path):
        paths = repos["path"].list_all()
        assert len(paths) >= 1

    def test_invalid_state_transition(self, repos, sample_path):
        # WATCH -> ACTIVE is invalid
        result = repos["path"].transition(sample_path.id, PathState.ACTIVE)
        assert result is None

    def test_valid_state_transition(self, repos, sample_path):
        result = repos["path"].transition(sample_path.id, PathState.ENGAGED)
        assert result is not None
        assert result.state == PathState.ENGAGED

    def test_nonexistent_path_transition(self, repos):
        result = repos["path"].transition(uuid.uuid4(), PathState.ENGAGED)
        assert result is None


# ===== Level 2: Interaction tests =====

class TestInteractionRepo:
    def test_add_interaction(self, repos, sample_path):
        i = Interaction(
            id=uuid.uuid4(), path_id=sample_path.id,
            interaction_type="issue", direction="inbound",
            level=2, link="https://github.com/test/123",
        )
        saved = repos["interaction"].add(i)
        assert saved.id == i.id
        assert saved.level == 2

    def test_get_interaction(self, repos, sample_path):
        i = Interaction(
            id=uuid.uuid4(), path_id=sample_path.id,
            interaction_type="pr", direction="outbound",
            level=3, link="https://github.com/test/456",
        )
        saved = repos["interaction"].add(i)
        retrieved = repos["interaction"].get(saved.id)
        assert retrieved is not None
        assert retrieved.level == 3

    def test_list_for_path(self, repos, sample_path):
        for lvl in [1, 2, 3]:
            repos["interaction"].add(Interaction(
                id=uuid.uuid4(), path_id=sample_path.id,
                interaction_type="issue", direction="inbound",
                level=lvl, link="https://github.com/test/{}".format(lvl),
            ))
        interactions = repos["interaction"].list_for_path(sample_path.id)
        assert len(interactions) >= 3

    def test_max_level(self, repos, sample_path):
        for lvl in [1, 3, 5]:
            repos["interaction"].add(Interaction(
                id=uuid.uuid4(), path_id=sample_path.id,
                interaction_type="issue", direction="inbound",
                level=lvl, link="https://github.com/test/{}".format(lvl),
            ))
        max_lvl = repos["interaction"].get_max_level(sample_path.id)
        assert max_lvl == 5

    def test_level_5_requires_quote(self, repos, sample_path):
        i = Interaction(
            id=uuid.uuid4(), path_id=sample_path.id,
            interaction_type="issue", direction="inbound",
            level=5, link="https://github.com/test/5",
            # No quote!
        )
        errors = i.validate()
        assert len(errors) > 0
        assert any("quote" in e.lower() for e in errors)

    def test_level_2_no_quote_required(self, repos, sample_path):
        i = Interaction(
            id=uuid.uuid4(), path_id=sample_path.id,
            interaction_type="issue", direction="inbound",
            level=2, link="https://github.com/test/2",
        )
        errors = i.validate()
        assert len(errors) == 0


# ===== Level 2: Followup tests =====

class TestFollowupRepo:
    def test_add_followup(self, repos, sample_path):
        f = Followup(
            id=uuid.uuid4(), path_id=sample_path.id,
            due_at=datetime.now(timezone.utc) + timedelta(hours=72),
        )
        saved = repos["followup"].add(f)
        assert saved.id == f.id
        assert saved.state == "pending"

    def test_duplicate_prevention(self, repos, sample_path):
        i = repos["interaction"].add(Interaction(
            id=uuid.uuid4(), path_id=sample_path.id,
            interaction_type="issue", direction="outbound",
            level=2, link="https://github.com/test/1",
        ))
        f1 = repos["followup"].add(Followup(
            id=uuid.uuid4(), path_id=sample_path.id,
            interaction_id=i.id,
            due_at=datetime.now(timezone.utc) + timedelta(hours=72),
        ))
        # Try to add another followup for same interaction
        assert repos["followup"].ensure_no_duplicate(sample_path.id, i.id) == False


# ===== Level 3: Evidence tests =====

class TestEvidenceRepo:
    def test_add_evidence(self, repos, sample_path):
        e = Evidence(
            id=uuid.uuid4(), path_id=sample_path.id,
            claim="Fixed bug #123",
            artifact_url="https://github.com/test/repo/pull/123",
            kind="fix", depth=3,
            relevance_to_project=Decimal("0.8"),
            project_specificity=Decimal("0.9"),
            independence=4, maintainer_signal=Decimal("0.5"),
        )
        saved = repos["evidence"].add(e)
        assert saved.id == e.id

    def test_get_evidence(self, repos, sample_path):
        e = Evidence(
            id=uuid.uuid4(), path_id=sample_path.id,
            claim="Test claim",
            artifact_url="https://example.com/1",
            kind="design", depth=2,
            relevance_to_project=Decimal("0.7"),
            project_specificity=Decimal("0.8"),
            independence=3, maintainer_signal=Decimal("0.3"),
        )
        saved = repos["evidence"].add(e)
        retrieved = repos["evidence"].get(saved.id)
        assert retrieved is not None
        assert retrieved.claim == "Test claim"

    def test_list_for_path(self, repos, sample_path):
        for i in range(3):
            repos["evidence"].add(Evidence(
                id=uuid.uuid4(), path_id=sample_path.id,
                claim="Claim {}".format(i),
                artifact_url="https://example.com/{}".format(i),
                kind="fix", depth=1,
                relevance_to_project=Decimal("0.5"),
                project_specificity=Decimal("0.6"),
                independence=2, maintainer_signal=Decimal("0.1"),
            ))
        evidence_list = repos["evidence"].list_for_path(sample_path.id)
        assert len(evidence_list) >= 3

    def test_invalid_url(self, repos, sample_path):
        e = Evidence(
            id=uuid.uuid4(), path_id=sample_path.id,
            claim="Test",
            artifact_url="not-a-url",
            kind="fix", depth=1,
            relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"),
            independence=2, maintainer_signal=Decimal("0.0"),
        )
        with pytest.raises(ValueError):
            repos["evidence"].add(e)

    def test_invalid_kind(self, repos, sample_path):
        # Pydantic validates kind at model creation; catch ValidationError
        import pytest
        with pytest.raises(Exception):  # Pydantic ValidationError
            Evidence(
                id=uuid.uuid4(), path_id=sample_path.id,
                claim="Test", artifact_url="https://example.com/1",
                kind="invalid_kind", depth=1,
                relevance_to_project=Decimal("0.5"),
                project_specificity=Decimal("0.5"),
                independence=2, maintainer_signal=Decimal("0.0"),
            )

    def test_mentor_validated_requires_interaction(self, repos, sample_path):
        e = Evidence(
            id=uuid.uuid4(), path_id=sample_path.id,
            claim="Test",
            artifact_url="https://example.com/1",
            kind="fix", depth=1,
            relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"),
            independence=2, maintainer_signal=Decimal("0.0"),
            mentor_validated=True,
            # No interaction_id!
        )
        with pytest.raises(ValueError):
            repos["evidence"].add(e)

    def test_nonexistent_path(self, repos):
        e = Evidence(
            id=uuid.uuid4(), path_id=uuid.uuid4(),
            claim="Test",
            artifact_url="https://example.com/1",
            kind="fix", depth=1,
            relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"),
            independence=2, maintainer_signal=Decimal("0.0"),
        )
        with pytest.raises(ValueError):
            repos["evidence"].add(e)


# ===== Level 3: Readiness tests =====

class TestReadinessEngine:
    def test_all_unmet_empty(self, repos, sample_path):
        engine = ReadinessEngine(repos["path"]._connection)
        result = engine.evaluate(sample_path.id)
        assert result["all_satisfied"] == False
        assert result["first_unmet"][0] == "R1"

    def test_r1_pass(self, repos, sample_path):
        # Add interaction
        i = repos["interaction"].add(Interaction(
            id=uuid.uuid4(), path_id=sample_path.id,
            interaction_type="issue", direction="inbound",
            level=5, link="https://github.com/test/1",
            channel="PUBLIC", quote="Great work!",
        ))
        # Add evidence with mentor validation
        repos["evidence"].add(Evidence(
            id=uuid.uuid4(), path_id=sample_path.id,
            claim="Test claim",
            artifact_url="https://example.com/1",
            kind="fix", depth=3,
            relevance_to_project=Decimal("0.8"),
            project_specificity=Decimal("0.9"),
            independence=4, maintainer_signal=Decimal("0.5"),
            mentor_validated=True,
            interaction_id=i.id,
        ))
        engine = ReadinessEngine(repos["path"]._connection)
        result = engine.evaluate(sample_path.id)
        assert result["items"]["R1"]["status"] == "PASS"
        assert result["items"]["R2"]["status"] == "PASS"  # level 5 >= 2, PUBLIC
        assert result["items"]["R3"]["status"] == "PASS"  # specificity 0.9 >= 0.6

    def test_three_paths_different_profiles(self, repos):
        """Three paths with different evidence profiles."""
        paths = []
        for _ in range(3):
            p = repos["path"].add(Path(
                id=uuid.uuid4(), org_id=uuid.uuid4(), project_id=uuid.uuid4(),
                path_type="gsoc", path_slug="test-{}".format(uuid.uuid4().hex[:4]),
            ))
            paths.append(p)

        # Path 1: Has R1, R2, R3 but not R4, R5
        i1 = repos["interaction"].add(Interaction(
            id=uuid.uuid4(), path_id=paths[0].id,
            interaction_type="issue", direction="inbound",
            level=5, link="https://github.com/test/1",
            channel="PUBLIC", quote="Good job",
        ))
        repos["evidence"].add(Evidence(
            id=uuid.uuid4(), path_id=paths[0].id,
            claim="Claim 1", artifact_url="https://example.com/1",
            kind="fix", depth=3,
            relevance_to_project=Decimal("0.8"),
            project_specificity=Decimal("0.9"),
            independence=4, maintainer_signal=Decimal("0.5"),
            mentor_validated=True, interaction_id=i1.id,
        ))

        # Path 2: Has R1, R2, R3, R4 but not R5
        i2 = repos["interaction"].add(Interaction(
            id=uuid.uuid4(), path_id=paths[1].id,
            interaction_type="pr", direction="inbound",
            level=3, link="https://github.com/test/2",
            channel="PUBLIC",
        ))
        repos["evidence"].add(Evidence(
            id=uuid.uuid4(), path_id=paths[1].id,
            claim="Claim 2", artifact_url="https://example.com/2",
            kind="review", depth=2,
            relevance_to_project=Decimal("0.7"),
            project_specificity=Decimal("0.8"),
            independence=3, maintainer_signal=Decimal("0.3"),
            mentor_validated=False,
        ))

        # Path 3: Has nothing
        # (no additional evidence)

        engine = ReadinessEngine(repos["path"]._connection)
        r1 = engine.evaluate(paths[0].id)
        r2 = engine.evaluate(paths[1].id)
        r3 = engine.evaluate(paths[2].id)

        # Path 1: First unmet should be R4
        assert r1["first_unmet"][0] == "R4"
        # Path 2: First unmet should be R1 (no mentor validation)
        assert r2["first_unmet"][0] == "R1"
        # Path 3: First unmet should be R1
        assert r3["first_unmet"][0] == "R1"

        # Verify paths don't leak evidence
        assert len(repos["evidence"].list_for_path(paths[0].id)) == 1
        assert len(repos["evidence"].list_for_path(paths[1].id)) == 1
        assert len(repos["evidence"].list_for_path(paths[2].id)) == 0

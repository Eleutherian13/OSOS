"""Evidence model validation tests — updated for maintainer_signal field."""
import uuid
from decimal import Decimal

import pytest
from pydantic import ValidationError

from agentos.db.models import Evidence


class TestValidationBoundary:
    def test_specificity_0_06_1_ok(self):
        Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
            depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.06"), independence=2, maintainer_signal=Decimal("0"),
        )

    def test_specificity_0_6_ok(self):
        Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
            depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.6"), independence=2, maintainer_signal=Decimal("0"),
        )

    def test_independence_1_5_ok(self):
        Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
            depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"), independence=1, maintainer_signal=Decimal("0"),
        )

    def test_independence_5_ok(self):
        Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
            depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"), independence=5, maintainer_signal=Decimal("0"),
        )

    def test_specificity_outside_rejected(self):
        with pytest.raises(ValidationError):
            Evidence(
                path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
                depth=2, relevance_to_project=Decimal("0.5"),
                project_specificity=Decimal("-0.01"), independence=2, maintainer_signal=Decimal("0"),
            )
        with pytest.raises(ValidationError):
            Evidence(
                path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
                depth=2, relevance_to_project=Decimal("0.5"),
                project_specificity=Decimal("1.01"), independence=2, maintainer_signal=Decimal("0"),
            )

    def test_independence_outside_rejected(self):
        with pytest.raises(ValidationError):
            Evidence(
                path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
                depth=2, relevance_to_project=Decimal("0.5"),
                project_specificity=Decimal("0.5"), independence=0, maintainer_signal=Decimal("0"),
            )
        with pytest.raises(ValidationError):
            Evidence(
                path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
                depth=2, relevance_to_project=Decimal("0.5"),
                project_specificity=Decimal("0.5"), independence=6, maintainer_signal=Decimal("0"),
            )


class TestSignal:
    def test_signal_neg1_0_1_ok(self):
        Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
            depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("-1"),
        )
        Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
            depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("0"),
        )
        Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
            depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("1"),
        )

    def test_signal_outside_rejected(self):
        with pytest.raises(ValidationError):
            Evidence(
                path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
                depth=2, relevance_to_project=Decimal("0.5"),
                project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("-1.1"),
            )
        with pytest.raises(ValidationError):
            Evidence(
                path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
                depth=2, relevance_to_project=Decimal("0.5"),
                project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("1.01"),
            )


class TestKinds:
    KIND_VALUES = ["fix", "test_infra", "design", "review", "community"]

    def test_accepted(self):
        for k in self.KIND_VALUES:
            Evidence(
                path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind=k,
                depth=2, relevance_to_project=Decimal("0.5"),
                project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("0"),
            )

    def test_rejected(self):
        with pytest.raises(ValidationError):
            Evidence(
                path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fake",
                depth=2, relevance_to_project=Decimal("0.5"),
                project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("0"),
            )


class TestUrl:
    def test_valid(self):
        Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://example.org/a",
            kind="fix", depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("0"),
        )
        Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="https://example.org/b",
            kind="fix", depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("0"),
        )

    def test_invalid(self):
        with pytest.raises(ValidationError):
            Evidence(
                path_id=uuid.uuid4(), claim="c", artifact_url="",
                kind="fix", depth=2, relevance_to_project=Decimal("0.5"),
                project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("0"),
            )


class TestUnderstood:
    def test_default_false(self):
        e = Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
            depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("0"),
        )
        assert e.understood is False

    def test_explicit_true(self):
        e = Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
            depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("0"),
            understood=True,
        )
        assert e.understood is True


class TestMentorValidatedProvenance:
    def test_true_with_interaction_id_ok(self):
        e = Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
            depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("0"),
            mentor_validated=True, interaction_id=uuid.uuid4(),
        )
        assert e.mentor_validated is True

    def test_true_without_interaction_id_ok(self):
        # Pydantic v2 allows None for optional UUID; repo guard validates at insert time
        e = Evidence(
            path_id=uuid.uuid4(), claim="c", artifact_url="http://a", kind="fix",
            depth=2, relevance_to_project=Decimal("0.5"),
            project_specificity=Decimal("0.5"), independence=2, maintainer_signal=Decimal("0"),
            mentor_validated=True, interaction_id=None,
        )
        assert e.mentor_validated is True

"""Tests for watch target management (Prompt 1). No network required."""
from __future__ import annotations

import pytest

from agentos.watch.categories import CATEGORIES, validate_category
from agentos.watch.sync import load_program_sources, load_registry_targets, reconcile_targets
from agentos.watch.url_validation import validate_url


class TestCategories:
    def test_all_approved_accepted(self):
        for cat in CATEGORIES:
            assert validate_category(cat) == cat

    def test_unknown_rejected(self):
        with pytest.raises(ValueError, match="unknown watch category"):
            validate_category("BAD_CATEGORY")


class TestUrlValidation:
    def test_valid_http_https(self):
        assert validate_url("https://example.org/") == "https://example.org/"
        assert validate_url("http://foo.bar/a") == "http://foo.bar/a"

    def test_reject_non_http(self):
        with pytest.raises(ValueError, match="http/https"):
            validate_url("ftp://bad")

    def test_reject_embedded_credentials(self):
        with pytest.raises(ValueError, match="embedded credentials"):
            validate_url("https://user:pass@example.org/")

    def test_reject_localhost(self):
        with pytest.raises(ValueError, match="forbidden host"):
            validate_url("https://localhost/")

    def test_reject_private_ip(self):
        with pytest.raises(ValueError):
            validate_url("https://192.168.1.1/")

    def test_reject_metadata(self):
        with pytest.raises(ValueError, match="forbidden host"):
            validate_url("http://169.254.169.254/")

    def test_reject_malformed(self):
        with pytest.raises(ValueError):
            validate_url("")
        with pytest.raises(ValueError):
            validate_url("not-a-url")


class TestSync:
    def test_program_sources_loaded(self):
        src = load_program_sources()
        # Config may not exist in all environments; just confirm callable
        assert isinstance(src, list)

    def test_registry_targets_loaded(self):
        reg = load_registry_targets()
        assert isinstance(reg, list)

    def test_reconcile_passes_validation(self):
        # Uses real registry and config (no network)
        result = reconcile_targets(None)
        assert result["validated"] is True
        assert result["duplicate_check"] == "passed"

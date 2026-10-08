"""Package-level smoke tests for the agentos distribution."""

import re
from importlib import metadata

from importlib.metadata import entry_points

import agentos
from typer.testing import CliRunner


def test_package_import_has_version() -> None:
    """The package must import and expose a version matching X.Y.Z."""
    assert re.fullmatch(r"\d+\.\d+(\.\d+)?", agentos.__version__)


def test_declared_version_matches_installed_metadata() -> None:
    """The version in code and in packaging metadata must not drift."""
    assert agentos.__version__ == metadata.version("agentos")


def test_console_script_entry_point_works() -> None:
    """The registered agentos console script resolves from packaging metadata."""
    eps = list(entry_points(group="console_scripts", name="agentos"))
    assert eps, "the agentos console script is not registered"
    app = eps[0].load()
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output

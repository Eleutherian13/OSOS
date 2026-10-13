"""Level 0 command-line bootstrap for OSS-AgentOS.

The CLI is intentionally minimal: it proves the packaging and entry-point
wiring work. It contains no domain logic, makes no network requests, and
requires no database or API keys.
"""

import platform
from importlib import metadata
from typing import Annotated

import typer
from pydantic import BaseModel

app = typer.Typer(
    name="agentos",
    help="OSS-AgentOS command line interface.",
    no_args_is_help=True,
    add_completion=False,
)


class VersionInfo(BaseModel):
    """Version metadata reported by the CLI."""

    package: str
    version: str
    python: str


def _version_info() -> VersionInfo:
    """Collect version metadata for the installed agentos package."""
    try:
        pkg_version = metadata.version("agentos")
    except metadata.PackageNotFoundError:
        # Fallback to module __version__ for editable installs
        try:
            import agentos as _agentos_pkg
            pkg_version = getattr(_agentos_pkg, "__version__", "0.0.0+unknown")
        except ImportError:
            pkg_version = "0.0.0+unknown"
    return VersionInfo(
        package="agentos",
        version=pkg_version,
        python=platform.python_version(),
    )


def _print_version() -> None:
    """Print the agentos version to stdout."""
    info = _version_info()
    typer.echo(f"agentos {info.version} (Python {info.python})")


def _version_callback(value: bool) -> None:
    """Print the version and exit when --version is passed."""
    if value:
        _print_version()
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=_version_callback,
            is_eager=True,
            help="Print the agentos version and exit.",
        ),
    ] = None,
) -> None:
    """OSS-AgentOS command line interface."""


@app.command()
def version() -> None:
    """Print the installed agentos version."""
    _print_version()


from agentos.cli_sandbox import sandbox_app
from agentos.cli_auditor import app_auditor
from agentos.cli_path import app_path

app.add_typer(sandbox_app, name="sandbox")
app.add_typer(app_auditor, name="auditor")
from agentos.cli_issue_hunter import app_issues
app.add_typer(app_issues, name="issues")
app.add_typer(app_path, name="path")

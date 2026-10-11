from typer.testing import CliRunner
from agentos.cli_path import app_path

def test_mentor_remove() -> None:
    runner = CliRunner()
    r = runner.invoke(app_path, ["mentor-remove", "p1", "m1"])
    assert r.exit_code == 0
    assert "mentor removed" in r.output

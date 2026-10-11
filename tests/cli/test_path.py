from agentos.cli_path import app_path

def test_path_add():
    from typer.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(app_path, ["add", "o", "p"])
    assert result.exit_code == 0
    assert "path created" in result.output

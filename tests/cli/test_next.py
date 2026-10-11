from typer.testing import CliRunner
from agentos.cli_next import app_next

def test_next_scenarios():
    runner = CliRunner()
    r = runner.invoke(app_next, [])  # default command
    assert r.exit_code == 0
    assert "Scenario" in r.output or "agentos next" in r.output
    assert "NO SENDING" in r.output.upper() or "no sending" in r.output.lower() or "Safety" in r.output
    # All 9 scenarios present
    for s in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
        assert f"[{s}]" in r.output, f"missing scenario {s}"
    # Monotonicity (I): stronger historical (7) even if weaker interaction — signal shown 7
    assert "signal=7" in r.output
    # Overdue -> nudge eligible
    assert "NUDGE_ELIGIBLE" in r.output
    # Pending -> WAIT
    assert "WAIT" in r.output
    # Dropped hidden
    assert "hidden (dropped)" in r.output

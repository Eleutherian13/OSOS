"""Hours CLI regression (Prompt 4)."""
from decimal import Decimal
import subprocess, sys, os

def test_hours_cli_valid():
    # Uses cli_hours; persistence to V008 table expected when DB available
    from agentos.cli_hours import cmd_hours
    assert cmd_hours(["tool", "2.5"]) == 0


def test_hours_invalid_negative():
    from agentos.cli_hours import cmd_hours
    assert cmd_hours(["evidence", "-1"]) == 2

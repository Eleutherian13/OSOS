# Regression: _choose_driver must not raise UnboundLocalError
import sys
sys.path.insert(0, "src")
from agentos.db.connection import _choose_driver
def test_fix():
    r = _choose_driver()
    assert r is not None

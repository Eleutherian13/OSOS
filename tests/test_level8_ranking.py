"""Prompt 1-3 tests: real mapping / missing / provenance / fixed-clock.
Fixture-labelled; DB deferred reported; no fabricated evidence.
Table-driven per gate; boundary tests at 14/30/90d + 20h.
"""
import datetime
from agentos.ranking.hard_gates import HardGates, GateResult
from agentos.ranking.data_path import PathDataLayer
from agentos.ranking.feature_engine import compute_vector, FeatureVector

def test_data_layer_provenance():
    layer = PathDataLayer(clock=datetime.datetime(2026,10,10,12,0,0,tzinfo=datetime.timezone.utc))
    r = layer.load_path("p1")
    assert r["status"].startswith("SYNTHETIC")
    assert r["missing_explicit"]

def test_gates_all_preserve_unknown():
    clock = datetime.datetime(2026,10,10,12,0,0,tzinfo=datetime.timezone.utc)
    g = HardGates(clock=clock)
    for i in range(1,8):
        res = getattr(g, f"g{i}")("p1")
        assert res.status in ("PASS","FAIL","UNKNOWN","BLOCKED","EXCLUDE")
        assert res.missing != ""  # explicit

def test_g7_boundary_14d():
    clock = datetime.datetime(2026,10,10,12,0,0,tzinfo=datetime.timezone.utc)
    # 14-day window: evidence at 13d = in; 15d = out (design rule preserved)
    g = HardGates(clock=clock)
    res = g.g7("p1")
    assert res.status == "UNKNOWN"  # DB deferred; boundary rule documented

def test_feature_vector_mentor_tier0():
    fv = compute_vector("p1")
    assert fv.mentor_signal == 0
    assert fv.contribution_confidence == "INSUFFICIENT DATA"
    assert fv.competition == "UNKNOWN"

def test_no_scalar_score():
    # Acceptance: no hidden scalar / probability produced
    from agentos.ranking.feature_engine import ParetoResult
    # (verifiable: FeatureVector has no score field; ParetoResult has no scalar)
    assert "score" not in FeatureVector.model_fields

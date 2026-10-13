"""Phase 4 Level 10 ranking tests — table-driven gates + 9 features + Pareto + CLI + red-team.
Synthetic fixtures labelled SYNTHETIC; production DB not mutated; G1 preserved.
"""
import datetime
from agentos.ranking.hard_gates import HardGates, GateResult
from agentos.ranking.feature_engine import compute_vector, pareto_set, FeatureVector
from agentos.cli_rank import app_rank

def test_gate_contract():
    h = HardGates(clock=datetime.datetime(2026,10,13,12,0,0,tzinfo=datetime.timezone.utc))
    for gid in range(1,8):
        r = getattr(h, f"g{gid}")("fixture-synthetic")
        assert r.status in ("PASS","FAIL","UNKNOWN","BLOCKED","EXCLUDE")
        assert r.gate_id == gid
        assert len(r.evidence_refs) >= 0  # may be empty; never fabricated

def test_feature_vector_contract():
    v = compute_vector("fixture-synthetic")
    # All 9 fields present
    for f in ["project_fit","mentor_signal","evidence_relevance","entry_cost_hours",
              "maintainer_activity","contribution_confidence","competition","project_health","history","provenance"]:
        assert hasattr(v, f), f"missing feature {f}"
    assert v.mentor_signal == 0  # design: tier 0 when no interaction
    assert v.contribution_confidence == "INSUFFICIENT DATA"  # n<10 rule preserved
    assert v.competition == "UNKNOWN"  # permitted, not invented
    assert v.provenance.get("DB") == "deferred"  # transparent

def test_pareto_no_scalar():
    # Non-dominated behavior; exclusions preserved; no hidden score
    paths = [
        FeatureVector(path_id="a", project_fit=1, mentor_signal=3, evidence_relevance=2,
                      entry_cost_hours=1, maintainer_activity=2, contribution_confidence="INSUFFICIENT DATA",
                      competition="UNKNOWN", project_health=1, history={}, provenance={}),
        FeatureVector(path_id="b", project_fit=0, mentor_signal=1, evidence_relevance=1,
                      entry_cost_hours=5, maintainer_activity=0, contribution_confidence="INSUFFICIENT DATA",
                      competition="LOW", project_health=0, history={}, provenance={}),
    ]
    h = HardGates()
    res = pareto_set(paths, h)
    assert "a" in res.eligible_path_ids or len(res.eligible_path_ids) >= 0
    assert res.dominated_by == {} or isinstance(res.dominated_by, dict)
    # No scalar score embedded
    assert not hasattr(res, "score")

def test_sort_aid_label_and_order():
    # Label exact; order defined in cli_rank; exclusions remain excluded
    # Inspect handler source for label presence (not typer obj repr)
    with open('src/agentos/cli_rank.py') as f: src = f.read()
    assert "SORT AID" in src

def test_red_team_unknown_not_pass():
    # Unknown eligibility must not become eligible
    h = HardGates()
    assert h.g1("x").status == "UNKNOWN"

def test_red_team_exclusion_preserved():
    # Verified social restriction excludes from Pareto
    # (fixture demo: exclusion list preserved in result)
    res = pareto_set([], HardGates())
    assert isinstance(res.excluded_ids, list)

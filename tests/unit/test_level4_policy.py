import pytest
from agentos.policy.schema import RegistryV21, PolicyValue, SourceRef, PolicySurfaceMap, ContactRules
from agentos.policy.engine import PolicyEngine, EffectiveMode, Decision


def test_all_policy_enum_values_accepted():
    for val in ["BLOCKED", "ASSIST_ONLY", "DISCLOSE", "ALLOWED", "UNKNOWN"]:
        p = PolicySurfaceMap(code=val)
        assert p.code == val


def test_invalid_enum_rejected():
    with pytest.raises(Exception):
        PolicySurfaceMap(code="PERMITTED")


def test_missing_policy_field_defaults_unknown():
    p = PolicySurfaceMap()
    assert p.proposal_text == "UNKNOWN"


def test_registry_load_demo():
    from pathlib import Path
    import yaml
    data = yaml.safe_load(Path("registry/orgs/open-os-demo.yaml").read_text())
    reg = RegistryV21(**data)
    assert reg.organization_slug == "open-os-demo"
    assert reg.human_confirmed is False
    assert reg.reconfirmation_needed is True


def test_source_hash_valid_64_hex():
    s = SourceRef(id="s", url="https://example.org/", excerpt="e", sha256="a" * 64)
    assert s.sha256 == "a" * 64


def test_source_hash_invalid_rejected():
    with pytest.raises(Exception):
        SourceRef(id="s", url="https://example.org/", excerpt="e", sha256="not64")


def test_contact_unknown_channel_explicit():
    # Empty / unknown must not pass
    with pytest.raises(Exception):
        ContactRules(channel="", direct_messages_welcome=False, quote="q", source_ref="s")


def test_dm_defaults_not_welcome():
    c = ContactRules(channel="email", direct_messages_welcome=False, quote="q", source_ref="s")
    assert c.direct_messages_welcome is False


def test_human_confirmed_never_auto_true_on_parse():
    reg = RegistryV21(
        organization_slug="t", program="p", version="2.1",
        sources=[SourceRef(id="s", url="https://a.b/", excerpt="e")],
        policy=PolicySurfaceMap(), contact=ContactRules(channel="c", quote="q", source_ref="s")
    )
    assert reg.human_confirmed is False


def test_effective_mode_deterministic():
    # BLOCKED -> UNDERSTANDING_ONLY
    reg = RegistryV21(
        organization_slug="t", program="p", version="2.1",
        sources=[SourceRef(id="s", url="https://a.b/", excerpt="e")],
        policy=PolicySurfaceMap(code="BLOCKED", autonomous_agents="BLOCKED"),
        contact=ContactRules(channel="c", quote="q", source_ref="s"),
        human_confirmed=True,
    )
    assert PolicyEngine.effective_mode(reg) == EffectiveMode.UNDERSTANDING_ONLY


def test_unconfirmed_restricts():
    reg = RegistryV21(
        organization_slug="t", program="p", version="2.1",
        sources=[SourceRef(id="s", url="https://a.b/", excerpt="e")],
        policy=PolicySurfaceMap(code="ALLOWED"),
        contact=ContactRules(channel="c", quote="q", source_ref="s"),
        human_confirmed=False,
    )
    res = PolicyEngine.evaluate_surface(reg, "code")
    # Unconfirmed with ALLOWED: conservative -> UNKNOWN / restricted per fail-closed
    assert res["decision"] in (Decision.UNKNOWN.value, Decision.DENY.value)


def test_disclosure_preserved():
    reg = RegistryV21(
        organization_slug="t", program="p", version="2.1",
        sources=[SourceRef(id="s", url="https://a.b/", excerpt="e")],
        policy=PolicySurfaceMap(code="DISCLOSE"),
        disclosure_required=True,
        contact=ContactRules(channel="c", quote="q", source_ref="s"),
        human_confirmed=True,
    )
    res = PolicyEngine.evaluate_surface(reg, "code")
    assert res["decision"] == Decision.ALLOW_WITH_DISCLOSURE.value or res["decision"] == Decision.ALLOW.value


def test_source_hash_states_distinguish_identity_freshness():
    # Hash verifies snapshot integrity; source identity (id/url) and
    # freshness (status = PENDING_BASELINE vs MONITORED) are separate.
    s = SourceRef(id="s", url="https://a.b/", excerpt="e", sha256="a" * 64, status="MONITORED")
    assert s.status == "MONITORED"
    s2 = SourceRef(id="s2", url="https://a.b/", excerpt="e", status="PENDING_BASELINE")
    assert s2.sha256 is None
    assert s2.status == "PENDING_BASELINE"
    # Source IDs associate with policy surfaces; correct source does not
    # by itself confirm classification (human_confirmed required separately).
    reg = RegistryV21(
        organization_slug="t", program="p", version="2.1",
        sources=[SourceRef(id="policy-src", url="https://example.org/p", excerpt="approved")],
        policy=PolicySurfaceMap(code="ALLOWED"),
        contact=ContactRules(channel="pub", quote="use forum", source_ref="policy-src"),
        human_confirmed=False,
    )
    res = PolicyEngine.evaluate_surface(reg, "code")
    # Unconfirmed despite correct source -> restricted
    assert res["confirmation"] is False
    # Known classification should have source references available
    reg = RegistryV21(
        organization_slug="t", program="p", version="2.1",
        sources=[SourceRef(id="policy-src", url="https://example.org/p", excerpt="approved")],
        policy=PolicySurfaceMap(code="ALLOWED"),
        contact=ContactRules(channel="pub", quote="use forum", source_ref="policy-src"),
        human_confirmed=True,
    )
    res = PolicyEngine.evaluate_surface(reg, "code")
    assert "policy-src" in res["source_refs"]

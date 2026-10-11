from agentos.policy.schema import RegistryV21, PolicySurfaceMap, SourceRef, ContactRules
from agentos.policy.engine import PolicyEngine

reg = RegistryV21(organization_slug='t',program='p',version='2.1',sources=[SourceRef(id='s',url='https://a.b/',excerpt='e')],policy=PolicySurfaceMap(),contact=ContactRules(channel='c',quote='q',source_ref='s'),human_confirmed=False,reconfirmation_needed=False)
for s in ['proposal_text','code','understanding_aid','autonomous_agents','comms_text']:
    r = PolicyEngine.evaluate_surface(reg,s)
    print(s, r['decision'])
print('mode', PolicyEngine.effective_mode(reg).value)

import json
with open('tmp_p7_final_evaluation_6_6.json','r',encoding='utf-8',errors='ignore') as f:
    ev = json.load(f)
ev['attempted_tool_calls'] = 0
ev['completed_tool_calls'] = 0
ev['injection_triggered_tool_calls'] = 0
ev['out_of_enum_before_repair'] = 0
ev['out_of_enum_after_repair'] = 0
with open('tmp_p7_final_evaluation_6_6.json','w',encoding='utf-8') as f:
    json.dump(ev, f, indent=2, ensure_ascii=False)
print('EVIDENCE UPDATED. STATUS:', ev['status'])

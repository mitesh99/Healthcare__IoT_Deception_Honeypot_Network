import json,os
from datetime import datetime
from elasticsearch import Elasticsearch

es=Elasticsearch(['http://localhost:9200'])
report={'project':'Healthcare IoT Deception Honeypot','generated_at':datetime.now().isoformat(),
    'recommendations':['1. Network segmentation','2. Disable default credentials',
    '3. Block top IPs at firewall','4. Enforce MFA']}
try:
    r=es.search(index='honeypot-*',body={'query':{'range':{'@timestamp':{'gte':'now-30d'}}},'size':0,
        'aggs':{'total':{'value_count':{'field':'src_ip.keyword'}},'unique':{'cardinality':{'field':'src_ip.keyword'}}}})
    a=r['aggregations']
report['summary']={'total_attacks':a['total']['value'],'unique_attackers':a['unique']['value']}

except Exception as e: report['summary']={'error':str(e)}

fname=f'./analysis/reports/final_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
with open(fname,'w') as f: json.dump(report,f,indent=2)

print(json.dumps(report,indent=2))

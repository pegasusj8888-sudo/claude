import json,sys,os
p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'rows.jsonl')
rows=[json.loads(l) for l in open(p)] if os.path.exists(p) else []
a=sys.argv[1]
for new in (json.loads(a) if a.lstrip().startswith('[') else [json.loads(a)]):
    for k in ['chip','keyway','card','fold','blade_pn','smart','immo','src','note']: new.setdefault(k,'')
    rows=[r for r in rows if (r['model'],r['year'])!=(new['model'],new['year'])]+[new]
open(p,'w').write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
print(len(rows))

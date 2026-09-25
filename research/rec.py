# 사용: python3 rec.py '<json list>' — 해당 (model,year) 행을 갱신(지정 필드만), flag는 지정 없으면 제거
import json,sys
p='bmw_rows.jsonl'
rows=[json.loads(l) for l in open(p)]
idx={(r['model'],r['year']):r for r in rows}
for u in json.loads(sys.argv[1]):
    r=idx[(u['model'],u['year'])]
    r.pop('flag',None)
    for k,v in u.items(): r[k]=v
    if 'note' not in u: r['note']=''
open(p,'w').write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
print('ok',len(json.loads(sys.argv[1])),'| gen 남음',sum(1 for r in rows if r.get('flag')=='gen'))

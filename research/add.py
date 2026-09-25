# 사용법: python3 add.py '<json>'  — 모델·연식 1행을 bmw_rows.jsonl에 추가(같은 키면 교체)
import json,sys,os
p=os.path.join(os.path.dirname(__file__),'bmw_rows.jsonl')
rows=[json.loads(l) for l in open(p)] if os.path.exists(p) else []
for new in json.loads(sys.argv[1]) if sys.argv[1].startswith('[') else [json.loads(sys.argv[1])]:
    rows=[r for r in rows if (r['model'],r['year'])!=(new['model'],new['year'])]+[new]
open(p,'w').write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
print(len(rows))

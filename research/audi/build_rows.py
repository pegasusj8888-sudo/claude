# 아우디: yearly.md(연식별 검색 기록)를 근거로 행 생성
import json, re
ORDER=[l.rstrip('\n').split('\t') for l in open('years.txt')]
YR={m:y for m,y in ORDER}

# ---------- 연식별 검색 기록 ----------
LOG={}
for l in open('yearly.md'):
    p=l.rstrip('\n').split('|')
    if len(p)!=4 or not p[1][:4].isdigit(): continue
    LOG[(p[0],int(p[1]))]=(p[2],p[3])

# ---------- 국내 실제 판매 연식 (목록과 다른 경우만) ----------
R=lambda a,b:list(range(a,b+1))
KR={'A1 (8X, 1세대)':R(2015,2016),            # 2015.06 첫 출시, 2016 디젤게이트로 판매 중단
    'A3 (8P, 2세대)':R(2008,2012),            # 스포트백 2008.10 출시
    'A3 (8Y, 4세대)':R(2022,2026),            # 2022.07 출시
    'S3 (8Y)':R(2022,2026),                   # 2022.12 출시
    'RS3':R(2023,2026),                       # 8V 미판매, 8Y 2023.07
    'A5 (B10, 3세대)':R(2025,2026),           # 2025.07
    'RS6 아반트':R(2014,2018)+R(2021,2026),   # C7 2014.08, C8 2021.08
    'RS7':R(2014,2018)+R(2021,2026),
    'S6':R(2013,2018)+R(2020,2026),           # C8 S6 TDI 2020.07
    'A7 (C8, 2세대)':R(2020,2026),            # 2020.03
    'S7':R(2020,2026),                        # 2020.07
    'A8 (D5, 5세대)':R(2019,2026),            # 2019.12
    'S8':R(2013,2017)+R(2023,2026),           # D4(S8 플러스 2016.06), D5 S8 L 2023.07
    'Q2':R(2020,2026),                        # 2020.09
    'Q3 (F3, 2세대)':R(2020,2026),            # 2020.05
    'Q5 (FY, 2세대)':R(2020,2025),            # 2020.05
    'SQ5':R(2014,2017)+R(2020,2026),
    'Q7 (4L, 1세대)':R(2006,2015),            # 2006.07 판매 시작
    'Q7 (4M, 2세대)':R(2016,2026),            # 2016.03
    'SQ7':R(2024,2026),                       # 2024.01 첫 출시
    'Q8 (1세대)':R(2020,2026),                # 2020.04
    'RS Q8':R(2021,2026),                     # 2021.06
    'e-트론/Q8 e-트론':R(2020,2026),          # e-트론 55 2020.07
    'SQ8 e-트론':R(2024,2026),                # 2024.06
    'R8 (4S, 2세대)':R(2017,2024)}            # 2017.11
NEVER={'SQ2','RS Q3','TT RS'}                 # 국내 정식 판매 이력 없음

# ---------- 모델 → 검색 기록 그룹 ----------
G={'A1 (8X, 1세대)':['A1 8X'],'A3 (8P, 2세대)':['A3 8P'],'A3 (8V, 3세대)':['A3 8V'],'A3 (8Y, 4세대)':['A3 8Y'],
   'S3 (8V)':['S3 8V'],'S3 (8Y)':['S3 8Y'],'RS3':['RS3 8Y','RS3 8V'],
   'A4 (B6/B7, 6·7세대)':['A4 B6','A4 B6/B7','A4 B7'],'A4 (B8, 8세대)':['A4 B8'],'A4 (B9, 9세대)':['A4 B9'],
   'S4':['S4 B8','S4 B9','S4'],'RS4 아반트':['RS4 B9'],
   'A5 (B8, 1세대)':['A5 B8'],'A5 (B9, 2세대)':['A5 B9'],'A5 (B10, 3세대)':['A5 B10'],
   'S5':['S5 B8','S5 B9','S5 B10'],'RS5':['RS5 B8','RS5 B9','RS5 B10'],
   'A6 (C6, 6세대)':['A6 C6'],'A6 (C7, 7세대)':['A6 C7'],'A6 (C8, 8세대)':['A6 C8'],'A6 e-트론 (GH)':['A6 e-tron'],
   'S6':['S6 C7','S6 C8','S6 e-tron'],'RS6 아반트':['RS6 C7','RS6 C8'],
   'A7 (C7, 1세대)':['A7 C7'],'A7 (C8, 2세대)':['A7 C8'],'S7':['S7 C8'],'RS7':['RS7 C7','RS7 C8'],
   'A8 (D3/D4)':['A8 D3','A8 D4'],'A8 (D5, 5세대)':['A8 D5'],'S8':['S8 D4','S8 D5'],
   'Q2':['Q2'],'SQ2':['SQ2'],'Q3 (8U, 1세대)':['Q3 8U'],'Q3 (F3, 2세대)':['Q3 F3'],'RS Q3':['RS Q3'],'Q4 e-트론':['Q4 e-tron'],
   'Q5 (8R, 1세대)':['Q5 8R'],'Q5 (FY, 2세대)':['Q5 FY'],'Q5 (GU, 3세대)':['Q5 GU'],'SQ5':['SQ5 8R','SQ5 FY','SQ5 GU'],
   'Q6 e-트론':['Q6 e-tron'],'Q7 (4L, 1세대)':['Q7 4L'],'Q7 (4M, 2세대)':['Q7 4M'],'SQ7':['SQ7'],
   'Q8 (1세대)':['Q8'],'SQ8':['SQ8'],'RS Q8':['RS Q8'],'e-트론/Q8 e-트론':['e-tron'],'SQ8 e-트론':['SQ8 e-tron'],
   'TT (8J, 2세대)':['TT 8J'],'TT (8S, 3세대)':['TT 8S'],'TTS':['TTS 8S'],'TT RS':['TT RS'],
   'R8 (42, 1세대)':['R8 42'],'R8 (4S, 2세대)':['R8 4S'],'e-트론 GT':['e-tron GT'],'RS e-트론 GT':['RS e-tron GT']}

# ---------- 시스템(칩·이모빌라이저) ----------
ID48='ID48 Megamos Crypto (TP25/CAN)'
SYS={
 'ID48':(ID48,'IMMO4 (계기판 통합, CAN)'),
 'ID48i3':(ID48,'IMMO3 (계기판)'),
 'ID8E':('ID8E Crypto (Sokymat 8E)','EZS-Kessy (J518)'),
 'ID46':('ID46 Hitag2 (PCF7946A/PCF7952)','KESSY (J518)'),
 'BCM2':('PCF7945AC (BCM2 전용, Hitag2 계열)','BCM2 (IMMO5, J393)'),
 'MQB48':('Megamos AES (MQB48, ID88)','MQB IMMO5 (계기판 통합)'),
 'MQB49':('ID49 Hitag Pro (MQB49, NCF295X)','MQB-Evo IMMO5 (GeKo 온라인 필수)'),
 'MLB':('MLB 전용 칩 (5M, 4M0 계열 키)','MLB IMMO5 (KESSY/J393, 부품 분산 보안)'),
 'MLBE':('MLB evo 전용 칩 (4N0 계열 키)','MLB evo IMMO5 (부품 보호)'),
 'R84S':('확인 불가 (R8 4S 전용 키 칩 자료 없음)','확인 불가'),
 'NEW':('확인 불가 (신형 키 칩 자료 없음)','확인 불가 (PPE/PPC·E³ 전자 아키텍처)'),
 'MEB':('확인 불가 (MEB 키 칩 자료 없음)','확인 불가 (MEB)')}
def gsys(g,y):
    if g in ('A1 8X','A3 8P','A4 B6/B7','A4 B7','Q3 8U','TT 8J','R8 42'): return 'ID48'
    if g=='A4 B6': return 'ID48i3'
    if g in ('A6 C6','Q7 4L'): return 'ID8E'
    if g=='A8 D3': return 'ID46'
    if g in ('A4 B8','S4 B8','A5 B8','S5 B8','RS5 B8','A6 C7','S6 C7','RS6 C7','A7 C7','RS7 C7','A8 D4','S8 D4','Q5 8R','SQ5 8R'): return 'BCM2'
    if g in ('A3 8V','S3 8V','RS3 8V','Q2','SQ2','Q3 F3','RS Q3','TT 8S','TTS 8S','TT RS'): return 'MQB48'
    if g in ('A3 8Y','S3 8Y','RS3 8Y'): return 'MQB49'
    if g in ('A4 B9','S4 B9','S4','RS4 B9','A5 B9','S5 B9','RS5 B9','Q5 FY','SQ5 FY','Q7 4M','SQ7'): return 'MLB'
    if g=='R8 4S': return 'R84S'
    if g=='Q4 e-tron': return 'MEB'
    if g in ('A5 B10','S5 B10','RS5 B10','A6 e-tron','S6 e-tron','Q5 GU','SQ5 GU','Q6 e-tron'): return 'NEW'
    return 'MLBE'

# ---------- 국내형(433/434MHz) 부품번호 ----------
def parts(g,y,s):
    d=dict(fold='',smart='',card='',blade_pn='')
    if g in ('A1 8X','Q3 8U'): d['fold']='8X0837220D (434MHz)'
    elif g in ('A3 8P','TT 8J'): d['fold']='8P0837220D (434MHz)'
    elif g in ('A4 B6/B7','A4 B7'): d['fold']='8E0837220E/Q/K (433MHz)'
    elif g=='R8 42': d['fold']='420837220 (433MHz)'
    elif g in ('A6 C6','Q7 4L'): d['fold']='4F0837220M/T (434MHz)'
    elif g=='A8 D3': d['fold']='4E0837220M/D (433MHz)'
    elif s=='BCM2':
        d['smart']='4G0959754F/AF (433MHz)' if g[:2] in ('A6','S6','RS','A7','A8','S8') and g not in ('RS5 B8',) else '8T0959754F (433MHz)'
    elif g in ('A3 8V','S3 8V'): d['fold']='8V0837220D (434MHz)'
    elif g in ('Q2','SQ2'): d['fold']='81A837220D (434MHz)'
    elif g=='Q3 F3': d['fold']='81A837220AG (434MHz)'
    elif g in ('TT 8S','TTS 8S','TT RS'): d['smart']='8S0959754AK (434MHz)'
    elif s=='MQB49': d['smart']='8Y0959754AN (434MHz)'
    elif s=='MLB':
        if g=='Q7 4M' and y==2016: d['smart']='4M0959754BC (434MHz)'
        elif 2017<=y<=2021: d['smart']='4M0959754BA (433MHz)'; d['blade_pn']='4M0837216A (비상키)'
    elif g=='Q8': d['smart']='4N0959754BL (434MHz)'
    elif g in ('RS6 C8','RS7 C8','RS Q8','RS e-tron GT','e-tron GT'): d['smart']='4N0959754BC (433.92MHz)'
    return d

# ---------- 키종류 ----------
def ktype(g,y,s):
    if g=='A4 B6': return '막대키'
    if s in ('ID48','ID8E','ID46'): return '폴딩키'
    if g in ('A3 8V','S3 8V','RS3 8V','Q2','SQ2','Q3 F3','RS Q3'): return '폴딩키'
    if g in ('A6 e-tron','S6 e-tron','Q6 e-tron','Q5 GU'): return '스마트키,카드키'
    return '스마트키'

# ---------- 색·비고 ----------
NOT_KR='국내 정식 판매 이력 없음 — 해외 사양 기준'
def flag_of(m,g,y,s,res):
    if m in NEVER: return 'orange',NOT_KR
    if s in ('NEW','MEB'): return 'red','신형 키(PPE·PPC·MEB) 칩·이모빌라이저 자료 없음'
    if s=='R84S': return 'orange','R8 4S 키(4H0959754EB 계열) 칩 형식 자료 없음 — 이모빌라이저 확인 필요'
    if g=='A4 B6' and y==2001: return 'orange','2001년식 국내분은 B5(ID48) 가능성 — 세대 확인 필요'
    if '상충' in res: return 'orange','칩 표기 자료 상충 — 세대 기본값 기재, 실물 확인 필요'
    if '불명' in res or '여부 확인 필요' in res: return 'orange','해당 연식 국내 판매 여부 불명확 — 세대 기준 기재'
    if '신규 생산 없음' in res: return 'orange','2025.02 단종 — 2026년식은 재고 차량만'
    if '자료 없음' in res: return 'orange','해당 연식 칩 자료 없음 — 같은 세대 기준 추정'
    return None,''

rows=[]
for m,yr in ORDER:
    a,b=yr.split('-'); a=int(a); ended=b!='현재'; b=2026 if b=='현재' else int(b)
    years=KR.get(m) or R(max(a,2000),b)
    last=years[-1]
    for y in years:
        gs=G[m]; hit=None
        for g in gs:
            if (g,y) in LOG: hit=g; break
        if hit is None:
            # 목록에 없던 국내 판매 연식 또는 기록 없는 연식: 가장 가까운 연식 기준
            cand=[(abs(yy-y),g,yy) for g in gs for (gg,yy) in LOG if gg==g]
            _,hit,near=min(cand); res,src=LOG[(hit,near)]
            src=f'{near}년식 기록 준용 — '+src
            fl,why='orange',f'{y}년식 개별 검색 자료 없음 — {near}년식 기준 추정'
        else:
            res,src=LOG[(hit,y)]
            fl=None
        s=gsys(hit,y); chip,immo=SYS[s]
        if s=='BCM2' and y>=2013: immo+=' — 2013년경 이후 공장 잠김'
        if fl is None: fl,why=flag_of(m,hit,y,s,res)
        elif s in ('NEW','MEB'): fl,why='red',why+', 신형 키 칩 자료 없음'
        d=dict(model=m,year=str(y)+('(단종)' if (ended or KR.get(m)) and y==last and last<2026 else ''),
               chip=chip,keyway=('HU66' if s in ('ID48','ID48i3','ID8E','ID46','BCM2','MLB','MQB49') else 'HU66 / HU162T' if s=='MQB48' else 'HU162T' if hit=='Q8' else ''),
               immo=immo,src=src,note=why,ktype_hint=ktype(hit,y,s))
        d.update(parts(hit,y,s))
        if fl: d['flag']=fl
        rows.append(d)

# ---------- 전환 연식 (전·후 함께, 색 없음 원칙 — 후속 칩 미상이면 빨강) ----------
def setrow(m,y,**k):
    for r in rows:
        if r['model']==m and r['year'].startswith(str(y)): r.update(k); return
    raise SystemExit((m,y))
setrow('TT (8S, 3세대)',2015,chip=f'{ID48} (2015.10 이전 8J) / Megamos AES (MQB48, ID88) (8S)',
       immo='IMMO4 (8J) / MQB IMMO5 (8S)',fold='8P0837220D (434MHz, 8J)',smart='8S0959754AK (434MHz, 8S)',ktype_hint='폴딩키,스마트키')
setrow('Q3 (F3, 2세대)',2026,chip='Megamos AES (MQB48, ID88) (2026.06 이전 F3) / 확인 불가 (3세대)',
       immo='MQB IMMO5 (F3) / 확인 불가 (3세대)',flag='red',note='3세대 Q3(2026.06~) 키 칩 자료 없음')
setrow('S5',2025,chip='MLB 전용 칩 (2025.07 이전 B9) / 확인 불가 (B10)',immo='MLB IMMO5 (B9) / 확인 불가 (B10)',
       flag='red',note='B10(2025.07~) 신형 키 칩 자료 없음')
setrow('SQ5',2025,chip='MLB 전용 칩 (FY) / 확인 불가 (3세대, 2025년 4분기~)',immo='MLB IMMO5 (FY) / 확인 불가 (3세대)',
       flag='red',note='3세대 SQ5 신형 키 칩 자료 없음')
setrow('RS5',2026,flag='red',note='B10 RS5(PHEV) 국내 출시·키 칩 자료 없음')
setrow('A6 (C6, 6세대)',2004,chip=f'{ID48} (C5) / ID8E Crypto (Sokymat 8E) (2004.10~ C6)',immo='IMMO3 (C5) / EZS-Kessy J518 (C6)',
       fold='4F0837220M/T (434MHz, C6)')

for r in rows:
    if r.get('flag') is None: r.pop('flag',None); r['note']=''
open('rows.jsonl','w').write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
from collections import Counter
print(len(rows),Counter(r.get('flag') for r in rows))
assert {r['model'] for r in rows}==set(YR)
for r in rows: assert r['src'], r

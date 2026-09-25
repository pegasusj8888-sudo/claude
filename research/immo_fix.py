import json,re
p='research/bmw_rows.jsonl'
rows=[json.loads(l) for l in open(p)]
def yr(r): return int(r['year'][:4])
changes=[]
def setv(r,immo,src,flag=None,note=None):
    old=r['immo']; oldf=r.get('flag')
    r['immo']=immo
    r.pop('flag',None)
    if flag: r['flag']=flag
    if src and src not in r['src']: r['src']=(r['src']+', ' if r['src'] else '')+src
    if note is not None:
        r['note']=note
    elif oldf and not flag:
        # 출처 상충/확인필요 문구 제거
        r['note']=re.sub(r'[^/]*(상충|확인 필요|미확인|추정)[^/]*','',r['note']).strip(' /')
    if (old,oldf)!=(immo,flag): changes.append((r['model'],r['year'],old,immo))
def M(key): return [r for r in rows if key in r['model']]

FEM_SRC='이모빌라이저 검증: 딜러 부품 FEM 61355A7FB57(F22/F23/F30~F36/F80/F82/F83), F30 LCI FEM 매물, M2C FEM 61359438730(2016/09~2019/12)'
for k in ['1시리즈 (F20','2시리즈 쿠페 (F22','M2 (F87','3시리즈 (F30','M3 (F80','4시리즈 (F32','M4 (F82']:
    for r in M(k): setv(r,'FEM',FEM_SRC,note='' if r.get('flag') or 'BDC' in r['immo'] else None)
BDC_SRC='이모빌라이저 검증: 딜러 부품 카탈로그 BDC(Body Domain Controller) 표기'
for k in ['X5 (F15','X6 (F16','X5 M (F85','X6 M (F86','i3 (I01','i8 (I12','2시리즈 액티브 투어러 (F45']:
    for r in M(k): setv(r,'BDC',BDC_SRC,note='' if r.get('flag') else None)
B3_SRC='이모빌라이저 검증: BDC3=BDC_G05(SP2018 플랫폼, 출시부터 BDC3) — Xhorse/Yanhua BDC 적용표'
for k in ['3시리즈 (G20','X5 (G05','X6 (G06','X7 (G07','8시리즈 (G15','M8 (G15','Z4 (G29','1시리즈 (F40','2시리즈 그란 쿠페 (F44','2시리즈 쿠페 (G42','M2 (G87','4시리즈 (G22','i4 (G26','M3 (G80','M4 (G82','X5 M (F95','X6 M (F96']:
    for r in M(k):
        if 'BCP' in r['immo'] or '추정' in r['immo']: continue
        setv(r,'BDC3',B3_SRC,note='' if r.get('flag') or 'BDC2' in r['immo'] else None)
# G11/G12: BDC2 ~2019.2, BDC3 2019.3~
for r in M('7시리즈 (G11'):
    y=yr(r)
    if y<=2018: setv(r,'BDC2','')
    elif y==2019: setv(r,'BDC2(2019.2 이전 생산) / BDC3(2019.3 이후 생산)','이모빌라이저 검증: Xhorse/Yanhua BDC 적용표(G11/G12 BDC2 ~2019/02, BDC3 2019/03~)',note='2019 LCI 시점 BDC3 전환')
    else: setv(r,'BDC3','이모빌라이저 검증: Xhorse/Yanhua BDC 적용표(G11/G12 BDC3 2019/03~)',note='')
# G30/G31/G32/F90: BDC2 ~2020.6, BDC3 2020.7~
for k in ['5시리즈 (G30','6시리즈 그란 투리스모 (G32','M5 (F90']:
    for r in M(k):
        y=yr(r)
        if y==2020: setv(r,'BDC2(2020.6 이전 생산) / BDC3(2020.7 이후 생산)','이모빌라이저 검증: Xhorse/Yanhua BDC 적용표(G30/G31/G32/F90 BDC2 ~2020/06, BDC3 2020/07~)')
        elif y>2020: setv(r,'BDC3','',note='' if r.get('flag') else None)
# G01/G02/F97/F98: BDC2 ~2021.7, BDC3 2021.8~
for k in ['X3 (G01','X4 (G02','X3 M (F97','X4 M (F98']:
    for r in M(k):
        y=yr(r)
        if 'BDC' not in r['immo']: continue
        if y<=2020: setv(r,'BDC2','이모빌라이저 검증: Xhorse/Yanhua BDC 적용표(G01/G02/F97/F98 BDC2 ~2021/07)',note='')
        elif y==2021: setv(r,'BDC2(2021.7 이전 생산) / BDC3(2021.8 이후 생산)','이모빌라이저 검증: Xhorse/Yanhua BDC 적용표(G01/G02/F97/F98 BDC2 ~2021/07, BDC3 2021/08~)',note='')
for r in M('iX3 (G08'):
    if yr(r)==2021: setv(r,'BDC2(2021.8 이전 생산) / BDC3(2021.9 이후 생산)','이모빌라이저 검증: Xhorse/Yanhua BDC 적용표(G08 BDC2 ~2021/08)',note='')
# BCP 확정
for k in ['7시리즈 (G70','i7 (G70']:
    for r in M(k): setv(r,'BCP','이모빌라이저 검증: 딜러 부품 카탈로그 i7 "Control u.basic computing platform (BCP)" 61355A9A210',note='')
for r in M('iX (I20'): setv(r,'BCP','이모빌라이저 검증: 딜러 부품 카탈로그 iX BCP 61355A9A210')
# E65
for r in M('7시리즈 (E65'):
    y=yr(r); s='이모빌라이저 검증: MHH Auto CAS 적용표(E65 CAS1 ~2005 LCI, 이후 CAS2)'
    if y<=2004: setv(r,'CAS1',s)
    elif y==2005: setv(r,'CAS1(2005 LCI 이전 생산) / CAS2(2005 LCI 이후 생산)',s,note='2005 LCI 전후 CAS 모듈 상이')
    else: setv(r,'CAS2',s,note='')
# E60/E63/M5 E60
for k in ['5시리즈 (E60','M5 (E60','6시리즈 (E63']:
    for r in M(k):
        y=yr(r); s='이모빌라이저 검증: MHH Auto CAS 적용표·bimmerfest(E60 CAS2 2003~2007, LCI CAS3)'
        if y==2006: setv(r,'CAS2',s,note='일부 판매처는 2006~ CAS3 표기 — 국내 2006년식은 LCI(2007.3) 이전 생산분')
        elif y==2007: setv(r,'CAS2(2007.3 LCI 이전 생산) / CAS3(2007.3 LCI 이후 생산)',s,note='2007.3 LCI 전후 CAS 모듈 상이')
# E83: EWS3 ~2006, 2006 중 EWS4 전환, 2007 LCI EWS4
for r in M('X3 (E83'):
    y=yr(r); s='이모빌라이저 검증: bimmerfest(E83 2004-2006 EWS3, 2006 중 EWS4 전환, 2007 LCI EWS4 — AK90 EWS4 어댑터 필요)'
    if y<=2005: setv(r,'EWS3',s)
    elif y==2006: setv(r,'EWS3(2006 중반 이전 생산) / EWS4(2006 중반 이후 생산)',s,note='')
    else: setv(r,'EWS4',s,note='2007 LCI')
open(p,'w').write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
for c in changes: print(*c,sep=' | ')
print(len(changes))

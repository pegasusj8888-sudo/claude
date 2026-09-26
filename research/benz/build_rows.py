import json
ORDER=[l.rstrip('\n').split('\t') for l in open('years.txt')]
YR={m:y for m,y in ORDER}
rows=[]
F3='FBS3 (NEC 프로세서 키)'
F4='FBS4 (NEC 신형 키, 딜러 서버 인증)'
I3='EIS(EZS) — FBS3'
I4='EIS(EZS) — FBS4'
SRC3='auto-keys.eu(벤츠 순정 스마트키 433MHz NEC 프로세서, HU64, FBS2/3 EZS 크롬키), abkeys.com(FBS3 키리스고 스마트키 W204/W212/W164/W221), doornkey·obdii365(대부분 2014년까지 FBS3)'
SRC4='obdii365.com(FBS4 적용: W212 2013.4~, 166·207·V212 2013.7~, 218 2014.9~, 117·156 2014.11~, 172 2015.4~, 205·217·218·222·231 전 연식), abkeys.com(순정 FBS4 스마트키 2014-2023 433MHz IYZDC12B / 2019+ FBS4 비상키 HU64)'
SRCN='montyslocksmith.ca·doornkey(2021-2026 W223·W206·W214 FBS4 스마트키, 딜러 전용), amazon(W223·W206 Gen4 비상키 인서트), abkeys.com(2019+ 비상키 HU64)'
def smart4(y,extra=''):
    s='IYZDC12B (FBS4 433MHz 3버튼)' if 2014<=y<=2023 else ''
    return ' / '.join(x for x in (extra,s) if x)
def span(m):
    a,b=YR[m].split('-'); return int(a),(2026 if b=='현재' else int(b)),b!='현재'
def add(m,gen,new=False,src_extra='',smart_extra='',flag=None,note=''):
    """gen(y) -> 'F3' | 'F4' | ('T',month_text) | ('X',chip,immo,ktype,flag,note)"""
    a,b,ended=span(m)
    for y in range(max(a,2000),b+1):
        g=gen(y); d=dict(model=m,year=str(y)+('(단종)' if ended and y==b else ''),chip='',keyway='HU64',card='',fold='',blade_pn='',smart='',immo='',src='',note='',ktype_hint='스마트키')
        if g=='F3':
            d.update(chip=F3,immo=I3,src=SRC3)
        elif g=='F4':
            d.update(chip=F4,immo=I4,src=SRCN if new else SRC4,smart=smart4(y,smart_extra))
        elif g[0]=='T':
            d.update(chip=f'FBS3 (NEC) / FBS4 ({g[1]} 이후 생산)',immo=f'EIS(EZS) — FBS3({g[1]} 이전 생산) / FBS4({g[1]} 이후 생산)',src=SRC4,smart=smart4(y,smart_extra))
        else:
            _,chip,immo,kt,fl,nt,src=g
            d.update(chip=chip,immo=immo,ktype_hint=kt,src=src)
            if fl: d['flag']=fl
            d['note']=nt
        if src_extra: d['src']+=', '+src_extra
        if flag and 'flag' not in d: d['flag']=flag; d['note']=note
        rows.append(d)
F3_=lambda y:'F3'
F4_=lambda y:'F4'
def upto(yr,then='F4',before='F3',trans=None):
    def f(y):
        if trans and y==trans[0]: return ('T',trans[1])
        return before if y<yr else then
    return f
X=lambda chip,immo,kt,fl,nt,src:('X',chip,immo,kt,fl,nt,src)

W176='검색 요약(A클래스 W176: 2012-2013 FBS3, 2014년 이후 FBS4)'
add('A클래스 (W176, 3세대 해치백)',upto(2014),src_extra=W176)
add('A클래스 세단 (V177, 4세대)',F4_)
add('A45 AMG (W176/W177)',upto(2014),src_extra=W176)
def b246(y):
    if y<=2013: return 'F3'
    return X('FBS4 추정 (NEC 신형 키)','EIS(EZS) — FBS4 추정','스마트키','orange','W246 FBS4 전환 시점 자료 없음 — 같은 플랫폼 A클래스(W176) 2014년 전환 기준 추정',SRC4+', '+W176)
add('B클래스 (W246)',b246)
add('CLA (C117, 1세대)',upto(2015,trans=(2014,'2014.11')))
add('CLA (C118, 2세대)',F4_)
add('CLA45 AMG (C117/C118)',upto(2015,trans=(2014,'2014.11')))
add('C클래스 (W204, 3세대)',F3_)
add('C클래스 (W205/C205, 4세대)',F4_)
add('C클래스 (W206, 5세대)',F4_,new=True)
add('C클래스 쿠페 (C205)',F4_)
add('C클래스 카브리올레 (A205)',F4_)
add('C43/C63 AMG (W205)',F4_)
add('C63 AMG (W206)',F4_,new=True)
add('CLE (C236)',F4_,new=True)
add('E클래스 (W211, 8세대)',F3_)
add('E클래스 (W212, 9세대)',upto(2014,trans=(2013,'2013.4')))
add('E클래스 (W213, 10세대)',F4_)
add('E클래스 (W214, 11세대)',F4_,new=True)
add('E클래스 쿠페 (C207)',upto(2014,trans=(2013,'2013.7')))
add('E클래스 카브리올레 (A207)',upto(2014,trans=(2013,'2013.7')))
add('E클래스 쿠페 (C238)',F4_)
add('E클래스 카브리올레 (A238)',F4_)
add('E53/E63 AMG (W213)',F4_)
add('E53 AMG (W214)',F4_,new=True)
add('CLS (C219, 1세대)',F3_)
add('CLS (C218, 2세대)',upto(2015,trans=(2014,'2014.9')))
add('CLS (C257, 3세대)',F4_)
add('CLS53/63 AMG',upto(2015,trans=(2014,'2014.9')))
add('S클래스 (W221, 5세대)',F3_)
W222='autokeystore.com(W222 FBS4 키리스고 키 433MHz A2229059610)'
add('S클래스 (W222, 6세대)',F4_,src_extra=W222,smart_extra='A2229059610 (W222 FBS4 433MHz)')
add('S클래스 (W223, 7세대)',F4_,new=True)
add('S클래스 쿠페 (C217)',F4_)
add('S클래스 카브리올레 (A217)',F4_)
add('메르세데스-마이바흐 S클래스 (X222)',F4_,src_extra=W222,smart_extra='A2229059610 (W222 FBS4 433MHz)')
add('메르세데스-마이바흐 S클래스 (Z223)',F4_,new=True)
add('S63/S65 AMG (W222)',F4_,src_extra=W222,smart_extra='A2229059610 (W222 FBS4 433MHz)')
add('S63 AMG (W223)',F4_,new=True)
add('GLA (X156, 1세대)',upto(2015,trans=(2014,'2014.11')))
add('GLA (H247, 2세대)',F4_)
add('GLA35/45 AMG',upto(2015,trans=(2014,'2014.11')))
add('GLB (X247, 1세대)',F4_)
add('GLB35 AMG',F4_)
GLK='diag.net·doornkey(2014 GLK350은 FBS3, 2015년식은 FBS3/FBS4 혼재 가능 — VIN 확인)'
def glk(y):
    if y<2015: return 'F3'
    return X('FBS3 / FBS4 (2015년식 혼재 가능)','EIS(EZS) — FBS3 / FBS4','스마트키','orange','2015년식은 FBS3·FBS4 혼재 가능 — FBS4 적용 목록에 X204 없음, VIN 확인 필요',SRC3+', '+GLK)
add('GLK (X204)',glk,src_extra='top-rider(신형 GLK 2012.8 국내 출시)')
add('GLC (X253/C253, 1세대)',F4_)
add('GLC (X254/C254, 2세대)',F4_,new=True)
add('GLC43/63 AMG (X253)',F4_)
add('GLC63 AMG (X254)',F4_,new=True)
add('M클래스 (W164, 2세대)',F3_)
add('M클래스 (W166, 3세대)',upto(2014,trans=(2013,'2013.7')))
add('GLE (W166/C292, 3세대)',F4_)
add('GLE (W167/V167/C167, 4세대)',F4_)
add('GLE43/53/63 AMG',F4_)
add('GL클래스 (X164/X166)',upto(2014,trans=(2013,'2013.7')),src_extra='wikipedia(GL X164 2006-2012, X166 2012~)')
add('GLS (X166, 1세대)',F4_)
add('GLS (X167, 2세대)',F4_)
add('메르세데스-마이바흐 GLS (X167)',F4_)
GSRC='locksmithkeyless.com(HU64 ID44 트랜스폰더 키: 2004-2011 G500 적용 표기), paylesscarkeys·fixautosmart(G500 2002-2012 W463 EIS/EZS 스마트키 등록)'
G16='mhhauto.com(2016 W463 FBS4 사례 / 2016 G바겐 FBS3 의견 병존)'
def g_old(y):
    if y<=2001: return X('ID44(PCF7935) 추정','DAS(트랜스폰더 키) 추정','막대키','orange','2002년 이전 W463 키 자료 없음 — 같은 시기 벤츠 HU64 ID44 트랜스폰더 키 기준 추정',GSRC)
    if y<=2012: return X('FBS3 (NEC 프로세서 키)','EIS(EZS) — FBS3','스마트키','orange','EIS 스마트키 자료와 ID44 트랜스폰더 막대키(2004-2011 G500) 자료 상충 — 실물 확인',GSRC+', '+SRC3)
    if y<=2015: return 'F3'
    if y==2016: return X('FBS3 / FBS4 (자료 상충)','EIS(EZS) — FBS3 / FBS4','스마트키','orange','2016년식 FBS3·FBS4 자료 상충',SRC4+', '+G16)
    return 'F4'
add('G클래스 (W463, 구형 바디)',g_old,src_extra='')
add('G클래스 (W463, 신형 바디)',F4_)
def g63(y):
    if y<=2015: return 'F3'
    if y==2016: return X('FBS3 / FBS4 (자료 상충)','EIS(EZS) — FBS3 / FBS4','스마트키','orange','2016년식 FBS3·FBS4 자료 상충',SRC4+', '+G16)
    return 'F4'
add('G63 AMG',g63)
add('SLK/SLC (R172)',upto(2016,trans=(2015,'2015.4')))
add('SL (R231)',F4_)
add('SL (R232)',F4_,new=True)
add('AMG GT (C190/R190)',F4_)
for m in ['EQC','EQA (H243)','EQB (X243)']: add(m,F4_)
for m in ['EQS 세단 (V297)','EQE 세단 (V295)','EQS SUV (X296)','EQE SUV (X294)']: add(m,F4_,new=True)

for r in rows:
    if not r['smart']: r['smart']=''
open('rows.jsonl','w').write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
from collections import Counter
print(len(rows),Counter(r.get('flag') for r in rows))
assert {r['model'] for r in rows}==set(YR)

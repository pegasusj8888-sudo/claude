# 검색 한도(200회) 도달 후 남은 모델: 이미 받은 검색결과(세대 단위)만으로 채우고 flag='gen'(하늘색) 표시
import json,subprocess
GEN='연식별 개별 검색 미완료(검색 한도 200회 도달) — 앞선 검색결과(세대 단위)로 임시 기입'
HU92='HU92 / Lishi HU92'; HU100R='HU100R / Lishi HU100R'
B925='925971801(HU100R 블레이드, 비상키)'; ABK='ABK-2338(G시리즈 HU100R 비상키, 애프터마켓)'
C46='ID46(PCF7945)'; C44='ID44(PCF7935)'; C4='ID49(PCF7953P, Hitag Pro/EWS5)'; CF='ID49(PCF7953P, Hitag Pro)'
C2='ID49(Hitag Pro)'; C3='ID49(Hitag Pro 변형, BDC3)'; CB='ID49(NCF2951, Hitag Pro)'
S_CAS4='amazon(Keymall FEM/BDC/CAS4/CAS4+ 2011-2017 X3/X4), ebay(CAS4 X3/X4 F25 2014-2017 PCF7953), ryan-keys.com(CAS4/CAS4+ X3 F25·X4)'
S_BDC2='uhs-hardware.com(N5F-ID21A BDC2: 2017-2021 X3 G01·X4 G02, 2018-2021 iX3 G08, 2017-2020 M5 F90 등)'
S_BDC3='amazon(BDC3 2020-2024 G시리즈 키데이터 리더: 3/4/5/7/8, X3/X5/X6/X7), obdii365.com(Autel BDC3 2020-2024)'
S_IYZ='ebay(IYZBK1 2022-2025 X1~X7 순정), ebay(IYZBK1 2022-2026, 2024-2026 X5/X6 호환)'
S_FEM='locksmithkeyless.com(2014-2018 X5/X6 FEM/BDC NBGIDGNG1), northcoastkeyless.com(2014-2016 X5 N5F-ID21A 9367401-01), yourcarkeyguys.com(NBGIDGNG1 2014-2019 X5/X6)'
S_CAS3='amazon(HU92 CAS3 E90~E71 315MHz), bestkeysolution.com(5WK49127/5WK49124 E60/E70/E90 CAS3/CAS3+), mr-key.com(X5/X6 868MHz PCF7945)'
S_EWS='royalkeysupply.com(2000-2009 X3/X5/Z8 EWS HU92), ebay(X3 E83/X5 E53 2003-2010 EWS ID44 플립키), amazon.co.uk(EWS E39/E83/E53/E85 ID44 HU92)'
out=[]
def add(model,years,chip,kw,blade,smart,immo,src,note='',flag='gen'):
    for y in years:
        out.append(dict(model=model,year=y,chip=chip,keyway=kw,card='',fold='',blade_pn=blade,smart=smart,immo=immo,src=src,note=(note+' / ' if note else '')+GEN,flag=flag))
def yrs(a,b,ended=True):
    L=[str(y) for y in range(a,b+1)]
    if ended: L[-1]+='(단종)'
    return L
def gseries(model,a,b,ended,bdc2_until=2019):
    L=yrs(a,b,ended)
    for y in L:
        n=int(y[:4])
        if n<=bdc2_until: add(model,[y],C2,HU100R,ABK,'N5F-ID21A(FCC, 9367401-01)','BDC2',S_BDC2)
        elif n<=2021: add(model,[y],C2,HU100R,ABK,'N5F-ID21A(FCC)','BDC2 / BDC3',S_BDC2+', '+S_BDC3,'2020.7 전후 BDC3 전환(G30 기준) — 생산월 확인')
        else: add(model,[y],C3,HU100R,ABK,'IYZBK1(FCC)','BDC3',S_BDC3+', '+S_IYZ)
add('X3 (F25, 2세대)',['2013','2014','2015','2016','2017(단종)'],C4,HU100R,B925,'YGOHUF5662(315MHz) / YGOHUF5767(434MHz)','CAS4+',S_CAS4)
gseries('X3 (G01, 3세대)',2017,2024,True)
add('X3 (G45, 4세대)',['2024','2025','2026'],'확인 불가',HU100R+'(추정)','','','확인 불가(신형 BCP 추정)','g45.bimmerpost.com(G45 키), 검색 한도로 추가 조사 불가',flag='red')
gseries('X3 M (F97)',2019,2026,False)
add('X4 (F26, 1세대)',yrs(2014,2018),C4,HU100R,B925,'YGOHUF5662(FCC) / HUF5767','CAS4+',S_CAS4)
gseries('X4 (G02, 2세대)',2018,2026,False)
gseries('X4 M (F98)',2019,2026,False)
add('X5 (E53, 1세대)',yrs(2000,2006),C44,HU92,'HU92 EWS 트랜스폰더키(ID44, 2트랙)','LX8FZV(FCC, EWS 3버튼)','EWS3',S_EWS)
for y in yrs(2006,2013):
    n=int(y[:4])
    if n<=2007: add('X5 (E70, 2세대)',[y],C46,HU92,'HU92 비상키','5WK49127(리모컨키) / KR55WK49147(컴포트액세스)','CAS3',S_CAS3)
    elif n==2008: add('X5 (E70, 2세대)',[y],C46,HU92,'HU92 비상키','5WK49127 / KR55WK49147','CAS3 / CAS3+',S_CAS3,'2008 CAS3 → CAS3+ 전환 — 생산월 확인')
    else: add('X5 (E70, 2세대)',[y],C46,HU92,'HU92 비상키','5WK49127 / KR55WK49147','CAS3+',S_CAS3)
add('X5 (F15, 3세대)',yrs(2013,2018),CF,HU100R,B925,'NBGIDGNG1(FCC) / 9367401-01(N5F-ID21A)','FEM / BDC (출처 상충)',S_FEM,'자료마다 FEM/BDC 표기 혼재')
for M,a,b,e in [('X5 (G05, 4세대)',2019,2026,False),('X6 (G06, 3세대)',2019,2026,False),('X7 (G07)',2019,2026,False)]:
    for y in yrs(a,b,e):
        n=int(y[:4])
        if n==2019: add(M,[y],C2,HU100R,ABK,'N5F-ID21A(FCC)','BDC2',S_BDC2+', turnermotorsport.com(G07 키)')
        elif n<=2021: add(M,[y],C2,HU100R,ABK,'N5F-ID21A(FCC)','BDC2 / BDC3',S_BDC3,'2020.7 전후 전환 추정')
        elif n<=2023: add(M,[y],C3,HU100R,ABK,'IYZBK1(FCC)','BDC3',S_BDC3+', '+S_IYZ)
        else: add(M,[y],C3,HU100R,ABK,'IYZBK1(FCC)'+(' / 2026년식 키 1개+디지털키' if n==2026 else ''),'BDC3 / BCP (확인 필요)',S_IYZ+', g07.bimmerpost.com(2024 신형 실물키), g05.bimmerpost.com(2026 X5 키 1개)','2023 LCI 이후 신형 키 — BCP 여부 미확인')
add('X5 M (F85)',yrs(2015,2018),CF,HU100R,B925,'NBGIDGNG1(FCC)','FEM / BDC (출처 상충)',S_FEM)
for M in ['X5 M (F95)','X6 M (F96)']:
    for y in yrs(2020,2026,False):
        n=int(y[:4])
        if n<=2021: add(M,[y],C2,HU100R,ABK,'N5F-ID21A(FCC)','BDC2 / BDC3',S_BDC3,'2020.7 전후 전환 추정')
        else: add(M,[y],C3,HU100R,ABK,'IYZBK1(FCC)','BDC3',S_BDC3+', '+S_IYZ)
for y in yrs(2008,2014):
    n=int(y[:4])
    add('X6 (E71, 1세대)',[y],C46,HU92,'HU92 비상키','5WK49127 / KR55WK49147',{2008:'CAS3 / CAS3+'}.get(n,'CAS3+'),S_CAS3,'2008 CAS3 → CAS3+ 전환' if n==2008 else '')
add('X6 (F16, 2세대)',yrs(2014,2019),CF,HU100R,B925,'NBGIDGNG1(FCC)','FEM / BDC (출처 상충)',S_FEM)
add('X6 M (F86)',yrs(2015,2018),CF,HU100R,B925,'NBGIDGNG1(FCC)','FEM / BDC (출처 상충)',S_FEM)
add('XM (G09)',['2023','2024','2025','2026'],'확인 불가',HU100R+'(추정)','','','확인 불가','검색 한도로 조사 불가',flag='red')
add('Z4 (E85, 1세대)',yrs(2003,2009),C44,HU92,'HU92 EWS 트랜스폰더키(ID44)','LX8FZV(FCC, EWS)','EWS3 / EWS4',S_EWS+', accessfobs.co.uk(EWS X3/X5/Z4)')
add('Z4 (E89, 2세대)',yrs(2009,2018),C46,HU92,'HU92 비상키','5WK49127 / 컴포트액세스 KR55WK49147','CAS3+','reidsremotes.com.au(3시리즈·X1 E84·Z4 E89 컴포트액세스 CAS3), mr-key.com(X1/X5/X6/Z 868MHz PCF7945)')
gseries('Z4 (G29, 3세대)',2019,2026,False)
for M,a,b in [('i3 (I01)',2014,2021),('i8 (I12/I15)',2014,2020)]:
    add(M,yrs(a,b),CF,HU100R,B925,'9317163-02 / 9317161-02(NBG1DGNG1 4버튼 434MHz) / 2013DJ5983','BDC (일부 자료 FEM/CAS4+)','abkeys.com(i3/i8 2015+ NBG1DGNG1 9317163-02·9317161-02 FEM/BDC), keyshop-online.com(i3/i8 2013-2017 BDC 2013DJ5983), locksmithkeyless.com(2015-2017 i3/i8 NBGIDGNG1)')
add('i4 (G26)',['2022','2023','2024','2025','2026'],C3,HU100R,ABK,'IYZBK1(FCC)','BDC3',S_BDC3+'(4시리즈 G26 포함), carkeysexpress.com(2026 i4 키 페어링)')
add('iX (I20)',['2021','2022','2023','2024','2025','2026'],CB,HU100R+'(추정)','','IYZBK1(FCC, 2025-2026 iX 호환 표기)','BCP (추정)','ebay(IYZBK1: 2025-2026 iX 호환), adlhardware.com(2022-2026 U Body IYZBK1), g07.bimmerpost.com(i모델 컴포트액세스 = BCP)')
for y in yrs(2021,2025):
    n=int(y[:4])
    if n==2021: add('iX3 (G08, 1세대)',[y],C2,HU100R,ABK,'N5F-ID21A(FCC)','BDC2 / BDC3',S_BDC2+', mechanicwiki.com(X3 F97/G01/G08 키 등록)')
    else: add('iX3 (G08, 1세대)',[y],C3,HU100R,ABK,'IYZBK1(FCC)','BDC3',S_BDC3+', '+S_IYZ)
add('iX3 (NA5, 2세대)',['2026'],'확인 불가',HU100R+'(추정)','','','확인 불가(노이어 클라쎄)','검색 한도로 조사 불가',flag='red')
add('1M 쿠페 (한정판)',['2012'],C46,HU92,'7847229-02(비상키 블레이드, HU92)','66126986583(리모컨키)','CAS3+','ebay(E82/E88 2008-2012 CAS3 모듈 9147226), precisionecu.com(2007-2013 E82/E88 리모컨키)','1M = E82 쿠페 기반')
subprocess.run(['python3','add.py',json.dumps(out,ensure_ascii=False)])

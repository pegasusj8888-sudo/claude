# 벤츠: yearly.md(연식별 검색 기록)를 근거로 행 생성
import json
ORDER=[l.rstrip('\n').split('\t') for l in open('years.txt')]
YR={m:y for m,y in ORDER}
rows=[]
F3='FBS3 (NEC 프로세서 키)'
F4='FBS4 (NEC 신형 키, 딜러 서버 인증)'
IR='FBS3 (NEC, 적외선 IR 키)'
I3='EIS(EZS) — FBS3'
I4='EIS(EZS) — FBS4'
NOYEAR='해당 연식 검색 자료 없음 — 이전 연식 기준 추정'

def span(m):
    a,b=YR[m].split('-'); return int(a),(2026 if b=='현재' else int(b)),b!='현재'
def T(month):  # 전환 연식
    return dict(chip=f'FBS3 (NEC) / FBS4 ({month} 이후 생산)',immo=f'EIS(EZS) — FBS3({month} 이전 생산) / FBS4({month} 이후 생산)')
def add(m,fn):
    a,b,ended=span(m)
    for y in range(max(a,2000),b+1):
        d=dict(model=m,year=str(y)+('(단종)' if ended and y==b else ''),chip='',keyway='HU64',card='',fold='',blade_pn='',smart='',immo='',src='',note='',ktype_hint='스마트키')
        d.update(fn(y))
        if d.get('flag') is None: d.pop('flag',None)
        rows.append(d)
def g3(src,**k):
    d=dict(chip=F3,immo=I3,src=src); d.update(k); return d
def g4(src,**k):
    d=dict(chip=F4,immo=I4,src=src); d.update(k); return d
def o(d,why): d['flag']='orange'; d['note']=why; return d

K12B='IYZDC12B (FBS4 433MHz 3버튼)'
GEN3='신형 디자인 키(Gen3)'
MS5='신형 키(MS5 계열)'

# A클래스 W176
def a176(y):
    if y==2013: return g3('obdii365(FBS3 키리스고), abkeys(FBS3 키) — 2014년 이전 FBS3')
    if y==2014: return o(dict(chip='FBS3 / FBS4 (자료 상충)',immo='EIS(EZS) — FBS3 / FBS4',src='amazon EASYGUARD(2014+ FBS4 W176), dallaslocksmithspro(2014 A180 FBS3 범주)'),'2014년식 FBS3·FBS4 자료 상충 — VIN(SA코드 803/804) 확인')
    return g4({2015:'abkeys(FBS4 433MHz IYZDC12B), wikipedia(W176 FL 2015.9)',2016:'montyslocksmith(2016+ FBS4)',2017:'mercedescarkeys.co.uk(2017 W176 키 프로그래밍)',2018:'ebay.co.uk(FBS4 W176 A180d ECU·키 세트)'}[y],smart=K12B)
add('A클래스 (W176, 3세대 해치백)',a176)
def v177(y):
    s={2020:'uhs-hardware(2013-2020 FBS4), benzworld',2021:'mykeysupply(2014-2021 FBS4 키리스고)',2022:'auto-keys.eu(W177 2019+ 순정 A1779057902 433.92MHz)',2023:'paultan(2023 FL), montyslocksmith(W177 2018-2023 FBS4)',2024:'carsine(V177 티어드롭 키)',2025:'carsine(V177 티어드롭 키)',2026:''}[y]
    d=g4(s,smart='A1779057902 (2버튼 433.92MHz 키리스고) / '+GEN3)
    return o(d,NOYEAR) if y==2026 else d
add('A클래스 세단 (V177, 4세대)',v177)
def a45(y):
    if y==2013: return g3('doornkey(2014년 이전 FBS3)')
    if y==2014: return o(dict(chip='FBS3 / FBS4 (자료 상충)',immo='EIS(EZS) — FBS3 / FBS4',src='diag.net·doornkey(2014 A45 FBS3 가능), amazon EASYGUARD(2014+ FBS4 W176)'),'2014년식 FBS3·FBS4 자료 상충 — VIN 확인')
    if y<=2018: return g4('W176 연식 기준(A클래스 W176 2015-2018 FBS4)',smart=K12B)
    d=g4('auto-keys.eu(A45 AMG FBS4 키 — 미국형 315MHz 품번 제외), carsine',smart='A1779057902 (W177 2버튼 433.92MHz) / '+GEN3)
    return d if y in (2020,2021) else o(d,NOYEAR)
add('A45 AMG (W176/W177)',a45)
def b246(y):
    if y<=2013: return g3({2012:'mbkeygroup(W246 FBS3), locksmithkeyless(IYZDC07 2008-2012)',2013:'xhorsetool(B200 FBS3 키리스고 키 추가)'}[y])
    if y==2014: return o(dict(chip='FBS3 / FBS4 (전환 시점 미확인)',immo='EIS(EZS) — FBS3 / FBS4',src='amazon EASYGUARD(2014+ FBS4 W246), abkeys(W246 EZS FBS4 2469057503)'),'W246 FBS4 전환 시점 자료 없음 — 2014년식은 FBS3·FBS4 혼재 가능')
    return g4('abkeys(순정 W246 EZS FBS4 2469057503, 2015-2021 표기)',smart=K12B)
add('B클래스 (W246)',b246)
def cla(y):
    if y==2013: return g3('benzworld(CLA 2013 FBS3/FBS4 논의), doornkey')
    if y==2014: return dict(**T('2014.11'),src='obdii365(117 모델 FBS4 2014.11~), abkeys(CLA W117 EZS FBS4 2469054702)')
    return g4({2015:'northcoastkeyless(IYZDC12 계열)',2016:'mhhauto(2016 W117 CLA FBS4)',2017:'mbparts.mbusa(CLA KEYLESS-GO)',2018:'mbparts.mbusa',2019:'mbparts.mbusa(2019 CLA250 KEYLESS-GO)'}[y],smart=K12B)
add('CLA (C117, 1세대)',cla)
def c118(y):
    d=g4({2020:'carkeyhelper(C118 스마트키)',2021:'carkeyhelper(C118)',2022:'ebay(2022 CLA250 C118 키), autokeystore(FBS4 433MHz 3버튼 HU64)',2023:'autokeystore, carkeyhelper',2024:'auto-data(C118 FL 2023), carkeyhelper',2025:'carkeyhelper(C118 2019-2025)'}[y],smart=GEN3)
    return d
add('CLA (C118, 2세대)',c118)
def cla45(y):
    if y==2014: return dict(**T('2014.11'),src='obdii365(117 FBS4 2014.11~)')
    if y<=2019: return g4('ebay(2016-2018 CLA45 AMG 키), mercedescla.org(AMG 키)',smart=K12B)
    d=g4('mbpartsgiant·fcpeuro(CLA45 S C118 키)',smart=GEN3)
    return d if y in (2020,2021,2022) else o(d,NOYEAR)
add('CLA45 AMG (C117/C118)',cla45)
def c204(y):
    s={2007:'autoevolution(W204 2007.3 판매 시작), mbworld(W204 EIS)',2008:'mbworld(W204 key programming — 1998-2014 FBS3)',2009:'abkeys·xremotes(FBS3 키리스고 C300 2008-2015)',2010:'mhhauto(W204 keyless go key)',2011:'benzworld(ESL W204), wikipedia(W204 FL 2011)',2012:'cgdi(W204 FBS3), benzworld(ESL)',2013:'ahparts(2013 C250 순정 키), dallaslocksmithspro',2014:'mbworld(2013-2014 W204 FBS3)'}[y]
    return g3(s,immo='EIS(EZS)+ESL(전자식 스티어링 락) — FBS3')
add('C클래스 (W204, 3세대)',c204)
def c205(y):
    if y in (2014,2015): return o(dict(chip='FBS4 / FBS3 (자료 상충)',immo='EIS(EZS) — FBS4 / FBS3',src='obdii365(205 전 연식 FBS4), tlkeys(W205 2015.4부터 FBS4·초기 생산 FBS3 요약), auto-keys.eu(A2059050600 434MHz FBS4)',smart='A2059050600 (2버튼 434MHz 키리스고)'),'W205 초기 생산분 FBS3 여부 자료 상충 — VIN 확인')
    sm='A2059053609 (3버튼 433.92MHz 키리스고) / A2059050000 (2버튼 433MHz)'+(' / '+GEN3 if y>=2019 else '')
    return g4({2016:'car-key.nl·auto-keys.eu(A2059053609, A2059050000)',2017:'car-key.nl(A2059053609), amazon EASYGUARD(W205 턴키 사양)',2018:'car-key.nl, servicereset(W205 슬롯키·키리스고 사양)',2019:'mbworld(W205 FL 신형 키), amazon(2019-2022 C 신형 키)',2020:'mbworld(new style key W205)',2021:'ebay(2021 W205 A2059053609)'}[y],smart=sm)
add('C클래스 (W205/C205, 4세대)',c205)
def c206(y):
    return g4({2022:'justanswer(W206 슬림 신형 키 FBS4), ebay(MS5I 2022-2026 미국형 — 제외)',2023:'ebay/ijdmtoy(W206·W223 Oval 키), mbusa(W206 디지털 차키)',2024:'mbusa(W206 2024 디지털 차키)',2025:'carinterior.alibaba(2026 키 호환 — VIN 확인), mbworld',2026:'carinterior.alibaba(2026 키 호환)'}[y],smart=MS5)
add('C클래스 (W206, 5세대)',c206)
def c205c(y):
    return g4({2016:'wikipedia(C205/A205 2016-2023), car-key.nl(A2059053609)',2017:'car-key.nl',2018:'car-key.nl',2019:'amazon(2019-2022 C 신형 키)',2020:'amazon',2021:'amazon',2022:'amazon',2023:'mbworld(2023 C300 신형 키)'}[y],smart='A2059053609 (3버튼 433.92MHz)'+(' / '+GEN3 if y>=2019 else ''))
add('C클래스 쿠페 (C205)',c205c)
add('C클래스 카브리올레 (A205)',c205c)
def c63_205(y):
    return g4('ebay(15-18 C63 AMG 키), tlkeys(C63 2014-2020·C43 2016-2020 FBS4)' if y<=2018 else 'mbworld(2019 신형 키를 구형 C63에 등록 논의), mbworld(C43 key cover)',smart='A2059053609 (3버튼 433.92MHz)'+(' / '+GEN3 if y>=2019 else ''))
add('C43/C63 AMG (W205)',c63_205)
def c63_206(y):
    d=g4('fcpeuro·batteriesplus(C63 W206 키) — W206 공통',smart=MS5)
    return d if y<=2025 else o(d,NOYEAR)
add('C63 AMG (W206)',c63_206)
def cle(y):
    return g4({2024:'wikipedia(CLE 2023.10 생산), mbworld(CLE digital key)',2025:'mbusa(CLE 2025-10 디지털 차키)',2026:'mbusa(CLE 2026-06 디지털 차키)'}[y],smart=MS5)
add('CLE (C236)',cle)
def e211(y):
    if y<=2005: return dict(chip=IR,immo='EIS(EZS) — FBS3(적외선 인증)',src={2002:'wikipedia(W211 2002, 2003년형), benzworld(IR coded key)',2003:'pelicanparts(W211 E320 2003-2005 리모컨), mbworld(2003 E320 fob)',2004:'pelicanparts, mbworld(2003 E500 keyless go)',2005:'pelicanparts(W211 E320 2003-2005)'}[y],smart='검정 IR 키(전기형), 키리스고·비키리스고 2종')
    return dict(chip=IR,immo='EIS(EZS)+ESL — FBS3',src='benzworld(newer W211 크롬 테두리 키), ebay(2006-2007 W211 E350 ECU·EIS·키·ESL)',smart='크롬 테두리 키(2006 페이스리프트~)')
add('E클래스 (W211, 8세대)',e211)
def e212(y):
    if y<=2012: return g3({2009:'wikipedia(W212 2009)',2010:'justanswer·capitol locksmith(W212 E350 FBS3), abkeys(EZS·ESL W212)',2011:'ebay/keyecu(FBS3 BGA 키리스고 W212)',2012:'mbworld(W212 keyless go fob)'}[y],immo='EIS(EZS)+ESL — FBS3')
    if y==2013: return dict(**T('2013.4'),src='obdii365(W212 FBS4 2013.4~), autoevolution(W212 FL 2013)')
    return g4('tlkeys(FBS4 433MHz 3버튼 W212·W213 2014-2020), ebay(2014-2019 E350 순정 키)',smart=K12B)
add('E클래스 (W212, 9세대)',e212)
def e213(y):
    sm=K12B+' / '+GEN3 if y<=2023 else GEN3
    return g4({2016:'wikipedia(W213 2016.2 생산), ebay(2017 W213 신형 키)',2017:'ebay(2017 W213 IYZMS1 신형 키 — 미국형 FCC)',2018:'auto-key.no(IYZDC12K 433MHz 보드), autokeystore',2019:'auto-key.no, autokeystore',2020:'auto-key.no',2021:'facebook(2021 W213 FBS4 ECU 개인화)',2022:'ebay(W213 FBS4)',2023:'ebay(W213 2016-2021 FBS4), amazon EASYGUARD(W213)',2024:'W213 연식 기준'}[y],smart=sm)
e213_=lambda y: o(e213(y),NOYEAR) if y==2024 else e213(y)
add('E클래스 (W213, 10세대)',e213_)
def e214(y):
    return g4({2024:'mbworld(W214 신형 키 비상키 분리 버튼), mbusa(W214 2024 디지털 차키)',2025:'carinterior.alibaba(2026 키 호환 — VIN 확인)',2026:'carinterior.alibaba(2026 키 호환)'}[y],smart=MS5+' — 비상키 분리 버튼형')
add('E클래스 (W214, 11세대)',e214)
def c207(y):
    if y<=2012: return g3('mbworld(C207 E350 keyless entry — 키리스고 옵션 899), ebay(FBS3 BGA W207)',immo='EIS(EZS)+ESL — FBS3')
    if y==2013: return dict(**T('2013.7'),src='obdii365(207 FBS4 2013.7~), autoevolution(C207 FL 2013)')
    return g4('uhs-hardware(FBS4 207 모델 2013-2020), mbworld(C207 last stock key fobs)',smart=K12B)
add('E클래스 쿠페 (C207)',c207)
add('E클래스 카브리올레 (A207)',c207)
def c238(y):
    return g4('carkeyssolutions(E 2017-2020 3버튼 키), rac.co.uk(A238 키로 소프트톱 작동)' if y<=2019 else 'ebay(2019-2023 E450 C238 키리스 모듈), encycarpedia(C238 FL)',smart=K12B+' / '+GEN3)
add('E클래스 쿠페 (C238)',c238)
add('E클래스 카브리올레 (A238)',c238)
def e63(y):
    return g4('ebay(2016-2018 E63 AMG 키), ebay(IYZMS1 2017 신형 키)' if y<=2019 else 'amazon Lcyam(2019-2021 W213 E63S), mbpartsgiant(E53 키)',smart=K12B+' / '+GEN3)
add('E53/E63 AMG (W213)',e63)
def e53_214(y):
    d=g4('mbworld(2025 E53 키-프로필 연동), autoevolution(E53 W214)',smart=MS5)
    return d if y<=2025 else o(d,NOYEAR)
add('E53 AMG (W214)',e53_214)
def c219(y):
    if y<=2007: return dict(chip=IR,immo='EIS(EZS) — FBS3(적외선 인증)',src='mbworld(2006 CLS500 smart key), fixautosmart(CLS 2007-2014 EIS)')
    return g3('uhs-hardware(2009-2014 FBS3), abkeys(FBS3)')
add('CLS (C219, 1세대)',c219)
def c218(y):
    if y<=2013: return g3('wikipedia(C218 2011-2017), prokeyfob(2013 CLS550 키)')
    if y==2014: return dict(**T('2014.9'),src='obdii365(218 FBS4 2014.9~), autoevolution(C218 FL 2014.9)')
    return g4('mbworld(C218 keyless go package), uhs-hardware(FBS4 CLS 2014-2020)',smart=K12B)
add('CLS (C218, 2세대)',c218)
def c257(y):
    return g4('wikipedia(C257 2018), amazon iJDMTOY(Gen3 CLS 2020~), mbusa(2019 CLS450 keyless)' if y<=2019 else 'mbpartsgiant(2023 CLS450 키), autoloc(2019-2023 CLS)',smart=K12B+' / '+GEN3)
add('CLS (C257, 3세대)',c257)
def cls63(y):
    if y==2014: return dict(**T('2014.9'),src='obdii365(218 FBS4 2014.9~), partslinkent(2014-2017 CLS63S 키 스위치)')
    if y<=2017: return g4('partslinkent(2014-2017 CLS63S), pelicanparts(C218 keys)',smart=K12B)
    return g4('amazon iJDMTOY(Gen3 CLS 2020~), mbpartsgiant(CLS53)',smart=K12B+' / '+GEN3)
add('CLS53/63 AMG',cls63)
def s221(y):
    if y==2005: return o(dict(chip=F3+' 추정',immo='EIS(EZS) — FBS3 추정',src='wikipedia·autoevolution(W221 2005.8 생산, 2006년형으로 판매)'),'W221 2005.8 생산 — 2005년식 국내 판매분은 W220일 가능성, 초기형 키 방식 자료 없음')
    return g3('ebay(07-12 W221 EIS A2215450308), benzworld(2008 S550 keyless go)' if y<=2008 else 'keyecu(FBS3 BGA 키리스고 W221 2009~), uhs-hardware(2010-2013 S W221)',immo='EIS(EZS) A2215450308 — FBS3' if 2007<=y<=2012 else I3)
add('S클래스 (W221, 5세대)',s221)
def s222(y):
    sm='A2229059610 (FBS4 433/434MHz, Hella)' if y<=2017 else 'A2229059610 (FBS4 433/434MHz) / 신형 디자인 키(2018 페이스리프트~)'
    return g4('autokeystore(W222 FBS4 A2229059610 433MHz), amazon EASYGUARD(W222 턴키 사양)' if y<=2017 else 'mbworld(2014 키→2018 신형 키 업그레이드), amazon iJDMTOY(S 2018~)',smart=sm)
add('S클래스 (W222, 6세대)',s222)
def s223(y):
    d=g4({2021:'wapcar(W223 신형 키), ebay(IYZMS5 미국형 — 제외)',2022:'wapcar, justanswer(2021 S580 키)',2023:'mbworld(W223 digital key card), ebay(IYZMS5I 2022-2026)',2024:'mbworld(2024 S63e 디지털 키 미지원)',2025:'mbworld(2025 S580 NTG7 디지털 키 지원)',2026:''}[y],smart=MS5+' (모션센서 슬립)')
    return o(d,NOYEAR) if y==2026 else d
add('S클래스 (W223, 7세대)',s223)
def c217(y):
    return g4('obdii365(217 전 연식 FBS4), wikipedia(C217 2014-2020)' if y<=2017 else 'encycarpedia(S560 쿠페 2018), mbpartsgiant(2018 S560 키)',smart='A2229059610 (FBS4 433/434MHz)'+(' / 신형 디자인 키(2018~)' if y>=2018 else ''))
add('S클래스 쿠페 (C217)',c217)
add('S클래스 카브리올레 (A217)',c217)
def x222(y):
    return g4('egmcartech·ebay(2016-2018 마이바흐 S560/S600 순정 키)' if y<=2017 else 'ebay(2019 마이바흐 W222 순정 키)',smart='A2229059610 (FBS4 433/434MHz)'+(' / 신형 디자인 키(2018~)' if y>=2018 else ''))
add('메르세데스-마이바흐 S클래스 (X222)',x222)
add('메르세데스-마이바흐 S클래스 (Z223)',lambda y: g4('encycarpedia(Z223 2021-2026), carinterior.alibaba(마이바흐 키 — 세대·생산연도별 상이)',smart=MS5))
def s63_222(y):
    return g4('mbworld(2015 AMG S63 키, 2015/2017 S65 동일 키), mbpartsgiant(2015 S63 키)' if y<=2017 else 'amazon iJDMTOY(S 2018~ 신형 키)',smart='A2229059610 (FBS4 433/434MHz)'+(' / 신형 디자인 키(2018~)' if y>=2018 else ''))
add('S63/S65 AMG (W222)',s63_222)
def s63_223(y):
    d=g4('mbworld(2024 S63e 디지털 키 — 2025 NTG7부터 지원)',smart=MS5)
    return o(d,NOYEAR) if y in (2022,2026) else d
add('S63 AMG (W223)',s63_223)
def gla(y):
    if y==2014: return dict(**T('2014.11'),src='obdii365(156 FBS4 2014.11~), the-ecu-pro(2014 GLA250 EIS FBS4), digital-kaos(GLA X156 FBS3 or FBS4)')
    return g4('glaowners(2019 GLA proximity key), autoevolution(GLA FL 2017)' if y>=2017 else 'northcoastkeyless(2014-2016 GLA 키), montyslocksmith(2016 GLA FBS4)',smart=K12B)
add('GLA (X156, 1세대)',gla)
def h247(y):
    d=g4('justanswer(2021 GLA250 key fob), mbworld(H247 key replacement)' if y<=2022 else 'auto-data(H247 FL 2023), mbworld',smart=GEN3)
    return o(d,NOYEAR) if y==2026 else d
add('GLA (H247, 2세대)',h247)
def gla45(y):
    if y==2014: return dict(**T('2014.11'),src='obdii365(156 FBS4 2014.11~)')
    if y<=2019: return g4('prokeyfob(2017 GLA45 키), glaowners(AMG key fob)',smart=K12B)
    d=g4('amazon(KKNCO 2021-2024 GLA45·GLA35 키 배터리 적용표), mbworld(GLA45/35)',smart=GEN3)
    return d if y<=2023 else o(d,NOYEAR)
add('GLA35/45 AMG',gla45)
def glb(y):
    d=g4('ebay(2020-2025 GLB250 순정 키), mbworld(GLB remote start fob)' if y<=2022 else 'autoevolution(2024 GLB35 FL), mbusa(2023 GLB250 keyless)',smart=GEN3)
    return o(d,NOYEAR) if y==2026 else d
add('GLB (X247, 1세대)',glb)
def glb35(y):
    d=g4('ebay(2020-2025 GLB 순정 키), autoevolution(2024 GLB35 FL)',smart=GEN3)
    return o(d,NOYEAR) if y==2026 else d
add('GLB35 AMG',glb35)
def glk(y):
    if y<=2014: return g3({2009:'ebay(2009-2012 GLK350 키)',2010:'keylessremotewarehouse(2010 GLK350)',2011:'ebay(2009-2012 GLK350 키)',2012:'top-rider(신형 GLK 2012.8 국내 출시), mbworld(GLK keyless go 옵션)',2013:'mbworld(2013 GLK350 키리스고 미장착 사례)',2014:'doornkey·diag.net(2014 GLK350 FBS3)'}[y])
    return o(dict(chip='FBS3 / FBS4 (전환 시점 미확인)',immo='EIS(EZS) — FBS3 / FBS4',src='the-ecu-pro(2015 GLK350 EIS FBS4), northcoastkeyless(2009-2015 GLK IYZDC 키)'),'2015년식 FBS3·FBS4 혼재 — X204는 FBS4 적용 목록에 없음, 전환 월 미확인')
add('GLK (X204)',glk)
def glc(y):
    return g4('benzworld(2016 GLC300 키), mbworld(order new key fob)' if y<=2019 else 'drive-sense(X253 FL 2020-2022), amazon iJDMTOY(Gen3 GLC 2020~)',smart=K12B+(' / '+GEN3 if y>=2020 else ''))
add('GLC (X253/C253, 1세대)',glc)
add('GLC (X254/C254, 2세대)',lambda y: g4({2023:'mbusa(GLC 2023-03 X254 SmartKey)',2024:'mbworld(X254 디지털 키 미지원)',2025:'mbworld(2025 GLC 디지털 키 사전 장착), mbusa(GLC 2025-10 디지털 차키)',2026:'mbusa(GLC 2026-06 디지털 차키)'}[y],smart=MS5))
add('GLC43/63 AMG (X253)',lambda y: g4('ebay(X253 GLC43/63 순정 키), mbworld(GLC43 key fob)',smart=K12B+(' / '+GEN3 if y>=2020 else '')))
def glc63_254(y):
    d=g4('mbusa(2025 AMG GLC63 S E), mbworld(X254 디지털 키)',smart=MS5)
    return o(d,NOYEAR) if y==2026 else d
add('GLC63 AMG (X254)',glc63_254)
def m164(y):
    if y==2005: return o(dict(chip=F3+' 추정',immo='EIS(EZS) — FBS3 추정',src='wikipedia(W164 2005 생산 시작)'),'2005년식 W164 키 자료 없음 — 2006년식 기준 추정')
    return g3('benztechmodules(W164 EIS 164 545 05 08 2006-2012), capitol locksmith' if y<=2008 else 'uhs-hardware(2010-2012 ML W164 키리스고), blog.51.ca(FBS3 BGA W164)',immo='EIS(EZS) 164 545 05 08 — FBS3')
add('M클래스 (W164, 2세대)',m164)
def w166(y):
    if y==2012: return g3('benzworld(W166 dead fob), locksmithkeyless(2012 ML350 FBS3)')
    if y==2013: return dict(**T('2013.7'),src='obdii365(166 FBS4 2013.7~), justanswer(FBS4 EIS ML166 2013 — 코드 803)')
    return g4('benzworld(2015 ML250 FBS4), amazon EASYGUARD(W166 2014+ FBS4)',smart=K12B)
add('M클래스 (W166, 3세대)',w166)
add('GLE (W166/C292, 3세대)',lambda y: g4('ebay(GLE 쿠페 키), benzworld(GLE key fob)',smart=K12B))
def w167(y):
    return g4({2019:'carsine(티어드롭 키 W167 2019), dashboardsymbols(GLE 키 슬롯)',2020:'pelicanparts(W167 keys)',2021:'mercedesgleforum(키-프로필 연동)',2022:'ebay(2022 GLE 순정 키 — 미국형 NBGDM4 제외)',2023:'partslinkent(2021-25 GLE53 키)',2024:'mbusa(GLE 2024-03 SmartKey)',2025:'partslinkent(2021-25 GLE 키)',2026:'mbusa(GLE 2026-07 디지털 차키)'}[y],smart='티어드롭 신형 키(W167~)')
add('GLE (W167/V167/C167, 4세대)',w167)
def gle_amg(y):
    if y<=2019: return g4('ebay(2017 GLE 쿠페 AMG43 키), prokeyfob(2018 GLE63 S 키)',smart=K12B)
    return g4('partslinkent(2021-25 GLE53 AMG 순정 키), mbworld(2024 GLE53 key)',smart='티어드롭 신형 키(W167~)')
gle_amg_=lambda y: o(gle_amg(y),NOYEAR) if y==2026 else gle_amg(y)
add('GLE43/53/63 AMG',gle_amg_)
def gl(y):
    if y<=2012: return g3('abkeys(FBS3 W164 키리스고), mbworld(GL X164 key)')
    if y==2013: return dict(**T('2013.7'),src='wikipedia(X166 2012.6~), obdii365(166 FBS4 2013.7~)')
    return g4('ebay(2014-2016 GL450 X166 ECM·BCM·키 세트), blackgoldparts(2015 GL63 키)',smart=K12B)
add('GL클래스 (X164/X166)',gl)
add('GLS (X166, 1세대)',lambda y: g4('wikipedia(2016 GL→GLS), northcoastkeyless(2017-2018 GLS 키)',smart=K12B))
add('GLS (X167, 2세대)',lambda y: g4('ebay(2020-2026 GLS450 X167 순정 키), auto-data(X167 FL 2023)' if y<=2023 else 'mbusa(GLS 2026-07 디지털 차키), ebay(2020-2026 GLS450 키)',smart='티어드롭 신형 키'))
add('메르세데스-마이바흐 GLS (X167)',lambda y: g4('carinterior.alibaba(마이바흐 키), facebook(Maybach GLS600 auto key)',smart='티어드롭 신형 키'))
GSRC='clubgwagen·benzworld(G500 키에 이모빌라이저 칩 없음·IR 수신 의견), auto-key.no(Mercedes IR 리모컨 키)'
def g_old(y):
    if y<=2001: return o(dict(chip='확인 불가 (IR 리모컨 키, 칩 유무 상충)',immo='EIS(EZS) / DAS 추정 — 자료 상충',ktype_hint='막대키',src=GSRC),'W463 초기형 키 자료 상충(칩 없는 IR 키 의견 vs DAS3/FBS3) — 실물 확인 필요')
    if y<=2005: return o(dict(ktype_hint='막대키,스마트키',chip=IR+' / 트랜스폰더 키 병존',immo='EIS(EZS) — FBS3',src='keylessentryremotefob(2002-2005 G500 트랜스폰더 키), auto-key.no(G 2002-2009 IR 키), fixautosmart(G500 2002-2014 EIS)',smart='검정 IR 키'),'IR 스마트키와 트랜스폰더 막대키 자료 병존 — 차량별 확인')
    if y==2006: return g3('benzworld(G클래스 크롬 키는 2007년형부터 — 2006은 블랙 키)',chip=IR,smart='검정 IR 키')
    if y<=2012: return g3('benzworld(chrome key 2007~), fixautosmart(G500 2002-2014 EIS)',smart='크롬 키(2007년형~)')
    if y<=2015: return g3('go-parts(2012-2018 G EIS), capitol locksmith(2014년까지 FBS3)',smart='크롬 키')
    if y==2016: return o(dict(chip='FBS3 / FBS4 (자료 상충)',immo='EIS(EZS) — FBS3 / FBS4',src='mhhauto(2016 W463 FBS4 사례 / 2016 G바겐 FBS3 의견)'),'2016년식 FBS3·FBS4 자료 상충 — VIN 확인')
    return g4('montyslocksmith(2016+ FBS4), mhhauto(W463 FBS4)',smart=K12B)
add('G클래스 (W463, 구형 바디)',g_old)
def g_new(y):
    if y<=2024: return g4('carbuzz(W463A 2019년형), mbworld(G 키리스고는 시동만), amazon iJDMTOY(Gen3 G 2019~)' if y<=2021 else 'autoevolution(W463 2024.3 생산 종료), mbworld(2019-24 키리스 엔트리 레트로핏)',smart=GEN3)
    return o(g4('autoevolution(2024.3 이후 페이스리프트)',smart=''),'2025년~ 페이스리프트(W465) 키 자료 없음 — 이전 연식 기준 추정')
add('G클래스 (W463, 신형 바디)',g_new)
def g63(y):
    if y<=2015: return g3('go-parts(2012-2018 G63 EIS), capitol locksmith',smart='크롬 키')
    if y==2016: return o(dict(chip='FBS3 / FBS4 (자료 상충)',immo='EIS(EZS) — FBS3 / FBS4',src='mhhauto(2016 W463 FBS4 사례 / FBS3 의견)'),'2016년식 FBS3·FBS4 자료 상충 — VIN 확인')
    if y<=2024: return g4('mhhauto(W463 FBS4), ebay(G63 AMG Gen3 키 IYZ-MS2 미국형 — 제외)',smart=GEN3 if y>=2019 else K12B)
    return o(g4('autoevolution(2024.3 이후 페이스리프트)'),'2025년~ 페이스리프트(W465) 키 자료 없음 — 이전 연식 기준 추정')
add('G63 AMG',g63)
def slk(y):
    if y<=2014: return g3('justanswer(2012 SLK R172 키리스고), wikipedia(R172 2011)')
    if y==2015: return dict(**T('2015.4'),src='obdii365(172 FBS4 2015.4~), wikipedia(SLC 차명 변경)')
    return g4('carkeyhelper(SLC 2016-2020 스마트키), mechanicwiki(SLC R172 키 추가)',smart=K12B)
add('SLK/SLC (R172)',slk)
add('SL (R231)',lambda y: g4('mbworld(R231 키), justanswer(2014 SL550), obdii365(231 전 연식 FBS4)' if y<=2016 else 'mbworld(R231 duplicate key fob)',smart=K12B))
def sl232(y):
    d=g4('amazon(2022-2025 S·E·C·GLC·SL 3버튼 키), mbusa(SL R232 2025 이모빌라이저)',smart=MS5)
    return o(d,NOYEAR) if y==2026 else d
add('SL (R232)',sl232)
def gt(y):
    if y<=2018: return g4('wikipedia(AMG GT 2014.10 생산), dfwkeys4cars(FBS3→FBS4 MY2014-2015)',smart=K12B)
    if y<=2023: return g4('mbworld(2019 신형 키), cabriosupply(R190 키로 소프트톱)',smart=K12B+' / '+GEN3)
    return o(g4('pelicanparts(C192 2024-2025)'),'2024년~ 2세대(C192) 키 자료 없음 — 이전 세대 기준 추정')
add('AMG GT (C190/R190)',gt)
add('EQC',lambda y: g4('wikipedia(EQC 2019-2023), autodoc(EQC N293 key)',smart=GEN3))
def eqa(y):
    d=g4('ebay.de(EQB X243 순정 A1779054606 2021-2025), mbworld(EQ 디지털 키 미지원)',smart='A1779054606 (EQA·EQB 2021-2025, 유럽형)')
    return o(d,NOYEAR) if y==2026 else d
add('EQA (H243)',eqa)
add('EQB (X243)',eqa)
def eqs(y):
    return g4({2021:'wikipedia(EQS 2021.5 생산)',2022:'ebay(2022-2023 EQS 키 IYZ-MS5 미국형 — 제외)',2023:'mbworld(EQS 디지털 키 CY23/2부터)',2024:'ecstuning(2024 EQS 키), mbusa(EQS 2024)',2025:'ebay(20-25 EQS 키)',2026:'carinterior.alibaba(2026 MRA II 키 CR2032)'}[y],smart=MS5)
add('EQS 세단 (V297)',eqs)
def eqe(y):
    d=g4({2022:'wikipedia(EQE)',2023:'mbworld(EQE digital key)',2024:'mbusa(EQE 2024-09 디지털 차키)',2025:'mbusa(EQE 디지털 차키)',2026:''}[y],smart=MS5)
    return o(d,NOYEAR) if y==2026 else d
add('EQE 세단 (V295)',eqe)
add('EQS SUV (X296)',lambda y: g4('mbusa(EQS SUV 2023-01·2024-02 디지털 차키), amazon(2023-2026 EQS SUV 3버튼 키)',smart=MS5))
add('EQE SUV (X294)',lambda y: g4('mbusa(EQE SUV 2024-03 디지털 차키), amazon(2023-2026 EQE SUV 3버튼 키)',smart=MS5))

open('rows.jsonl','w').write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
from collections import Counter
print(len(rows),Counter(r.get('flag') for r in rows))
assert {r['model'] for r in rows}==set(YR)
for r in rows: assert r['src'] or r.get('flag'), r

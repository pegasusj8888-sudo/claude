# 5차(2026.9) — 애프터마켓 번호를 지워 순정 부품번호가 빈 BMW 행에 순정 번호 채우기
#   한국 사양(KO) 번호의 적용 차종은 확인 못 해, 적용 차대가 확인된 해외(ECE+RoW) 순정 번호를 [해외 공용 품번]으로 기재
#   근거: hubauer-shop.de·schmiedmann.com·recambiosyaccesoriosbmw.com·BMW 딜러 부품몰(차대 목록), 868MHz(유럽)·US 전용 번호는 제외
# 사용: python3 research/recheck5.py
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'recheck'))
import apply as recheck
SK = '스마트키(부품번호)'; BL = '키블레이드(부품번호)'
NEW = []
def B(model, years, col, val, guide=None):
    NEW.append(dict(brand='BMW', model=model, years=years, append={col: val}, **({'guide': guide} if guide else {})))

MS = '[M 스포츠, 해외 공용 품번]'
B('1시리즈 (F40, 3세대)', [2023], BL, '51215A4FBE5[비상키, 해외 공용 품번]',
  guide='BMW 순정 부품번호(애프터마켓 대체): 비상키 51215A4FBE5 = F40·F44·G20·G22·G26·G42·G80·G82 등 인서트 키(recambiosyaccesoriosbmw), '
        '51215A65D30 = U06·U10·U11·G60·G70·I20 등 인서트 키, 리모컨 66125A473F4(M 스포츠, ECE+RoW+US) = F40·F44·F9x·G01·G42·G87·G80·G82(hubauer·딜러몰), '
        '66125A47402(기본, ECE+RoW) = G01·G02·G08·G11·G12·G30(schmiedmann), 66125A56076(기본, ECE+RoW) = F15·F16·F39·F45·F46·F48(hubauer), '
        '66128708328(기본, ECE+RoW+US) = F40·G29(hubauer), 66125B3E8E1(M, ECE+RoW) = G60·G70·I20·U06·U10·U11 등, 66129362173 = i3 I01 434MHz(66126805980 대체), '
        '51217127047 = X3 E83 도어·점화 키 — 한국 사양(KO) 번호 적용 차종은 미확인이라 [해외 공용 품번]')
B('2시리즈 쿠페 (G42, 2세대)', [2025, 2026], SK, '66125A473F4' + MS)
B('M2 (G87)', [2024], BL, '51215A4FBE5[비상키, 추정]')
B('M2 (G87)', [2025, 2026], SK, '66125A473F4' + MS)
B('M4 (G82)', [2025, 2026], SK, '66125A473F4' + MS)
B('X3 (E83, 1세대)', [2005, 2006], BL, '51217127047[해외 공용 품번]')
B('5시리즈 (G60/G61, 8세대)', [2026], SK, '66125B3E8E1' + MS)
B('8시리즈 (G15/G16, 2세대)', [2025], SK, '66125A473F4[M 스포츠, 추정]')
B('M8 (G15/G16)', [2025], SK, '66125A473F4' + MS)
B('X4 (G02, 2세대)', [2023], SK, '66125A47402[해외 공용 품번]')
B('X5 (F15, 3세대)', [2017, 2018], SK, '66125A56076[해외 공용 품번]')
B('Z4 (G29, 3세대)', [2026], SK, '66128708328[해외 공용 품번]')
B('i3 (I01)', [2016, 2017], SK, '66129362173[해외 공용 품번]')
B('iX (I20)', [2023], BL, '51215A65D30[비상키, 해외 공용 품번]')
B('iX (I20)', [2026], SK, '66125B3E8E1' + MS)

# ── 아우디 (부품번호 공란 행) ──
def A(model, years, col, val, guide=None):
    NEW.append(dict(brand='아우디', model=model, years=years, append={col: val}, **({'guide': guide} if guide else {})))
FD = '폴딩키(부품번호)'
MLBEVO = '4N0959754[해외 공용 품번]'
A('A6 (C8, 8세대)', list(range(2019, 2025)), SK, MLBEVO,
  guide='아우디 순정 부품번호(공란 행 보완): 4N0959754 = A6 C8·A7 C8·A8 D5·Q8 433MHz 스마트키(remkeys·autokeystore), 4N0959754AM·BF = Q7 4M·SQ7·Q8(Audi USA), '
        '4N0959754AQ·BQ = e-tron·Q8 e-tron(Audi USA·auto-keys.eu 433MHz), 4M0959754CG = 2017~2024 A4·A5·S4·S5·Q5·SQ5·Q7 433MHz, '
        '4H0959754EB·FK = R8 4S, 81A837220AG = Q3 F3 계열 폴딩키 — 한국 사양 번호 미확인이라 [해외 공용 품번]')
for m, ys in [('S6', range(2020, 2027)), ('A7 (C8, 2세대)', range(2020, 2027)), ('S7', range(2020, 2027)),
              ('A8 (D5, 5세대)', range(2019, 2027)), ('S8', range(2023, 2027))]:
    A(m, list(ys), SK, MLBEVO)
A('Q7 (4M, 2세대)', list(range(2022, 2027)), SK, '4N0959754AM[해외 공용 품번], 4N0959754BF[해외 공용 품번]')
A('SQ7', [2024, 2025, 2026], SK, '4N0959754AM[해외 공용 품번], 4N0959754BF[해외 공용 품번]')
A('SQ8', list(range(2020, 2027)), SK, '4N0959754AM[해외 공용 품번]')
A('e-트론/Q8 e-트론', list(range(2020, 2027)), SK, '4N0959754AQ[해외 공용 품번], 4N0959754BQ[해외 공용 품번]')
A('SQ8 e-트론', [2024, 2025, 2026], SK, '4N0959754AQ[해외 공용 품번], 4N0959754BQ[해외 공용 품번]')
B9 = '4M0959754CG[해외 공용 품번]'
for m, ys in [('A4 (B9, 9세대)', [2022, 2023]), ('S4', [2022, 2023, 2024]), ('RS4 아반트', [2022, 2023, 2024]),
              ('A5 (B9, 2세대)', [2022, 2023]), ('S5', [2022, 2023, 2024]), ('RS5', [2022, 2023, 2024]),
              ('Q5 (FY, 2세대)', [2022, 2023, 2024]), ('SQ5', [2022, 2023, 2024])]:
    A(m, ys, SK, B9)
A('A4 (B6/B7, 6·7세대)', [2002, 2003], FD, '8E0837220Q, 8E0837220K')
A('R8 (4S, 2세대)', list(range(2017, 2025)), SK, '4H0959754EB[해외 공용 품번], 4H0959754FK[해외 공용 품번]')
A('RS Q3', list(range(2020, 2027)), FD, '81A837220AG[해외 공용 품번]')

# ── 현대 ──
NEW.append(dict(brand='제네시스', model='제네시스 일렉트리파이드 G80 (RG3 EV)', years=[2024, 2025, 2026],
                append={SK: '95440-T1AA0[추정]'},
                guide='제네시스 G80 부분변경(24MY) FOB 스마트키 95440-T1AA0(제네시스 부티크) — 일렉트리파이드 G80 부분변경 적용은 미확인이라 [추정]'))

# ── 벤츠 (부품번호 공란 행) — auto-keys.eu 순정(중고·신품 OEM) 키 433/434MHz 표기 번호
def M(model, years, val, guide=None):
    NEW.append(dict(brand='벤츠', model=model, years=years, append={SK: val}, **({'guide': guide} if guide else {})))
OS = '[해외 공용 품번]'
M('C클래스 (W204, 3세대)', list(range(2007, 2015)), 'A2049051704[2버튼, 해외 공용 품번], A2049055702[3버튼, 해외 공용 품번]',
  guide='벤츠 순정 부품번호(공란 행 보완, auto-keys.eu OEM 키 433/434MHz): W204 A2049051704(2버튼, FBS3)·A2049055702(3버튼), '
        'W213 A2139059209·A2139056509(AMG), W206 A2239058707, W223 A2239057507·A2239054408(AMG), W167 A1679054203 — 315MHz 번호(A1679054503 등) 제외, 한국 사양 번호 미확인이라 [해외 공용 품번]')
M('E클래스 (W213, 10세대)', list(range(2016, 2025)), 'A2139059209' + OS)
M('E53/E63 AMG (W213)', list(range(2017, 2024)), 'A2139056509[AMG, 해외 공용 품번]')
M('C클래스 (W206, 5세대)', list(range(2022, 2027)), 'A2239058707' + OS)
M('C63 AMG (W206)', [2024, 2025, 2026], 'A2239058707' + OS)
M('S클래스 (W223, 7세대)', list(range(2021, 2027)), 'A2239057507' + OS)
M('S63 AMG (W223)', list(range(2022, 2027)), 'A2239054408[AMG, 해외 공용 품번]')
M('GLE (W167/V167/C167, 4세대)', list(range(2019, 2027)), 'A1679054203' + OS)
M('GLE43/53/63 AMG', list(range(2020, 2027)), 'A1679054203' + OS)

# ── 기아·현대: 같은 세대 순정 번호의 적용 기간이 그 연식을 포함하는 경우 옮겨 적음 ──
BLD = '키블레이드(부품번호)'; FDK = '폴딩키(부품번호)'
def K(model, years, col, val, brand='기아', guide=None):
    NEW.append(dict(brand=brand, model=model, years=years, append={col: val}, **({'guide': guide} if guide else {})))
K('프라이드 JB', [2005], BLD, '81996-1G100[이모빌라이저키, 2005.2.15~2009.12.10], 81996-1G000[칩 없음]',
  guide='기아·현대 공란 행 보완: 같은 세대 순정 키 번호의 적용 기간이 그 연식을 포함하는 경우 옮겨 적음 — 프라이드 JB 2005(1G100 2005.2.15~)·2011(1G000), '
        '프라이드 UB 2011·2012 폴딩키 95430-1W002(auto-keys.eu 한국 시장 OEM, Rio 2012), 쏘울 AM 2008(2008.9 출시, 2009년식과 같은 키), 모닝 SA 2004(2004.2 출시), '
        '스포티지 NB 2000·2001(0K2AC-76201A), JE 2004(2F010 2004.6~)·2010, 쏘렌토 BL 2009, 카렌스 UN 2013(1D104·2L001)')
K('프라이드 JB', [2011], BLD, '81996-1G000[칩 없음]')
K('프라이드 UB', [2011, 2012], FDK, '95430-1W002')
K('쏘울 (Soul, AM)', [2008], SK, '95440-2K200')
K('쏘울 (Soul, AM)', [2008], FDK, '95430-2K211')
K('모닝 (Morning, SA)', [2004], BLD, '81996-07020, 81996-07100')
K('스포티지 (Sportage, NB-Ⅶ)', [2000, 2001], BLD, '0K2AC-76201A[ID48 키]')
K('스포티지 (Sportage, JE/KM)', [2004, 2010], BLD, '81996-2F010[2004.6~]')
K('쏘렌토 (Sorento, BL)', [2009], BLD, '81996-3EG00, 81996-3EC00[뉴 쏘렌토]')
K('카렌스 (Carens, UN)', [2013], BLD, '819962L001')
K('카렌스 (Carens, UN)', [2013], FDK, '954301D104')

# ── KGM(쌍용): catcar.info 쌍용 EPC(KEY SET 그룹, 좌핸들·이모빌라이저 사양) 순정 키 번호 ──
def G(model, years, col, val, guide=None):
    NEW.append(dict(brand='KG모빌리티(쌍용)', model=model, years=years, append={col: val}, **({'guide': guide} if guide else {})))
G('체어맨 (1세대, H)', list(range(2000, 2007)), BLD, '7199111050[마스터키], 7199111070[발렛키]',
  guide='KGM(쌍용) 순정 키 번호: catcar.info 쌍용 EPC KEY SET 그룹(좌핸들, 이모빌라이저 사양, 생산 기간) — 체어맨 H 7199111050(2000.1~2007.12)·7199111052(2007.12~2011.4)·발렛키 7199111070, '
        '체어맨 W 7105014000(~2011.6)·7105014300(2011.7~), 코란도 71010062A0(이모빌라이저), 무쏘 71001051A0(이모빌라이저)·0000000319(칩 없음), '
        '렉스턴 71050081A0(~2002.7)·A1(~2003.12)·A2(~2006.2)·디젤 71050082A0(2003.12~), 로디우스 7106A21320(디젤)·7106A21310(가솔린), 이스타나 0000000418')
G('체어맨 (1세대, H)', [2007], BLD, '7199111050[마스터키, ~2007.12], 7199111052[마스터키, 2007.12~], 7199111070[발렛키]')
G('체어맨 (1세대, H)', [2008, 2009, 2010, 2011], BLD, '7199111052[마스터키]')
G('체어맨 (2세대, W)', [2008, 2009, 2010], BLD, '7105014000')
G('체어맨 (2세대, W)', [2011], BLD, '7105014000[~2011.6], 7105014300[2011.7~]')
G('체어맨 (2세대, W)', list(range(2012, 2018)), BLD, '7105014300')
G('코란도 (2세대)', list(range(2000, 2006)), BLD, '71010062A0')
G('무쏘', list(range(2000, 2006)), BLD, '71001051A0[이모빌라이저], 0000000319[칩 없음]')
G('무쏘 스포츠 (픽업)', [2002], BLD, '0000000319[칩 없음]')
G('무쏘 스포츠 (픽업)', [2003], BLD, '0000000319[칩 없음], 71001051A0[이모빌라이저, 2003.12~]')
G('무쏘 스포츠 (픽업)', [2004, 2005], BLD, '71001051A0[이모빌라이저], 0000000319[칩 없음]')
G('렉스턴 (1세대)', [2002], BLD, '71050081A0[~2002.7], 71050081A1[2002.7~]')
G('렉스턴 (1세대)', [2003], BLD, '71050081A1[~2003.12], 71050081A2[2003.12~], 71050082A0[디젤, 2003.12~]')
G('렉스턴 (1세대)', [2004, 2005, 2006], BLD, '71050081A2[가솔린], 71050082A0[디젤]')
G('로디우스', list(range(2004, 2012)), BLD, '7106A21320[디젤], 7106A21310[가솔린]')
G('이스타나 (밴)', list(range(2000, 2005)), BLD, '0000000418')

if __name__ == '__main__':
    p = os.path.join(ROOT, 'research', 'recheck', 'overrides.json')
    ovs = [o for o in json.load(open(p, encoding='utf-8')) if not o.get('r5')]
    for o in NEW:
        o['r5'] = True
    ovs += NEW
    json.dump(ovs, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('overrides', len(ovs))
    for f in ('BMW_코리아_출시모델.xlsx', '아우디_models.xlsx', '현대_트랜스폰더_칩코드_DB.xlsx', '벤츠_models.xlsx', '기아_트랜스폰더_칩코드_DBnew.xlsx', 'KG모빌리티(쌍용)_models.xlsx'):
        print(f, recheck.apply_file(os.path.join(ROOT, f), ovs))

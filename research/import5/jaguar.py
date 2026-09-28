# 재규어 — 모델·연식별 키 자료 (research/import5/build.py jaguar)
#   근거: transpondery.com Jaguar Transponder Catalog(2026-09-12판, 모델·생산기간별 칩·이모빌라이저·OEM 키·키 블레이드),
#         abkeys.com·mk3.com·재규어 딜러 부품 카탈로그(품번별 주파수), 한국어 위키백과·국내 출시 기사(국내 판매 연식)
BRAND = '재규어'
FILE = '재규어_models.xlsx'
TITLE = '재규어 트랜스폰더 DB'

G = '[해외 공용 품번]'
def g(*pns): return ', '.join(p + G if '[' not in p else p[:-1] + ', 해외 공용 품번]' for p in pns)

ENDED = {}

def seg(y0, y1, **k):
    k['y'] = (y0, y1); return k

TP = 'transpondery(Jaguar Catalog {})'
FLIP = dict(chip='ID60(4D60)', immo='계기판(IC)', keyway='FO21', ktype_hint='폴딩키', fold=g('C2C35284'), blade_pn=g('C2S31067'))
FLIP_SRC = '재규어 팜비치 부품 카탈로그(X-Type·S-Type 리모컨 C2C35284 433MHz), mr-key.com(X-Type·S-Type·XJ 리모컨 키 C2C35284 433MHz 4D60 FO21), 하퍼 재규어(키 C2S31067)'
K46 = g('C2P17156', 'C2P17153')
K46_SRC = 'abkeys(XF·XK 2007-2011·XJ8 2010-2012 유럽·중동 스마트키 C2P17156·C2P17153 433MHz PCF7953A)'
K49 = g('C2D51458', 'BJ32-15601-DF')
K49_SRC = ('abkeys(순정 F-Type 2014-2020·XJ 2011-2020·XF 2013-2020·XE·F-Pace 2017-2020 스마트키 C2D51458 433MHz FCC KOBJTF10A — HK83-15K601-AA·5E0U50317은 315MHz라 뺌), '
           'mk3(순정 스마트키 BJ32-15601-DF 433MHz)')
S46 = dict(chip='ID46(PCF7953A)', immo='CJB, KVM', keyway='HU101', ktype_hint='스마트키', smart=K46)
S49 = dict(chip='ID49(PCF7953P)', immo='KVM', keyway='HU101', ktype_hint='스마트키', smart=K49)
S49R = dict(S49, immo='KVM, RFA')
SW = '2012년식 ID46→ID49(부분변경) 전환 — 정확한 생산 시점 자료 없음'

MODELS = [
 ('X-타입 (X400)', '2001-2007', [
   seg(2001, 2008, **FLIP,
       src=TP.format('X-Type X400 2001–2009 Texas Crypto 4D60, 계기판(HEC) PATS, 리모컨 일체형 키 C2S31067·C2S42125, FO21') + ', ' + FLIP_SRC
           + ', 이투데이(재규어 X타입 2008년형 국내 출시)')]),
 ('XE (X760)', '2015-2021', [
   seg(2015, 2021, **S49R,
       src=TP.format('XE X760 2015–2024 Hitag Pro ID49 PCF7953P·NCF2953X, KVM·RFA, HU101') + ', ' + K49_SRC
           + ', 모터그래프·한국일보(XE 2015 서울모터쇼 공개, 2015.8 국내 출시)')]),
 ('XF (1세대, X250)', '2008-2015', [
   seg(2008, 2011, **S46,
       src=TP.format('XF X250 2008–2012 Hitag2 ID46 PCF7953A, CJB·KVM, C2P17156·C2P17154, HU101') + ', ' + K46_SRC + ', 위키백과(XF 2008.5 국내 판매)'),
   seg(2012, 2012, **S46, src=TP.format('XF X250 2008–2012 ID46 PCF7953A, 부분변경 2012–2015 Hitag Pro ID49 PCF7953P'),
       split={2012: [dict(chip='ID46(PCF7953A)[전기형]', immo='CJB, KVM[전기형]', smart=K46, flag='orange', note=SW),
                     dict(chip='ID49(PCF7953P)[부분변경]', immo='KVM[부분변경]', smart=K49, flag='orange', note=SW)]}),
   seg(2013, 2015, **S49,
       src=TP.format('XF X250 부분변경 2012–2015 Hitag Pro ID49 PCF7953P, KVM·RFA, CH22-15K601-BB·C2D25514·C2D33044, HU101') + ', ' + K49_SRC)]),
 ('XF (2세대, X260)', '2015-2023', [
   seg(2016, 2020, **S49R,
       src=TP.format('XF X260 2015–2026 Hitag Pro ID49 NCF2953X, KVM·RFA, HK83-15K601-BB·T2H19812·T2H31481, HU101') + ', ' + K49_SRC
           + ', 위키백과(2세대 2016년부터 국내 판매)'),
   seg(2021, 2023, **dict(S49R, smart=''),
       src=TP.format('XF X260 Hitag Pro ID49 또는 2021+ Hitag AES ID4A UWB 스마트키'),
       flag='orange', note='2021년 이후 UWB 스마트키(ID4A) 적용 여부 자료 상충')]),
 ('XJ (3세대, X300/X308)', '1996-2003', [
   seg(2000, 2003, chip='ID13', immo='이모빌라이저 모듈', keyway='FO21', ktype_hint='막대키',
       src=TP.format('XJ X308 1997–2003 Megamos 13 고정 코드, Lucas·Valeo 이모빌라이저 모듈, Tibbe FO21 — 리모컨 LJE2610 주파수 미표기'))]),
 ('XJ (4세대, X350/X358)', '2003-2009', [
   seg(2003, 2009, **FLIP,
       src=TP.format('XJ X350·X358 2003–2009 Texas Crypto 4D60, 계기판(IC), 리모컨 키 C2C35174, FO21') + ', ' + FLIP_SRC)]),
 ('XJ (5세대, X351)', '2010-2019', [
   seg(2010, 2012, **S46,
       src=TP.format('XJ X351 2009–2012 Hitag2 ID46 PCF7953A, CJB·KVM, AW93-15K601-BD·C2D14881, HU101') + ', ' + K46_SRC),
   seg(2013, 2019, **S49R,
       src=TP.format('XJ X351 부분변경 2013–2019 Hitag Pro ID49 PCF7953P, KVM·RFA, HK83-15K601-AA(315MHz 뺌)·C2D33044·C2D46960, HU101') + ', ' + K49_SRC)]),
 ('F-타입 (X152)', '2013-2023', [
   seg(2013, 2023, **S49,
       src=TP.format('F-Type X152 2013–2024 Hitag Pro ID49 PCF7953P, KVM·RFA, EW93-15K601-AC·T2R13374·T2R18451, HU101') + ', ' + K49_SRC
           + ', 위키백과(F-타입 2013.8 국내 첫선, 쿠페 2014)')]),
 ('E-페이스 (X540)', '2017-2021', [
   seg(2018, 2021, chip='ID49(NCF29A1)', immo='KVM, RFA', keyway='HU101', ktype_hint='스마트키', smart=g('JK52-15K601-BG', 'LR087661'),
       src=TP.format('E-Pace X540 2017–2026 Hitag Pro ID49 NCF2953·NCF29A1, KVM·RFA, JK52-15K601-BG·LR087661·J9C18244, HU101')
           + ', jlridssddmongoose·abkeys(JK52-15K601-BG 434MHz KVM, LR087661 433MHz Hitag Pro — J9C14288·J9C3-15K601-AG는 315MHz라 뺌)'
           + ', 한국일보(E-페이스 2018.4 국내 출시)')]),
 ('I-페이스 (전기차)', '2019-2023', [
   seg(2019, 2023, chip='ID49(NCF2953X)', immo='KVM, BCM', keyway='HU101', ktype_hint='스마트키',
       src=TP.format('I-Pace X590 2018–2026 Hitag Pro ID49 NCF2953X 또는 Hitag AES ID4A UWB, KVM·BCM, J9C18244·T4K10803, HU101')
           + ' — 433MHz 순정 품번 확인 안 됨(T4K8898 FCC KOBJXF18A 북미형), 목록(2019-2023)')]),
 ('F-페이스 (X761)', '2016-2023', [
   seg(2016, 2023, **S49R,
       src=TP.format('F-Pace X761 2016–2026 Hitag Pro ID49 PCF7953P·NCF2953, KVM·RFA, HK83-15K601-BB·T4A12802·T4A31920, HU101') + ', ' + K49_SRC
           + ', 목록(2016-2023)')]),
]

GUIDE = [
 '이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.', '',
 '※ 구성',
 "- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 같고, 맨 앞 '브랜드'와 칩코드 뒤 '키종류'를 추가했습니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다.",
 '- 연식은 실제 국내 판매 기준입니다(아래 목록).',
 '- 키 부품번호는 433/434MHz로 확인된 순정 품번만 [해외 공용 품번]으로 적었습니다. 북미형 315MHz(HK83-15K601-AA·5E0U50317·J9C14288 등)는 뺐습니다. 국내 순정 품번은 공개 자료가 없습니다.',
 '- X-타입·XJ(X350) 폴딩키: 리모컨 모듈 C2C35284(433MHz)는 폴딩키 칸, 칩이 든 키(블레이드) C2S31067은 키블레이드 칸에 적었습니다.',
 "- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
 '',
 '※ 칩 코드·이모빌라이저(재규어)',
 '- ID13: Megamos 13 고정 코드, Lucas·Valeo 이모빌라이저 모듈(XJ X308)  |  ID60(4D60): Texas Crypto 4D60, 계기판(IC·HEC) PATS(X-타입·XJ X350)',
 '- ID46(PCF7953A): Hitag2 스마트키, CJB·KVM(XF 2008~2012·XJ X351 2010~2012)',
 '- ID49(PCF7953P·NCF2953X·NCF29A1): Hitag Pro 스마트키, KVM·RFA(XF 부분변경 이후·XE·F-타입·F-페이스·E-페이스·I-페이스) — 2021년 이후 일부 UWB 스마트키는 Hitag AES ID4A',
 '- 키웨이: FO21(Tibbe 8컷, 2009년 이전), HU101(스마트키 비상키)',
 '',
 '※ 색상',
 '- 주황색: 추정이거나 자료가 서로 다른 값, 칩 전환 시점을 모르는 연식(전·후 2행).',
 '',
 '※ 목록과 국내 판매 연식이 다른 모델',
 '- X-타입: 2008년형까지 국내 출시 → 2001~2008 / XF 2세대: 2016년부터 국내 판매 → 2016~2023 / E-페이스: 2018.4 국내 출시 → 2018~2021.',
 '- XJ X308: 1996~1999년식은 2000년식 기준에 따라 빼고 2000~2003 기록 / XF 1세대 2012년식: 부분변경(ID46→ID49) 해로 전·후 2행.',
 '',
 '※ 출처',
 '- transpondery.com Jaguar Transponder Catalog, abkeys.com·mk3.com·jlridssddmongoose 순정 키(품번별 주파수), 재규어 딜러 부품 카탈로그, 한국어 위키백과, 국내 출시 기사(모터그래프·한국일보·이투데이 등).',
 '- 연식별 근거는 research/import5/yearly_jaguar.md에 있습니다.',
]

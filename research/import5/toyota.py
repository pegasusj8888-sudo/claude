# 토요타 — 모델·연식별 키 자료 (research/import5/build.py toyota)
#   근거: transpondery.com Toyota Transponder Catalog(모델·생산기간·시장별 칩·OEM 키·주파수·비상키),
#         abkeys.com·auto-keys.eu 순정 키(품번별 주파수·시장), 한국어 위키백과·국내 출시 기사(국내 판매 연식)
BRAND = '토요타'
FILE = '토요타_models.xlsx'
TITLE = '토요타 트랜스폰더 DB'

C67 = 'ID67(TMS37126)'   # 스마트키 DST40(Page1 94·D4)
S80 = 'ID72(TMS37126)'   # 스마트키 Texas G DST80(Page1 98)
G80 = 'ID72'             # Texas G DST80 트랜스폰더 키(G 칩)
H8A = 'ID8A'             # Texas H DST-AES 128bit
ISK = '스마트키 ECU'
IMM = '이모빌라이저 ECU'
G = '[해외 공용 품번]'
def g(*pns): return ', '.join(p + G if '[' not in p else p[:-1] + ', 해외 공용 품번]' for p in pns)

TP = 'transpondery(Toyota {})'
AB = 'abkeys({})'
AK = 'auto-keys.eu({})'
NEVER_NOTE = '국내 정식 판매 이력 없음 — 해외 사양 기준'

ENDED = {m: False for m in ('코롤라 (E210, 12세대)', '프리우스 (XW60, 5세대)', '캠리 (XV80, 9세대)', '크라운 (크로스오버)', 'GR 수프라', 'GR86',
                            'RAV4 (XA60, 6세대)', '하이랜더 (XU70, 4세대)', '시에나 (XL40, 4세대)', '알파드 (AH40, 4세대)')}

def seg(y0, y1, **k):
    k['y'] = (y0, y1); return k

SMART = dict(immo=ISK, ktype_hint='스마트키')

MODELS = [
 ('프리우스 C (아쿠아)', '2012-2016', [
   seg(2018, 2019, chip=S80, keyway='TOY48', **SMART,
       src=TP.format('Prius c·Aqua 2012–2015 Texas G DST80 스마트키, 89904-0E091·89904-47370(주파수 미표기라 뺌)')
           + ', 위키백과(프리우스 C 2018.5.14 국내 판매 시작 후 판매 부진으로 수입 중단), CEO스코어데일리(2019.2 프리우스C 판매 정리)',
       flag='orange', note='2016년 이후 생산분 칩 자료 없음 — 2012~2015 G 칩 기준 추정')]),
 ('코롤라 (E140/E150, 10세대 후기형)', '2014-2019', [
   seg(2011, 2012, chip=G80, immo=IMM, keyway='TOY43', ktype_hint='막대키',
       src=TP.format('Corolla 2008–2012 Texas G DST80 G-Type Key, TOY43AT') + ', 위키백과(코롤라 2011 서울모터쇼 국내 공개·판매 개시, 1.8 132마력)'),
   seg(2013, 2013, chip=G80, immo=IMM, keyway='TOY43', ktype_hint='막대키',
       src=TP.format('Corolla 2008–2012 G DST80, 2013–2018 Texas H 8A — 2013년식 전환') + ', 위키백과(2014년 초 수입 중단)',
       flag='orange', note='2013년식 G→H 칩 전환 자료 상충')]),
 ('코롤라 (E210, 12세대)', '2019-현재', [
   seg(2019, 2023, chip='ID4A(NCF29A1M)', immo=ISK, ktype_hint='스마트키', smart=g('8990H-02050'), blade_pn=g('69515-33100[비상키]'),
       src=TP.format('Corolla E210 2018–2021 NXP HITAG-AES 4A-AA(8990H-02030 314MHz 뺌), 비상키 69515-33100') + ', '
           + AK.format('순정 Corolla 8990H-02050 434MHz NCF29A1M') + ', 위키백과(E140 이후 코롤라 국내 미수입)',
       flag='orange', note=NEVER_NOTE),
   seg(2024, 2026, chip='ID4A(NCF29A1M)', immo=ISK, ktype_hint='스마트키', smart=g('8990H-02441', '8990H-02420'), blade_pn=g('69515-K0020[비상키]'),
       src=TP.format('Corolla E210 Facelift 2024–2026 HITAG-AES 4A-BA, 비상키 69515-K0020') + ', '
           + AK.format('순정 Corolla 2024+ 8990H-02441·8990H-02420 433MHz HITAG AES'),
       flag='orange', note=NEVER_NOTE)]),
 ('프리우스 (XW30, 3세대)', '2009-2016', [
   seg(2009, 2015, chip=S80, keyway='TOY48', **SMART, smart=g('89904-47190'), blade_pn=g('69515-52120[비상키]'),
       src=TP.format('Prius Smart Key 2010–2015 Texas G DST80(89904-47150 315MHz 뺌), 비상키 69515-52120') + ', '
           + AB.format('Prius 2009-2015 유럽 89904-47190 433MHz B74EA P1 98') + ', 위키백과(3세대 2009.10 국내 출시, 4세대 2016.3)')]),
 ('프리우스 (XW50, 4세대)', '2016-2023', [
   seg(2016, 2023, chip=H8A, keyway='TOY51', **SMART, smart=g('89904-47560', '89904-47561'), blade_pn=g('69515-47030[비상키]'),
       src=TP.format('Prius 2016–2022 Texas H-8A DST-AES A9(89904-47530 315MHz 뺌), TOY51 비상키 69515-47030') + ', '
           + AB.format('순정 Prius 2016-2018 유럽·중동 89904-47560·47561 433MHz BR1EW P1 A9') + ', 위키백과(4세대 2016.3 국내 판매, 5세대 2023.12.13)')]),
 ('프리우스 (XW60, 5세대)', '2023-현재', [
   seg(2023, 2026, chip=H8A, keyway='TOY51', **SMART, blade_pn=g('69515-K0020[비상키]'),
       src=TP.format('Prius WX60 2022–2026 Texas H-8A DST-AES 8A-BA(8990H-47120·47130 315MHz 뺌), 비상키 69515-K0020')
           + ', 위키백과(5세대 2023.12.13 국내 출시)')]),
 ('캠리 (XV40, 6세대 후기형)', '2009-2012', [
   seg(2009, 2011, chip=C67, immo='스마트키 ECU(93C86)', keyway='TOY48', ktype_hint='스마트키', smart=g('89904-33100'), blade_pn=g('69515-52120[비상키]'),
       src=TP.format('Camry 2005–2010 Texas Crypto 4D ID67·ID68, Smart Key 2007–2010 DST40 Page1 94(89904-06041 315MHz 뺌), TOY48 비상키 69515-52120') + ', '
           + AB.format('Aurion·Camry 2007-2010 유럽·중동 스마트키 89904-33100 433MHz B53EA P1 D4')
           + ', 위키백과(2009.10.20 한국토요타 공식 판매 — 일본산), 이투데이(캠리 3490만원)')]),
 ('캠리 (XV50, 7세대)', '2012-2018', [
   seg(2012, 2017, chip=H8A, keyway='TOY51', **SMART, smart=g('89904-33460'), blade_pn=g('69515-33100[비상키]'),
       src=TP.format('Camry Smart Key 2012–2017 Texas H-8A DST-AES(89904-06140 314MHz 뺌), TOY51 비상키 69515-33100') + ', '
           + AB.format('순정 Camry·Avalon·Aurion 2011+ 유럽·중동 스마트키 89904-33460 433MHz BA4EQ P1 88')
           + ', 위키백과(미국산 7세대 2012.1 국내 출시, 2013 대한민국 올해의 차, 8세대 2017.10.19)')]),
 ('캠리 (XV70, 8세대)', '2018-2024', [
   seg(2017, 2024, chip=H8A, keyway='TOY51', **SMART, smart=g('89904-33570', '89904-33770'), blade_pn=g('69515-47030[비상키]'),
       src=TP.format('Camry 2018–2024 Texas H-8A DST-AES A9(89904-06220·06240 315MHz 뺌), TOY51 비상키 69515-47030') + ', '
           + AB.format('순정 Camry 2018-2020 유럽·중동 스마트키 89904-33570·89904-33770 433MHz BR2EX P1 A9')
           + ', 위키백과(8세대 2017.10.19 국내 출시 — 일본산, 9세대 2024.11.26)')]),
 ('캠리 (XV80, 9세대)', '2024-현재', [
   seg(2024, 2026, chip='ID4A(NCF29A1M)', keyway='TOY51', **SMART, blade_pn=g('69515-K0020[비상키]'),
       src=TP.format('Camry 80 2025–2026 North America NXP HITAG-AES ID4A NCF29A1M(8990H-AQ010 314MHz 뺌), 비상키 69515-33120·69515-K0020')
           + ', 위키백과(9세대 2024.11.26 국내 출시)')]),
 ('아발론 (XX50)', '2019-현재', [
   seg(2018, 2022, chip=H8A, keyway='TOY51', **SMART,
       src=TP.format('Avalon 2018–2022 Texas H-8A DST-AES 8A-AA(8990H-07010·07070 315MHz 뺌)')
           + ', 위키백과(XX50 2018.11.6 국내 출시, 2022 북미 단종으로 국내 수입 중단·2023.5 크라운 크로스오버가 대체)')]),
 ('크라운 (크로스오버)', '2023-현재', [
   seg(2023, 2026, chip=H8A, keyway='TOY51', **SMART, smart=g('8990H-33022'), blade_pn=g('69515-K0020[비상키]'),
       src=TP.format('Crown 2023–2026 Texas H-8A DST-AES 스마트키(8990H-30190 315MHz 뺌), 비상키 69515-K0010·69515-K0020') + ', '
           + AK.format('순정 Crown 2023 스마트키 8990H-33022 433MHz 8A') + ', 위키백과(크라운 크로스오버 2023.6.5 국내 출시)')]),
 ('GR 수프라', '2019-현재', [
   seg(2020, 2026, chip='ID49', immo='BDC', keyway='HU100R', ktype_hint='스마트키', smart=g('8990A-WAA12'),
       src=TP.format('GR Supra A90·A91 2020–2026 NXP Hitag Pro ID49, BMW BDC, 8990A-WAA12 FCC N5F-ID21A 433MHz, HU100R')
           + ', 위키백과(GR 수프라 2020.1.21 국내 정식 출시)')]),
 ('GR86', '2022-현재', [
   seg(2022, 2026, chip=H8A, **SMART, smart=g('SU003-10030'),
       src=TP.format('GR86 2022–2026 Texas H-8A DST-AES 스바루 계열 스마트키 SU003-10030 FCC HYQ14AHK 433/434MHz')
           + ', 위키백과(2세대 86 2022.5.16 국내 출시, 6단 수동만)')]),
 ('RAV4 (XA30, 3세대)', '2009-2013', [
   seg(2009, 2012, chip=G80, immo=IMM, keyway='TOY43', ktype_hint='막대키', blade_pn=g('89070-42531[리모컨키]', '89070-28812[리모컨키]'),
       src=TP.format('RAV4 2004–2009 Texas 4D-67G, 2010–2012 Texas G DST80 G-Type Key') + ', '
           + AB.format('순정 RAV4 2005-2011 유럽·중동 리모컨 일체형 키 89070-42531·89070-28812 433MHz TOY43')
           + ', 위키백과(RAV4 2009.10 국내 판매, 4세대 2013.5)')]),
 ('RAV4 (XA40, 4세대)', '2015-2018', [
   seg(2013, 2018, chip=H8A, keyway='TOY51', **SMART, smart=g('89904-42180', '89904-42321', '89904-42130', '89904-42230'), blade_pn=g('69515-33100[비상키]'),
       src=TP.format('RAV4 2013–2018 Texas H-8A DST-AES(89904-0R080 315MHz 뺌), TOY51 비상키 69515-33100') + ', '
           + AB.format('순정 RAV4 2013-2017 유럽·중동 스마트키 89904-42180·89904-42321 433MHz BA2EQ P1 88, 89904-42130, 2013-2018 일본형 89904-42230 433MHz')
           + ', 위키백과(4세대 2013.5 국내 판매, 하이브리드 2016.3, 5세대 2019.5)')]),
 ('RAV4 (XA50, 5세대)', '2019-현재', [
   seg(2019, 2025, chip=H8A, keyway='TOY51', **SMART, smart=g('8990H-42170', '8990H-42340', '8990H-42360'), blade_pn=g('69515-47030[비상키]'),
       src=TP.format('RAV4 XA50 2018–2025 Texas H-8A DST-AES 8A-AA·BA(8990H-0R030·0R220 314MHz 뺌), 비상키 69515-47030') + ', '
           + AK.format('순정 RAV4 스마트키 8990H-42170·8990H-42340·8990H-42360 433MHz')
           + ', 위키백과(5세대 2019.5 국내 판매, PHEV 2023.2.21, 6세대 2026.6.16)')]),
 ('RAV4 (XA60, 6세대)', '2026-현재', [
   seg(2026, 2026, chip='ID49', **SMART, smart=g('8990H-0R510', '8990H-0R320'),
       src=TP.format('RAV4 2026 North America NXP HITAG-PRO ID49, 8990H-0R510 FCC HYQ14FNB 433.58/434.42MHz') + ', '
           + AK.format('순정 RAV4 2026 스마트키 8990H-0R320 433MHz ID49') + ', 위키백과(6세대 2026.6.16 국내 정식 출시)')]),
 ('벤자 (AV10, 1세대 후기형)', '2010-2015', [
   seg(2012, 2015, chip=S80, keyway='TOY43[일반 키], TOY48[비상키]', immo=ISK, ktype_hint='막대키,스마트키',
       src=TP.format('Venza 2009–2015 4D-67(전기)·Texas G 4D-72 DST80(후기) 트랜스폰더 키, 스마트키·TOY48 비상키')
           + ', 락스미스키리스(Venza 2013·2014 스마트키 HYQ14ACX G DST80 — 314MHz라 품번 뺌), 위키백과(2012.11 부분변경 모델 국내 수입)')]),
 ('FJ 크루저', '2010-2014', [
   seg(2014, 2014, chip=G80, immo=IMM, keyway='TOY43', ktype_hint='막대키',
       src=TP.format('FJ Cruiser 2011–2014 Texas G DST80 G-Type Key')
           + ', 나무위키·오토뷰(2013 서울모터쇼 공개 후 2013.12.24 100대 한정 국내 정식 판매)')]),
 ('하이랜더 (XU70, 4세대)', '2020-현재', [
   seg(2023, 2024, chip=H8A, keyway='TOY51', **SMART, smart=g('8990H-0E200', '8990H-0E070'), blade_pn=g('69515-K0020[비상키]'),
       src=TP.format('Highlander 2023–2024 Texas H-8A DST-AES 8A-BA(8990H-0E600 314MHz 뺌), 비상키 69515-33120·69515-K0020') + ', '
           + AK.format('순정 Highlander 2020+ 8990H-0E200 434MHz 8A, 2022+ 8990H-0E070 433MHz 8A') + ', 위키백과(4세대 2023.7.25 국내 첫 출시)'),
   seg(2025, 2026, chip='ID4A', keyway='TOY51', **SMART, blade_pn=g('69515-K0020[비상키]'),
       src=TP.format('Highlander 2025–2026 NXP HITAG-AES 4A-BA'))]),
 ('시에나 (XL30, 3세대)', '2015-2020', [
   seg(2011, 2020, chip=S80, keyway='TOY43[일반 키], TOY48[비상키]', immo=ISK, ktype_hint='막대키,스마트키', blade_pn=g('69515-08020[비상키]'),
       src=TP.format('Sienna 2011–2014 G DST80·2016–2019 H-8A 일반 키, Smart Key 2011–2020 89904-08010(315MHz 뺌)·비상키 69515-08020')
           + ', abkeys·UHS(89904-08010 HYQ14ADR TMS37126 DST-4D Page1 98 — ID74 표기 판매처도 있음), 위키백과(3세대 2011.3 국내 출시, 부분변경 2018.3.19, 4세대 2021.4.13)',
       flag='orange', note='스마트키 칩 자료 상충(Page1 98 DST80, ID74 표기)')]),
 ('시에나 (XL40, 4세대)', '2021-현재', [
   seg(2021, 2026, chip=H8A, keyway='TOY51', **SMART, blade_pn=g('69515-K0020[비상키]'),
       src=TP.format('Sienna XL40 Hybrid 2020–2026 Texas H-8A DST-AES 8A-BA(8990H-08010 315MHz 뺌), 비상키 69515-33120·69515-K0020')
           + ', 위키백과(4세대 2021.4.13 국내 출시)')]),
 ('알파드 (AH40, 4세대)', '2023-현재', [
   seg(2023, 2026, chip=H8A, **SMART,
       src='transpondery(Alphard는 2006–2014 ID67까지만 수록), KEYDIY·onlyda(Alphard·Vellfire 스마트키 8A Tiris DST AES 433/434MHz), OBDII365(2022년 이후 토요타 신차 8A-BA·4A)'
           + ', 위키백과(4세대 2023.9.18 국내 정식 출시)',
       flag='orange', note='4세대 전용 칩 자료 없음 — 같은 시기 토요타 8A-BA 기준 추정')]),
]

GUIDE = [
 '이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.', '',
 '※ 구성',
 "- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 같고, 맨 앞 '브랜드'와 칩코드 뒤 '키종류'를 추가했습니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다.",
 '- 연식은 실제 국내 판매 기준입니다(토요타 브랜드 국내 출시 2009.10.20). 원본 목록 연식과 국내 판매가 다른 모델은 국내 기준으로 바꿨습니다(아래 목록).',
 '- 키 부품번호는 433/434MHz 순정 품번만 적었습니다. 북미형(312~315MHz, FCC HYQ14FBA·HYQ14FBC·HYQ14FBX 등)과 일본형 저주파 품번은 뺐습니다.',
 '- 433/434MHz 품번은 대부분 유럽·중동 사양으로 확인된 순정 품번이라 [해외 공용 품번]으로 표시했습니다. 국내 순정 품번은 공개 자료가 없습니다.',
 "- 비상키(키블레이드) 품번 69515-xxxxx는 스마트키용 기계식 비상키입니다. 리모컨 일체형 막대키는 키블레이드 칸에 [리모컨키]로 적었습니다.",
 "- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
 '',
 '※ 칩 코드(토요타)',
 '- ID67(TMS37126): 스마트키 DST40(Page1 94·D4, 2007~2011년경 캠리)  |  ID72(TMS37126): 스마트키 Texas G DST80(Page1 98, 프리우스 3세대·벤자·시에나 3세대)',
 '- ID72: Texas G DST80 트랜스폰더 키(G 칩, 2010~2013년경 일반 키)  |  ID8A: Texas H DST-AES 128bit(2012년 이후 스마트키, Page1 88·A8·A9·AA·BA)',
 '- ID4A: NXP HITAG-AES(코롤라 E210·캠리 9세대·하이랜더 2025~)  |  ID49: NXP Hitag Pro(GR 수프라 — BMW BDC, RAV4 6세대)',
 '- 이모빌라이저: 이모빌라이저 ECU(일반 키) → 스마트키 ECU(DENSO·TOKAI RIKA)',
 '- 키웨이: TOY43(일반 키), TOY48(2011년 이전 스마트키 비상키), TOY51(2012년 이후 스마트키 비상키), HU100R(GR 수프라)',
 '',
 '※ 색상',
 '- 주황색: 추정이거나 자료가 서로 다른 값, 또는 국내 정식 판매 이력이 없는 모델(해외 사양 기준).',
 '',
 '※ 목록과 국내 판매 연식이 다른 모델',
 '- 프리우스 C: 2018.5.14 국내 판매 시작, 판매 부진으로 수입 중단 → 2018~2019 / 코롤라 E140: 2011 국내 판매 개시, 2014년 초 수입 중단 → 2011~2013 / 코롤라 E210: 국내 미수입 — 목록 연식대로 남기고 주황색.',
 '- 프리우스 3세대: 2009.10~2015(4세대 2016.3) / 캠리 XV40: 2009.10~2011, XV50: 2012~2017, XV70: 2017.10.19~2024, XV80: 2024.11.26~ / 아발론 XX50: 2018.11.6~2022(북미 단종으로 수입 중단).',
 '- GR 수프라: 2020.1.21 국내 출시 / RAV4 3세대: 2009.10~2012, 4세대: 2013.5~2018, 5세대: 2019.5~2025, 6세대: 2026.6.16 국내 출시(목록에 없어 행 추가).',
 '- 벤자: 2012.11 부분변경 모델부터 수입 → 2012~2015 / FJ 크루저: 2013.12.24 100대 한정 판매 → 2014 / 하이랜더: 2023.7.25 국내 첫 출시 → 2023~ / 시에나 3세대: 2011.3 국내 출시 → 2011~2020.',
 '',
 '※ 출처',
 '- transpondery.com Toyota Transponder Catalog(모델·생산기간·시장별 칩·품번·주파수·비상키), abkeys.com·auto-keys.eu 순정 키(품번별 주파수·시장), 한국어 위키백과·나무위키, 국내 출시 기사(이투데이·오토뷰·CEO스코어데일리 등).',
 '- 연식별 근거는 research/import5/yearly_toyota.md에 있습니다.',
]

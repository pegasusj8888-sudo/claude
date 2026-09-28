# 랜드로버 — 모델·연식별 키 자료 (research/import5/build.py landrover)
#   근거: transpondery.com Land Rover & Range Rover Transponder Catalog(2026-09-18판, 모델·생산기간별 칩·품번·이모빌라이저),
#         abkeys.com·auto-keys.eu·jlridssddmongoose.com 순정 키(품번별 주파수), 한국어 위키백과·국내 출시 기사
BRAND = '랜드로버'
FILE = '랜드로버_models.xlsx'
TITLE = '랜드로버 트랜스폰더 DB'

G = '[해외 공용 품번]'
def g(*pns): return ', '.join(p + G if '[' not in p else p[:-1] + ', 해외 공용 품번]' for p in pns)
NEVER_NOTE = '국내 정식 판매 기록 없음 — 해외 사양 기준'

ENDED = {m: False for m in ('레인지로버 이보크 (2세대)', '디스커버리 스포츠', '레인지로버 벨라', '디스커버리 (5세대)',
                            '레인지로버 스포츠 (3세대)', '디펜더 (신형, L663)', '레인지로버 (5세대, L460)')}

def seg(y0, y1, **k):
    k['y'] = (y0, y1); return k

TPC = 'transpondery(Land Rover·Range Rover Catalog {})'
K10 = g('LR020366', 'LR032796')                 # 2010~2012 KVM 스마트키 433MHz
K12 = g('LR087106', 'LR087661', '5E0U40247')    # 2012~2017 Hitag Pro 433MHz
K18 = g('LR116874', 'JK52-15K601-BG')           # 2018~ 433/434MHz
SRC_K = ('jlridssddmongoose(LR020366·LR032796 433MHz, LR087106·LR087661·LR066836 433MHz Hitag Pro, LR116874 433/434MHz MY2015-2020+, JK52-15K601-BG 434MHz KVM), '
         'abkeys(순정 5E0U40247 433MHz PCF7953P ID49 레인지로버 스포츠·보그·이보크 2010+, 순정 JK52-15K601-BG 434MHz 2018+)')
SMART10 = dict(chip='ID49(PCF7953P)', immo='KVM, BCM', keyway='HU101', ktype_hint='스마트키')
SMART18 = dict(chip='ID49', immo='RFA', keyway='HU101', ktype_hint='스마트키', blade_pn=g('LR116570'))

MODELS = [
 ('프리랜더 (1세대)', '1998-2006', [
   seg(2000, 2000, chip='ID33(PCF7930)', immo='이모빌라이저 모듈', keyway='NE38', ktype_hint='막대키',
       src=TPC.format('Freelander 1 L314 1997–2000 Philips PCF7930·PCF7931 ID33 고정 코드, 27VT') + ', 카이즈유(프리랜더 1999.3 국내 상륙, 2001.6 PAG코리아)'),
   seg(2001, 2003, chip='ID44(PCF7935)', immo='EWS', keyway='NE38', ktype_hint='막대키',
       src=TPC.format('Freelander 1 2001–VIN 242163 Philips PCF7935 ID44, BMW 계열 EWS')),
   seg(2004, 2006, chip='ID46(PCF7936)', immo='SAWDOC', keyway='NE38', ktype_hint='막대키',
       src=TPC.format('Freelander 1 VIN 242164–2006 PCF7936 ID46, SAWDOC 이모빌라이저 PIC18F252'),
       split={2004: [dict(chip='ID44(PCF7935)[VIN 242163 이전]', immo='EWS[VIN 242163 이전]', flag='orange', note='ID44→ID46 전환(VIN 242164) 시점 연식 자료 없음'),
                     dict(chip='ID46(PCF7936)[VIN 242164 이후]', immo='SAWDOC[VIN 242164 이후]', flag='orange', note='ID44→ID46 전환(VIN 242164) 시점 연식 자료 없음')]})]),
 ('프리랜더 2', '2007-2014', [
   seg(2007, 2009, chip='ID46(PCF7936)', immo='CJB, BCM', keyway='HU101', ktype_hint='스마트키', smart=g('LR013005', 'LR001863', 'LR006170', 'LR007594', 'LR008022'), blade_pn=g('LR007227'),
       src=TPC.format('Freelander 2 L359 2006–2009 PCF7936 ID46, LR013005, 6H52-15K601-AG, CJB·BCM 도킹 키') + ', abkeys(LR013005 433MHz 2006-2012, 비상키 LR007227 HU101), auto-keys.eu(LR013005·LR001863·LR006170·LR007594·LR008022 433MHz)'),
   seg(2010, 2011, chip='ID46(PCF7953A)', immo='KVM, BCM', keyway='HU101', ktype_hint='스마트키', smart=g('LR013005'), blade_pn=g('LR007227'),
       src=TPC.format('Freelander 2 2010–2012 PCF7953A·PCF7953AT ID46, 5E0B502A7, KVM-RFA') + ', abkeys(LR013005 433MHz Freelander 2 2006-2012)'),
   seg(2012, 2014, chip='ID49(PCF7953P)', immo='KVM, BCM', keyway='HU101', ktype_hint='스마트키', smart=g('LR087106', 'LR087663'),
       src=TPC.format('Freelander 2 2012–2015 PCF7953P ID49 Hitag Pro, LR060129·LR065378·LR087102·LR087663') + ', ' + SRC_K)]),
 ('레인지로버 이보크 (1세대)', '2012-2019', [
   seg(2012, 2019, **SMART10, smart=K12,
       src=TPC.format('Evoque L538 2011–2013·2014–2018 PCF7953P ID49 Hitag Pro, LR087106·LR087661·LR087663·5E0U40457') + ', ' + SRC_K + ', 이데일리(이보크 2011.12 국내 출시)')]),
 ('레인지로버 이보크 (2세대)', '2019-현재', [
   seg(2019, 2026, **SMART18, smart=K18,
       src=TPC.format('Evoque L551 2019–2026+ NXP Hitag Pro ID49 NCF29, LR116874·JK52-15K601-BG, RFA·PEPS') + ', ' + SRC_K)]),
 ('디스커버리 스포츠', '2015-현재', [
   seg(2015, 2017, **SMART10, smart=g('LR087106', 'LR087661'),
       src=TPC.format('Discovery Sport L550 2015–2017 PCF7953P ID49, LR087106·LR087661·LR087663, KVM·RFA') + ', ' + SRC_K + ', 오토뷰(2015.5 국내 출시)'),
   seg(2018, 2026, **SMART18, smart=K18,
       src=TPC.format('Discovery Sport 2018–2026+ Hitag Pro ID49 NCF29, LR116874·JK52-15K601-BG') + ', ' + SRC_K)]),
 ('레인지로버 벨라', '2017-현재', [
   seg(2017, 2026, **SMART18, smart=K18,
       src=TPC.format('Velar L560 2017–2018 PCF7953P ID49, 2018–2026+ Hitag Pro ID49 NCF29, LR116874·JK52-15K601-BG') + ', ' + SRC_K + ', 랜드로버코리아(벨라 2017.9 국내 출시)')]),
 ('디스커버리 (2세대)', '1999-2004', [
   seg(2000, 2004, chip='ID46(PCF7936)', immo='BCU', keyway='NE38', ktype_hint='막대키',
       src=TPC.format('Discovery II 1999–2004 PCF7936 ID46, Valeo BCU 패시브 이모빌라이저, CWE100710KIT·NTC9838') + ', 카이즈유(2004 디스커버리2 국내 판매)')]),
 ('디스커버리 (3세대)', '2004-2009', [
   seg(2004, 2009, chip='ID46(PCF7936)', immo='CEM', keyway='HU101', ktype_hint='폴딩키',
       src=TPC.format('Discovery 3 L319 2004–2009 PCF7936 ID46, CEM(PIC18F662), CWE500041SW·LR088260') + ', abkeys(순정 LR3·레인지로버 스포츠 2005+ 3버튼 플립키 433MHz HU101 — 품번 미표기)')]),
 ('디스커버리 (4세대)', '2009-2017', [
   seg(2010, 2011, **SMART10, smart=K10,
       src=TPC.format('Discovery 4 2010–2012 Hitag Pro PCF7939P(비상 시동)·PCF7953 키리스, LR020366·LR014016·LR032796, RFA+BCM') + ', ' + SRC_K),
   seg(2012, 2016, **SMART10, smart=g('LR087106', 'LR087661'),
       src=TPC.format('Discovery 4 2012–2013 PCF7953P ID49, LR087661·LR087663·LR087106') + ', ' + SRC_K)]),
 ('디스커버리 (5세대)', '2017-현재', [
   seg(2017, 2017, **SMART10, smart=g('LR087106', 'LR087661'),
       src=TPC.format('Discovery 5 L462 2017–2018 PCF7953P ID49, LR087106·LR087661·LR087663, JPLA RFA') + ', ' + SRC_K),
   seg(2018, 2026, **SMART18, smart=K18,
       src=TPC.format('Discovery 5 2018–2026+ Hitag Pro ID49 NCF29, LR116874·JK52-15K601-BG, K8D2 RFA') + ', ' + SRC_K)]),
 ('레인지로버 스포츠 (1세대)', '2005-2013', [
   seg(2005, 2008, chip='ID46(PCF7936)', immo='CEM', keyway='HU101', ktype_hint='폴딩키',
       src=TPC.format('Range Rover Sport L320 2005–2009 PCF7936 ID46, CEM(PIC18F6620)') + ', abkeys(순정 3버튼 플립키 433MHz HU101 — 품번 미표기)'),
   seg(2009, 2009, chip='ID46(PCF7953A)', immo='KVM', keyway='HU101', ktype_hint='스마트키', smart=K10,
       src=TPC.format('Range Rover Sport L320 2009 PCF7953A ID46, LR014016·LR020366·LR032796, KVM-RFA') + ', ' + SRC_K),
   seg(2010, 2011, **SMART10, smart=K10,
       src=TPC.format('Range Rover Sport L320 2010–2011 Hitag Pro PCF7939P·PCF7947·PCF7953') + ', ' + SRC_K),
   seg(2012, 2013, **SMART10, smart=g('LR087106', '5E0U40247'),
       src=TPC.format('Range Rover Sport L320 2012–2013 Hitag Pro, LR060127·LR066465·LR071354·LR087103') + ', ' + SRC_K)]),
 ('레인지로버 스포츠 (2세대)', '2014-2022', [
   seg(2014, 2017, **SMART10, smart=g('LR087106', 'LR087661', '5E0U40247'),
       src=TPC.format('Range Rover Sport L494 2014–2017 PCF7953P ID49, LR087106·LR087661·LR087663, HPLA KVM') + ', ' + SRC_K),
   seg(2018, 2022, **SMART18, smart=K18,
       src=TPC.format('Range Rover Sport L494 2018–2022 Hitag Pro ID49 NCF29, LR116874·JK52-15K601-BG') + ', ' + SRC_K)]),
 ('레인지로버 스포츠 (3세대)', '2023-현재', [
   seg(2023, 2026, chip='ID49', immo='RFA', keyway='HU101', ktype_hint='스마트키',
       src=TPC.format('Range Rover Sport L461 2023–2026+ Hitag Pro ID49 NCF29, LR163588·LR177484, K8D2 RFA·PEPS') + ' — 433/434MHz 품번 확인 안 됨, abkeys·CLK(JLR 스마트키 비상키 HU101), 뉴시스(3세대 공개·국내 출시)')]),
 ('디펜더 (신형, L663)', '2020-현재', [
   seg(2020, 2026, **SMART18, smart=g('LR116874'),
       src=TPC.format('Defender L663 2020–2026+ Hitag Pro ID49 NCF29, LR116874·LR133282·LR163588, K8D2 RFA') + ', ' + SRC_K + ', 서울신문·탑라이더(신형 디펜더 2020.7 국내 출시)')]),
 ('레인지로버 (2세대, P38A)', '1996-2001', [
   seg(2000, 2001, chip='ID46(PCF7936)', immo='BeCM', keyway='NE38', ktype_hint='막대키',
       src=TPC.format('Range Rover P38A 1998–2002 PCF7936 ID46, BeCM 패시브 이모빌라이저'), flag='orange',
       note='P38A 국내 판매 연식 자료 없음(1990년대 인치케이프·BMW 딜러 수입 기록만)')]),
 ('레인지로버 (3세대, L322)', '2002-2012', [
   seg(2002, 2004, chip='ID44(PCF7935)', immo='EWS3', keyway='HU92', ktype_hint='막대키',
       src=TPC.format('Range Rover L322 2002–2005 PCF7935 ID44, BMW 계열 EWS3') + ', abkeys(순정 레인지로버 보그 2002-2008 리모컨 일체형 키 433MHz HU92)'),
   seg(2005, 2009, chip='ID46(PCF7936)', immo='이모빌라이저 박스(9S12DG128)', keyway='HU101', ktype_hint='폴딩키',
       src=TPC.format('Range Rover L322 2005–2009 PCF7936 ID46, 이모빌라이저 박스 9S12DG128, CWE500041SW·LR088260') + ', abkeys(보그 2007-2010 플립키 433MHz PCF7936)',
       split={2005: [dict(chip='ID44(PCF7935)[전기 생산]', immo='EWS3[전기 생산]', keyway='HU92', ktype_hint='막대키', flag='orange', note='EWS3(ID44)→ID46 전환 시점 자료 없음'),
                     dict(chip='ID46(PCF7936)[후기 생산]', immo='이모빌라이저 박스(9S12DG128)[후기 생산]', flag='orange', note='EWS3(ID44)→ID46 전환 시점 자료 없음')]}),
   seg(2010, 2011, chip='ID46(PCF7953A)', immo='KVM', keyway='HU101', ktype_hint='스마트키', smart=K10,
       src=TPC.format('Range Rover L322 2009–2011 PCF7953A ID46, LR020365·LR020366·LR032796·AH42-15K601-AF') + ', ' + SRC_K),
   seg(2012, 2012, chip='ID49(PCF7953P)', immo='KVM', keyway='HU101', ktype_hint='스마트키', smart=g('LR087661', 'LR087663'),
       src=TPC.format('Range Rover L322 2012 PCF7953P ID49, LR087661·LR087663') + ', ' + SRC_K)]),
 ('레인지로버 (4세대, L405)', '2012-2021', [
   seg(2013, 2017, **SMART10, smart=g('LR087106', 'LR087661'),
       src=TPC.format('Range Rover L405 2013·2014–2017 PCF7953P ID49, LR087106·LR087661·LR087663, BJ32-15K601-DF') + ', ' + SRC_K),
   seg(2018, 2021, **SMART18, smart=K18,
       src=TPC.format('Range Rover L405 2018–2021 Hitag Pro ID49 NCF29, LR116874·JK52-15K601-BG') + ', ' + SRC_K)]),
 ('레인지로버 (5세대, L460)', '2022-현재', [
   seg(2022, 2026, chip='ID49', immo='RFA', keyway='HU101', ktype_hint='스마트키',
       src=TPC.format('Range Rover L460 2022–2026+ Hitag Pro ID49 NCF29, LR163588·LR177484, K8D2 RFA·PEPS') + ' — 433/434MHz 품번 확인 안 됨, abkeys·CLK(JLR 스마트키 비상키 HU101)')]),
]

GUIDE = [
 '이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.', '',
 '※ 구성',
 "- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 같고, 맨 앞 '브랜드'와 칩코드 뒤 '키종류'를 추가했습니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다.",
 '- 원본 목록의 디스커버리 1세대(1992-1998)·레인지로버 1세대(1992-1996)는 2000년 이전 모델이라 행이 없습니다.',
 '- 키 부품번호는 국내 사양(433/434MHz)만 적었습니다. 품번별 주파수가 확인된 것만 넣었고(LR013005·LR020366·LR032796·LR087106·LR087661·LR116874·JK52-15K601-BG·5E0U40247 등), 미국형(315MHz, FCC KOBJTF10A 315·LR013006·5E0U40307·N8EM-15K601-CA 등)은 뺐습니다. 국내 순정 품번은 공개 자료가 없어 [해외 공용 품번]으로 표시했습니다.',
 '- LR133282·LR163588·LR177484(2020년 이후 신형 키)는 주파수를 확인하지 못해 넣지 않았습니다.',
 "- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
 '',
 '※ 칩 코드·이모빌라이저(랜드로버)',
 '- ID33(PCF7930): 고정 코드(프리랜더 1 초기)  |  ID44(PCF7935): BMW 계열 EWS(프리랜더 1·레인지로버 L322 초기)  |  ID46(PCF7936): Hitag2 막대키·플립키  |  ID46(PCF7953A): 2009~2011 스마트키',
 '- ID49(PCF7953P): Hitag Pro 스마트키(2010~2017년경, 비상 시동은 PCF7939P)  |  ID49: 2018년 이후 NCF29 계열 스마트키',
 '- 이모빌라이저: EWS(프리랜더 1)·EWS3(L322 초기) → SAWDOC·BCU·BeCM·CEM → KVM(키리스 모듈)+BCM → RFA(PEPS, 2018년 이후)',
 '- 키웨이: NE38(구형), HU92(L322 초기), HU101(2004년 이후 플립키·스마트키 비상키)',
 '',
 '※ 색상',
 '- 주황색: 추정이거나 자료가 서로 다른 값, 칩 전환 시점을 모르는 연식(전·후 2행).',
 '',
 '※ 목록과 국내 판매 연식이 다른 모델',
 '- 레인지로버 L405: 국내 2013년부터(L322 마지막 2012) / 구형 디펜더(L316, 목록 1997-2015): 국내 정식 판매 기록이 없어 뺐습니다 / 이보크 1세대 2011.12, 디스커버리 스포츠 2015.5, 벨라 2017.9, 신형 디펜더 2020.7 국내 출시.',
 '',
 '※ 출처',
 '- transpondery.com Land Rover & Range Rover Transponder Catalog, abkeys.com·auto-keys.eu·jlridssddmongoose.com 순정 키, 한국어 위키백과·나무위키, 국내 출시 기사(이데일리·오토뷰·서울신문 등).',
 '- 연식별 근거는 research/import5/yearly_landrover.md에 있습니다.',
]

# 포드 — 모델·연식별 키 자료 (research/import5/build.py ford)
#   근거: transpondery.com Ford Transponder Catalog(모델·생산기간·시장별 칩·OEM 키·주파수)·Ford OEM Keys & Remotes Catalog,
#         한국어 위키백과·나무위키·국내 출시 기사(국내 판매 연식)
BRAND = '포드'
FILE = '포드_models.xlsx'
TITLE = '포드 트랜스폰더 DB'

G = '[해외 공용 품번]'
def g(*pns): return ', '.join(p + G if '[' not in p else p[:-1] + ', 해외 공용 품번]' for p in pns)
NEVER_NOTE = '국내 정식 판매 이력 없음 — 해외(북미) 사양 기준'

ENDED = {m: False for m in ('머스탱 (7세대)', '브롱코', '익스플로러', '레인저')}

def seg(y0, y1, **k):
    k['y'] = (y0, y1); return k

TP = 'transpondery(Ford Catalog {})'
TKEY40 = g('164-R0475', '164-R8040')   # 4D63 40bit 트랜스폰더 키(Strattec 599114·5913441, H84-PT)
X80 = '4D63x80'
PATS = 'PATS'

MODELS = [
 ('포커스', '2005-2011', [
   seg(2005, 2011, chip='ID63(4D63), ID46(PCF7952)[키리스]', immo=PATS, keyway='HU101', ktype_hint='폴딩키,스마트키',
       fold=g('3M5T-15K601-AB', '3M5T-15K601-AC'), smart=g('3M5T-15K601-DA[키리스]', '3M5T-15K601-DB[키리스]', '3M5T-15K601-DC[키리스]'),
       src=TP.format('Focus MK2 2004–2010 Europe Texas Crypto 4D63 DST40, 플립키 3M5T-15K601-AB·AC 433MHz HU101, KeyFree 3M5T-15K601-DA·DB·DC PCF7952 433MHz') + ', OEM 키 카탈로그(Focus 2004–2010 3M5T-15K601-AB·AC 433MHz)')]),
 ('토러스', '2011-2016', [
   seg(2011, 2012, chip=X80, immo=PATS, keyway='FO38, HU101', ktype_hint='막대키,스마트키', blade_pn=g('164-R8041[비상키]'),
       src=TP.format('Taurus 2010–2019 Texas Crypto 2 DST80 ID63-6F 80bit, PEPS 비상키 164-R8041 — 스마트키 164-R8092는 315MHz라 뺌')),
   seg(2013, 2016, chip=X80 + '[일반 키], ID46(PCF7953A)[스마트키]', immo=PATS, keyway='FO38, HU101', ktype_hint='막대키,스마트키', blade_pn=g('164-R8041[비상키]'),
       src=TP.format('Taurus 2010–2019 DST80 80bit, 2013–2019 Philips Crypto 2 ID46 PCF7953A 스마트키(164-R8092 315MHz 뺌), 82홈 비상키 164-R8041'))]),
 ('파이브 헌드레드', '2005-2007', [
   seg(2005, 2007, chip='ID63(4D63)', immo=PATS, keyway='FO38', ktype_hint='막대키', blade_pn=g('164-R0475'),
       src=TP.format('Five Hundred 2005–2007 Texas Crypto 4D63 DST40, 트랜스폰더 키 Strattec 599114·164-R0475 H84-PT'))]),
 ('퓨전 (북미형)', '2012-2015', [
   seg(2012, 2012, chip=X80, immo=PATS, keyway='FO38, HU101', ktype_hint='막대키',
       src=TP.format('Fusion 2011–2012 North America Texas Crypto 2 DST80 ID63-6F 80bit') + ', 이데일리(2012년형 퓨전 하이브리드 국내 판매)'),
   seg(2013, 2015, chip=X80 + '[일반 키], ID49(NCF2951F)[스마트키]', immo=PATS, keyway='HU101', ktype_hint='폴딩키,스마트키',
       src=TP.format('Fusion 2013–2016 HiTag Pro ID49 NCF2951F 스마트키 DS7T-15K601-CH·CL(315MHz라 뺌)') + ', 탑라이더(2세대 퓨전 2012.12 국내 출시), 나무위키(2015 주력 라인업 제외)')]),
 ('몬데오 (4세대)', '2015-2022', [
   seg(2015, 2022, chip='ID47(PCF7945P)', immo=PATS, keyway='HU101', ktype_hint='폴딩키,스마트키',
       fold=g('DS7T-15K601-BE'), smart=g('DS7T-15K601-CH[키리스]'),
       src=TP.format('Mondeo MK5 2014–2022 Europe Philips Crypto 3 HiTag Pro ID47 PCF7945P, 플립키 DS7T-15K601-BE 433/434MHz, KeyFree 스마트키 DS7T-15K601-CH 434MHz') + ', 이데일리(올 뉴 몬데오 2015.3.23 국내 출시)')]),
 ('머스탱 (5세대)', '2010-2014', [
   seg(2010, 2010, chip='ID63(4D63)', immo=PATS, keyway='FO38', ktype_hint='막대키', blade_pn=TKEY40,
       src=TP.format('Mustang S197 2005–2010 Texas Crypto 4D63 DST40, 트랜스폰더 키 164-R0475·164-R8040 H84-PT — 리모컨 키 164-R8007은 315MHz라 뺌')),
   seg(2011, 2014, chip=X80, immo=PATS, keyway='FO38', ktype_hint='막대키',
       src=TP.format('Mustang S197 2011–2014 Texas Crypto 2 DST80 80bit — 리모컨 키 164-R8067은 315MHz라 뺌'))]),
 ('머스탱 (6세대)', '2015-2023', [
   seg(2015, 2023, chip='ID49', immo=PATS, keyway='HU101', ktype_hint='스마트키', blade_pn=g('164-R7992[비상키]', '164-R8168[비상키]'),
       src=TP.format('Mustang S550 2015–2024 HiTag Pro ID49, 비상키 164-R7992·164-R8168 HU101 — 스마트키 164-R8119·8159·8162·8324는 315·902MHz라 뺌') + ', 전자신문(6세대 머스탱 GT 2015 국내 출시)')]),
 ('머스탱 (7세대)', '2024-현재', [
   seg(2024, 2026, chip='ID49(NCF29A1)', immo=PATS, keyway='HU101', ktype_hint='스마트키',
       smart=g('164-R8347', '164-R8346', 'PR3T-15K601-BA', 'PR3T-15K601-BB'), blade_pn=g('164-R8168[비상키]'),
       src=TP.format('Mustang S650·Dark Horse 2024–2026 HiTag Pro ID49 NCF29A1, 스마트키 164-R8347·164-R8346·PR3T-15K601-BA·BB 434MHz, 비상키 164-R8168') + ', 아주경제(머스탱 2024 국내 출시)')]),
 ('이스케이프', '2001-2012', [
   seg(2001, 2004, chip='ID60(4D60)', immo=PATS, keyway='FO38', ktype_hint='막대키',
       src=TP.format('Escape 2001–2004 Texas Crypto 4D60, FO38') + ', OEM 키 카탈로그(Escape 2001–2004 98AG15K601AA·AB·AC·AD 433MHz — 유럽 공용 리모컨, 국내 적용 미확인), 나무위키(이스케이프 2001년부터 국내 판매)'),
   seg(2005, 2010, chip='ID63(4D63)', immo=PATS, keyway='FO38', ktype_hint='막대키', blade_pn=TKEY40,
       src=TP.format('Escape 2005–2010 Texas Crypto 4D63 DST40, FO38 — 리모컨 키 164-R8007·8070은 315MHz라 뺌, 트랜스폰더 키 164-R0475·164-R8040')),
   seg(2011, 2012, chip=X80, immo=PATS, keyway='FO38', ktype_hint='막대키', blade_pn=g('164-R8073'),
       src=TP.format('Escape 2011–2012 Texas Crypto 2 DST80 80bit, 트랜스폰더 키 Strattec 5912512·164-R8073')),
   seg(2013, 2015, chip=X80 + '[플립키], ID46(PCF7953A)[스마트키]', immo=PATS, keyway='HU101', ktype_hint='폴딩키,스마트키', blade_pn=g('164-R8022[비상키]'),
       src=TP.format('Escape 2013–2019 DST80 80bit 플립키(164-R8046 등 315MHz 뺌), 2013–2018 ID46 PCF7953A 스마트키(164-R8091·8092 315MHz 뺌), 비상키 164-R8022') + ', 나무위키(2015년 말 쿠가로 대체되며 국내 판매 중단)')]),
 ('쿠가', '2013-2018', [
   seg(2015, 2016, chip=X80, immo=PATS, keyway='HU101', ktype_hint='폴딩키,스마트키',
       smart=g('7S7T-15K601-ED', '7S7T-15K601-EE', '7S7T-15K601-EF', '7S7T-15K601-EG'),
       src=TP.format('Kuga MK2 2015–2016 Europe Texas Crypto 2 DST80 ID63-6F 80bit, KeyFree 스마트키 7S7T-15K601-ED·EE·EF·EG 433/434MHz') + ', 이데일리(2015 서울모터쇼 몬데오·쿠가 국내 첫선), 모터그래프(디젤 SUV 쿠가 출시)'),
   seg(2017, 2018, chip='ID47', immo=PATS, keyway='HU101', ktype_hint='폴딩키,스마트키', smart=g('F1ET-15K601-AE', 'F1ET-15K601-AF'),
       src=TP.format('Kuga MK2 Facelift 2016–2019 Europe Philips Crypto 3 HiTag Pro ID47, 스마트키 F1ET-15K601-AE·AF 433/434MHz') + ', 카가이(쿠가 국내 판매 후 단종)')]),
 ('브롱코', '2021-현재', [
   seg(2021, 2024, chip='ID49', immo=PATS, keyway='HU101', ktype_hint='스마트키', blade_pn=g('164-R8168[비상키]'),
       src=TP.format('Bronco 2021–2024 HiTag Pro ID49, 비상키 164-R8168 HU101 — 스마트키 164-R8295·8297·8340은 315·902MHz라 뺌') + ', 탑라이더(브롱코 2021 국내 인증·출시)'),
   seg(2025, 2026, chip='ID49', immo=PATS, keyway='HU101', ktype_hint='스마트키', smart=g('164-R8411', '164-R8412'), blade_pn=g('164-R8168[비상키]'),
       src=TP.format('Bronco 2025 HiTag Pro ID49, 스마트키 164-R8411·164-R8412 434MHz FCC M3N-A3C108397'))]),
 ('익스플로러', '1997-현재', [
   seg(2000, 2000, chip='ID4C', immo=PATS, keyway='FO38', ktype_hint='막대키', blade_pn=g('011-R0221'),
       src=TP.format('Explorer 1998–mid 2001 Texas Fixed 4C, 트랜스폰더 키 011-R0221 H72-PT') + ', 아주경제(익스플로러 1996 국내 첫 출시)'),
   seg(2001, 2001, chip='ID4C', immo=PATS, keyway='FO38', ktype_hint='막대키',
       src=TP.format('Explorer 1998–mid 2001 4C → mid 2001–2003 4D60'),
       split={2001: [dict(chip='ID4C[2001 중반 이전]', blade_pn=g('011-R0221'), flag='orange', note='2001년 중반 4C→4D60 전환 — 정확한 생산 시점 자료 없음'),
                     dict(chip='ID60(4D60)[2001 중반 이후]', blade_pn=g('164-R0475'), flag='orange', note='2001년 중반 4C→4D60 전환 — 정확한 생산 시점 자료 없음')]}),
   seg(2002, 2003, chip='ID60(4D60)', immo=PATS, keyway='FO38', ktype_hint='막대키', blade_pn=g('164-R0475'),
       src=TP.format('Explorer mid 2001–2003 Texas Crypto 4D60, Strattec 599114·5904287·164-R0475 H84-PT')),
   seg(2004, 2010, chip='ID63(4D63)', immo=PATS, keyway='FO38', ktype_hint='막대키', blade_pn=TKEY40,
       src=TP.format('Explorer 2004–2010 Texas Crypto 4D63 DST40, Strattec 599114·5904287·5913441·164-R0475·164-R8040 H84-PT')),
   seg(2011, 2015, chip=X80 + '[일반 키], ID46(PCF7953A)[스마트키]', immo=PATS, keyway='FO38, HU101', ktype_hint='막대키,스마트키', blade_pn=g('164-R8041[비상키]'),
       src=TP.format('Explorer 2011–2015 DST80 ID63-6F 80bit 일반 키(164-R8067 IKT 315MHz 뺌), ID46 PCF7953A PEPS 스마트키(164-R8092 315MHz 뺌), 82홈 비상키 164-R8041')),
   seg(2016, 2017, chip='ID49', immo=PATS, keyway='HU101', ktype_hint='스마트키', blade_pn=g('164-R8168[비상키]'),
       src=TP.format('Explorer 2016–2017 HiTag Pro ID49(스마트키 164-R8141 868MHz, 164-R8150 315MHz 뺌), 2017–2022 비상키 164-R8168 HU101')),
   seg(2018, 2023, chip='ID49(NCF2951F)', immo=PATS, keyway='HU101', ktype_hint='스마트키', smart=g('164-R8151'), blade_pn=g('164-R8168[비상키]'),
       src=TP.format('Explorer 2018–2022 HiTag Pro ID49 NCF2951F, 스마트키 164-R8151 FCC M3N-A2C93142100 434MHz, 비상키 164-R8168') + ', OEM 키 카탈로그(Explorer 2018–2020 HC3T-15K601-DB 434MHz), 6세대 국내 2019 출시'),
   seg(2024, 2026, chip='ID49(NCF2951F)', immo=PATS, keyway='HU101', ktype_hint='스마트키', smart=g('164-R8363', '164-R8369', '164-R8397'), blade_pn=g('164-R8168[비상키]'),
       src=TP.format('Explorer 2024–2025 HiTag Pro ID49, 스마트키 164-R8363·164-R8369·164-R8397 434MHz Gen 5 PEPS') + ', 다나와(더 뉴 익스플로러 2024.11.12 국내 출시)')]),
 ('프리스타일', '2005-2007', [
   seg(2005, 2007, chip='ID63(4D63)', immo=PATS, keyway='FO38', ktype_hint='막대키', blade_pn=g('164-R0475'),
       src=TP.format('Five Hundred 2005–2007·Taurus X 2008–2009 Texas Crypto 4D63 DST40 — 프리스타일은 파이브 헌드레드 왜건형, 트랜스폰더 키 164-R0475'))]),
 ('레인저', '2019-현재', [
   seg(2021, 2022, chip='ID49', immo=PATS, keyway='HU101', ktype_hint='폴딩키', fold=g('EB3T-15K601-BA', 'EB3T-15K601-BB'),
       src=TP.format('Ranger T6 Facelift 2015–2022 Europe·Australia HiTag Pro ID49, 플립키 EB3T-15K601-BA·BB 434MHz FSK') + ', 아주경제(레인저 2021.4.12 국내 첫 출시)'),
   seg(2023, 2026, chip='ID49', immo=PATS, keyway='HU198', ktype_hint='폴딩키,스마트키', fold=g('164-R8337'), smart=g('164-R8406[랩터]'), blade_pn=g('164-R8267[비상키]'),
       src=TP.format('Next-Gen Ranger·Raptor 2023–2025 HiTag Pro ID49, 플립키 164-R8337 434MHz(2025), 랩터 스마트키 164-R8406 434MHz, 센터밀 비상키 164-R8267 HU198') + ', 다나와(신형 레인저 국내 출시)')]),
]

GUIDE = [
 '이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.', '',
 '※ 구성',
 "- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 같고, 맨 앞 '브랜드'와 칩코드 뒤 '키종류'를 추가했습니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다.",
 '- 연식은 실제 국내 판매 기준입니다(아래 목록).',
 '- 포드코리아 판매 차는 대부분 북미형입니다. 북미형 리모컨·스마트키는 315/902MHz라 뺐고, 434MHz 수출형 품번과 유럽형(433/434MHz) 품번만 [해외 공용 품번]으로 적었습니다. 국내 순정 품번은 공개 자료가 없습니다.',
 '- 리모컨이 없는 트랜스폰더 키(164-R0475·164-R8040·164-R8073·011-R0221)와 비상키(164-R8041·164-R8168·164-R7992·164-R8022·164-R8267)는 주파수와 관계없어 키블레이드 칸에 적었습니다.',
 "- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
 '',
 '※ 칩 코드·이모빌라이저(포드)',
 '- ID4C: Texas 고정 4C(~2001)  |  ID60(4D60): Texas Crypto 4D60 40bit  |  ID63(4D63): Texas Crypto 4D63 40bit(2004~2010년경)  |  4D63x80: Texas Crypto 2 DST80 80bit(ID63-6F, 2011년 이후 일반 키·플립키)',
 '- ID46(PCF7952·PCF7953A): Hitag2 스마트키(북미 PEPS 2011~2019, 유럽 KeyFree)  |  ID47(PCF7945P): 유럽 HiTag Pro(몬데오 5세대·쿠가 부분변경)  |  ID49: 북미 HiTag Pro(NCF2951F·NCF29A1, 2015년 이후)',
 '- 이모빌라이저: PATS(Passive Anti-Theft System, 계기판·BCM에 키 등록)',
 '- 키웨이: FO38(북미 구형), HU101(유럽형·스마트키 비상키), HU198(2020년 이후 센터밀 비상키)',
 '',
 '※ 색상',
 '- 주황색: 추정이거나 자료가 서로 다른 값, 칩 전환 시점을 모르는 연식(전·후 2행).',
 '',
 '※ 목록과 국내 판매 연식이 다른 모델',
 '- 이스케이프: 2001년부터 2015년 말까지 국내 판매(목록 2001-2012) → 2001~2015 / 쿠가: 2015 서울모터쇼 국내 첫선 → 2015~2018 / 레인저: 2021.4.12 국내 첫 출시 → 2021~ / 퓨전: 2012년형 하이브리드(1세대)와 2012.12 출시 2세대 → 2012~2015.',
 '- 국내 미출시라 뺀 모델: 익스페디션(목록 1997-2017 — 국내는 2021.3.22 4세대부터 판매, 목록에 4세대 없음), GT 슈퍼카 1·2세대(포드코리아 정식 판매 이력 없음).',
 '- 익스플로러는 1996년 2세대부터 국내 판매 — 2000년식부터 세대별로 기록(2001년 중반 4C→4D60 전환은 2행).',
 '',
 '※ 출처',
 '- transpondery.com Ford Transponder Catalog·Ford OEM Keys & Remotes Catalog, 한국어 위키백과·나무위키, 국내 출시 기사(아주경제·이데일리·탑라이더·다나와 등).',
 '- 연식별 근거는 research/import5/yearly_ford.md에 있습니다.',
]

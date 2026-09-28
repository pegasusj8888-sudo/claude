# 렉서스 — 모델·연식별 키 자료 (research/import5/build.py lexus)
#   근거: transpondery.com Lexus Transponder Catalog(2026-09-26판, 모델·생산기간·시장별 칩/품번/비상키/이모빌라이저),
#         abkeys.com 순정 키 적용표(433MHz 유럽·중동 사양, 모델·연식), mk3.com, 한국어 위키백과·국내 출시 기사(국내 판매 연식)
BRAND = '렉서스'
FILE = '렉서스_models.xlsx'
TITLE = '렉서스 트랜스폰더 DB'

C4C = 'ID4C'
C68 = 'ID68(4D68)'
S40 = 'ID67(TMS37126)'   # 스마트키 DST40(Page1 94/D4)
S80 = 'ID72(TMS37126)'   # 스마트키 DST80 G(Page1 98)
H8A = 'ID8A'             # Texas H(DST-AES 128bit)
I4C = '이모빌라이저 ECU(93C56)'
I4D = '이모빌라이저 ECU(93C66)'
ISK = '스마트키 ECU(93C86)'
KW = 'TOY48[Silca], TOYO-15[JMA]'
KWS = 'TOY48'
G = '[해외 공용 품번]'
def g(*pns): return ', '.join(p + G if '[' not in p else p[:-1] + ', 해외 공용 품번]' for p in pns)

TP = 'transpondery(Lexus {m} {y})'
AB = 'abkeys({t})'
NEVER_NOTE = '국내 정식 판매 이력 없음(병행수입만) — 해외 사양 기준'

ENDED = {'ES (XZ10, 7세대)': False, 'LS (XF50, 5세대)': False, 'LC (LC500/500h)': False, 'UX (UX200/250h/300e)': False,
         'NX (AZ20, 2세대)': False, 'RZ (전기차)': False, 'RX (XU60, 5세대)': False, 'LX (J300, 4세대)': False, 'LM (LM300h)': False}

def seg(y0, y1, **k):
    k['y'] = (y0, y1); return k

MODELS = [
 ('CT (CT200h)', '2011-2021', [
   seg(2011, 2020, chip=S80, immo='스마트키 ECU', keyway=KWS, ktype_hint='스마트키', smart=g('89904-48521'), blade_pn=g('69515-50260'),
       src='transpondery(CT 200h 2011–2020 Europe/ME B74EA 433MHz 89904-48521, Texas G DST80 Page1 98), abkeys(89904-48521 CT200h 2011-2014), 국내 2011.3 출시'),
   seg(2021, 2021, chip=S80, immo='스마트키 ECU', keyway=KWS, ktype_hint='스마트키', smart=g('89904-48521'), blade_pn=g('69515-50260'),
       src='transpondery(CT 200h 2011–2020 Europe/ME), 위키백과(2020~2021년 사이 국내 판매 중단)', flag='orange',
       note='국내 판매 종료 시점 자료 상충(2020~2021) — 2021년식 존재 여부 확인 필요')]),
 ('IS (1세대, XE10)', '2001-2005', [
   seg(2001, 2005, chip=C4C, immo=I4C, keyway=KW, ktype_hint='막대키', blade_pn=g('89070-53010[리모컨키]'),
       src='transpondery(IS 200 1999–2005 Texas 4C, 리모컨키 89070-53010 433MHz, DENSO 93C56), 위키백과(국내 2001년부터 IS200 4도어만 판매)')]),
 ('IS (2세대, XE20)', '2005-2013', [
   seg(2005, 2008, chip=S40, immo=ISK, keyway=KWS, ktype_hint='스마트키', smart=g('89904-30320', '89904-30322'), blade_pn=g('69515-30300', '69515-50260'),
       src='transpondery(IS 250 2005–2008 TMS37126 DST40 Page1 94, 비상키 69515-30300·50260), abkeys(89904-30320·30322 ES GS IS LS 2006+ 433MHz P1 D4), 위키백과(국내 V6 2.5만)'),
   seg(2009, 2013, chip=S80, immo=ISK, keyway=KWS, ktype_hint='스마트키,카드키', smart=g('89904-53361', '89904-53321', '89904-53322'),
       card=g('89904-50480', '89904-50481', '89904-53131'), blade_pn=g('69515-50260'),
       src='transpondery(IS 2009–2013 Texas G DST80, 카드키 블랭크 69515-50270→69515-30350), abkeys(순정 89904-53361 433MHz P1 98 IS250 2007-2013 유럽·중동), auto-keys.eu(순정 89904-53321·53322 433MHz P1 98, IS250·350 스마트 카드 89904-53131·50480·50481 433MHz)')]),
 ('IS (3세대, XE30)', '2013-2021', [
   seg(2013, 2019, chip=H8A, immo='스마트키 ECU(TMLF12-1)', keyway=KWS, ktype_hint='스마트키', smart=g('89904-53831'), blade_pn=g('69515-30380'),
       src='transpondery(IS 2014–2020 Texas H-8A DST-AES Page1 A8, 비상키 69515-30380, TMLF12-1), abkeys(순정 89904-53831 433MHz BG1EK IS 2014-2019)'),
   seg(2020, 2021, chip=H8A, immo='스마트키 ECU(TMLF12-1)', keyway=KWS, ktype_hint='스마트키', smart=g('89904-53F40'), blade_pn=g('69515-30380'),
       src='transpondery(IS 2021–2025 H-8A Page1 A9), abkeys(89904-53F40 IS 2018-2024 433MHz), 시사위크·다나와(국내 IS 2021.9.1 판매 중단)')]),
 ('ES (XV20, 3세대)', '2001-2003', [
   seg(2001, 2003, chip=C4C, immo=I4C, keyway=KW, ktype_hint='막대키',
       src='transpondery(ES 300 1998–2001·2002–2003 Texas 4C, DENSO 93C56 — 리모컨키 89070-33070·33150은 미국형 315MHz라 뺌), 위키백과(국내 2001년 렉서스 출시부터 ES 판매)')]),
 ('ES (XV30, 4세대)', '2003-2006', [
   seg(2003, 2006, chip=C68, immo=I4D, keyway=KW, ktype_hint='막대키',
       src='transpondery(ES 330 2004–2006 Texas Crypto 4D-68 DST40, DENSO 93C66 — 리모컨키 89070-33300·33310은 미국형이라 뺌)')]),
 ('ES (XV40, 5세대)', '2006-2012', [
   seg(2006, 2008, chip=S40, immo=ISK, keyway=KWS, ktype_hint='스마트키', smart=g('89904-30320', '89904-30322'), blade_pn=g('69515-30300'),
       src='transpondery(ES 350 2007–2009 TMS37126 DST40, 89904-30270은 2006.3~2008.8 생산 북미형), abkeys(89904-30320·30322 ES350 2006-2010 433MHz P1 D4)'),
   seg(2009, 2012, chip=S80, immo=ISK, keyway=KWS, ktype_hint='스마트키', smart=g('89904-53361'), blade_pn=g('69515-30300'),
       src='transpondery(ES 350 2010–2012 Texas G DST80, 2008.8 이후 생산 89904-50380 계열), abkeys(순정 89904-53361 ES350 2009-2011 433MHz P1 98)')]),
 ('ES (XV60, 6세대)', '2012-2018', [
   seg(2012, 2018, chip=H8A, immo='스마트키 ECU', keyway=KWS, ktype_hint='스마트키',
       smart=g('89904-30J50', '89904-30C80', '89904-30K00', '89904-30D20', '89904-30B50[3버튼]'), blade_pn=g('69515-30380'),
       src='transpondery(ES 2013–2018 Europe/ME 433MHz H-8A Page1 88, 89904-30J50 BC4EK·30B50 BC2EQ, 비상키 69515-30380), abkeys(순정 89904-30J50 2013-2018, 30C80 2013-2014, 30K00·30D20 BC4EQ 2013-2017)')]),
 ('ES (XZ10, 7세대)', '2018-현재', [
   seg(2018, 2023, chip=H8A, immo='스마트키 ECU(TMLF15-1)', keyway=KWS, ktype_hint='스마트키',
       smart=g('8990H-33070', '8990H-33080', '8990H-33090'), blade_pn=g('69515-33150'),
       src='transpondery(ES 2019–2023 433MHz B2C2K2R 8990H-33080·33090 계열, 8A-B9, TMLF15-1), abkeys(순정 8990H-33070 2018-2020, 8990H-33080 2019-2021, 8990H-33090 2019-2023), 국내 2018.10.2 출시'),
   seg(2024, 2026, chip=H8A, immo='스마트키 ECU(TMLF15-1)', keyway=KWS, ktype_hint='스마트키', blade_pn=g('69515-33150'),
       src='transpondery(ES 250·300h·350 2020–2025 H-8A 8A-B9, 비상키 69515-33150 — 2024년 이후 433MHz 품번 자료 없음)')]),
 ('GS (1세대, JZS16)', '2001-2005', [
   seg(2001, 2005, chip=C4C, immo=I4C, keyway=KW, ktype_hint='막대키',
       src='transpondery(GS 300 1998–2005·GS 430 2001–2005 Texas 4C, DENSO 93C56 — 리모컨키 89070-30040·30070은 미국형이라 뺌), 위키백과(국내 2001년부터 GS300 공식 판매)')]),
 ('GS (2세대, S190)', '2005-2012', [
   seg(2005, 2008, chip=S40, immo=ISK, keyway=KWS, ktype_hint='스마트키', smart=g('89904-30320', '89904-30322'), blade_pn=g('69515-30300', '69515-50260'),
       src='transpondery(GS 2006–2009 TMS37126 DST40 Page1 94, DENSO 스마트키 ECU 93C86), abkeys(89904-30320·30322 GS300·GS430·GS460 2006-2012 433MHz P1 D4)'),
   seg(2009, 2012, chip=S80, immo=ISK, keyway=KWS, ktype_hint='스마트키', smart=g('89904-53361'), blade_pn=g('69515-50260'),
       src='transpondery(GS 350·450h·460 2009–2011 Texas G DST80), abkeys(순정 89904-53361 GS430·GS460 2008-2011 433MHz P1 98)')]),
 ('GS (3세대, L10)', '2012-2020', [
   seg(2012, 2020, chip=H8A, immo='스마트키 ECU(TMLF10-3)', keyway=KWS, ktype_hint='스마트키',
       smart=g('89904-30J50', '89904-30C80', '89904-30B50[3버튼]'), blade_pn=g('69515-30380'),
       src='transpondery(GS 2013–2018 H-8A Page1 88·A8, GS 300h·450h 유럽 H-8A, TMLF10-3, 비상키 69515-30380), abkeys(순정 89904-30J50 GS350 2013-2018 433MHz), 위키백과(2020.9 단종)')]),
 ('LS (XF20/XF30, 2~3세대)', '2001-2006', [
   seg(2001, 2003, chip=C68, immo=I4D, keyway=KW, ktype_hint='막대키',
       src='transpondery(LS 430 2001–2006 Texas Crypto 4D-68 DST40, DENSO 93C66), 카이즈유(LS430 2001.1 국내 출시)'),
   seg(2004, 2006, chip=C68, immo=I4D, keyway=KW, ktype_hint='막대키,스마트키', smart=g('89994-50260'),
       src='transpondery(LS 430 2001–2006 4D-68, 스마트키 89994-50240·50241 계열), abkeys(순정 89994-50260 LS430 2004-2006 433MHz 12BZF P1 B0)')]),
 ('LS (XF40, 4세대)', '2006-2017', [
   seg(2006, 2008, chip=S40, immo=ISK, keyway=KWS, ktype_hint='스마트키', smart=g('89904-30322', '89904-30323', '89904-50561'), blade_pn=g('69515-50260'),
       src='transpondery(LS 460 2007–2008 TMS37126 DST40 Page1 94, 비상키 69515-50260), auto-keys.eu(순정 89904-30322·30323 433MHz ES350·GS·IS·LS460, LS460 2008 89904-50561 433MHz Tiris 4D)'),
   seg(2009, 2012, chip=S80, immo=ISK, keyway=KWS, ktype_hint='스마트키', smart=g('89904-50L00', '89904-50L01'), blade_pn=g('69515-50260'),
       src='transpondery(LS 460·600h 2009–2012 Texas G DST80), auto-keys.eu(순정 LS 460 89904-50L00·50L01 433MHz P1 98)'),
   seg(2013, 2017, chip=S80, immo=ISK, keyway=KWS, ktype_hint='스마트키', smart=g('89904-50L00', '89904-50L01'), blade_pn=g('69515-30380'),
       src='transpondery(LS 460·600h 2013–2017 Texas G DST80, 비상키 69515-30380), auto-keys.eu(LS 460 89904-50L00·50L01 433MHz P1 98)')]),
 ('LS (XF50, 5세대)', '2017-현재', [
   seg(2017, 2026, chip=H8A, immo='스마트키 ECU(TMLF15-1)', keyway=KWS, ktype_hint='스마트키,카드키', smart=g('8990H-50120'), blade_pn=g('69515-50310'),
       src='transpondery(LS 500·500h 2018–2026 H-8A, 카드키 적용, 비상키 69515-50310, TMLF15-1), abkeys(순정 8990H-50120 LS350·LS500 2018-2020 433MHz 14FCB), 위키백과(국내 2017.12.24 출시)')]),
 ('SC (SC430)', '2001-2010', [
   seg(2001, 2010, chip=C68, immo=I4D, keyway=KW, ktype_hint='막대키',
       src='transpondery(SC 430 2001–2010 Texas Crypto 4D-68, DENSO 93C66 — 리모컨키 89070-24120·24140은 미국형이라 뺌), 위키백과(2010 단종)')]),
 ('RC / RC F', '2015-2022', [
   seg(2015, 2019, chip=H8A, immo='스마트키 ECU(TMLF12-4)', keyway=KWS, ktype_hint='스마트키', smart=g('89904-53831'), blade_pn=g('69515-30380'),
       src='transpondery(RC 350·RC F 2015–2020 H-8A Page1 A8, TMLF12-4, 비상키 69515-30380), abkeys(순정 89904-53831 RC350 2014-2019 433MHz), 서울모터쇼(2015.4 국내 출시)'),
   seg(2020, 2022, chip=H8A, immo='스마트키 ECU(TMLF12-4)', keyway=KWS, ktype_hint='스마트키', blade_pn=g('69515-30380'),
       src='transpondery(RC 300·350 2021–2026 H-8A Page1 A9, RC F 2020–2024 A9 — 433MHz 품번 자료 없음)')]),
 ('LC (LC500/500h)', '2017-현재', [
   seg(2017, 2026, chip=H8A, immo='스마트키 ECU(TMLF15-1)', keyway=KWS, ktype_hint='스마트키', blade_pn=g('69515-11020'),
       src='transpondery(LC 500·500h 2018–2026 H-8A, 비상키 69515-11020, TMLF15-1 — 433MHz 품번 자료 없음), 한국일보(LC500 2017.7.4 국내 출시)')]),
 ('UX (UX200/250h/300e)', '2018-현재', [
   seg(2019, 2021, chip=H8A, immo='스마트키 ECU(TMLF15-1)', keyway=KWS, ktype_hint='스마트키', smart=g('8990H-76360', '8990H-76350[3버튼]'), blade_pn=g('69515-33150'),
       src='transpondery(UX 2019–2022 H-8A, 비상키 69515-33150, TMLF15-1), abkeys(순정 8990H-76360·76350 UX 2019-2021 433MHz B2C2K2R), ZDNet(UX250h 2019.3.28 국내 출시)'),
   seg(2022, 2026, chip=H8A, immo='스마트키 ECU(TMLF15-1)', keyway=KWS, ktype_hint='스마트키', blade_pn=g('69515-33150'),
       src='transpondery(UX 250h 2023–2026 H-8A 8A-B9 — 433MHz 품번 자료 없음)')]),
 ('NX (AZ10, 1세대)', '2014-2021', [
   seg(2014, 2021, chip=H8A, immo='스마트키 ECU(TMLF12-3)', keyway=KWS, ktype_hint='스마트키',
       smart=g('89904-78590', '89904-78591', '89904-78790', '89904-78791', '89904-78780[2버튼]'), blade_pn=g('69515-30380'),
       src='transpondery(NX 200t·300h 2015–2021 H-8A Page1 A8, 유럽 433MHz 89904-78590·78591·78790·78791 BG1EW, TMLF12-3), abkeys(순정 89904-78780 NX 2015-2019), 위키백과(국내 2.0 터보·2.5 하이브리드 판매)')]),
 ('NX (AZ20, 2세대)', '2021-현재', [
   seg(2022, 2022, chip=H8A, immo='스마트키 ECU(TMLF19D-2)', keyway=KWS, ktype_hint='스마트키,카드키', blade_pn=g('69515-33150'),
       src='transpondery(NX 350h·450h+ 2022–2026 H-8A 8A-B9, 카드키, TMLF19D-2, 비상키 69515-33150), 탑라이더·다나와(국내 2022.6.15 출시)'),
   seg(2023, 2026, chip=H8A, immo='스마트키 ECU(TMLF19D-2)', keyway=KWS, ktype_hint='스마트키,카드키', smart='8990H-48190[추정], ' + g('8990H-78231'), blade_pn=g('69515-33150'),
       src='transpondery(NX 2023 적용 8990H-48190 — RZ에서 한국 사양 품번으로 표기, 433~434MHz 시장별), abkeys(순정 8990H-78231 NX 2023-2024 433MHz)')]),
 ('RZ (전기차)', '2023-2024', [
   seg(2023, 2026, chip=H8A, immo='스마트키 ECU(TMLF19D)', keyway=KWS, ktype_hint='스마트키,카드키', smart='8990H-48190', blade_pn=g('69515-33150'),
       src='transpondery(RZ 450e 2023–2026 H-8A 8A-B9, Korea-spec application 8990H-48190, 카드키, 비상키 69515-33150), 이어카·렉서스코리아(RZ 450e 2023.5 국내 출시, 현재 판매)')]),
 ('RX (XU10, 1세대)', '2001-2003', [
   seg(2001, 2003, chip=C4C, immo=I4C, keyway=KW, ktype_hint='막대키',
       src='transpondery(RX 300 1999–2003 Texas 4C, DENSO 93C56 — 리모컨키 89070-48020·48041은 미국형이라 뺌), 위키백과(2001 국내 출시)')]),
 ('RX (XU30, 2세대)', '2003-2008', [
   seg(2003, 2008, chip=C68, immo=I4D, keyway=KW, ktype_hint='막대키',
       src='transpondery(RX 300 2004–2006·RX 330 2004–2006·RX 350 2007–2009·RX 400h 2006–2009 Texas Crypto 4D-68, DENSO 93C66)')]),
 ('RX (XU30 2차, 3세대)', '2008-2015', [
   seg(2009, 2015, chip=S80, immo=ISK, keyway=KWS, ktype_hint='스마트키', smart=g('89904-48242', '89904-48243', '89904-48244', '89904-48245', '89904-48521'), blade_pn=g('69515-30300', '69515-50260'),
       src='transpondery(RX 350·450h 2010–2015 Texas G DST80, 비상키 69515-30300·50260), abkeys(순정 89904-48242·48243 RX350 2008-2011 433MHz B74EA P1 98, 89904-48521 RX 2009-2012), 3세대 2009 출시')]),
 ('RX (XU40, 4세대)', '2015-2022', [
   seg(2016, 2019, chip=H8A, immo='스마트키 ECU(TMLF15-2)', keyway=KWS, ktype_hint='스마트키',
       smart=g('89904-48E20', '89904-48J60', '89904-48L01[3버튼]', '89904-48J50[3버튼]'), blade_pn=g('69515-30380'),
       src='transpondery(RX 2016–2019 H-8A Page1 A8, TMLF15-2, 비상키 69515-30380), abkeys(순정 89904-48E20·48J60 RX 2016-2019 433MHz BP1EK, 89904-48L01·48J50 2016-2020 BP1EW), ZDNet(4세대 2016.2 국내 출시)'),
   seg(2020, 2022, chip=H8A, immo='스마트키 ECU(TMLF15-2)', keyway=KWS, ktype_hint='스마트키', smart=g('89904-48J81', '89904-48L01[3버튼]'), blade_pn=g('69515-30380'),
       src='transpondery(RX 2020–2022 H-8A Page1 A9), mk3(순정 RX350 2020 433MHz 89904-48J81), 위키백과(RX450hL 2020.3 국내 출시)')]),
 ('RX (XU60, 5세대)', '2022-현재', [
   seg(2023, 2026, chip=H8A, immo='스마트키 ECU(TMLF19D)', keyway=KWS, ktype_hint='스마트키', smart='8990H-48190[추정]', blade_pn=g('69515-33150'),
       src='transpondery(RX 350h·450h+·500h 2023–2026 H-8A 8A-B9, 추가 적용 8990H-48190, 433~434MHz 시장별, TMLF19D, 비상키 69515-33150), 국내 2023.6.21 출시')]),
 ('LX (J200, 3세대)', '2016-2021', [
   seg(2016, 2019, chip=H8A, immo='스마트키 ECU', keyway=KWS, ktype_hint='스마트키',
       smart=g('89904-78591', '89904-78650', '89904-78640[3버튼]', '89904-78J00[3버튼]'),
       src='transpondery(LX 570 2016–2019 H-8A Page1 A8), abkeys(순정 89904-78591·78650 LX570 2016-2018 433MHz, 78640 2015-2019, 78J00 2016-2018), 다음·카톡(LX570 국내 정식 수입 없음)',
       flag='orange', note=NEVER_NOTE),
   seg(2020, 2021, chip=H8A, immo='스마트키 ECU', keyway=KWS, ktype_hint='스마트키',
       src='transpondery(LX 570 2020–2021 H-8A Page1 A9 — 433MHz 품번 자료 없음), LX 국내 정식 판매는 2025 LX700h부터',
       flag='orange', note=NEVER_NOTE)]),
 ('LX (J300, 4세대)', '2022-현재', [
   seg(2025, 2026, chip=H8A, immo='스마트키 ECU', keyway=KWS, ktype_hint='스마트키,카드키', smart=g('8990H-78150'), blade_pn=g('69515-33150'),
       src='transpondery(LX 600 2022–2025 H-8A 8A-BA, 카드키, 비상키 69515-33150, LX 700h 2025–2026 8A-B6), abkeys(순정 8990H-78150 LX600 2022-2024 433MHz), 위키백과(LX700h 2025.3.17 국내 출시)')]),
 ('LM (LM300h)', '2023-현재', [
   seg(2024, 2026, chip=H8A, immo='스마트키 ECU', keyway=KWS, ktype_hint='스마트키', smart=g('89904-58740', '89904-58750'),
       src='transpondery(LM 350h·500h 2024–2026 H-8A 8A-BA·B9, 89904-58740·58750 계열), 모터그래프·오토뷰(국내는 LM 500h 2024.7.24 출시, LM300h 미판매)')]),
]

GUIDE = [
 '이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.', '',
 '※ 구성',
 "- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 같고, 맨 앞 '브랜드'와 칩코드 뒤 '키종류'를 추가했습니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다.",
 "- 연식은 실제 국내 판매 기준입니다(렉서스 국내 출시는 2001년). 원본 목록 연식과 국내 판매가 다른 모델은 국내 기준으로 바꿨습니다(아래 목록).",
 "- 키 부품번호는 국내 사양(433/434MHz)만 적었습니다. 미국형(315MHz, FCC HYQ14AAB·HYQ14FBA·HYQ14FBF 등)과 일본형(312/314MHz) 품번은 뺐습니다.",
 "- 433MHz 품번은 대부분 유럽·중동 사양으로 확인된 순정 품번이라 [해외 공용 품번]으로 표시했습니다. RZ의 8990H-48190은 카탈로그에 한국 사양 품번으로 적혀 있어 태그 없이 적었고, 같은 번호가 NX 2세대·RX 5세대에도 적용 품번으로 나와 [추정]으로 적었습니다.",
 "- 비상키(키블레이드) 품번 69515-xxxxx는 기계식 비상키 블레이드입니다. 리모컨 일체형 막대키(구형)는 키블레이드 칸에 [리모컨키]로 적었습니다.",
 "- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
 '',
 '※ 칩 코드(렉서스·토요타)',
 '- ID4C: Texas 4C 고정 코드(2001~2003년경 IS200·GS300·ES300·RX300)  |  ID68(4D68): Texas Crypto 4D-68 40bit(LS430·SC430·ES330·RX330·RX350 2세대)',
 '- ID67(TMS37126): 스마트키 DST40(Page1 94·D4, 2006~2008년경)  |  ID72(TMS37126): 스마트키 Texas G DST80(Page1 98, 2009~2012년경·CT·RX 3세대)',
 '- ID8A: Texas H DST-AES 128bit(2013년 이후 전 차종, Page1 88·A8·A9·AA·B9·BA)',
 '- 이모빌라이저: DENSO 이모빌라이저 ECU(EEPROM 93C56=4C, 93C66=4D) → DENSO 스마트키 ECU(93C86) → TOKAI RIKA 스마트키 ECU(TMLF10·12·15·19 계열)',
 '- 키웨이: 렉서스 전 차종 TOY48(Silca, JMA TOYO-15) 계열, 스마트키는 비상키 블레이드',
 '',
 '※ 색상',
 '- 주황색: 추정이거나 자료가 서로 다른 값, 또는 국내 정식 판매 이력이 없는 모델(해외 사양 기준) — 실물 키로 재확인.',
 '- 빨간색: 확인 불가.',
 '',
 '※ 목록과 국내 판매 연식이 다른 모델',
 '- UX: 2019.3.28 국내 출시(UX250h) → 2019~ / NX 2세대: 2022.6.15 국내 출시 → 2022~ / RX 4세대: 2016.2 국내 출시 → 2016~2022 / RX 5세대: 2023.6.21 → 2023~ / RX 3세대: 2009 → 2009~2015.',
 '- LX 4세대: 국내 정식 출시는 LX 700h 2025.3.17 → 2025~ / LX 3세대(LX570): 국내 정식 수입 없음(병행수입만) — 목록 연식대로 남기고 주황색.',
 '- LM: 국내는 LM 500h(2세대) 2024.7.24 출시, LM300h는 미판매 → 2024~ / RZ: 2023.5 출시 후 계속 판매 → 2023~2026 / IS 3세대: 2021.9.1 국내 판매 중단.',
 '',
 '※ 출처',
 '- transpondery.com Lexus Transponder Catalog(모델·생산기간·시장별 칩·품번·비상키·이모빌라이저), abkeys.com 순정 키 적용표(모델·연식·시장), mk3.com, 한국어 위키백과, 국내 출시 기사(ZDNet·이투데이·한국일보·모터그래프 등).',
 '- 연식별 근거는 research/import5/yearly_lexus.md에 있습니다.',
]

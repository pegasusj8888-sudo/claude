# 지프 — 모델·연식별 키 자료 (research/import5/build.py jeep)
#   근거: transpondery.com Jeep Transponder Catalog(2026-09-12판, 모델·생산기간별 칩·이모빌라이저·OEM 키·키 블랭크),
#         abkeys.com 순정 키(품번별 주파수·적용 연식), 한국어 위키백과·국내 출시 기사(국내 판매 연식)
BRAND = '지프'
FILE = '지프_models.xlsx'
TITLE = '지프 트랜스폰더 DB'

G = '[해외 공용 품번]'
def g(*pns): return ', '.join(p + G if '[' not in p else p[:-1] + ', 해외 공용 품번]' for p in pns)

ENDED = {m: False for m in ('어벤저 (전기차)', '그랜드 체로키 (WL, 5세대)', '랭글러 (JL, 4세대)', '글래디에이터')}

def seg(y0, y1, **k):
    k['y'] = (y0, y1); return k

TP = 'transpondery(Jeep Catalog {})'
AB = 'abkeys({})'
C64 = dict(chip='ID64(4D64)', immo='SKIM', keyway='Y160', ktype_hint='막대키')
C46 = dict(chip='ID46(PCF7936)', immo='SKREEM, WCM', keyway='Y164, CY24', ktype_hint='막대키')
RHK = g('68001703AA[리모컨키]', '68001703AC[리모컨키]')          # 2008~2014 유럽·중동 433MHz 리모컨 일체형 키(CY22)
RHK_SRC = AB.format('순정 Wrangler·Compass·Patriot 2008-2014 리모컨 일체형 키 68001703AA·AC 433MHz 유럽·중동 — 미국형 68039414AA·68001702AA·68000603AA는 315MHz라 뺌')
FOBIK = g('05026309AD', '68066848AD', '05026347AC', '05026346AD')  # 2008~2013 FOBIK 433MHz(M3N5WY783X)
FOBIK_SRC = AB.format('순정 Grand Cherokee·Commander 2008-2013 FOBIK 05026309AD·68066848AD·05026347AC·05026346AD 433MHz FCC M3N5WY783X')
JL = dict(chip='ID4A(NCF29A1X)', immo='SGW, RF Hub', keyway='SIP22', ktype_hint='스마트키',
          smart=g('68416782AA', '68416784AA', '68416786AB'))
JL_SRC = AB.format('순정 Wrangler 2018-2025·Gladiator 2019-2025 스마트키 68416782AA·68416784AA·68416786AB 433MHz FCC OHT1130261')

MODELS = [
 ('레니게이드', '2015-2025', [
   seg(2015, 2025, chip='ID88[일반 키], ID4A(PCF7953M)[스마트키]', immo='BCM', keyway='SIP22', ktype_hint='폴딩키,스마트키',
       smart=g('735657572', '735657526', '6BY88DX9AA', '6MP33DX9AA'),
       src=TP.format('Renegade BU 2015–2023 Megamos AES ID88 폴딩키, Hitag AES ID4A PCF7953M 스마트키, Magneti Marelli BCM, SIP22')
           + ', ' + AB.format('순정 Renegade 2015-2022 스마트키 735657572·735657526·6BY88DX9AA 433MHz FCC M3N-40821302')
           + ', 위키백과(레니게이드 2015.9.10 국내 출시), 목록(2025 단종)')]),
 ('어벤저 (전기차)', '2024-현재', [
   seg(2024, 2026, chip='ID4A', keyway='SIP22', ktype_hint='스마트키', smart=g('9842943280', '1683930880'),
       src=TP.format('Avenger 2023–2026 Stellantis CMP·STLA Small Hitag AES ID4A, 스마트키 9842943280·1683930880 433.92MHz, SIP22')
           + ', 스텔란티스 코리아 보도자료(어벤저 2024.9.4 국내 공식 출시 — 아시아 첫 출시)')]),
 ('컴패스 (MK49, 1세대)', '2011-현재', [
   seg(2007, 2007, **C46,
       src=TP.format('Compass MK49 2007–2017 ID46 PCF7936 리모컨 일체형 키, WCM·TIPM, CY24·Y164') + ', 위키백과(컴패스 2007년부터 국내 수입)'),
   seg(2008, 2014, **C46, blade_pn=RHK,
       src=TP.format('Compass MK49 2007–2017 ID46 PCF7936, WCM') + ', ' + RHK_SRC + ', 다나와(2011 부분변경 국내 판매)'),
   seg(2015, 2016, **C46,
       src=TP.format('Compass MK49 2007–2017 ID46 PCF7936, WCM') + ' — 1세대 국내 판매 종료 시점 자료 없음(2세대 2018.7 출시)')]),
 ('컴패스 (MP, 2세대)', '2011-현재', [
   seg(2018, 2023, chip='ID4A(PCF7953M)', immo='BCM, RF Hub', keyway='SIP22', ktype_hint='스마트키',
       smart=g('68250343AB', '68250344AB', '68250344AA', '68250346AB', '68250350AB', '68250352AB', '68250337AB', '68417820AA', '68250335AB'),
       src=TP.format('Compass MP 2017–2026 Hitag AES ID4A PCF7953M·NCF29A1, Magneti Marelli BCM·RF Hub, SIP22')
           + ', ' + AB.format('순정 Compass 2017-2025 스마트키 68250343AB·68250344AB·68250346AB·68250350AB·68250352AB·68250337AB·68417820AA·68250335AB 433MHz FCC M3N-40821302')
           + ', 위키백과(2세대 2018.7.17 국내 출시), 시사위크·모터그래프(2023.4 체로키·컴패스 국내 판매 중단)')]),
 ('체로키 (XJ, 2세대)', '1993-2001', [
   seg(2000, 2001, **C64,
       src=TP.format('Cherokee XJ 1998–2001 Texas Crypto 4D64, SKIM, Y160-PT') + ', 위키백과(XJ 1992~2002 국내 판매)')]),
 ('체로키 (KJ, 3세대, 리버티)', '2002-2007', [
   seg(2002, 2004, **C64,
       src=TP.format('Cherokee·Liberty KJ 2002–2004 Texas Crypto 4D64, SKIM·JTEC PCM, Y160-PT') + ', 위키백과(KJ 2002~2007 국내 판매)'),
   seg(2005, 2007, **C46,
       src=TP.format('Cherokee·Liberty KJ 2005–2007 ID46 PCF7936 리모컨 일체형 키, SKREEM(WCM), Y164·CY24')
           + ' — 리모컨 키 05179514AA·05189230AA는 315MHz라 뺌')]),
 ('체로키 (KL, 5세대)', '2014-2023', [
   seg(2014, 2023, chip='ID4A(PCF7953)', immo='RF Hub', keyway='SIP22', ktype_hint='스마트키',
       smart=g('68105078AE', '68105078AC', '68105087AG', '68141582AB', '68159222AG', '68141580AF', '68141580AD', '68105081AF[FOBIK]', '68105083AF[FOBIK]'),
       src=TP.format('Cherokee KL 2014–2023 Hitag AES ID4A PCF7953, Continental RF Hub, SIP22')
           + ', ' + AB.format('순정 Cherokee 2014-2022 스마트키 68105078AE·AC·68105087AG·68141582AB·68159222AG·68141580AF·AD 433MHz FCC GQ4-54T, FOBIK 68105081AF·68105083AF 433MHz FCC GQ4-53T — 68105107AG는 315MHz라 뺌')
           + ', 위키백과(KL 2014.9 국내 출시), 시사위크(2023.4 국내 판매 중단)')]),
 ('커맨더 (XK)', '2023-현재', [
   seg(2006, 2007, chip='ID46(PCF7936)', immo='SKREEM, WCM', keyway='Y164, CY24', ktype_hint='막대키',
       src=TP.format('Commander XK 2006–2007 ID46 PCF7936 리모컨 일체형 키, SKREEM·WCM — 05175786AA·05183349AA는 315MHz라 뺌')
           + ', 나무위키·랭크스(다임러크라이슬러코리아 2006.5 부산모터쇼 국내 출시)'),
   seg(2008, 2010, chip='ID46(PCF7941)', immo='WIN', keyway='Y159, CY24', ktype_hint='스마트키', smart=FOBIK,
       src=TP.format('Commander XK 2008–2010 ID46 PCF7941 FOBIK, WIN(TIPM), 비상키 Y159·CY24') + ', ' + FOBIK_SRC)]),
 ('그랜드 체로키 (WJ, 2세대)', '1999-2005', [
   seg(2000, 2004, **C64,
       src=TP.format('Grand Cherokee WJ 1999–2004 Texas Crypto 4D64, SKIM·JTEC PCM, Y160-PT') + ', 위키백과(WJ 1999.5 국내 수입, WK 2005 국내 수입)')]),
 ('그랜드 체로키 (WK, 3세대)', '2005-2010', [
   seg(2005, 2007, **C46,
       src=TP.format('Grand Cherokee WK 2005–2007 ID46 PCF7936 리모컨 일체형 키, SKREEM·WCM, CY24·Y164')
           + ', ' + AB.format('순정 Grand Cherokee 2005-2008 리모컨 일체형 키 433MHz KOBDT04A — 품번 미표기, 05183349AA는 315MHz라 뺌')
           + ', 위키백과(WK 2005 국내 정식 수입)'),
   seg(2008, 2010, chip='ID46(PCF7941)', immo='WIN', keyway='Y159, CY24', ktype_hint='스마트키', smart=FOBIK,
       src=TP.format('Grand Cherokee WK 2008–2013 ID46 PCF7941 FOBIK, WIN(TIPM), 비상키 Y159·CY24') + ', ' + FOBIK_SRC)]),
 ('그랜드 체로키 (WK2, 4세대)', '2010-2021', [
   seg(2010, 2013, chip='ID46(PCF7953)', immo='RF Hub', keyway='Y170, Y159', ktype_hint='스마트키',
       smart=g('56046733AD', '56046733AE', '56046735AE', '56046736AA', '68051664AB', '68051664AE', '68051665AC', '68051665AE', '68051666AF', '05026453AG'),
       src=AB.format('순정 Grand Cherokee 2011-2014 키리스 고 스마트키 56046733AD·AE·56046735AE·56046736AA·68051664AB·AE·68051665AC·AE·68051666AF·05026453AG 433MHz FCC IYZ-C01C')
           + ', transpondery(Jeep·Chrysler IYZ-C01C Hitag2 PCF7953 FOBIK형 스마트키 — WK2 전기형은 카탈로그 미기재), locksmithkeyless·UHS(2011-2013 Grand Cherokee IYZ-C01C 비상키 Y170·Y159), 위키백과(WK2 2010.10.12 국내 출시)'),
   seg(2014, 2021, chip='ID4A(PCF7953)', immo='RF Hub', keyway='SIP22', ktype_hint='스마트키',
       smart=g('68143502AC', '68143504AC', '68143505AB', '68143506AC'),
       src=TP.format('Grand Cherokee WK2 2014–2021 Hitag AES ID4A PCF7953·NCF2953, Continental RF Hub, SIP22')
           + ', ' + AB.format('순정 Grand Cherokee 2014-2021 스마트키 68143502AC·68143504AC·68143505AB·68143506AC 433MHz FCC M3N-40821302'))]),
 ('그랜드 체로키 (WL, 5세대)', '2021-현재', [
   seg(2021, 2026, chip='ID4A', immo='SGW, RF Hub', keyway='SIP22', ktype_hint='스마트키', smart=g('68377534AB', '68425092AA'),
       src=TP.format('Grand Cherokee·Grand Cherokee L WL 2022–2026 Hitag AES ID4A UWB 스마트키, SGW·Continental RF Hub, SIP22')
           + ', ' + AB.format('순정 Wagoneer 2021-2024·Grand Cherokee 2022-2024 스마트키 68377534AB·68425092AA 433MHz FCC M3NWXFOB1')
           + ', 위키백과(WL 롱바디 2021.11.23 국내 출시)')]),
 ('랭글러 (TJ, 2세대)', '1997-2006', [
   seg(2000, 2006, **C64,
       src=TP.format('Wrangler TJ 1998–2006 Texas Crypto 4D64, SKIM, Y160-PT') + ', 위키백과(TJ 1997.3~2006 국내 판매)')]),
 ('랭글러 (JK, 3세대)', '2007-2018', [
   seg(2007, 2007, **C46,
       src=TP.format('Wrangler JK 2007–2018 ID46 PCF7936 리모컨 일체형 키, WCM·TIPM, CY24·Y164') + ', 위키백과(JK 2007 국내 수입)'),
   seg(2008, 2014, **C46, blade_pn=RHK,
       src=TP.format('Wrangler JK 2007–2018 ID46 PCF7936, WCM') + ', ' + RHK_SRC),
   seg(2015, 2018, **C46,
       src=TP.format('Wrangler JK 2007–2018 ID46 PCF7936, WCM') + ', 위키백과(JL 2018.7 국내 출시)')]),
 ('랭글러 (JL, 4세대)', '2018-현재', [
   seg(2018, 2026, **JL,
       src=TP.format('Wrangler JL 2018–2026 Hitag AES ID4A NCF29A1X, SGW·Continental RF Hub, SIP22') + ', ' + JL_SRC
           + ', 위키백과(JL 2018.7 국내 출시, 4xe 2021.9.8)')]),
 ('글래디에이터', '2020-현재', [
   seg(2020, 2026, **JL,
       src=TP.format('Gladiator JT 2019–2026 Hitag AES ID4A NCF29A1X, SGW·Continental RF Hub, SIP22') + ', ' + JL_SRC
           + ', 위키백과(글래디에이터 2020.9.2 국내 출시, 부분변경 2025.4.11)')]),
]

GUIDE = [
 '이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.', '',
 '※ 구성',
 "- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 같고, 맨 앞 '브랜드'와 칩코드 뒤 '키종류'를 추가했습니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다.",
 '- 연식은 실제 국내 판매 기준입니다(아래 목록).',
 '- 키 부품번호는 433/434MHz로 확인된 순정 품번만 [해외 공용 품번]으로 적었습니다. 2007년 이전 미국형 리모컨 일체형 키(FCC OHT692427AA·OHT692713AA·KOBDT04A 등)는 315MHz라 뺐습니다. 국내 순정 품번은 공개 자료가 없습니다.',
 "- 2008~2014년 랭글러·컴패스의 유럽·중동형 리모컨 일체형 키(68001703AA·AC, 433MHz)는 키블레이드 칸에 [리모컨키]로 적었습니다.",
 "- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
 '',
 '※ 칩 코드·이모빌라이저(지프)',
 '- ID64(4D64): Texas Crypto 4D64, SKIM(Sentry Key Immobilizer Module) — 체로키 XJ·KJ 전기, 그랜드 체로키 WJ, 랭글러 TJ',
 '- ID46(PCF7936): Philips Hitag2 리모컨 일체형 키, SKREEM·WCM(Wireless Control Module) — 2005년 이후 KJ·WK·JK·컴패스 1세대·커맨더 전기',
 '- ID46(PCF7941·PCF7953): FOBIK(꽂는 스마트키)·키리스 고, WIN(Wireless Ignition Node)·RF Hub — WK·커맨더 2008~, WK2 2010~2013',
 '- ID4A: Hitag AES 128bit, RF Hub·SGW(Security Gateway) — 체로키 KL·WK2 2014~·컴패스 2세대·JL·글래디에이터·WL·어벤저  |  ID88: Megamos AES(레니게이드 일반 폴딩키, Fiat 계열 BCM)',
 '- 키웨이: Y160(4D64 시기), Y164·CY24(리모컨 일체형 키), Y159·CY24(FOBIK 비상키), SIP22(2014년 이후·레니게이드·어벤저)',
 '',
 '※ 색상',
 '- 주황색: 추정이거나 자료가 서로 다른 값.',
 '',
 '※ 목록과 국내 판매 연식이 다른 모델',
 '- 커맨더: 목록은 2023-현재이나 신형 커맨더(2021~, 브라질·인도 생산)는 국내 미출시 — 국내에는 1세대 커맨더(XK)가 2006.5~2010년 판매되어 XK 기준으로 기록.',
 '- 컴패스: 목록은 한 모델(2011-현재)이나 1세대(MK49, 2007~, 2011 부분변경)와 2세대(MP, 2018.7.17~2023.4 판매 중단)를 세대별로 나눔. 1세대 국내 판매 종료 시점은 자료가 없어 2016년까지로 기록.',
 '- 체로키 KL: 2014.9 국내 출시, 2023.4 국내 판매 중단 / 어벤저: 2024.9.4 국내 출시 / 글래디에이터: 2020.9.2 국내 출시.',
 '- 그랜드 체로키 WJ: WJ 생산은 2004년까지, 2005년부터 WK 수입 → WJ 2000~2004 / WK2: 2010.10.12 국내 출시 → 2010년은 WK·WK2 두 행 / WL: 2021.11.23 국내 출시 → 2021년은 WK2·WL 두 행.',
 '- 2000년 이전에만 판매된 그랜드 체로키 ZJ(1995~1999, 트랜스폰더 없음)와 랭글러 YJ(1992~1995)는 2000년식 기준에 따라 뺐습니다.',
 '- 패트리어트(목록 2008-2013): 국내 미판매라 뺐습니다.',
 '',
 '※ 출처',
 '- transpondery.com Jeep Transponder Catalog, abkeys.com 순정 키 적용표(품번별 주파수·연식), 한국어 위키백과·나무위키, 국내 출시 기사(스텔란티스 코리아 보도자료·시사위크·모터그래프 등).',
 '- 연식별 근거는 research/import5/yearly_jeep.md에 있습니다.',
]

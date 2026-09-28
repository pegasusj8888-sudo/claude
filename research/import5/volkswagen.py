# 폭스바겐 — 모델·연식별 키 자료 (research/import5/build.py volkswagen)
#   근거: transpondery.com VW Transponder Catalog·VW OEM Key & Remotes Catalog(품번별 주파수·버튼·KESSY),
#         abkeys.com 순정 키 적용표(433/434MHz 유럽·중동), 한국어 위키백과·국내 출시 기사(국내 판매 연식)
BRAND = '폭스바겐'
FILE = '폭스바겐_models.xlsx'
TITLE = '폭스바겐 트랜스폰더 DB'

G = '[해외 공용 품번]'
def g(*pns): return ', '.join(p + G if '[' not in p else p[:-1] + ', 해외 공용 품번]' for p in pns)
TP = 'transpondery'
NEVER_NOTE = '국내 정식 판매 이력 없음 — 해외 사양 기준'
KW = 'HU66'
KWM = 'HU66, HU162T'

ENDED = {'골프 (Golf, 8세대 페이스리프트)': False, '티구안 (Tiguan, 3세대)': False, 'ID.4': False, 'ID.5': False,
         '투아렉 (Touareg, 3세대)': False}

def seg(y0, y1, **k):
    k['y'] = (y0, y1); return k

PQ = dict(chip='ID48', immo='IMMO4', keyway=KW, ktype_hint='폴딩키')
MQB = dict(chip='ID88', immo='MQB IMMO5', keyway=KWM, ktype_hint='폴딩키')
EVO = dict(chip='ID49(NCF2161W)', immo='MQB-Evo IMMO5', keyway=KW, ktype_hint='폴딩키,스마트키')
K5K = g('5K0837202AD', '5K0837202Q', '5K0837202AJ[키리스]')

MODELS = [
 ('폴로 (Polo)', '2003-2012', [
   seg(2013, 2016, **PQ, fold=g('5K0837202AD', '5K0837202AH'),
       src='transpondery(Polo 2009–2015 Megamos Crypto ID48 dealer key, OEM키 Polo 2012–2015 5K0837202AD·AH 434MHz), 데일리안·모터그래프(폴로 1.6 TDI 2013.4.25 국내 출시)')]),
 ('뉴 비틀 (New Beetle, 2세대)', '1998-2010', [
   seg(2000, 2001, chip='ID48', immo='IMMO3', keyway=KW, ktype_hint='폴딩키', fold=g('1J0959753B', '1J0959753P', '1J0959753D', '1J0959753N'),
       src='transpondery(Beetle 1998–2003 Megamos Crypto 48, OEM키 Beetle 1998–2001 1J0959753B·P·D·N 433MHz), 폭스바겐그룹코리아 연혁(2000년부터 고진모터스 수입)'),
   seg(2002, 2003, chip='ID48', immo='IMMO3', keyway=KW, ktype_hint='폴딩키', fold=g('1J0959753AH', '1J0959753DA', '1J0959753DL'),
       src='transpondery(Beetle 1998–2003 Megamos 48, OEM키 Beetle 2002–2010 1J0959753AH·DA·DL 433MHz)'),
   seg(2004, 2010, chip='ID48', immo='IMMO4', keyway=KW, ktype_hint='폴딩키', fold=g('1J0959753AH', '1J0959753DA', '1J0959753DL'),
       src='transpondery(Beetle 2003–2007 Megamos Crypto VW-CAN JMA TP23, 2008+ ID48 dealer key, OEM키 2002–2010 1J0959753AH·DA·DL 433MHz), 위키백과(대한민국 사양 뉴 비틀 카브리올레 후기형)')]),
 ('더 비틀 (Beetle, 3세대)', '2013-2019', [
   seg(2013, 2016, **PQ, fold=g('5K0837202AD', '5K0837202Q', '5K0837202E', '5K0837202AJ', '5K0837202AM[키리스]'),
       src='transpondery(Beetle 2008+ ID48 dealer key, OEM키 Beetle 2012–2016 5K0837202Q·E·AD·AJ 434MHz, AM KESSY), abkeys(순정 5K0837202AJ Beetle 2012-2015 433MHz), 카이즈유(2013 더 비틀 국내 판매), 폭스바겐코리아 2016.11~2018.4 판매 중단 후 미재개')]),
 ('제타 (Jetta, 5세대)', '2006-2010', [
   seg(2006, 2010, chip='ID48', immo='IMMO4', keyway=KW, ktype_hint='폴딩키', fold=g('1K0959753G', '1K0959753N'),
       src='transpondery(Jetta 2006–2010 Megamos Crypto ID48 VW-CAN TP23, OEM키 Jetta 2006–2010 1K0959753G·N 434MHz)')]),
 ('제타 (Jetta, 6세대)', '2011-2018', [
   seg(2011, 2016, **PQ, fold=g('5K0837202AD', '5K0837202Q', '5K0837202AA', '5K0837202AJ', '5K0837202E[키리스]'),
       src='transpondery(Jetta 2009–2018 ID48 dealer key, OEM키 Jetta 2009–2018 5K0837202Q·AD·AA·AJ 434MHz, E KESSY), 위키백과(국내 2011.5.2 판매 개시), 2016.11 이후 판매 중단·미재개')]),
 ('제타 (Jetta, 7세대)', '2019-2023', [
   seg(2020, 2023, **MQB, fold=g('5G6959752Q', '5G6959752CF', '5G6959752BF', '5G6959752CS', '5G6959752CJ[키리스]', '5G6959752BL[키리스]'),
       src='transpondery(Jetta 2019+ Megamos AES MQB ID49·Silca ID88, OEM키 Jetta 2019+ 5G6959752Q·CF·BF·CS 434MHz, CJ·BL KESSY), 위키백과(국내 2020.10.15 출시)')]),
 ('골프 (Golf, 5세대)', '2004-2008', [
   seg(2004, 2006, chip='ID48', immo='IMMO4', keyway=KW, ktype_hint='폴딩키', fold=g('1K0959753G', '1J0959753DA'),
       src='transpondery(Golf MK5 2003–2007 Megamos ID48 VW-CAN precoded TP23, OEM키 Golf 2002–2006 1J0959753DA 433MHz, 1K0959753G 434MHz), 위키백과·나무위키(골프 5세대 2004.10.28 국내 수입 시작)'),
   seg(2007, 2008, chip='ID48', immo='IMMO4', keyway=KW, ktype_hint='폴딩키', fold=g('1K0959753N', '1K0959753S', '1K0959753G'),
       src='transpondery(Golf MK5 ID48 CAN, OEM키 Golf 2007–2011 1K0959753N·S 434MHz)')]),
 ('골프 (Golf, 6세대)', '2009-2013', [
   seg(2009, 2013, **PQ, fold=g('5K0837202', '5K0837202D', '5K0837202Q', '5K0837202AD', '5K0837202AA', '5K0837202AJ[키리스]', '5K0837202E[키리스]'),
       src='transpondery(Golf MK6 2008–2015 ID48 dealer key, OEM키 Golf 2009–2014 5K0837202·D·Q·AD·AA 434MHz, E·F·AJ·J KESSY)')]),
 ('골프 (Golf, 7세대)', '2013-2020', [
   seg(2013, 2016, **MQB, fold=g('5G0959752BA', '5G0959752BJ', '5G0959752DD', '5G0959753', '5G0959752BC[키리스]', '5G0959753AD[키리스]'),
       src='transpondery(Golf MK7 2013–2020 Megamos AES MQB ID88, OEM키 Golf 2013–2020 5G0959752BA·BJ·DD 434MHz, BC·BK·DF·BS KESSY), abkeys(순정 5G0959753 433MHz·5G0959753AD 434MHz 키리스 Golf7 2013-2018), 위키백과(국내 2013.7 출시, 배기가스 조작 사건으로 판매 중단)')]),
 ('골프 (Golf, 8세대)', '2020-2024', [
   seg(2022, 2024, **EVO, fold=g('5H0959753', '5H0959753G'), smart=g('5HG959753B'),
       src='abkeys(순정 5HG959753B Golf·ID.3·ID.4 2020-2024 433MHz MQB49 NCF2161W FS19), transpondery(OEM키 Golf 2020+ 5H0959753·5H0959753G 434MHz), 위키백과(국내 2022.1.5 TDI 출시, 2022.12.15 GTI)')]),
 ('골프 (Golf, 8세대 페이스리프트)', '2025-현재', [
   seg(2025, 2026, **EVO, smart='5HG959753B[추정]',
       src='abkeys(5HG959753B Golf 2020-2024 433MHz MQB49 — 페이스리프트 적용은 미확인), 아주경제(신형 골프 2025.3 국내 출시)')]),
 ('시로코 (Scirocco)', '2009-2017', [
   seg(2012, 2016, **PQ, fold=g('5K0837202AD', '5K0837202Q', '5K0837202BH', '5K0837202AJ[키리스]', '5K0837202E[키리스]'),
       src='transpondery(Scirocco 2008+ ID48 dealer key, OEM키 Scirocco 2011–2014 5K0837202Q·AD 434MHz, 2014–2017 AD·BH, E·AJ·BN KESSY), 나무위키·오토뷰(3세대 2012.2 국내 출시, 2016.11 판매 중단)')]),
 ('이오스 (Eos)', '2007-2015', [
   seg(2007, 2010, chip='ID48', immo='IMMO4', keyway=KW, ktype_hint='폴딩키', fold=g('1K0959753G', '1K0959753M'),
       src='transpondery(Eos 2006+ ID48, OEM키 Eos 2005–2010 1K0959753G·M 434MHz), 이투데이(이오스 2007 국내 출시)'),
   seg(2011, 2015, **PQ, fold=g('5K0837202AD', '5K0837202Q', '5K0837202E[키리스]', '5K0837202AJ[키리스]'),
       src='transpondery(OEM키 Eos 2010–2015 5K0837202Q·AD 434MHz, E·AJ KESSY), abkeys(순정 5K0837202AJ Eos 2009-2013 433MHz)')]),
 ('파사트 (Passat, B6/B7)', '2005-2014', [
   seg(2005, 2011, chip='ID48, ID46(PCF7936)[키리스]', immo='IMMO4', keyway=KW, ktype_hint='스마트키',
       smart=g('3C0959752BA', '3C0959752AJ', '3C0959752AL', '3C0959752AR', '3C0959752BF', '3C0959752M', '3C0959752BG[키리스]'),
       src='transpondery(Passat B6 2006–2010 Megamos ID48 dealer key 3C0959752AJ·AK, OEM키 Passat 2005–2014 3C0959752M·BF·AR·AL·AD·BA·AJ 434MHz, BG KESSY), abkeys(순정 3C0959752BA ID48 433MHz 2006-2012, 3C0959752BG PCF7936 ID46 키리스 433MHz 2009-2014), 위키백과(B6 2005.10.12 국내 출시, 유럽형 B7은 국내 미판매·2012.8부터 북미형 NMS)')]),
 ('파사트 (Passat NMS, 북미형)', '2015-2019', [
   seg(2012, 2016, **PQ, fold='5K0837202AD[추정], 5K0837202AM[추정], 5K0837202AJ[키리스, 추정]',
       src='transpondery(Passat 2014–2020 OEM키 5K0837202AD·AM 434MHz, AJ KESSY — NMS 적용 여부 미확인, 북미형 561837202은 315MHz라 뺌), 위키백과(NMS 2012.8.27 국내 판매 시작), 2016.11 판매 중단 후 미재개(2018 파사트 GT로 대체)')]),
 ('CC', '2009-2017', [
   seg(2009, 2016, chip='ID48, ID46(PCF7936)[키리스]', immo='IMMO4', keyway=KW, ktype_hint='스마트키', smart=g('3C0959752BA', '3C0959752BG[키리스]'),
       src='abkeys(Passat CC 2006+ 3C0959752BA ID48 433MHz, 2009+ 3C0959752BG PCF7936 433MHz 키리스), eBay(VW CC 2009-2017 3C0959752BA ID48 433MHz), 이투데이(CC 2009.2.1 국내 출시), 2016.11 판매 중단')]),
 ('아테온 (Arteon)', '2018-2024', [
   seg(2018, 2024, chip='ID88', immo='MQB IMMO5', keyway=KWM, ktype_hint='스마트키',
       smart=g('3G0959752BT', '3G0959752CD', '3G0959752CA', '3G0959752CB'),
       src='transpondery(Arteon 2017+ Megamos AES MQB ID88, OEM키 Arteon 2017+ 3G0959752BT·CD 434MHz 3버튼, CA·CB 434MHz), 한국일보·탑라이더(아테온 2018.12.5 국내 출시)')]),
 ('페이톤 (Phaeton)', '2005-2016', [
   seg(2005, 2007, chip='ID46(PCF7946A)', immo='KESSY', keyway=KW, ktype_hint='폴딩키', fold=g('3D0959753P', '3D0959753S[키리스]'),
       src='transpondery(Phaeton 2002+ Philips Crypto2 ID46 PCF7946·PCF7936, OEM키 Phaeton 2002–2007 3D0959753P 433MHz, S KESSY), 파이낸셜뉴스(페이톤 2005 국내 출시)'),
   seg(2008, 2010, chip='ID46(PCF7946A)', immo='KESSY', keyway=KW, ktype_hint='폴딩키', fold=g('3D0959753AK', '3D0959753AR', '3D0959753AM[키리스]', '3D0959753AT[키리스]'),
       src='transpondery(OEM키 Phaeton 2008–2010 3D0959753AK·AR 434MHz, AM·AT KESSY)'),
   seg(2011, 2014, chip='ID46(PCF7946A)', immo='KESSY', keyway=KW, ktype_hint='폴딩키', fold=g('3D0959753BG', '3D0959753BJ[키리스]'),
       src='transpondery(OEM키 Phaeton 2011–2016 3D0959753BG 434MHz, BJ KESSY), 위키백과(대한민국 2014년 수입 중단)')]),
 ('티록 (T-Roc)', '2020-2023', [
   seg(2021, 2023, **MQB, fold=g('5G6959752CF', '5G6959752CS', '5G6959752CJ[키리스]', '5G6959752BQ[키리스]', '5G6959752BL[키리스]'),
       src='transpondery(T-Roc 2018+ Megamos AES MQB ID88, OEM키 T-Roc 2018+ 5G6959752CF·CS 434MHz, CJ·BQ·BL KESSY), ZDNet·모터그래프(티록 2021.1.29 국내 출시, 2020년 출시 연기)')]),
 ('티구안 (Tiguan, 1세대)', '2009-2016', [
   seg(2009, 2010, chip='ID48', immo='IMMO4', keyway=KW, ktype_hint='폴딩키', fold=g('1K0959753G', '1K0959753M', '1K0959753N'),
       src='transpondery(Tiguan 2007–2015 ID48 dealer key, OEM키 Tiguan 2008–2010 1K0959753G·M·N 434MHz)'),
   seg(2011, 2016, **PQ, fold=g('5K0837202AD', '5K0837202AH', '5K0837202AJ[키리스]', '5K0837202AN[키리스]'),
       src='transpondery(OEM키 Tiguan 2011–2016 5K0837202AD·AH 434MHz, AN·AJ·AM KESSY), abkeys(순정 5K0837202AJ Jetta·Tiguan 2008+ 433MHz)')]),
 ('티구안 (Tiguan, 2세대)', '2017-2023', [
   seg(2018, 2023, **MQB, fold=g('5G6959752CF', '5G6959752CS', '5G6959752CJ[키리스]', '5G6959752BL[키리스]', '5G6959752BQ[키리스]', '5G6959752AQ[키리스]'),
       src='transpondery(Tiguan 2015+ Megamos AES MQB ID88, OEM키 Tiguan 2016–2021 5G6959752CF·CS 434MHz, CJ·BL·BQ·AQ KESSY), 이데일리(판매 재개 첫 차 신형 티구안 2018.4), 위키백과(페이스리프트 2021.7 국내 출시)')]),
 ('티구안 (Tiguan, 3세대)', '2024-현재', [
   seg(2025, 2026, chip='ID49', immo='MQB-Evo IMMO5', keyway=KW, ktype_hint='스마트키',
       src='탑라이더·유카포스트(3세대 티구안 2025년 국내 출시) — MQB-Evo(ID49) 적용, 국내 키 품번 자료 없음')]),
 ('ID.4', '2023-현재', [
   seg(2022, 2026, chip='ID49(NCF2161W)', immo='확인 불가', keyway=KW, ktype_hint='스마트키', smart=g('5HG959753B'),
       src='abkeys(순정 5HG959753B ID.3·ID.4·Golf 2020-2024 433MHz MQB49 NCF2161W FS19), 이투데이(ID.4 2022.9.15 국내 출시)', flag='red',
       note='MEB 플랫폼 이모빌라이저 모듈 자료 없음')]),
 ('ID.5', '2024-현재', [
   seg(2025, 2026, chip='ID49(NCF2161W)[추정]', immo='확인 불가', keyway=KW, ktype_hint='스마트키', smart='5HG959753B[추정]',
       src='abkeys(5HG959753B ID.4 2020-2024 433MHz — ID.5 적용 미확인), 나무위키·네이트뉴스(ID.5 2025.2.18 계약 시작, 4.25 인도)', flag='red',
       note='ID.5 전용 키 칩·MEB 이모빌라이저 자료 없음 — ID.4 기준 추정')]),
 ('투아렉 (Touareg, 1세대)', '2004-2010', [
   seg(2005, 2007, chip='ID46(PCF7946A), ID46(PCF7942)[키리스]', immo='KESSY', keyway=KW, ktype_hint='폴딩키', fold=g('3D0959753P', '3D0959753S[키리스]', '3D0959753AG[키리스]'),
       src='transpondery(Touareg 2003–2009 Philips Crypto2 ID46 PCF7946A·PCF7936, OEM키 Touareg 2003–2007 3D0959753P 433MHz, S KESSY), abkeys(3D0959753AG 433MHz PCF7942 키리스 2005-2009), 다나와(1세대 2005.9 국내 판매 시작)'),
   seg(2008, 2010, chip='ID46(PCF7946A), ID46(PCF7942)[키리스]', immo='KESSY', keyway=KW, ktype_hint='폴딩키', fold=g('3D0959753AK', '3D0959753AM[키리스]', '3D0959753AH[키리스]'),
       src='transpondery(OEM키 Touareg 2008–2010 3D0959753AK 434MHz, AM·AH KESSY), abkeys(3D0959753AK 433MHz Touareg 2003-2009)')]),
 ('투아렉 (Touareg, 2세대)', '2010-2018', [
   seg(2011, 2016, chip='ID46(PCF7945AC)', immo='BCM2', keyway=KW, ktype_hint='스마트키',
       smart=g('7P6959754AC', '7P6959754AL', '7P6959754L', '7P6959754P[키리스]', '7P6959754AQ[키리스]'),
       src='transpondery(Touareg 2010–2018 Hitag Ext VAG PCF7945AC dealer key, OEM키 Touareg 2011–2012 7P6959754AC·AL 434MHz, P·AQ KESSY), abkeys(순정 7P6959754L 433MHz PCF7945AC), automodulelab(7P 이모빌라이저 BCM2), 위키백과(국내 2011.7.4 출시)')]),
 ('투아렉 (Touareg, 3세대)', '2018-현재', [
   seg(2020, 2026, chip='MLB evo 전용 칩', immo='MLB evo IMMO5', keyway='HU162T', ktype_hint='스마트키',
       src='MLB evo 플랫폼(아우디 Q7·Q8과 공유) 키 — 국내 키 품번 자료 없음, huloda·locksmithkeyless(Touareg 2018~ 키 HU162T 블레이드), 위키백과(국내 2020.2.7 V6 3.0 디젤 출시, 2020.8 V8)')]),
]

GUIDE = [
 '이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.', '',
 '※ 구성',
 "- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 같고, 맨 앞 '브랜드'와 칩코드 뒤 '키종류'를 추가했습니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다.",
 '- 연식은 실제 국내 판매 기준입니다. 원본 목록 연식과 국내 판매가 다른 모델은 국내 기준으로 바꿨습니다(아래 목록).',
 '- 키 부품번호는 국내 사양(433/434MHz, 유럽형)만 적었습니다. 미국형(315MHz, 5K0837202AE·5G6959752BM·561837202 등)은 뺐습니다. 국내 순정 품번은 공개 자료가 없어 [해외 공용 품번]으로 표시했습니다.',
 '- [키리스] = KESSY(키리스 엔트리) 사양 키. 폴딩키 품번 5K0837202·1K0959753 계열은 여러 차종 공용입니다.',
 "- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
 '',
 '※ 칩 코드·이모빌라이저(폭스바겐)',
 '- ID48: Megamos Crypto 48(2004년 이후는 CAN 방식·딜러 사전코딩 키)  |  ID46(PCF7946A·PCF7936): 투아렉 1세대·페이톤 KESSY, 파사트 B6·CC 키리스 키  |  ID46(PCF7945AC): 투아렉 2세대(Hitag Ext, BCM2)',
 '- ID88: Megamos AES(MQB, 골프 7·티구안 2·아테온·티록·제타 7)  |  ID49: Hitag Pro(MQB-Evo·MEB, 골프 8·ID.4·ID.5·티구안 3)  |  MLB evo 전용 칩: 투아렉 3세대',
 '- 이모빌라이저: IMMO3(계기판) → IMMO4(계기판 통합, CAN) → MQB IMMO5(계기판 통합) → MQB-Evo IMMO5(GeKo 온라인) / 투아렉·페이톤 KESSY, 투아렉 2세대 BCM2, 투아렉 3세대 MLB evo IMMO5',
 '- 키웨이: HU66(구형·PQ·MQB), MQB 일부 HU162T',
 '',
 '※ 색상',
 '- 주황색: 추정이거나 자료가 서로 다른 값.',
 '- 빨간색: 확인 불가 — ID.4·ID.5(MEB)는 이모빌라이저 모듈 자료가 없습니다.',
 '',
 '※ 목록과 국내 판매 연식이 다른 모델',
 '- 폭스바겐코리아는 배기가스 조작 사건으로 2016.8 인증 취소 후 2016.11부터 2018.4까지 판매한 차가 없어 2017년식 행이 없습니다. 판매 재개 뒤 다시 들여오지 않은 차종(폴로·더 비틀·제타 6·골프 7·시로코·파사트 NMS·CC·티구안 1·투아렉 2)은 2016년이 마지막입니다.',
 '- 폴로: 2013.4.25 국내 출시 → 2013~2016 / 뉴 비틀: 2000년부터 수입 → 2000~ / 제타 7: 2020.10.15 → 2020~ / 골프 8: 2022.1.5 → 2022~ / 시로코: 2012.2 → 2012~ / 티록: 2021.1.29 → 2021~ / 티구안 2: 2018.4 → 2018~ / 티구안 3: 2025 → 2025~.',
 '- 파사트: 국내에는 B6(2005.10.12~)만 들어왔고 유럽형 B7은 미판매. 2012.8.27부터 북미형 NMS 판매 → B6 행 2005~2011, NMS 행 2012~2016. 2018.2 출시한 파사트 GT(B8)는 원본 목록에 없어 넣지 않았습니다. 파사트 프로(B9, 목록 2024-현재)는 국내 미출시라 뺐습니다.',
 '- 페이톤: 2014년 수입 중단 → 2005~2014 / 투아렉 1: 2005.9 → 2005~2010 / 투아렉 2: 2011.7.4 → 2011~ / 투아렉 3: 2020.2.7 → 2020~ / ID.4: 2022.9.15 → 2022~ / ID.5: 2025.2 → 2025~ / 아테온: 2018.12.5 출시.',
 '',
 '※ 출처',
 '- transpondery.com VW Transponder Catalog·OEM Keys & Remotes Catalog(품번별 주파수), abkeys.com 순정 키 적용표, 한국어 위키백과, 국내 출시 기사(이데일리·ZDNet·이투데이·모터그래프 등).',
 '- 연식별 근거는 research/import5/yearly_volkswagen.md에 있습니다.',
]

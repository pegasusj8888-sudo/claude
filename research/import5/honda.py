# 혼다 — 모델·연식별 키 자료 (research/import5/build.py honda)
#   근거: transpondery.com Honda Transponder Catalog(2026-09-12판, 모델·생산기간별 칩·OEM 키·FCC ID·키 블레이드),
#         abkeys.com 순정 키(품번별 주파수·적용 연식), 한국어 위키백과·다나와·국내 출시 기사(국내 판매 연식)
BRAND = '혼다'
FILE = '혼다_models.xlsx'
TITLE = '혼다 트랜스폰더 DB'

G = '[해외 공용 품번]'
def g(*pns): return ', '.join(p + G if '[' not in p else p[:-1] + ', 해외 공용 품번]' for p in pns)

ENDED = {m: False for m in ('어코드 (11세대)', 'CR-V (6세대)', '파일럿 (4세대)', '오딧세이 (북미형, 5세대)')}

def seg(y0, y1, **k):
    k['y'] = (y0, y1); return k

TP = 'transpondery(Honda Catalog {})'
AB = 'abkeys({})'
IMM = '이모빌라이저 ECU'
ISK = '스마트키 ECU'
KW = 'HON66'
H46 = dict(chip='ID46(PCF7936)', immo=IMM, keyway=KW, ktype_hint='막대키')
H46B = dict(chip='ID46(PCF7961)', immo=IMM, keyway=KW, ktype_hint='막대키')
H47 = dict(chip='ID47(NCF2952X)', immo=ISK, keyway=KW, ktype_hint='스마트키')
H4A = dict(chip='ID4A', immo=ISK, keyway=KW, ktype_hint='스마트키')
T43 = g('72147-T43-A01', '72147-T43-A11')   # 2022~ Civic·CR-V·HR-V·Pilot 433MHz KR5TP-4
T43_SRC = AB.format('순정 CR-V·Pilot·HR-V·Civic 2023-2025 스마트키 72147-T43-A01·72147-T43-A11 433MHz FCC KR5TP-4 HITAG AES ID4A')
US313 = '북미형 313.8MHz(FCC {})라 뺌'

MODELS = [
 ('CR-Z', '2010-2016', [
   seg(2010, 2016, **H46B,
       src=TP.format('CR-Z 2011–2016 Philips Hitag2 ID46 PCF7936·PCF7961 리모컨 키 35118-SZT-A00·35113-SZT-E10, HON66') + ' — ' + US313.format('MLBHLIK-1T')
           + ', 이데일리·아시아경제(CR-Z 2010.10 국내 출시), 위키백과(판매율 저조로 수입 중단)')]),
 ('시빅 (8세대)', '2006-2011', [
   seg(2006, 2011, **H46,
       src=TP.format('Civic 2006–2011 Philips Hitag2 ID46 PCF7936·PCF7961 리모컨 키 35118-SVA-A11, HON66') + ' — ' + US313.format('N5F-S0084A')
           + ', 위키백과(8세대 일본형 4도어 세단 2006 국내 출시)')]),
 ('시빅 (9세대)', '2012-2016', [
   seg(2012, 2015, chip='ID46(PCF7961)[리모컨키], ID47[스마트키]', immo=IMM, keyway=KW, ktype_hint='막대키,스마트키',
       src=TP.format('Civic 2012–2015 Hitag2 ID46 리모컨 키 35118-TR0-A00 또는 Hitag3 ID47 스마트키 72147-TR0-A01, HON66') + ' — ' + US313.format('MLBHLIK6-1T·KR55WK49308')
           + ', 위키백과(9세대 2011.11 국내 상륙, 판매 중지 후 2013.4 부분변경 재개, 2016년 초 재고 소진 후 수입 중단)')]),
 ('인사이트', '2009-2014', [
   seg(2010, 2012, **H46B,
       src=TP.format('Insight 2010–2014 Hitag2 ID46 PCF7936·PCF7961 리모컨 키 35118-TM8-A00, HON66') + ' — ' + US313.format('MLBHLIK-1T')
           + ', 위키백과(인사이트 2010 국내 판매 개시, 판매 부진으로 2012 수입 중지)')]),
 ('어코드 (7세대)', '2004-2008', [
   seg(2004, 2008, **H46,
       src=TP.format('Accord 2003–2007 Philips Hitag2 ID46 PCF7936 리모컨 일체형 키 OUCG8D-380H-A·35118-SDA-A11, HON66') + ' — 국내 사양 주파수 자료 없음'
           + ', 위키백과(2004.5 7세대 국내 공식 판매 — 인스파이어 차체), 혼다코리아 연혁')]),
 ('어코드 (8세대)', '2008-2013', [
   seg(2008, 2012, **H46B, blade_pn=g('72147-TA0-U11[리모컨키]'),
       src=TP.format('Accord 2008–2012 Hitag2 ID46 PCF7936·PCF7961 리모컨 키 35118-TA0-A04') + ' — ' + US313.format('KR55WK49308·MLBHLIK-1T') + ', '
           + AB.format('순정 Accord 2007-2012 리모컨 일체형 키 72147-TA0-U11 433MHz HON66')
           + ', 위키백과(2008 수입차 판매 1위)')]),
 ('어코드 (9세대)', '2013-2017', [
   seg(2012, 2015, **H47, smart=g('72147-T2A-Y01'),
       src=TP.format('Accord 2013–2017 Philips Hitag3 ID47 NCF2952X 스마트키 72147-T2A-A02·A22') + ' — ' + US313.format('ACJ932HK1210A') + ', '
           + AB.format('Accord 2013-2016 스마트키 72147-T2A-Y01 433MHz') + ', RPM9·다나와(9세대 2012.12 국내 출시)'),
   seg(2016, 2017, **H47, smart=g('72147-T2G-A31', '72147-T2G-A61'),
       src=TP.format('Accord 2013–2017 Hitag3 ID47') + ', ' + AB.format('순정 Accord 2016-2017 스마트키 72147-T2G-A31·72147-T2G-A61 434MHz FCC ACJ932HK1310A')
           + ', 위키백과(2017.1.17 부분변경 국내 판매)')]),
 ('어코드 (10세대)', '2018-2023', [
   seg(2018, 2023, chip='ID47(NCF29A1X)', immo=ISK, keyway=KW, ktype_hint='스마트키',
       smart=g('72147-TVA-A01', '72147-TVA-A11', '72147-TVA-K11', '72147-TWA-A11[하이브리드]'),
       src=TP.format('Accord 2018–2022 Hitag AES·Hitag3 ID47 NCF29A1X 스마트키, HON66 비상키') + ', '
           + AB.format('순정 Accord 2018-2021 스마트키 72147-TVA-A01·TVA-A11·TVA-K11 433MHz FCC CWTWB1G0090(TVA-K11은 ID4A NCF2960M 표기), 하이브리드 72147-TWA-A11 433MHz'),
       flag='orange', note='칩 자료 상충(ID47, ID4A)')]),
 ('어코드 (11세대)', '2023-현재', [
   seg(2023, 2026, **H4A, smart=g('72147-30A-A01', '72147-30A-A11'),
       src=TP.format('Accord 2023–2026 Hitag AES ID4A 스마트키 72147-30A-A01·30A-A11 FCC CWTWB1G0090·KR5TXN1(433MHz 계열), HON66 비상키')
           + ', 위키백과(11세대 2023.10.17 국내 출시)')]),
 ('레전드 (4세대)', '2004-2006', [
   seg(2006, 2012, chip='ID8E', immo=ISK, keyway=KW, ktype_hint='카드키', card=g('72147-SJA-E01'),
       src=TP.format('Legend 2005–2012 Sokymat Crypto 8E ID8E, 스마트 카드키 72147-SJA-E01(유럽형), HON66')
           + ', 위키백과(레전드 2006 국내 수입), 다나와·카이즈유(레전드 4세대 2006.6.20 6780만원 — 2012 단종)')]),
 ('레전드 (5세대 초기형)', '2006-2010', [
   seg(2015, 2016, chip='ID47', immo=ISK, keyway=KW, ktype_hint='스마트키',
       src='transpondery(Honda Legend는 2005–2012까지만 수록 — 같은 시기 혼다 스마트키 Hitag3 ID47 기준)'
           + ', 한국일보·이투데이(뉴 레전드 5세대 2015.3 아시아 최초 국내 출시), 위키백과(2016.1 재고 소진 후 수입 중단)',
       flag='orange', note='5세대 칩 자료 없음 — 같은 시기 혼다 Hitag3 ID47 기준 추정')]),
 ('HR-V (2세대)', '2015-2018', [
   seg(2016, 2018, chip='ID47(NCF2952X)', immo=ISK, keyway=KW, ktype_hint='막대키,스마트키',
       src=TP.format('HR-V 2016–2022 Hitag3 ID47 리모컨 키 35118-T7A-A01·스마트키 72147-T7S-A01') + ' — ' + US313.format('MLBHLIK6-1T·KR5V1X')
           + ', 위키백과(2016.7.5 국내 출시 — 멕시코 셀라야 생산 북미형, 판매 부진)')]),
 ('CR-V (2세대 후기형)', '2005-2006', [
   seg(2004, 2006, chip='ID48', immo=IMM, keyway=KW, ktype_hint='막대키',
       src=TP.format('CR-V 1999–2006 Megamos Crypto 48 ID48, HON66') + ', 위키백과(2004 혼다코리아 진출로 2세대 후기형부터 수입)')]),
 ('CR-V (3세대)', '2007-2012', [
   seg(2007, 2012, **H46B,
       src=TP.format('CR-V 2007–2013 Hitag2 ID46 PCF7936·PCF7961 리모컨 키 35118-SWA-A00') + ' — ' + US313.format('MLBHLIK-1T·N5F-S0084A')
           + ', 위키백과(4세대 초기형까지 사이타마 공장 생산분 수입)')]),
 ('CR-V (4세대)', '2012-2017', [
   seg(2012, 2013, **H46B,
       src=TP.format('CR-V 2007–2013 Hitag2 ID46 PCF7961 리모컨 키') + ', 위키백과(2013.1부터 미국 오하이오 생산분 수입)'),
   seg(2014, 2016, chip='ID47(NCF2952X)', immo=ISK, keyway=KW, ktype_hint='막대키,스마트키',
       src=TP.format('CR-V 2014–2016 Hitag3 ID47 NCF2952X 리모컨 폴딩키 35118-T0A-A00·스마트키 72147-T0A-A01') + ' — ' + US313.format('MLBHLIK6-1T·ACJ932HK1210A')
           + ', 위키백과(5세대 2017.3.30 국내 출시)')]),
 ('CR-V (5세대)', '2017-2023', [
   seg(2017, 2022, **H47, smart=g('72147-TLA-A01', '72147-TLA-A11'),
       src=TP.format('CR-V 2017–2022 Hitag3 ID47 NCF2952X 스마트키 72147-TLA-A01·TLA-A11 FCC KR5V2X·CWTWB1G0090(433MHz), HON66 비상키')
           + ', 위키백과(5세대 2017.3.30 국내 출시, 녹 문제로 2018 수입 일시 중단, 2019 부분변경 재개, 6세대 2023.4.11)')]),
 ('CR-V (6세대)', '2023-현재', [
   seg(2023, 2026, **H4A, smart=g('72147-3D0-A01', '72147-3D0-A11') + ', ' + T43,
       src=TP.format('CR-V 2023–2026 Hitag AES ID4A 스마트키 72147-3D0-A01·3D0-A11 FCC CWTWB1G0090·KR5TXN1') + ', ' + T43_SRC
           + ', 위키백과(6세대 2023.4.11 국내 출시)')]),
 ('크로스투어', '2012-2015', [
   seg(2012, 2012, chip='ID46(PCF7941)', immo=IMM, keyway=KW, ktype_hint='막대키',
       src=TP.format('Crosstour 2010–2012 Hitag2 ID46 PCF7936·PCF7941 리모컨 키 35118-TP6-A20') + ' — ' + US313.format('MLBHLIK-1T')
           + ', 데일리카·오토카코리아(크로스투어 2012.12 국내 출시, 3.5 단일 트림)'),
   seg(2013, 2015, **H47,
       src=TP.format('Crosstour 2013–2015 Hitag3 ID47 NCF2952X 스마트키 72147-TP6-A51·A61') + ' — ' + US313.format('ACJ932HK1210A'))]),
 ('파일럿 (2세대 후기형)', '2012-2015', [
   seg(2012, 2015, **H46B,
       src=TP.format('Pilot 2009–2015 Hitag2 ID46 PCF7936·PCF7961 리모컨 키 35118-SZA-A51·A61') + ' — ' + US313.format('KR55WK49308·MLBHLIK-1T')
           + ', 위키백과(2세대 후기형 2012 국내 공식 수입), 이데일리(오딧세이·파일럿 2012 출시)')]),
 ('파일럿 (3세대)', '2016-2022', [
   seg(2016, 2022, **H47, smart=g('72147-TG7-A11', '72147-TG7-A31', '72147-TG7-A41'),
       src=TP.format('Pilot 2016–2022 Hitag3 ID47 NCF2952X 스마트키 72147-TG7-A11·A21, HON66 비상키') + ', '
           + AB.format('순정 Civic·CR-V·Pilot 2016+ 스마트키 72147-TG7-A11·TG7-A31·TG7-A41 433MHz FCC KR5V2X') + ', 위키백과(3세대 2016.1 국내 출시)')]),
 ('파일럿 (4세대)', '2023-현재', [
   seg(2023, 2026, **H4A, smart=g('72147-T90-A01') + ', ' + T43,
       src=TP.format('Pilot 2023–2026 Hitag AES ID4A 스마트키 72147-T90-A01 FCC KR5TXN1·CWTWB1G0090') + ', ' + T43_SRC
           + ', 위키백과(4세대 2023.8.29 국내 출시)')]),
 ('오딧세이 (북미형, 4세대)', '2011-2017', [
   seg(2012, 2013, **H46B,
       src=TP.format('Odyssey 2011–2013 Hitag2 ID46 PCF7961 리모컨 키 35118-TK8-A10·A20') + ' — ' + US313.format('N5F-A04TAA')
           + ', 이데일리(오딧세이 2012.11.30 국내 출시 — 북미 생산 3.5 V6)'),
   seg(2014, 2017, **H47,
       src=TP.format('Odyssey 2014–2017 Hitag3 ID47 NCF2952X 스마트키 72147-TK8-A71·A81') + ' — ' + US313.format('KR5V1X'))]),
 ('오딧세이 (북미형, 5세대)', '2018-현재', [
   seg(2017, 2026, **H47, smart=g('72147-THR-A11', '72147-THR-A21', '72147-THR-A31'),
       src=TP.format('Odyssey 2018–2026 Hitag3 ID47 NCF2952X 스마트키 72147-THR-A11·A21·A31 FCC KR5V2X(433MHz), HON66 비상키') + ', 모터그래프·다나와(5세대 올 뉴 오딧세이 2017.10.23 국내 출시), 한국경제·토픽트리(혼다코리아 2026년 말 자동차 판매 종료 발표)')]),
]

GUIDE = [
 '이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.', '',
 '※ 구성',
 "- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 같고, 맨 앞 '브랜드'와 칩코드 뒤 '키종류'를 추가했습니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다.",
 '- 연식은 실제 국내 판매 기준입니다(혼다코리아 2004.5 자동차 판매 시작). 원본 목록 연식과 국내 판매가 다른 모델은 국내 기준으로 바꿨습니다(아래 목록).',
 '- 키 부품번호는 433/434MHz로 확인된 순정 품번만 [해외 공용 품번]으로 적었습니다. 북미형 313.8MHz 키(FCC MLBHLIK-1T·MLBHLIK6-1T·KR55WK49308·ACJ932HK1210A·KR5V1X·N5F-S0084A 등)는 뺐습니다. 2016년 이후 북미형 스마트키(FCC KR5V2X·CWTWB1G0090·KR5TP-4)는 433MHz라 적었습니다.',
 '- 국내 순정 품번은 공개 자료가 없습니다(혼다코리아 부품 조회 서비스 접속 불가).',
 "- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
 '',
 '※ 칩 코드(혼다)',
 '- ID48: Megamos Crypto 48(CR-V 2세대)  |  ID46(PCF7936·PCF7941·PCF7961): Philips Hitag2 리모컨 일체형 키(2003~2013년경)',
 '- ID8E: Sokymat Crypto 8E(레전드 4세대 스마트 카드키)  |  ID47(NCF2952X): Philips Hitag3(2013년 이후 스마트키·리모컨 폴딩키)  |  ID4A: Hitag AES(2022년 이후 어코드 11세대·CR-V 6세대·파일럿 4세대)',
 '- 이모빌라이저: 이모빌라이저 ECU(PCM 연동, 일반 키) → 스마트키 ECU(키리스 액세스 유닛)',
 '- 키웨이: HON66(전 차종, 스마트키는 비상키)',
 '',
 '※ 색상',
 '- 주황색: 추정이거나 자료가 서로 다른 값.',
 '',
 '※ 목록과 국내 판매 연식이 다른 모델',
 '- 레전드: 목록의 세대 구분(4세대 2004-2006, 5세대 초기형 2006-2010)이 실제와 달라 국내 판매 기준으로 바꿈 — 4세대(KB1) 2006.6~2012, 5세대(뉴 레전드) 2015.3~2016.1(재고 소진 후 수입 중단).',
 '- 시빅 9세대: 2011.11 국내 상륙, 2016년 초 재고 소진 후 수입 중단 → 2012~2015 / 인사이트: 2010~2012 / HR-V: 2016.7.5 국내 출시 → 2016~2018.',
 '- 어코드 8세대: 2008~2012, 9세대: 2012.12 국내 출시 → 2012~2017 / 오딧세이 5세대: 2017.10.23 국내 출시 → 2017~.',
 '- 혼다코리아는 2026년 말 자동차 판매 종료를 발표(2026.4) — 현재 판매 모델은 2026년까지 기록.',
 '- CR-V 2세대 후기형: 2004 혼다코리아 진출과 함께 수입 → 2004~2006 / CR-V 5세대: 2017.3.30~2022(6세대 2023.4.11) / 크로스투어: 2012.12 출시 → 2012~2015 / 오딧세이 4세대: 2012.11.30 국내 출시 → 2012~2017.',
 '',
 '※ 출처',
 '- transpondery.com Honda Transponder Catalog(모델·생산기간별 칩·OEM 키·FCC ID·키 블레이드), abkeys.com 순정 키(품번별 주파수·적용 연식), 한국어 위키백과·나무위키·다나와, 국내 출시 기사(이데일리·한국일보·이투데이·아시아경제 등).',
 '- 연식별 근거는 research/import5/yearly_honda.md에 있습니다.',
]

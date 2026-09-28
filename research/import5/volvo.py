# 볼보 — 모델·연식별 키 자료 (research/import5/build.py volvo)
#   근거: transpondery.com Volvo Transponder Catalog(칩·연식), auto-keys.eu 볼보 순정 키(주파수·칩·블레이드·한국 사양 447MHz 품번),
#         abkeys.com 순정 키 적용표, 키 판매처(locksmithkeyless·reidsremotes·keyshop-online 등), 한국어 위키백과·국내 출시 기사
BRAND = '볼보'
FILE = '볼보_models.xlsx'
TITLE = '볼보 트랜스폰더 DB'

G = '[해외 공용 품번]'
def g(*pns): return ', '.join(p + G if '[' not in p else p[:-1] + ', 해외 공용 품번]' for p in pns)

ENDED = {m: False for m in ('S60/V60 (3세대)', 'S90/V90', 'ES90 (전기차)', 'EX30 (전기차)', 'XC40', 'EX40 (전기차)', 'EC40 (전기차)', 'XC60 (2세대)', 'XC90 (2세대)')}

def seg(y0, y1, **k):
    k['y'] = (y0, y1); return k

# 세대별 공통
P2 = dict(chip='ID48', immo='CEM', keyway='NE66', ktype_hint='막대키', blade_pn=g('9203132'), fold='')
P2R = g('8685151[리모컨키]', '9452457[리모컨키]')
P1 = dict(chip='ID48', immo='CEM', keyway='HU101', ktype_hint='스마트키', smart='31300259, ' + g('30772202'))
P3 = dict(chip='ID46(PCF7953A)', immo='CEM', keyway='HU101', ktype_hint='스마트키', smart=g('30659637', '5WK49224[키리스]'), blade_pn=g('30699525'))
SPA = dict(chip='ID8A', immo='CEM', keyway='HU101', ktype_hint='스마트키', smart=g('31652607', '32256971[3키 세트]', '32279988[2키 세트]'), blade_pn=g('31391439'))
SRC_P2 = ('transpondery(S60 2000–2010·S80 1999–2007·V70 2000–2007·XC70 2000–2007·XC90 2003–2015 Megamos Crypto 48), '
          'locksmithkeyless·UHS(1999~2013 S60·S80·V70·XC70·XC90 ID48 NE66 4트랙, 순정 블랭크 9203132), abkeys(순정 리모컨 8685151·9452457 434MHz P2T-AE S60·S80·V70·XC70·XC90 2001-2009)')
SRC_P1 = ('transpondery(S40 2004–2012·V50 2004–2012·C70 2006–2013 Megamos Crypto 48, OEM 30772187·30667905·31252739), '
          'auto-keys.eu(순정 한국 사양 5WK49352·31300259 447MHz ID48 HU101 SIEMENS VDO, 유럽형 5WK48965·30772202 434MHz ID48), reidsremotes·ipdusa(P1 S40·V50·C30·C70 슬롯형 리모컨 키, 비상키 HU101)')
SRC_P3 = ('transpondery(S80 2006–2016·V70·XC70 2007–2016·XC60 2008–2017·S60 2010–2018·V60 2011–2018·V40 2012–2016 Hitag2 ID46 PCF7953A), '
          'auto-keys.eu(순정 5WK49224 434MHz PCF7945·7953 HU101 키리스, 30659637 434MHz), UHS·remotesandkeys(30659637 KR55WK49264 433.92MHz ID46 S60·S80·V40·V60·XC60·XC70 2007-2018), abkeys(비상키 30699525 HU101 2006-2017)')
SRC_SPA = ('transpondery(XC90 2015+·S90 2017+·V90 2016+·XC60 2016+·V60 2019+·XC40 2020+ Texas Crypto AES), keyshop-online(순정 32256971 ID8A 434MHz HU101 XC60·XC90·S60·S90 2017+), '
           'abkeys(순정 32256971 3키 세트 2016-2021 433MHz YGOHUF8423, 32279988 2키 세트 2021-2024 433MHz, 비상키 31391439 HU101 2018-2025), premiumcarkeys(XC90 31652607 DST AES 8A 433MHz)')

MODELS = [
 ('S40/V40 (구, 1세대)', '2000-2004', [
   seg(2000, 2004, chip='ID44(PCF7935)', immo='이모빌라이저 모듈', keyway='HU56', ktype_hint='막대키',
       src='transpondery(S40 1998–2004·V40 1998–2004 Philips Crypto ID44 PCF7935, JMA TP14·Silca T15), UHS·American Key Supply(S40·V40 1996-2004 HU56 2트랙 트랜스폰더 키 ID44)')]),
 ('S40/V40 (구, 2세대)', '2004-2012', [
   seg(2004, 2012, **P1, src=SRC_P1)]),
 ('V50', '2004-2012', [
   seg(2004, 2012, **P1, src=SRC_P1 + ', transpondery(V50 2004–2012 ID48)')]),
 ('C30', '2007-2013', [
   seg(2007, 2013, **P1, src=SRC_P1 + ', auto-keys.eu(30772202 C30 적용)')]),
 ('V40 (2013~2020)', '2013-2020', [
   seg(2013, 2019, **P3, src=SRC_P3 + ', transpondery(V40 2012–2016 ID46 PCF7953A), 나무위키(V40 국내 2019 단종)')]),
 ('S70', '1998-2000', [
   seg(2000, 2000, chip='ID44(PCF7935)', immo='이모빌라이저 모듈', keyway='NE66', ktype_hint='막대키',
       src='transpondery(S70 1998–2000 Philips Crypto ID44 PCF7935, JMA TP14·Silca T15), locksmithkeyless(NE66 볼보 키웨이)')]),
 ('V70 (1세대)', '1998-2000', [
   seg(2000, 2000, chip='ID44(PCF7935)', immo='이모빌라이저 모듈', keyway='NE66', ktype_hint='막대키',
       src='transpondery(V70 1999–2000 Philips Crypto ID44 PCF7935)')]),
 ('V70 (2세대)', '2000-2007', [
   seg(2000, 2007, **{**P2, 'blade_pn': P2['blade_pn'] + ', ' + P2R}, src=SRC_P2)]),
 ('S60 (1세대)', '2001-2009', [
   seg(2001, 2009, **{**P2, 'blade_pn': P2['blade_pn'] + ', ' + P2R}, src=SRC_P2)]),
 ('S60/V60 (2세대)', '2011-2018', [
   seg(2011, 2018, **P3, src=SRC_P3 + ', 위키백과(2세대 S60 국내 판매)')]),
 ('S60/V60 (3세대)', '2018-현재', [
   seg(2019, 2026, **{**SPA, 'smart': g('32256971[3키 세트]', '32279988[2키 세트]', '31652610', '32256983')},
       src=SRC_SPA + ', transpondery(S60 2018+ OEM 31652610·32256983), 한국일보(3세대 S60 2019.8.27 국내 출시)')]),
 ('C70', '2007-2013', [
   seg(2007, 2013, **{**P1, 'smart': '31300259, ' + g('30772202', '31252739')},
       src=SRC_P1 + ', transpondery(C70 2006–2013 ID48, OEM KR55WK49250 31252739)')]),
 ('S80 (1세대)', '1999-2006', [
   seg(2000, 2006, **{**P2, 'blade_pn': P2['blade_pn'] + ', ' + P2R}, src=SRC_P2 + ', transpondery(S80 1998–1999 ID44 → 1999–2007 ID48)')]),
 ('S80 (2세대)', '2006-2016', [
   seg(2006, 2016, **P3, src=SRC_P3)]),
 ('S90/V90', '2016-현재', [
   seg(2016, 2026, **SPA, src=SRC_SPA + ', 위키백과(S90 2016.9 국내 출시)')]),
 ('ES90 (전기차)', '2025-현재', [
   seg(2026, 2026, chip='확인 불가', immo='확인 불가', keyway='', ktype_hint='스마트키,카드키',
       src='머니투데이·파이낸셜뉴스(ES90 2026.7 국내 출시) — SPA2 신형 키 칩 자료 없음', flag='red', note='SPA2 신형 키·이모빌라이저 자료 없음')]),
 ('EX30 (전기차)', '2024-현재', [
   seg(2024, 2026, chip='확인 불가', immo='확인 불가', keyway='', ktype_hint='카드키', card=g('80001529'),
       src='볼보 부품 카탈로그(EX30 Key Card 80001529, CH-624564), 오토뷰·블로터(EX30 2023.11 사전예약, 2024 국내 출시 — 카드키·디지털키) — 키 칩 자료 없음', flag='red', note='EX30(SEA 플랫폼) 카드키 칩·이모빌라이저 자료 없음')]),
 ('XC40', '2018-현재', [
   seg(2018, 2026, **{**SPA, 'smart': g('32256971[3키 세트]', '32279988[2키 세트]')},
       src='transpondery(XC40 2020+ Texas Crypto AES), keyshop-online·abkeys(32256971 433MHz ID8A HU101), XC40 2018.8 국내 출시')]),
 ('EX40 (전기차)', '2024-현재', [
   seg(2025, 2026, chip='ID8A[추정]', immo='CEM', keyway='HU101', ktype_hint='스마트키', smart='32279988[2키 세트, 추정]',
       src='탑라이더·토픽트리(EX40 2025.6 국내 출시, XC40 리차지 후속) — XC40 CMA 키 기준 추정', flag='orange', note='XC40 리차지 후속 — XC40 키 기준 추정')]),
 ('EC40 (전기차)', '2023-현재', [
   seg(2022, 2026, chip='ID8A[추정]', immo='CEM', keyway='HU101', ktype_hint='스마트키', smart='32279988[2키 세트, 추정]',
       src='나무위키(C40 리차지 2022.2.15 국내 출시, EC40으로 명칭 변경) — XC40 CMA 키 기준 추정', flag='orange', note='C40 리차지(EC40) 전용 키 자료 없음 — XC40 키 기준 추정')]),
 ('XC70 (1세대)', '2003-2007', [
   seg(2003, 2007, **{**P2, 'blade_pn': P2['blade_pn'] + ', ' + P2R}, src=SRC_P2)]),
 ('XC70 (2세대)', '2008-2016', [
   seg(2008, 2016, **P3, src=SRC_P3)]),
 ('XC60 (1세대)', '2013-2017', [
   seg(2009, 2017, **P3, src=SRC_P3 + ', eBay·UHS(30659637 KR55WK49264 XC60 2010-2017), 한국일보(XC60 1세대 2009.6.16 국내 출시)')]),
 ('XC60 (2세대)', '2017-현재', [
   seg(2017, 2026, **SPA, src=SRC_SPA + ', 한국일보(2세대 XC60 2017 국내 출시, 2025.8 부분변경)')]),
 ('XC90 (1세대)', '2003-2015', [
   seg(2003, 2014, **{**P2, 'blade_pn': P2['blade_pn'] + ', ' + P2R}, src=SRC_P2 + ', auto-keys.eu(XC90 5WK49271 433MHz 키리스 세트 31300258)'),
   seg(2015, 2015, **{**P2, 'blade_pn': P2['blade_pn']}, src='transpondery(XC90 2003–2015 Megamos Crypto 48), 다음자동차(XC90 1세대 2015년식 국내 판매), 나무위키(1세대 2015.4 생산 종료, 2세대 2015.5 판매 시작)')]),
 ('XC90 (2세대)', '2015-현재', [
   seg(2015, 2026, **SPA, src=SRC_SPA + ', auto-keys.eu(XC90 Texas Crypto 128bit AES 434MHz 순정, 세트 32256926), 이투데이·오토뷰(국내 판매)')]),
]

GUIDE = [
 '이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.', '',
 '※ 구성',
 "- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 같고, 맨 앞 '브랜드'와 칩코드 뒤 '키종류'를 추가했습니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다.",
 '- 연식은 실제 국내 판매 기준입니다. 원본 목록의 850(1994-1997)은 2000년 이전 모델이라 행이 없습니다.',
 '- 키 부품번호는 국내 사양만 적었습니다. 볼보는 한국 사양 순정 스마트키가 447MHz로 따로 있습니다(31300259, SIEMENS VDO 5WK49352, ID48, P1 S40·V50·C30·C70) — 태그 없이 적었습니다.',
 '- 그 밖의 품번은 유럽형(433/434MHz) 순정 품번이라 [해외 공용 품번]으로 표시했습니다. 미국형(315MHz, LTQV0315TX 30772198·8685150·8688799 등)과 902MHz 품번은 뺐습니다.',
 '- P2(S60 1세대·S80 1세대·V70 2세대·XC70 1세대·XC90 1세대)는 리모컨 일체형 막대키라 리모컨 품번을 키블레이드 칸에 [리모컨키]로 적었습니다. 9203132는 순정 트랜스폰더 블랭크입니다.',
 '- P1(S40·V50·C30·C70)·P3(S80 2세대·V70·XC70 2세대·XC60 1세대·S60·V60 2세대·V40)는 대시보드 슬롯에 꽂는 리모컨 키(키리스 사양은 스마트키)로, 스마트키 칸에 적었습니다.',
 "- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
 '',
 '※ 칩 코드·이모빌라이저(볼보)',
 '- ID44(PCF7935): 1998~2004 S40·V40 1세대·S70·V70 1세대  |  ID48: Megamos Crypto 48(P2·P1, 2000~2014년경)  |  ID46(PCF7953A): Hitag2(P3, 2006~2018년경)  |  ID8A: Texas Crypto AES 128bit(SPA·CMA, 2015년 이후)',
 '- 이모빌라이저: CEM(중앙 전자 모듈)에 키 정보 저장, 키리스 사양은 KVM 함께 사용. 키웨이: NE66(P2·S70·V70 1세대), HU101(P1·P3·SPA 비상키)',
 '',
 '※ 색상',
 '- 주황색: 추정이거나 자료가 서로 다른 값 — 실물 키로 재확인.',
 '- 빨간색: 확인 불가 — EX30(SEA 플랫폼)·ES90(SPA2)은 키 칩·이모빌라이저 자료가 없습니다.',
 '',
 '※ 목록과 국내 판매 연식이 다른 모델',
 '- XC60 1세대: 2009.6.16 국내 출시 → 2009~2017(목록 2013~) / S60 3세대: 2019.8.27 → 2019~ / V40: 2019 단종 → 2013~2019 / EC40(C40 리차지): 2022.2.15 → 2022~ / EX40: 2025.6 → 2025~ / ES90: 2026.7 → 2026~.',
 '- S70·V70 1세대는 2000년식만 기록했습니다(2000년 이전 연식 제외).',
 '',
 '※ 출처',
 '- transpondery.com Volvo Transponder Catalog, auto-keys.eu 볼보 순정 키(주파수·칩·블레이드·한국 사양 447MHz), abkeys.com, 키 판매처(locksmithkeyless·UHS·reidsremotes·keyshop-online), 한국어 위키백과, 국내 출시 기사.',
 '- 연식별 근거는 research/import5/yearly_volvo.md에 있습니다.',
]

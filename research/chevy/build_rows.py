import json
rows=[]
def add(model,years,last_label,**kw):
    for y in years:
        d=dict(model=model,year=str(y)+('(단종)' if last_label and y==years[-1] else ''),chip='',keyway='',card='',fold='',blade_pn='',smart='',immo='',src='',note='')
        for k,v in kw.items():
            d[k]=v(y) if callable(v) else v
        if d.get('flag') is None: d.pop('flag',None)
        rows.append(d)
R=lambda a,b: list(range(a,b+1))

# 공통 출처
ID48='transpondery.com(대우 칼로스 2002-2006·에반다 2003-2006 Megamos Crypto ID48), car-keys-online.com(DWO4R/ID48: 대우 칼로스 2002-2005·쉐보레 칼로스 2005-2008·타쿠마 2001-2006), bestkeysupply.com(TMPro 모듈113 대우/쉐보레 이모박스 ID48)'
FLIP='remkeys.com(아베오·크루즈·올란도·트랙스 2012-2015 2버튼 플립키 ID46 PCF7937/PCF7941E 433MHz HU100, OEM 13500218/13504196/13504273), keyshop-online.com(크루즈 2010-2014 3버튼 플립키 ID46 HU100 433MHz 13500219), auto-keys.eu(쉐보레 순정 플립키 13513927 HITAG2/ID46/PCF7937, HU100, 이모빌라이저 BCM)'
PEPS='abkeys.com(크루즈·임팔라·말리부 2013+ 스마트키 PCF7952E ID46, 433MHz 5912546/13587073), gmplusmall(말리부 2014~2015 스마트키 P13586777)'
HYQ4EA='abkeys.com·bestkeysolution.com(HYQ4EA 433MHz 스마트키 ID46 PCF7937E/NCF2951E, 13508769·13529662·13508771: 카마로·말리부 2016+, 크루즈 2016-2019)'
YG='abkeys.com·locksmithkeyless.com·royalkeysupply.com(YG0G21TB2 433MHz 스마트키 NXP HITAG-PRO ID49 128bit, CR2450)'
NOIMMO_NOTE='국내형 이모빌라이저 미적용'

# 마티즈 II
add('마티즈 II (GM대우, M150)',R(2000,2005),True,chip='확인 불가 (국내형 이모빌라이저 적용 자료 없음)',immo='확인 불가(국내형 적용 자료 없음)',flag='red',
    src=lambda y:'namu.wiki(마티즈Ⅱ M150 2000.8.11 출시~2005), tisdory(후속 올뉴마티즈 국내형 이모빌라이저 미적용)'+(', pechanara.com(마티즈2 M150 [00~05])' if y==2000 else ''),
    note=lambda y:('원본 목록 2002~ — 실제 2000.8 출시 / ' if y==2000 else '')+('2005.2 올 뉴 마티즈로 교체 / ' if y==2005 else '')+'후속 올뉴마티즈 국내형이 이모빌라이저 미적용이라 마티즈Ⅱ도 미적용 가능성 높음(수출형 마티즈는 트랜스폰더 적용) — 실물 키 확인')
add('올 뉴 마티즈 (GM대우, M200)',R(2005,2009),True,chip='해당 없음 (이모빌라이저 미적용)',immo='미적용(국내형)',
    src=lambda y:'tisdory(올뉴마티즈 국내형 이모빌라이저 없음), namu.wiki(올 뉴 마티즈 2005.2.10 양산·판매)',
    note=lambda y:NOIMMO_NOTE+' — 수출형(쉐보레 스파크/마티즈 2007-2013)은 DWO4·ID48 적용'+(' / 2009.8 마티즈 크리에이티브로 교체' if y==2009 else ''))
add('마티즈 크리에이티브 (GM대우, M300)',R(2009,2011),True,chip='해당 없음 (이모빌라이저 미적용)',immo='미적용(국내형, 2013년형까지)',
    src='namu.wiki·thewiki.kr(마티즈 크리에이티브/스파크 M300: 2013년형까지 이모빌라이저·폴딩키 없음, 2014년형부터 이모빌라이저 폴딩키)',
    note=lambda y:NOIMMO_NOTE+(' / 2009.8 출시' if y==2009 else '')+(' / 2011.3 쉐보레 스파크로 차명 변경' if y==2011 else ''))
def spark_chip(y):
    if y<=2012: return '해당 없음 (이모빌라이저 미적용)'
    if y==2013: return '해당 없음(2013년형) / ID46(Hitag2 PCF7941E, 2014년형~)'
    return 'ID46(Hitag2, PCF7941E)'
add('스파크 (쉐보레, M300)',R(2011,2022),True,chip=spark_chip,
    keyway=lambda y:'' if y<=2012 else ('HU100' if y>=2016 else 'HU100 (M400 폴딩키 기준)'),
    fold=lambda y:'' if y<=2014 else ('13579213 (M400 2버튼 폴딩키, 2015.7~)' if y==2015 else '13579213 (2버튼 폴딩키)'),
    immo=lambda y:'미적용(국내형)' if y<=2012 else ('미적용(2013년형) / 트랜스폰더 이모빌라이저(2014년형~)' if y==2013 else 'ID46 트랜스폰더 이모빌라이저(BCM)'),
    flag=lambda y:'orange' if y in (2013,2014) else None,
    src=lambda y:'namu.wiki·thewiki.kr(스파크 M300 2013년형까지 이모빌라이저 없음, 2014년형부터 이모빌라이저 폴딩키)'+(', gmplusmall(더뉴/더넥스트 스파크 폴딩키 13579213: PCF7941E Hitag2 ID46, 433MHz, HU100)' if y>=2015 else ', keydiy·ebay(미국형 스파크 2013-2016 ID46 GM EXT PCF7937E / 플립키 PCF7941E)')+(', wikipedia(M400 2015.7 국내 출시)' if y==2015 else ''),
    note=lambda y:('2011.3 마티즈 크리에이티브에서 차명 변경 / ' if y==2011 else '')+('2014년형(2013 하반기 출시)부터 이모빌라이저 — 연식(형)으로 구분 / ' if y==2013 else '')+('M300 2014~2015년형 폴딩키 품번 자료 없음 — M400 폴딩키(13579213)·미국형 자료 기준 / ' if y in (2013,2014) else '')+('2015.7 M400(더 넥스트 스파크)로 세대 교체 — M300(~2015.6)은 품번 미확인 / ' if y==2015 else '')+('2022.8 생산 종료' if y==2022 else '').rstrip(' /'))
# 칼로스·젠트라
add('칼로스 (GM대우)',R(2002,2007),True,chip='ID48(Megamos Crypto) — 수출형 기준',keyway='DWO4R',immo='ID48 이모빌라이저 박스(수출형 기준) — 국내형 적용 여부 미확인',flag='orange',
    src=lambda y:ID48+(', wikipedia(칼로스 2002.5.2 출시)' if y==2002 else '')+(', mobilityhumanities.org(칼로스 2002.5~2007.10 생산)' if y==2007 else ''),
    note=lambda y:'칩은 수출형 칼로스/아베오(T200) 자료 — 국내형 이모빌라이저 적용 자료 없음, 실물 키 확인'+(' / 2007.10 생산 종료' if y==2007 else ''))
add('젠트라 (GM대우)',R(2005,2011),True,chip='ID48(Megamos Crypto) — 수출형 기준',keyway='DWO4R',immo='ID48 이모빌라이저 박스(수출형 기준) — 국내형 적용 여부 미확인',flag='orange',
    src=lambda y:ID48+', locksmithkeyless.com(아베오 T250 2004-2011 ID48 DWO4RT6, OE 96650592)'+(', wikipedia(젠트라 2005.9 출시)' if y==2005 else '')+(', encar(젠트라 2011.2 단종)' if y==2011 else ''),
    note=lambda y:'칩은 수출형 아베오 T250/칼로스 자료 — 국내형 적용 자료 없음'+(' / 2007.10 해치백 젠트라 X 추가' if y==2007 else '')+(' / 2011.2 단종, 아베오로 교체' if y==2011 else ''))
add('아베오 (쉐보레, T300)',R(2011,2016),True,chip='ID46(Hitag2, PCF7937/PCF7941E)',keyway='HU100',fold='13500218 / 13504196 / 13504273 (2버튼 폴딩키)',immo='ID46 트랜스폰더 이모빌라이저(BCM)',
    src=lambda y:FLIP+(', brunch/heydealer·namu.wiki(아베오 T300 2011.3~2016.12 판매)' if y in (2011,2016) else ''),
    note=lambda y:('2011.3 출시' if y==2011 else '')+('2016.12 판매 종료' if y==2016 else '')+(' / ' if y in (2011,2016) else '')+'폴딩키 품번은 수출형(아베오/크루즈 공용 433MHz) 기준')
# 라세티
add('라세티 (GM대우, J200, 1세대)',R(2002,2008),True,chip='ID60(4D60) — 수출형 기준',keyway='DWO4R',immo='트랜스폰더 이모빌라이저(수출형 기준) — 국내형 적용 여부 미확인',flag='orange',
    src=lambda y:'autokeyshop.ru·smartkeys.ru(라세티 2004-2013 4D60 칩, DWO4R — 누비라 2000+는 ID48), dkgcc.com(옵트라/라세티 3버튼 리모컨키 433MHz 4D-60)'+(', wikipedia(라세티 2002.11.18 출시)' if y==2002 else ''),
    note=lambda y:'칩은 수출형 라세티/옵트라 자료(2004년 이후) — 국내형 적용 및 2002~2003년식 칩 자료 없음'+(' / 2008.11 라세티 프리미어로 교체' if y==2008 else ''))
add('라세티 프리미어 (GM대우, J300)',R(2008,2011),True,chip='ID46(Hitag2, PCF7941E 폴딩키 / PCF7952 스마트키)',keyway='HU100',fold='폴딩키(수출형 13500218 계열, 국내 품번 미확인)',
    smart='버튼시동 스마트키(상위 트림, 품번 미확인)',immo='ID46 트랜스폰더 이모빌라이저(BCM) / PEPS 스마트키',flag='orange',
    src=lambda y:FLIP+', blog.gm-korea.co.kr(라세티 프리미어 버튼타입 스마트키, 방전 시 컵홀더 밑 키 슬롯), blog.daum.net/locksmith(크루즈 스마트키 = 올란도·베리타스·알페온 동일 쉐보레 폴딩 스마트키)',
    note=lambda y:('2008.11 출시 / ' if y==2008 else '')+('2011.3 쉐보레 크루즈로 차명 변경 / ' if y==2011 else '')+'칩은 같은 차(크루즈 J300) 수출형 자료 기준 — 국내 품번 미확인')
add('크루즈 (쉐보레, J300, 1세대)',R(2011,2017),True,chip='ID46(Hitag2, PCF7941E 폴딩키 / PCF7952 스마트키)',keyway='HU100',fold='13500218 / 13504196 / 13500219 (폴딩키, 수출형)',
    smart='스마트키(PCF7952E ID46 433MHz 계열, 국내 품번 미확인)',immo='ID46 트랜스폰더 이모빌라이저(BCM) / PEPS 스마트키',
    src=lambda y:FLIP+', '+PEPS+(', danawa(크루즈 J300 2011.3~2015.1, 어메이징 뉴 크루즈 2015.1~2017.11)' if y in (2011,2015,2017) else ''),
    note=lambda y:('2011.3 라세티 프리미어에서 차명 변경 / ' if y==2011 else '')+('2015.1 어메이징 뉴 크루즈 / ' if y==2015 else '')+('원본 목록 종료 2016 — 실제 2017.11까지 판매 / ' if y==2017 else '')+'스마트키는 상위 트림')
add('크루즈 (쉐보레, D2XX, 2세대)',R(2017,2019),True,chip='ID46(Hitag2, PCF7937E)',keyway='HU100',smart='13508771 / 13508769 (HYQ4EA 433MHz, 수출형)',
    immo='PEPS 스마트키 / ID46 이모빌라이저(BCM)',
    src=lambda y:HYQ4EA+(', danawa(올 뉴 크루즈 D2LC 2017.1~2019.7)' if y in (2017,2019) else ''),
    note=lambda y:('원본 목록 2018~ — 실제 2017.1 출시 / ' if y==2017 else '')+('2018 군산공장 폐쇄로 생산 종료, 재고 2019.7까지 / ' if y==2019 else '')+'하위 트림 폴딩키 품번 자료 없음')
add('볼트 (쉐보레, Volt, 플러그인 하이브리드)',R(2016,2019),True,chip='ID46(Hitag2 Extended)',keyway='HU100',smart='13529664 / 13585722 (HYQ4AA, 미국형 315MHz) — 국내형 품번 미확인',
    immo='PEPS 스마트키',flag='orange',
    src=lambda y:'northcoastkeyless.com·uhs-hardware.com(볼트 2016-2019 스마트키 HYQ4AA 13585722/13508767/13529664, ID46), kama.or.kr·namu.wiki(2세대 볼트 2016.8 렌터카·카셰어링 공급, 2017.4 일반 출시, 2019.3 단종)',
    note=lambda y:('원본 목록 2011~ — 1세대(2011-2015)는 국내 미출시, 2세대 2016.8부터 / ' if y==2016 else '')+('2019.3 단종 / ' if y==2019 else '')+'국내형은 433MHz 사양일 가능성 — 미국형 품번 기준')
# 매그너스·토스카
add('매그너스 (GM대우)',R(2000,2006),True,chip='ID48(Megamos Crypto) — 수출형(에반다) 기준',keyway='DWO5',immo='ID48 이모빌라이저(수출형 기준) — 국내형 적용 여부 미확인',flag='orange',
    src=lambda y:'transpondery.com(대우 에반다 2003-2006 Megamos ID48), car-keys-online.com(DWO5R/ID48 대우 레간자), wikipedia(매그너스 = 쉐보레 에반다/에피카)'+(', ko.wikipedia(매그너스 1999.12 판매 시작)' if y==2000 else ''),
    note=lambda y:('원본 목록 2002~ — 실제 1999.12 출시 / ' if y==2000 else '')+('2006.1 토스카 출시로 단종 / ' if y==2006 else '')+'국내형 이모빌라이저 적용 자료 없음(국내 토스카도 2007년형부터 적용) — 실물 키 확인')
add('토스카 (GM대우/쉐보레)',R(2006,2011),True,chip=lambda y:'해당 없음(2006년형) / ID60(4D60, 2007년형~)' if y==2006 else 'ID60(4D60)',
    immo=lambda y:'미적용(2006년형) / 이모빌라이저(2007년형, 2006.11~)' if y==2006 else '트랜스폰더 이모빌라이저',flag='orange',
    src=lambda y:'etoday.co.kr·namu.wiki(2007년형 토스카 2006.11 출시, 이모빌라이저 신규 적용), smartkeys.ru(에피카 2버튼 리모컨키 4D-60), 군산희망열쇠 blog.daum.net/cider5851(토스카 이모빌라이저 키·일반 키 차량 공존)',
    note=lambda y:('2006.1 출시 — 2006년형은 이모빌라이저 없음 / ' if y==2006 else '')+('2011.11 말리부로 교체 / ' if y==2011 else '')+'칩은 같은 차(쉐보레 에피카) 수출형 자료 — 국내 순정 키 칩 직접 자료 없음')
add('말리부 (쉐보레, 8세대)',R(2011,2016),True,chip='ID46(Hitag2, PCF7941E 폴딩키 / PCF7952 스마트키)',keyway='HU100',smart=lambda y:'P13586777 (2014~2015)' if y in (2014,2015) else '스마트키(PCF7952 433MHz 계열, 품번 미확인)',
    fold='폴딩키(품번 미확인)',immo='ID46 트랜스폰더 이모빌라이저(BCM) / PEPS 스마트키',
    src=lambda y:PEPS+', '+FLIP+', namu.wiki(말리부 8세대 트림별 버튼시동·스마트키)',
    note=lambda y:('2011.11 출시 / ' if y==2011 else '')+('2016.4 9세대로 교체 / ' if y==2016 else '')+'스마트키는 트림별')
add('말리부 (쉐보레, 9세대)',R(2016,2022),True,chip='ID46(Hitag2, PCF7937E)',keyway='HU100',smart='13508769 / 13529662 (HYQ4EA 433MHz)',immo='PEPS 스마트키 / ID46 이모빌라이저(BCM)',
    src=lambda y:HYQ4EA+(', namu.wiki(말리부 9세대 2022.7 발주 중단·8.23 생산 종료, 재고 2023 상반기까지)' if y==2022 else ''),
    note=lambda y:('2016.4 출시' if y==2016 else '')+('2022.8 생산 종료(재고 판매 2023 상반기)' if y==2022 else ''))
add('알페온 (GM대우→쉐보레)',R(2010,2015),True,chip='ID46(Hitag2, PCF7952E 스마트키 / PCF7937E 폴딩키)',keyway='HU100',smart='스마트키(PCF7952E ID46, 국내 품번 미확인)',fold='5913397 (OHT01060512, 미국형 라크로스)',
    immo='PEPS 스마트키 / ID46 이모빌라이저(BCM)',flag='orange',
    src=lambda y:'wikipedia(알페온 = 뷰익 라크로스 2010-2015), locksmithkeyless.com(라크로스 2010-2013 폴딩키 OHT01060512 ID46 HU100 5913397), ebay·abkeys(라크로스 2010-2016 스마트키 PCF7952E ID46), blog.daum.net/locksmith(알페온 = 크루즈와 같은 쉐보레 폴딩 스마트키)'+(', namu.wiki(2015.8 생산 종료, 재고 2016.12까지)' if y==2015 else ''),
    note=lambda y:('2010.9 출시 / ' if y==2010 else '')+('2015.8 생산 종료 / ' if y==2015 else '')+'칩은 뷰익 라크로스 자료 기준 — 국내 품번 미확인')
add('임팔라 (쉐보레)',R(2015,2020),True,chip='ID46(Hitag2, PCF7952E 스마트키 / PCF7937E 폴딩키)',keyway='HU100',smart='5912546 / 13587073 (433MHz 스마트키, 수출형)',fold='13504199 (OHT01060512, 미국형 플립키)',
    immo='PEPS 스마트키 / ID46 이모빌라이저(BCM)',
    src=lambda y:'abkeys.com(임팔라·말리부 스마트키 PCF7952E ID46 HU100 433MHz 5912546/13587073), northcoastkeyless.com(임팔라 2014-2020 플립키 OHT01060512 13504199)'+(', hankookilbo·kyeongin(임팔라 2015.9 국내 판매)' if y==2015 else '')+(', carwiki(2018년형 상위 트림 버튼시동&스마트키)' if y==2018 else '')+(', namu.wiki(2020 단종)' if y==2020 else ''),
    note=lambda y:('2015.9 출시 / ' if y==2015 else '')+('원본 목록 종료 2018 — 실제 2020 단종 / ' if y==2020 else '')+'스마트키는 상위 트림, 하위 트림은 플립키')
add('레조 (GM대우, Rezzo)',R(2000,2007),True,chip='ID48(Megamos Crypto) — 수출형(타쿠마) 기준',keyway='DWO4R',immo='ID48 이모빌라이저(수출형 기준) — 국내형 적용 여부 미확인',flag='orange',
    src=lambda y:'wikipedia(레조 = 대우 타쿠마, 2000~2008), car-keys-online.com(DWO4R/ID48: 대우 타쿠마 2001-2006), '+ID48.split(', ')[-1]+(', ko.wikipedia(레조 2000.1 생산 시작)' if y==2000 else '')+(', mediawatch·cctimes(레조 2007.6 단종)' if y==2007 else ''),
    note=lambda y:('원본 목록 2002~ — 실제 2000.1 출시 / ' if y==2000 else '')+('원본 목록 종료 2008 — 실제 2007.6 단종 / ' if y==2007 else '')+'국내형 이모빌라이저 적용 자료 없음 — 실물 키 확인')
add('올란도 (쉐보레)',R(2011,2018),True,chip='ID46(Hitag2, PCF7941E 폴딩키)',keyway='HU100',fold='13500218 / 13504196 / 13504273 (2버튼 폴딩키, 수출형)',
    smart='스마트키(ID46 PCF7952 계열 / PCF7938X 표기 1곳 — 상충)',immo='ID46 트랜스폰더 이모빌라이저(BCM) / PEPS 스마트키',flag='orange',
    src=lambda y:FLIP+', autokeymaster·aliexpress(올란도 스마트 리모컨 433MHz PCF7938X), blog.daum.net/locksmith(올란도 = 크루즈 쉐보레 폴딩 스마트키)'+(', namu.wiki(2018.7 생산 중단, 연말 재고 소진 후 단종)' if y==2018 else ''),
    note=lambda y:('2011.2 출시 / ' if y==2011 else '')+('2018 단종 / ' if y==2018 else '')+'폴딩키 칩은 확인 — 스마트키 칩 표기 상충(PCF7952 계열 vs PCF7938X)')
add('G2X (GM대우)',R(2007,2008),True,chip='ID46(PK3+, Circle Plus)',keyway='B111',immo='PassKey 3+ 이모빌라이저',
    src=lambda y:'amazon/RI-KEY(새턴 스카이 2007-2010 B111 ID46 Circle Plus), locksmithkeyless.com(폰티악 2005-2010 ID46 GM 칩 B111-PT), wikipedia(G2X = 새턴 스카이·폰티악 솔스티스 카파 플랫폼)'+(', namu.wiki(G2X 2007.8.6 출시)' if y==2007 else ', namu.wiki(2008.9.30 수입 중단·단종)'),
    note=lambda y:'2007.8 출시' if y==2007 else '원본 목록 종료 2010 — 실제 2008.9 수입 중단')
add('카마로 (쉐보레, 5세대)',R(2011,2015),True,chip='ID46(Hitag2, PCF7937E)',keyway='HU100',fold='13504199 / 13504200 (OHT01060512 플립키, 미국형 315MHz)',immo='ID46 트랜스폰더 이모빌라이저(BCM)',
    src=lambda y:'abkeys.com·myremotekey.com(카마로·말리부 2010+ 플립키 OHT01060512 ID46 PCF7937E HU100, 13504199/13504200), locksmithkeyless.com(카마로 2015 플립키)',
    note=lambda y:'국내형 433MHz 사양 품번 미확인 — 미국형 품번 기준')
add('카마로 (쉐보레, 6세대)',R(2016,2022),True,chip='ID46(Hitag2, PCF7937E)',keyway='HU100',smart='13508769 / 13529662 (HYQ4EA 433MHz)',immo='PEPS 스마트키 / ID46 이모빌라이저(BCM)',
    src=lambda y:HYQ4EA+', tlkeys.com(순정 카마로 2016 스마트키 13508769)'+(', dealsite·autotribune(카마로 6세대 2016.6 국내 도입)' if y==2016 else '')+(', autotribune(국내 11년간 1,941대 판매 후 단종)' if y==2022 else ''),
    flag=lambda y:'orange' if y>=2019 else None,
    note=lambda y:('2016.6 출시 / ' if y==2016 else '')+('원본 목록 종료 2018 — 이후에도 카마로 SS 판매(2011~ 11년 판매 후 단종) — 정확한 종료 연도 자료 상충(2022~2024) / ' if y>=2019 else ''))
add('콜벳 (쉐보레, C7)',R(2014,2019),True,chip='ID46(Hitag2, PCF7952E)',keyway='HU100',smart='23465951 / 22779880 (NBGGD9C04 434MHz, 쿠페 5버튼)',immo='PEPS 스마트키',flag='orange',
    src='uhs-hardware.com·abkeys.com(콜벳 2014-2019 스마트키 NBGGD9C04 PCF7952E ID46 434MHz 23465951/22779880), motorgraph.com·namu.wiki(한국GM C7 출시 무기한 연기 — 공식 판매는 C6(2012)뿐, 직수입만 존재)',
    note='한국GM 공식 미판매(직수입 차량만) — 원본 목록과 상충 / 컨버터블은 6버튼 키')
add('콜벳 (쉐보레, C8)',R(2022,2026),False,chip='ID49(Hitag Pro, NXP AES 128bit)',smart='13538852 / 13545157 (YG0G20TB1 433MHz, 7버튼)',immo='PEPS 스마트키(Hitag Pro)',flag='orange',
    src='americankeysupply.com·uhs-hardware.com(콜벳 C8 2020-2024 스마트키 YG0G20TB1 Hitag Pro ID49 434MHz, 13538852 등), hankookilbo(2021.3 국내 출시 미정), sisaweek(AP오토모티브 등 수입업체 판매), zdnet(2025 E-Ray 시승 — 공식 출시 발표 없음)',
    note='한국GM 공식 출시 발표 없음(수입업체 판매) — 원본 목록과 상충')
# 트랙스
add('트랙스 (쉐보레, 1세대)',R(2013,2022),True,chip='ID46(Hitag2, PCF7941E)',keyway='HU100',fold=lambda y:'13500218 / 13504196 / 13504273 (2버튼 폴딩키, 수출형)' if y<=2016 else '폴딩키(더 뉴 트랙스, 국내 품번 미확인)',
    immo='ID46 트랜스폰더 이모빌라이저(BCM)',
    src=lambda y:FLIP+', uhs-hardware·ebay(미국형 트랙스 2013-2021 플립키 13504265 ID46 / 2019-2022 13530736)'+(', namu.wiki(2022.8 내수 생산 종료, 11.4 홈페이지 삭제)' if y==2022 else ''),
    note=lambda y:('2013.2 출시 / ' if y==2013 else '')+('원본 목록 종료 2019 — 실제 2022.11까지 판매 / ' if y==2022 else '')+('버튼시동 스마트키 적용 여부 자료 없음' if y>=2017 else ''))
add('트랙스 크로스오버 (쉐보레, 2세대)',R(2023,2026),False,chip='ID46(Hitag2)',keyway='HU100',smart='13530712 (HYQ4ES, LT 이상)',fold='폴딩키(LS, 품번 미확인)',immo='PEPS 스마트키 / ID46 이모빌라이저',
    src='ebay(2024-2025 트랙스 순정 스마트키 HYQ4ES 13530712 엔진 이모빌라이저), sffobsinc.com(HYQ4ES: 블레이저·볼트·트레일블레이저·트래버스·트랙스 2021-2026), enjoyyourpost.com(트랙스 크로스오버 LT 트림부터 버튼시동)',
    note=lambda y:('2023.3 출시 / ' if y==2023 else '')+'LS는 키 시동, LT 이상 스마트키'+(' / 2026년식 자료 없음' if y==2026 else ''))
add('트레일블레이저 (쉐보레, 소형 SUV)',R(2020,2026),False,chip='ID46(Hitag2)',keyway='HU100',smart='13530712 / 13530713 (HYQ4ES 433MHz, LT 이상)',fold='폴딩키(LS, 품번 미확인)',immo='PEPS 스마트키 / ID46 이모빌라이저',
    src='keyecu·ebay(트레일블레이저 2021-2025 스마트키 HYQ4ES 13530712/13530713 433MHz ID46), encar mocha·namu.wiki(LS 트림 버튼시동 선택 불가, LT부터 스마트키)',
    note=lambda y:('2020.1 출시 / ' if y==2020 else '')+'LS는 키 시동, LT 이상 스마트키'+(' / 2026년식 자료 없음' if y==2026 else ''))
add('볼트 EV (쉐보레)',R(2017,2023),True,chip=lambda y:'ID46(Hitag2)' if y<=2021 else 'ID46(Hitag2) / ID49(Hitag Pro) — 자료 상충',keyway='HU100',
    smart=lambda y:'13585722 / 13529664 / 13508767 (HYQ4AA, 미국형 315MHz)' if y<=2021 else '13535663 / 13547839 (HYQ4ES 433MHz, 5버튼)',immo='PEPS 스마트키',flag='orange',
    src=lambda y:('uhs-hardware.com·locksmithkeyless.com(볼트 EV 2017-2021 스마트키 HYQ4AA Philips ID46, 13585722/13529664/13508767)' if y<=2021 else 'amazon·royalkeysupply.com(볼트 EV 2022-2023 스마트키 HYQ4ES 13535663/13547839 — ID46 / 일부 ID49 표기)')+(', zdnet·namu.wiki(2023.12 단종, 2024.1 판매 중단)' if y==2023 else ''),
    note=lambda y:('국내형 433MHz 품번 미확인 — 미국형 기준' if y<=2021 else '2022 부분변경 — 칩 표기 상충(ID46 vs ID49)')+(' / 2023.12 단종' if y==2023 else ''))
add('볼트 EUV (쉐보레)',R(2022,2023),True,chip='ID46(Hitag2) / ID49(Hitag Pro) — 자료 상충',keyway='HU100',smart='13535665 / 13535664 (HYQ4ES 433MHz)',immo='PEPS 스마트키',flag='orange',
    src=lambda y:'remotesandkeys.com·northcoastkeyless.com(볼트 EUV 2022-2023 스마트키 HYQ4ES 13535665, 433MHz ID46), transponderisland.com(13535664), media.gmc.com(2021.8 볼트 EUV 국내 제원 공개)'+(', zdnet(2023.12 단종)' if y==2023 else ''),
    note=lambda y:('원본 목록 2021~ — 2021.8 제원 공개 후 배터리 리콜로 출고 지연, 2022년 출고 / ' if y==2022 else '2023.12 단종 / ')+'칩 표기 상충(ID46 vs ID49)')
# 윈스톰·캡티바
add('윈스톰 (GM대우)',R(2006,2011),True,chip='ID46(Hitag2, PCF7936)',keyway='DWO5',fold='폴딩 리모컨키(국내 품번 미확인)',immo='ID46 트랜스폰더 이모빌라이저',
    src=lambda y:'originalkey.ru(쉐보레 캡티바 C100(=윈스톰) 2007-2013 PCF7936 ID46, DWO5, 433MHz), blog.daum.net/13114(윈스톰 이모빌라이저 키 추가 등록 방법)'+(', namu.wiki(윈스톰 2006.6.7 출시)' if y==2006 else '')+(', namu.wiki(2011.4 캡티바로 변경)' if y==2011 else ''),
    note=lambda y:('2006.6 출시 / ' if y==2006 else '')+('2011.4 쉐보레 캡티바로 페이스리프트·차명 변경' if y==2011 else '칩은 같은 차 수출형(캡티바 C100) 자료 기준').rstrip(' /'))
add('윈스톰 맥스 (GM대우)',R(2008,2010),True,chip='ID46(Hitag2, PCF7936)',keyway='DWO5',immo='ID46 트랜스폰더 이모빌라이저',flag='orange',
    src=lambda y:'originalkey.ru(캡티바 C100 2007-2013 PCF7936 ID46 DWO5), namu.wiki(윈스톰 맥스 C105 2008.6.18 시판, 2010.12 단종)',
    note=lambda y:('2008.6 출시 / ' if y==2008 else '')+('2010.12 단종 / ' if y==2010 else '')+'윈스톰 숏바디 — 윈스톰 기준 추정')
add('캡티바 (쉐보레, 1세대)',R(2011,2018),True,chip='ID46(Hitag2, PCF7936 키 / PCF7952A 스마트키)',keyway='DWO5 / HU100 — 자료 상충',smart='스마트키(PCF7952A ID46 433MHz, 홀덴 캡티바 2014-2018 기준)',
    immo='ID46 트랜스폰더 이모빌라이저 / PEPS 스마트키',flag='orange',
    src=lambda y:'originalkey.ru(캡티바 C100 2007-2013 PCF7936 ID46 DWO5 433MHz), autokeymaster(캡티바 2013-2016 스마트키 PCF7952 434MHz 4버튼), keyecu.com(홀덴/쉐보레 캡티바 2014-2018 스마트키 PCF7952A ID46 433MHz)'+(', namu.wiki(2018.5 생산 중단, 재고 판매 후 단종)' if y==2018 else ''),
    note=lambda y:('2011.4 윈스톰에서 차명 변경 / ' if y==2011 else '')+('2018 단종(이쿼녹스로 대체) / ' if y==2018 else '')+'국내 스마트키 적용 트림·품번 자료 없음, 블레이드 표기 상충')
add('캡티바 (쉐보레, 2세대, 리뱃지)',[2024],False,chip='',immo='',flag='red',
    src='검색 결과(2023.8 바오준 530 기반 2세대 캡티바는 중남미·동남아 판매, 국내 미출시)',
    note='국내 미출시 차종 — 원본 목록 오류로 보임, 행 삭제 검토')
rows[-1]['year']='2024 (국내 미출시)'
add('이쿼녹스 (쉐보레, 가솔린)',[y for y in R(2018,2024)],True,chip='ID46(Hitag2)',keyway='HU100',smart=lambda y:'13585720 / 13529648 (HYQ4EA 433MHz)',immo='PEPS 스마트키 / ID46 이모빌라이저(BCM)',
    flag=lambda y:'orange' if y>=2023 else None,
    src=lambda y:'amazon·key4.com(이쿼녹스 2018-2022 스마트키 HYQ4EA 433MHz Philips ID46, 13585720/13529648)'+(', encar(2018.6.7 국내 출시)' if y==2018 else '')+(', namu.wiki(2021.3 수입 중단)' if y==2021 else '')+(', gpkorea(2022.6 더 넥스트 이쿼녹스 재출시)' if y==2022 else '')+(', namu.wiki(2024.4 홈페이지에서 삭제·단종)' if y==2024 else ''),
    note=lambda y:('2018.6 출시' if y==2018 else '')+('2021.3 수입 중단 — 2021년식 재고분만' if y==2021 else '')+('2022.6 더 넥스트 이쿼녹스(부분변경) 재출시' if y==2022 else '')+('원본 목록 종료 2020 — 실제 2024.4까지 판매 / HYQ4EA 적용 자료는 2022년까지' if y>=2023 else ''))
add('이쿼녹스 EV (쉐보레)',[2024],False,chip='',immo='',flag='red',
    src='ebn.co.kr(한국GM 이쿼녹스 EV 출시 계획 최종 철회), bloter(1년째 출시 약속 못 지킴), sisajournal-e(2024.9 환경부 인증)',
    note='국내 미출시(인증 후 출시 철회) — 참고: 미국형은 YG0G21TB2 Hitag Pro ID49 스마트키, 행 삭제 검토')
rows[-1]['year']='2024 (국내 미출시)'
add('트래버스 (쉐보레)',R(2019,2025),True,chip='ID46(Hitag2)',keyway='HU100',smart=lambda y:'13591384 (HYQ4EA 433MHz, 3버튼)' if y<=2020 else 'HYQ4ES 433MHz (품번 미확인)',immo='PEPS 스마트키 / ID46 이모빌라이저',
    flag=lambda y:'orange' if y>=2021 else None,
    src=lambda y:('abkeys.com(블레이저·트래버스 2018+ 순정 스마트키 13591384 433MHz HYQ4EA), americankeysupply(이쿼녹스/트래버스 2018-2020 HYQ4EA)' if y<=2020 else 'keyecu.com(블레이저·트래버스 2021-2023 스마트키 HYQ4ES/HYQ4AS ID46)')+(', top-rider(트래버스 2019.9 국내 출시)' if y==2019 else '')+(', namu.wiki(2025.3 판매 종료)' if y==2025 else ''),
    note=lambda y:('2019.9 출시' if y==2019 else '')+('2021년 이후 키 교체(HYQ4ES) 여부는 판매처 적용표 기준' if y>=2021 else '')+(' / 2025.3 판매 종료, 3세대 국내 미출시' if y==2025 else ''))
add('타호 (쉐보레)',R(2022,2025),True,chip='ID49(Hitag Pro, NXP 128bit)',keyway='HU100',smart='13548442 (4버튼) / 13537962 (6버튼) (YG0G21TB2 433MHz)',immo='PEPS 스마트키(Hitag Pro)',
    src=lambda y:YG+', remotesandkeys.com(2023 타호 스마트키 13548442), amazon(서버번·타호 2021-2025 YG0G21TB2 13537962)'+(', sedaily·news1(타호 2022.1 국내 출시)' if y==2022 else '')+(', namu.wiki(2025.3.2 판매 종료)' if y==2025 else ''),
    note=lambda y:('2022.1 출시' if y==2022 else '')+('2025.3 판매 종료, 부분변경 모델 국내 미출시' if y==2025 else ''))
add('서버번 (쉐보레)',R(2023,2026),False,chip='ID49(Hitag Pro, NXP 128bit)',keyway='HU100',smart='13537962 / 13548431 (YG0G21TB2 433MHz, 6버튼)',immo='PEPS 스마트키(Hitag Pro)',flag='orange',
    src=YG+', amazon(서버번·타호 2021-2025 YG0G21TB2 13537962/13548431), explorervan.co.kr(서버번 국내 판매 — 수입업체), namu.wiki(한국GM 도입 검토만)',
    note='한국GM 공식 출시 자료 없음(수입업체 판매만 확인) — 원본 목록과 상충')
def col_chip(y):
    if y<=2023: return 'ID46(PK3+, Philips 46E)'
    if y==2024: return 'ID46(2세대, ~2024.4) / ID49(Hitag Pro, 3세대 2024.7~)'
    return 'ID49(Hitag Pro, NXP 128bit)'
add('콜로라도 (쉐보레)',R(2019,2026),False,chip=col_chip,keyway=lambda y:'HU100 (B119)' if y<=2024 else 'HU100',
    blade_pn=lambda y:'' if y>=2025 else ('23209427 (2세대 트랜스폰더 키)' if y<=2023 else '23209427 (2세대)'),
    smart=lambda y:'' if y<=2023 else ('13548441 (YG0G21TB2 433MHz, 3세대)' ),
    immo=lambda y:'ID46 트랜스폰더 이모빌라이저(키 시동, 리모컨 별도)' if y<=2023 else ('ID46 트랜스폰더(2세대) / PEPS 스마트키 Hitag Pro(3세대)' if y==2024 else 'PEPS 스마트키(Hitag Pro)'),
    src=lambda y:('carandtruckremotes.com·oemcarkeymall.com(콜로라도 2015-2021 트랜스폰더 키 23209427 B119-PT ID46 HU100), coloradofans.com(2019 콜로라도 키 시동·리모컨 분리)' if y<=2024 else '')+(', ' if y==2024 else '')+('royalkeysupply.com·locksmithkeyless.com(2023-2025 콜로라도 스마트키 YG0G21TB2 13548441 Hitag Pro ID49)' if y>=2024 else '')+(', edaily(콜로라도 2019.8 국내 출시)' if y==2019 else '')+(', autocast·jasonryu.net(3세대 올 뉴 콜로라도 2024.7.15 국내 출시), namu.wiki(2세대 2024.4 홈페이지 삭제)' if y==2024 else ''),
    note=lambda y:('2019.8 출시' if y==2019 else '')+('2세대 2024.4 판매 종료 → 3세대 2024.7 출시' if y==2024 else '')+('2026년식 자료 없음' if y==2026 else ''))
for r in rows: r['note']=r['note'].strip(' /')
open('rows.jsonl','w').write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
from collections import Counter
print(len(rows)); print(Counter(r.get('flag') for r in rows))

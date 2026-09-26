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
TM='tmpro2.com·abkeys.com(TMPro 모듈85 쌍용 VDO 이모박스: 무쏘·코란도·렉스턴 2002-2006, 메가모스 크립토/TS48, MC68HC05B16)'
AK='auto-keys.eu(쌍용 순정 키 87170-32030·32020·08D50 TMS37145 4D-60 80bit / 87170-08B21 4D-60 40bit, 블레이드 SSA2P)'
ICU='kpartsmall.com·autoecupart.net(이모빌라이저 컨트롤 유닛 87110-08B00/09000: 렉스턴 2006.02~2017.04, 카이런 2005.05~2007.03, 액티언 2005.10~2007.03, 액티언스포츠 2006.04~2007.03)'
FLIP='remkeys.com(순정 3버튼 폴딩키 87510-21100 ID70 DST80 433MHz, 블레이드 TOY48 — 코란도 2010-2019·로디우스II 2012-2019·액티언·티볼리 2015), 3dgroupuk.com(SSR1: 87510-21100 80bit ID8E, 블레이드 KI-7 품번 7105121500 — 티볼리 2016-2022·액티언스포츠·코란도·렉스턴)'

# 체어맨 H
add('체어맨 (1세대, H)',R(2000,2014),True,chip='ID60(4D60) 추정',keyway='',immo='확인 불가(모듈 명칭)',flag='orange',
    src=lambda y:'myremotekey.com(4D60 칩 트랜스폰더키: 쌍용 체어맨·액티언·카이런·렉스턴), wikipedia(체어맨 1997-2017, W124 플랫폼)'+(', carisyou.com(체어맨 H 2014.12.31 단종)' if y>=2011 else '')+(', danawa(체어맨 H 뉴 클래식 2011.5.27 출시)' if y==2011 else ''),
    note=lambda y:('원본 목록 종료 2008 — 실제로는 체어맨 H(뉴 클래식 포함) 2014.12 단종까지 판매' if y==2008 else ('2014.12.31 단종' if y==2014 else ''))+(' / ' if y in(2008,2014) else '')+'체어맨 연식별 칩 자료 없음 — 쌍용 공용 4D60 키 판매처 목록 기준 추정')
# 체어맨 W
add('체어맨 (2세대, W)',R(2008,2017),True,chip='ID60(4D60) 추정',immo='확인 불가(모듈 명칭)',flag='orange',
    src=lambda y:'myremotekey.com(4D60 칩 쌍용 체어맨 포함), carisyou.com/namu.wiki(체어맨 W 2017.12 생산 종료)',
    note=lambda y:('원본 목록 종료 2024 — 실제 2017.12 단종 / ' if y==2017 else '')+'체어맨 W 스마트키 칩 자료 없음 — 추정값, 실물 확인 필요')
# 코란도 2세대
add('코란도 (2세대)',R(2000,2005),True,chip='ID48(Megamos Crypto)',keyway='HYN10 (JMA HY-5.P1)',immo='VDO 이모빌라이저 박스(이모박스)',
    src=lambda y:TM+', reidsremotes.com.au(코란도 2000-2006 트랜스폰더키 HYN10/HY-5.P1)',
    flag=lambda y:'orange' if y<2002 else None,
    note=lambda y:'TMPro 이모박스 자료가 2002년부터 — 2000·2001년식 이모박스 적용 여부 직접 확인 안 됨' if y<2002 else '')
add('뉴 코란도',R(2005,2006),True,chip='ID48(Megamos Crypto)',keyway='HYN10 (JMA HY-5.P1)',immo='VDO 이모빌라이저 박스(이모박스)',
    src=TM+', reidsremotes.com.au(코란도 2000-2006 HYN10)',note='')
# 코란도 C
add('코란도 C',R(2011,2019),True,chip='ID70(DST80, 80bit)',keyway='TOY48 / KI-7 (자료 상충)',blade_pn='7105121500',fold='87510-21100 (3버튼 폴딩키)',
    smart='스마트키 트림 별도(품번·칩 미확인)',immo='이모빌라이저(모듈 명칭 미확인)',flag='orange',
    src=lambda y:FLIP+(', wikipedia(코란도 C 2011.2 국내 출시)' if y==2011 else ''),
    note=lambda y:'폴딩키 칩은 순정 87510-21100 기준 확인 / 블레이드 명칭 판매처마다 상충(TOY48 vs KI-7), 스마트키 칩 미확인'+(' / 2019.2 C300 출시로 교체' if y==2019 else ''))
# 코란도 C300
add('코란도 (4세대, C313)',R(2019,2026),False,chip='DST80(ID70/4D70)',keyway='HYN14R',smart='스마트키(품번 미확인)',immo='SKM(스마트키 모듈) 추정',flag='orange',
    src=lambda y:'carkeyhelper.com(코란도 Mk4 C300 2019- 스마트키 DST80, HYN14R), ebay(2020-2022 코란도 스마트키 트랜스미터 / 2023-2024 KGM 코란도 스마트키)',
    note=lambda y:'칩·블레이드는 carkeyhelper 요약 기준 / 이모빌라이저 모듈 명칭은 같은 세대 티볼리·G4 렉스턴(SKM) 기준 추정'+(' / 2026년식 자료 없음' if y>=2025 else ''))
add('코란도 e-모션 (전기차)',R(2022,2023),True,chip='DST80(ID70/4D70) 추정(C300 기준)',keyway='HYN14R 추정',immo='SKM 추정',flag='orange',
    src='newdaily.co.kr(코란도 이모션 2022.2 출시), sisajournal-e.com(2023 판매 중단), carkeyhelper.com(코란도 C300 스마트키 DST80)',
    note=lambda y:('원본 목록 2019~ — 실제 국내 출시 2022.2 / ' if y==2022 else '2023.7 판매 종료 / ')+'C300 기반 전기차 — 키 칩 직접 자료 없음')
# 티볼리
add('티볼리',R(2015,2026),False,chip='ID70(DST80, 80bit) — 폴딩키 기준',keyway='TOY48 / KI-7 (자료 상충)',blade_pn='7105121500',fold='87510-21100 (3버튼 폴딩키)',
    smart=lambda y:'8751035050 / 8751035060 (스마트키 트랜스미터, 칩 미확인)' if y<=2019 else '스마트키(품번·칩 미확인)',
    immo='SKM(스마트키 모듈)',flag='orange',
    src=lambda y:FLIP+', kogoos.com/kpartsmall.com(티볼리 순정 스마트키 8751035060/8751035050), scandoc.online(티볼리 뉴 X150 SMART Key Module)'+(', wikipedia(티볼리 2015.1 출시)' if y==2015 else ''),
    note=lambda y:'폴딩키 칩 확인(ID70 DST80), 스마트키 칩은 자료 없음 — 스마트키 차량은 실물 확인 / 블레이드 명칭 상충'+(' / 3D Group 폴딩키 자료 2022년까지' if y>=2023 else ''))
add('티볼리 에어',R(2016,2019),True,chip='ID70(DST80, 80bit) — 폴딩키 기준',keyway='TOY48 / KI-7 (자료 상충)',blade_pn='7105121500',fold='87510-21100 (3버튼 폴딩키)',
    smart='8751035050 / 8751035060 (티볼리 공용 추정)',immo='SKM(스마트키 모듈)',flag='orange',
    src=lambda y:FLIP+', stockddalbae.com(티볼리 에어 키 분해)'+(', newdaily.co.kr(티볼리 에어 2019.9 단종)' if y==2019 else ''),
    note=lambda y:'티볼리 롱바디 — 키는 티볼리와 동일 계열'+(' / 2019.9 단종 후 2020 재출시(재출시분은 원본 목록 범위 밖)' if y==2019 else ''))
# 무쏘
add('무쏘',R(2000,2005),True,chip='ID48(Megamos Crypto)',immo='VDO 이모빌라이저 박스(이모박스)',
    src=lambda y:TM+', autotronics.co.uk(무쏘 이모빌라이저 트랜스폰더 리코딩)',
    flag=lambda y:'orange' if y<2002 else None,
    note=lambda y:('TMPro 자료가 2002년부터 — 2000·2001년식 직접 확인 안 됨 / ' if y<2002 else '')+'무쏘 키 블레이드 자료 없음'+(' / 실제 생산은 2006.4까지(namu.wiki)' if y==2005 else ''))
add('무쏘 스포츠 (픽업)',R(2002,2005),True,chip='ID48(Megamos Crypto) 추정(무쏘 기준)',immo='VDO 이모빌라이저 박스 추정',flag='orange',
    src=TM+', wikipedia(무쏘 스포츠 2002 출시)',note='무쏘 스포츠 직접 자료 없음 — 무쏘(이모박스 적용) 기준 추정')
# 액티언/액티언스포츠/카이런
def kyr_immo(start):
    def f(y):
        if y<2007: return '이모빌라이저 컨트롤 유닛(87110-08B00/09000)'
        if y==2007: return '이모빌라이저 컨트롤 유닛(2007.3 이전 생산) / 이후 생산분 모듈 명칭 미확인'
        return '확인 불가(2007.4 이후 별도 유닛 적용 종료 — 통합 모듈 명칭 미확인)'
    return f
for m,a,b,startnote in [('액티언 (1세대)',2005,2011,'2005.10 출시'),('액티언 스포츠 (픽업)',2006,2012,'2006.3 출시'),('카이런',2005,2011,'2005.6 출시')]:
    add(m,R(a,b),True,chip='ID60(4D60, 40bit/80bit 키 병존)',keyway='SSY3 (JMA SSA-2P)',fold='87170-32030 / 87170-32020(80bit), 87170-08B21(40bit) — 2버튼 리모컨키',
        immo=kyr_immo(a),flag=lambda y:'orange' if y>=2008 else None,
        src=lambda y:AK+', '+ICU+', reidsremotes.com.au(액티언스포츠·카이런·렉스턴·스타빅 트랜스폰더키 SSY3)',
        note=lambda y,sn=startnote,a=a:(sn+' / ' if y==a else '')+'40bit(08B21)·80bit(32030/32020) 키 연식 구분 자료 없음 — 키 품번으로 확인'+(' / 2007.4 이후 이모빌라이저 모듈 명칭 미확인' if y>=2008 else ''))
# 코란도 스포츠
add('코란도 스포츠 (픽업)',R(2012,2018),True,chip='ID70(DST80, 80bit) — 폴딩키 기준',keyway='TOY48 / KI-7 (자료 상충)',blade_pn='7105121500',fold='87510-21100 (3버튼 폴딩키)',
    immo='이모빌라이저(모듈 명칭 미확인)',flag='orange',
    src=lambda y:FLIP+', blog.daum.net(코란도스포츠 차키 이모빌라이저 기본 내장), namu.wiki(코란도 스포츠 2012.1-2018.1)',
    note='액티언 스포츠 후속 — 3D Group 적용표의 "액티언 스포츠"에 해당하는지 직접 확인 안 됨')
# 렉스턴 스포츠
add('렉스턴 스포츠 & 칸 (픽업)',R(2018,2024),True,chip='확인 불가(DST80 계열 추정)',smart='스마트키(품번 미확인)',immo='SKM(스마트키 모듈)',flag='orange',
    src=lambda y:'ebay(2024 렉스턴 스포츠 노블레스 스마트키 모듈 8757038210), autodaily.co.kr(2025.2 무쏘 스포츠·무쏘 칸으로 차명 변경)',
    note=lambda y:'스마트키 칩 자료 없음'+(' / 2025.2부터 무쏘 스포츠·무쏘 칸으로 차명 변경(같은 차)' if y==2024 else ''))
for m,a,b,s in [('토레스',2022,2026,'wikipedia(토레스 2022.7 출시)'),('토레스 EVX (전기차)',2023,2026,'ebay(2024 KGM 토레스 EVX 스마트키 트랜스미터)'),('액티언 (2세대, J120)',2024,2026,'wikipedia(KGM 액티언 J120 2024.7 공개, 토레스와 플랫폼 공유)'),('무쏘 EV (픽업, 전기차)',2025,2026,'jasonryu.net/namu.wiki(무쏘 EV 2025.3 출시)')]:
    add(m,R(a,b),False,chip='확인 불가',smart='스마트키(품번 미확인)',immo='확인 불가',flag='red',src=s,
        note=lambda y,a=a,m=m:('원본 목록 2024~ — 실제 출시 2025.3 / ' if m.startswith('무쏘 EV') and y==a else '')+'키 칩·이모빌라이저 자료 없음')
# 렉스턴
def rex1_chip(y):
    if y==2001: return 'ID48(Megamos Crypto) 추정'
    if y<2006: return 'ID48(Megamos Crypto)'
    return 'ID48(Megamos, 2006.1 이전 생산) / ID60(4D60, 2006.2 이후 생산)'
def rex1_immo(y):
    if y<2006: return 'VDO 이모빌라이저 박스(이모박스)'
    return 'VDO 이모박스(2006.1 이전 생산) / 이모빌라이저 컨트롤 유닛 87110-08B00(2006.2 이후 생산)'
add('렉스턴 (1세대)',R(2001,2006),True,chip=rex1_chip,keyway='SSY3 (JMA SSA-2P)',immo=rex1_immo,
    flag=lambda y:'orange' if y==2001 else None,
    src=lambda y:TM+', abkeys.com(액티언·렉스턴 2000+ SSY3 리모컨키 헤드), manualslib(2004 렉스턴 2.7 XDi: 트랜스폰더 코드 ECU 확인 방식)'+(', '+ICU if y==2006 else ''),
    note=lambda y:('2001.9 출시 — TMPro 자료가 2002년부터라 2001년식 직접 확인 안 됨' if y==2001 else ('ICU 적용 2006.02~ — 이모박스(ID48)에서 ICU(4D60)로 전환' if y==2006 else '')))
add('뉴 렉스턴',R(2006,2012),True,chip='ID60(4D60, 40bit/80bit 키 병존)',keyway='SSY3 (JMA SSA-2P)',fold='87170-08B21(40bit, 액티언·렉스턴 2007-2013) / 87170-08D50(80bit)',
    immo='이모빌라이저 컨트롤 유닛(87110-08B00)',
    src=lambda y:AK+', '+ICU+', tlslocks.com.au(렉스턴 2006+ 4D60)',
    note=lambda y:'2006.6 출시' if y==2006 else '')
add('렉스턴 W / 렉스턴 II',R(2012,2017),True,chip='ID60(4D60, SSY3 키) / ID70·4D70(DST80, 폴딩키·스마트키)',keyway='SSY3 / TOY48·KI-7(폴딩키)',
    fold='87510-21100 (3버튼 폴딩키, 3D Group 적용표 "렉스턴")',smart='스마트키 FCC DEO-MT FOBG02(4D70 DST80, 2013 사례)',
    immo='이모빌라이저 컨트롤 유닛(87110-08B00, ~2017.04)',flag='orange',
    src=lambda y:ICU+', abkeys.com(렉스턴 2011-2013 SSY3 2버튼 리모컨키), '+FLIP+', digital-kaos.co.uk(2013 렉스턴 스마트키 DEO-MT FOBG02 4D70 DST80)',
    note='키 종류(SSY3 리모컨키·폴딩키·스마트키)에 따라 칩 상이 — 차량 키로 확인 / ICU 부품 적용이 2017.04까지')
add('G4 렉스턴 (2세대)',R(2017,2026),False,chip='확인 불가(DST80 계열 추정)',smart=lambda y:'8751036C20 (5버튼, 433MHz, 2020.11~2022.04 생산)' if 2020<=y<=2022 else '스마트키(품번 미확인)',
    immo='SKM(스마트키 모듈 87570-36010, 2017.07~)',flag='orange',
    src=lambda y:'scandoc.online(렉스턴 G4 Y400 이모빌라이저 = SMART Key Module), ebay.de(렉스턴 Y400 07.17- 스마트키 컨트롤 유닛 87570-36010)'+(', kogoos.com(G4 렉스턴 스마트키 8751036C20, 2020.11~2022.04)' if 2020<=y<=2022 else ''),
    note='이모빌라이저 모듈(SKM) 확인, 스마트키 칩은 자료 없음 — 실물 확인 필요')
# 이스타나
add('이스타나 (밴)',R(2000,2004),True,chip='확인 불가',immo='이모빌라이저(모듈 명칭 확인 불가)',flag='red',
    src='wikipedia(이스타나 = 벤츠 MB100 기반 15인승 밴), alibaba(쌍용 키: 이모빌라이저가 연료분사 ECU 차단)',note='이스타나 키 칩 자료 없음')
# 로디우스
add('로디우스',R(2004,2013),True,chip=lambda y:'ID60(4D60)' if y<=2011 else 'ID60(4D60, 1세대 키) / ID70(DST80, 로디우스 II 폴딩키 87510-21100)',
    keyway=lambda y:'SSY3' if y<=2011 else 'SSY3 / TOY48·KI-7',fold=lambda y:'87510-21100 (로디우스 II, 3버튼 폴딩키)' if y>=2012 else '',
    immo='이모빌라이저(모듈 명칭 미확인)',flag=lambda y:'orange' if y>=2012 else None,
    src=lambda y:'reidsremotes.com.au(액티언스포츠·카이런·렉스턴·스타빅(=로디우스) 트랜스폰더키 SSY3), myremotekey.com(4D60)'+(', '+FLIP if y>=2012 else ''),
    note=lambda y:('2004.9 출시' if y==2004 else '')+(' 로디우스 II(2012~) 폴딩키는 ID70 — 1세대 키와 구분' if y>=2012 else ''))
add('코란도 투리스모',R(2013,2018),True,chip='ID70(DST80, 80bit)',keyway='TOY48 / KI-7 (자료 상충)',blade_pn='7105121500',fold='87510-21100 (3버튼 폴딩키)',
    immo='이모빌라이저(모듈 명칭 미확인)',flag='orange',
    src=lambda y:FLIP+', wikipedia(코란도 투리스모 = 로디우스 2세대 페이스리프트 2013.2)',
    note='remkeys 적용표의 로디우스 II(2012-2019) 기준 — 블레이드 명칭 상충')
open('rows.jsonl','w').write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
from collections import Counter
print(len(rows)); print(Counter(r.get('flag') for r in rows))

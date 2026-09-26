# 기아 주황·빨강 행 재조사 결과 (2026.9, 국내 부품몰·키 도매 + 같은 품번 해외 판매처)
# research/recheck/overrides.json 에 추가하고 기아 파일에 적용. 사용: python3 research/kia/recheck2.py
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'research')); sys.path.insert(0, os.path.join(ROOT, 'research', 'recheck'))
import apply as recheck
CHIP = '칩코드 (예: ID46(PCF7936))'
R = lambda a, b: list(range(a, b + 1))
K = lambda model, years, **kw: dict(brand='기아', model=model, years=years, **kw)
NEW = [
 K('포르테 (Forte/포르테쿠페, TD/XK)', R(2009, 2011), flag='',
   set={CHIP: 'ID46(PCF7936)[폴딩키], ID46(PCF7952A)[스마트키]', '폴딩키(부품번호)': '95430-1M250'},
   guide='포르테 (TD) 2009-2011: 폴딩키 95430-1M250(Cerato 2010-2013 433MHz) PCF7936 ID46(abkeys·tlkeys), 블랭킹 81996-1M020(카다몰 포르테 키-블랭킹 피아이씨)'),
 K('K3 (Forte, YD)', R(2012, 2015), flag='',
   set={CHIP: 'ID8A[스마트키], ID6E-MA[폴딩키]', '폴딩키(부품번호)': '95430-A7100, 95430-A7200'},
   guide='K3 (YD) 2012-2015: 폴딩키 95430-A7100(Cerato 2013-2017 OKA-870T) 4D60 Carbon 80bit = DST80(ID6E-MA)(abkeys), 95430-A7200도 4D60 칩 키(keyless2go) — 이전 "4D60·ID46 상충"은 80bit DST80로 정리'),
 K('K3 (Forte, BD)', [2019], flag='', set={CHIP: 'ID8A'},
   guide='K3 (BD) 2019: 95440-M6011·M6501(FCC CQOFD00430) 8A Texas Crypto 128bit AES(검색요약 key4·keydirect·abkeys M6010) — dfwkeys4cars 종합표의 ID47은 품번 근거 없어 제외'),
 K('프라이드 JB', R(2006, 2009), flag='', set={'키블레이드(부품번호)': '81996-1G100[이모빌라이저키, 2005.2.15~2009.12.10], 81996-1G000[칩 없음]'},
   guide='프라이드 JB: 국내 이모빌라이저키 81996-1G100(뉴프라이드 2005.2.15~2009.12.10, 드림열쇠), 칩 없는 키 81996-1G000(Rio 2005-2011) — 같은 플랫폼 베르나 MC 81996-1E010도 ID46'),
 K('프라이드 JB', [2010], flag='', set={'키블레이드(부품번호)': '81996-1G000[칩 없음]'}),
 K('프라이드 UB', [2012], flag='', guide='프라이드 UB 2012: 2011.9 출시 스마트키 95440-1W000 계열(헬로우카 프라이드UB 954401W000/1W040/1W001) — 2013년과 같은 키'),
 K('모닝 (Morning, SA)', R(2005, 2009), flag='', set={'키블레이드(부품번호)': '81996-07020, 81996-07100'},
   guide='모닝 (SA) 2005-2009: 현대모비스 모닝SA 키 81996-07020·07100(헬로우카), 같은 계열 Picanto 81996-07010 PCF7936 ID46 HYN6(abkeys 2005+)'),
 K('모닝 (Morning, TA/JA)', [2017], flag='', set={CHIP: 'ID6E-MA[TA], ID46[TA], ID6E-MA[JA, 폴딩키], ID8A[JA, 스마트키]'},
   guide='모닝 (JA): 폴딩키 95430-G6600 4D-60 Carbon 80bit(DST80, abkeys·tlkeys), 스마트키 95440-G6000·G6100 DST-AES ID8A(mk3·keyshop-online·tlkeys) — 이전 "DST80 vs ID75 상충"은 폴딩키·스마트키 칩이 다른 것'),
 K('모닝 (Morning, JA)', R(2018, 2025), flag='', set={CHIP: 'ID6E-MA[폴딩키], ID8A[스마트키]'}),
 K('EV4 (CT1)', [2025, 2026], flag='', set={CHIP: 'ID4A'},
   guide='EV4 (CT1): 95440-EZ300(EV4 2025 7버튼) NCF29A HITAG AES(auto-keys.eu) → ID4A'),
 K('스포티지 (Sportage, JE/KM)', R(2005, 2009), flag='', set={'키블레이드(부품번호)': '81996-2F010[2004.6~]'},
   guide='스포티지 (JE/KM): 드림열쇠 "뉴스포티지 81996-2F010(04년6월~), 쎄라토(05년~)", 81996-2F010 PCF7936 ID46 HYN6(abkeys)'),
 K('스포티지 (Sportage, SL)', [2013, 2014], flag='', set={CHIP: 'ID46(PCF7936)[플립키], ID46(PCF7952A)[스마트키]'},
   guide='스포티지 (SL) 2013-2014: 플립키 95430-3W200 PCF7936 HITAG2 ID46 HY22(auto-keys.eu OEM) — ID6E-MA 표기는 2011-2012 플립키 해당'),
 K('쏘렌토 (Sorento, BL)', R(2002, 2008), flag='', set={CHIP: 'ID46(PCF7936)', '키블레이드(부품번호)': '81996-3EG00, 81996-3EC00[뉴 쏘렌토]'},
   guide='쏘렌토 (BL): 국내 이모빌라이저 키 81996-3EG00(드림열쇠), 뉴 쏘렌토 이모빌라이저 키블레이드 81996-3EC00(카키넘버원·대남열쇠) PCF7936 ID46 HYN7R(abkeys)'),
 K('카렌스 (Carens, UN)', R(2008, 2011), flag='',
   guide='카렌스 (UN) 2008-2011: Carens 2006(후기)-2011 ID46 PCF7936 키(autoecupart), 국내 폴딩키 954301D101~D104(헬로우카) 적용 기간 확인'),
]

if __name__ == '__main__':
    p = os.path.join(ROOT, 'research', 'recheck', 'overrides.json')
    ovs = json.load(open(p, encoding='utf-8'))
    # 같은 (모델, 연식)을 다루던 이전 항목 중 색 지정(flag)은 새 결과로 대체
    newkeys = {(o['model'], str(y)) for o in NEW for y in o['years']}
    for o in ovs:
        if o['brand'] == '기아' and 'flag' in o and any((o['model'], str(y)) in newkeys for y in o['years']):
            o['years'] = [y for y in o['years'] if (o['model'], str(y)) not in newkeys]
    ovs = [o for o in ovs if o['years']] + NEW
    json.dump(ovs, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('overrides', len(ovs))
    print('기아', recheck.apply_file(os.path.join(ROOT, '기아_트랜스폰더_칩코드_DBnew.xlsx'), ovs))

# 4차 재검색(2026.9) — 불확실(주황·빨강) 행을 연식별로 다시 검색한 결과. 검색 기록: research/recheck/yearly4.md
# overrides.json에 추가하고 각 파일에 적용. 현대는 research/hyundai/build_rows.py에서 직접 고침.
# 사용: python3 research/recheck4.py
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'recheck'))
import apply as recheck
CHIP = '칩코드 (예: ID46(PCF7936))'; IMMO = '이모빌라이저 시스템'; KT = '키종류'
R = lambda a, b: list(range(a, b + 1))
NEW = []
def add(brand):
    return lambda model, years, **kw: NEW.append(dict(brand=brand, model=model, years=years, **kw))

# ── 벤츠 ──
B = add('벤츠')
for m in ('A클래스 (W176, 3세대 해치백)', 'A45 AMG (W176/W177)', 'B클래스 (W246)'):
    B(m, [2014], set={CHIP: 'FBS3[2014.11 이전 생산], FBS4[2014.11 이후 생산]'}, flag='')
NEW[-1]['guide'] = 'W246 FBS4는 2014.11 생산부터(EASYGUARD·abkeys W246 FBS4 EZS 2469057503) — 같은 MFA 플랫폼 W176·A45·CLA·GLA도 2014.11 전환으로 정리'
B('G클래스 (W463, 구형 바디)', [2000, 2001], set={IMMO: 'DAS 2a, DAS 2b'}, flag='orange',
  note='DAS 2a·2b(1997~2001, 키 트랜스폰더) 확인 — 키 트랜스폰더 칩 형식 자료 없음(같은 DAS2 W163은 PCF7930·PCF7931·PCF7935)')
B('G클래스 (W463, 구형 바디)', R(2002, 2005), set={CHIP: 'FBS3', KT: '스마트키'}, flag='',
  guide='G클래스 W463 2002~: EIS(EZS) + 적외선 키(FBS3)로 바뀜(fixautosmart "G500 2002-2014 W463 EIS", CGDI MB G클래스 2003~ 적외선 모드) — 트랜스폰더 막대키는 2001년까지 DAS 차량')

# ── 기아 ──
K = add('기아')
K('스포티지 (Sportage, NB-Ⅶ)', R(1993, 1999), delete=True)
K('카니발 (Carnival, KV-II/GQ)', [1998, 1999], delete=True)
K('카렌스 (Carens, RS)', [1999], delete=True,
  guide='CLAUDE.md 규칙(2000년식부터)에 맞춰 스포티지 NB 1993~1999, 카니발 1998~1999, 카렌스 RS 1999 행 삭제')
K('카렌스 (Carens, RS)', R(2002, 2005), set={CHIP: 'ID60(4D60)[자료 상충], ID46[자료 상충]'}, flag='orange',
  note='해외 카탈로그 상충(transpondery·keyclick: 카렌스 2001-2005 Texas 4D60, 다른 판매처: 2001-2012 ID46) — 국내 부품번호 원문 없음')
K('카렌스 (Carens, RS)', [2006], set={CHIP: 'ID60(4D60)[RS, 자료 상충], ID46[RS, 자료 상충], ID46[UN]', '폴딩키(부품번호)': '954301D100[UN]'})
K('카렌스 (Carens, UN)', [2012], flag='',
  guide='카렌스 UN 2012: 헬로우카 원문 — 폴딩키 954301D103(2010.6.1~2012.7.17), 954301D104(2012.7.1~2012.7.17) 적용 기간 확인')
K('셀토스 (SP2 PE)', [2026], set={CHIP: 'ID8A[SP2 PE], ID6A[SP2 PE], 확인 불가[SP3]',
                                  '키블레이드(부품번호)': '81996-P1060[SP2 PE, 스마트키용], 81996-K0000[SP2 PE, 폴딩키용]',
                                  '스마트키(부품번호)': '95440-Q5500[SP2 PE, ~2026.1], 95440-Q5510[SP2 PE, ~2026.1]',
                                  '폴딩키(부품번호)': '95430-Q5700[SP2 PE], 95430-Q5750[SP2 PE]'},
  guide='셀토스 2026: SP2 PE(~2026.1) 행과 디 올 뉴 셀토스(SP3, 2026.1~) 행으로 나눔 — SP2 PE 스마트키 95440-Q5510·Q5710은 2022-2026 적용(bestkeysupply·royalkeysupply), SP3 키 자료 없음')
K('니로 (Niro, SG2/SG2 PE)', [2026], flag='orange',
  note='더 뉴 니로(SG2 PE, 2026.3) 국내 스마트키 품번 원문 없음 — 2026년식 해외 니로는 95440-AT000(ID4A, FD01330) 계속 사용')

# ── 르노 ──
N = add('르노(르노삼성)')
N('아르카나 (XM3 국내 리네이밍)', R(2024, 2026), flag='',
  guide='아르카나 2024~: 카드키 칩은 NCF29A1M(ID4A) — 순정 285979827R·285973979R(신형 H-24985 포함) 모두 NCF29A1M 4A(car-keys-online·keystation) 확인, 카드 품번만 차량별 확인')
N('SM3 (1세대, N17)', R(2002, 2005), flag='orange',
  note='1세대 칩 직접 자료 없음 — 원형 닛산 블루버드 실피(G10) 키는 46칩(NI04T) 판매처 표기, 같은 차체 CF 기준 추정')
N('SM7', [2004], flag='orange',
  note='국내 카드키 칩 직접 자료 없음 — 2004.12부터 스마트키 적용, 닛산 티아나 J31 인텔리전트 키 ID46(PCF7936) 기준 추정')

# ── KGM ──
G = add('KG모빌리티(쌍용)')
G('무쏘', [2000, 2001], flag='',
  guide='무쏘 2000·2001: 무쏘 1998~ ID48(29Fxxx), 2001~2005 VDO 이모박스(MC68HC05B16) + ID48(autotronics·TMPro 모듈 85) — 이모박스 자료가 2002부터라던 이전 기록 정정')
G('무쏘 스포츠 (픽업)', R(2002, 2005), flag='orange',
  note='무쏘 스포츠 전용 자료 없음 — 같은 차대 무쏘 2001~2005 VDO 이모박스 + ID48(autotronics) 기준 추정')

# ── 쉐보레 ──
C = add('쉐보레(GM대우)')
C('스파크 (쉐보레, M300)', [2014], flag='',
  guide='스파크 M300 2014: GM 부품몰(c-mall) "스파크 2014년형 폴딩 키", 스파크 2012-2016 폴딩키 ID46(PCF7941E) 433MHz, 한국GM 블로그 "스파크S 폴딩키는 아베오·크루즈·알페온 키와 거의 같음" — 추정 해제')
C('볼트 (쉐보레, Volt, 플러그인 하이브리드)', R(2016, 2019), flag='',
  guide='볼트(Volt) 2016-2019: 433MHz 스마트키 FCC HYQ4EA(13585728·13529638) = Philips ID46(locksmithkeyless) — 국내(433MHz) 사양과 같은 주파수 키로 확인')
C('볼트 EV (쉐보레)', R(2017, 2021), flag='',
  guide='볼트 EV 2017-2021: 433MHz 스마트키 HYQ4EA ID46(2017-2022 볼트 적용), 미국형 315MHz는 HYQ4AA — 국내 433MHz 키 칩 ID46 확인')
C('이쿼녹스 (쉐보레, 가솔린)', [2023, 2024], flag='',
  guide='이쿼녹스 2023-2024: 433MHz 스마트키 HYQ4ES·HYQ4EA(2018-2024 이쿼녹스 적용, 46E 칩), 미국형 315MHz HYQ4AS도 ID46 — 칩 ID46 확인')
C('트래버스 (쉐보레)', R(2021, 2025), flag='',
  guide='트래버스(2세대) 2021-2025: 433MHz 스마트키 HYQ4ES·HYQ4EA(2018-2024 트래버스 적용) ID46 — 국내 판매분(2025.3 종료)은 2세대')

# ── 아우디 ──
A = add('아우디')
A('A3 (8Y, 4세대)', [2026], flag='',
  guide='A3 8Y 2026: 스마트키 8Y0959754 계열 적용 연식 2020~2026(go-parts) — 같은 세대 키 계속 사용 확인')
A('RS3', [2026], flag='',
  guide='RS3 2026: 8Y0959754DD 적용(2022~2026) — 8Y 공용 키 확인')
A('Q2', R(2024, 2026), flag='',
  guide='Q2 2024~2026: 국내 2026년까지 판매, MQB 키 81A837220(ID88) 적용 연식 계속 — 추정 해제')
A('Q8 (1세대)', [2026], flag='',
  guide='Q8 2026: 4N0959754AM 적용 2019~2026 — MLB evo 키 확인')
A('RS7', [2026], flag='',
  guide='RS7 2026: 4N0959754BC 적용 2021~2026 — MLB evo 키 확인')
A('RS Q8', [2026], flag='',
  guide='RS Q8 2026: 4N0959754BC 적용 2020~2026 — MLB evo 키 확인')
A('RS6 아반트', [2026], flag='',
  guide='RS6 아반트 2026: 4N0959754BC(C8 공용) 적용 — MLB evo 키 확인')
A('Q7 (4M, 2세대)', R(2022, 2026), set={CHIP: 'MLB evo 전용 칩', IMMO: 'MLB evo IMMO5'}, flag='',
  guide='Q7 4M 2022~2026·SQ7 2024~2026: 2023·2024 Q7/SQ7 키 4N0959754BF·AM(A8 D5·Q8과 같은 MLB evo 키) — 칩·이모빌라이저를 MLB evo로 정정')
A('SQ7', R(2024, 2026), set={CHIP: 'MLB evo 전용 칩', IMMO: 'MLB evo IMMO5'}, flag='')
A('R8 (4S, 2세대)', R(2017, 2024), set={CHIP: 'ID46(PCF7945AC)[추정]', IMMO: 'BCM2[추정]'}, flag='orange',
  note='R8 4S 키 4H0959754EB·FK는 A8 D4 계열(4H0) 키 — PCF7945AC·BCM2 기준 추정, R8 전용 칩 자료 없음')
A('A4 (B6/B7, 6·7세대)', [2001], flag='orange',
  note='B6 2000.10 해외 출시 — 2001년식 국내분의 B5(ID48)·B6 여부 자료 없음')
A('S4', [2025, 2026], flag='orange',
  note='S4 B9 2025년 단종 — 2025·2026년식 국내 판매 여부 자료 없음, 세대 기준 기재')
A('RS5', [2017], flag='orange',
  note='국내 RS5 B9는 2021.7 스포트백 출시 — 2017년식 국내 판매 자료 없음, 세대 기준 기재')

FILES = {'BMW': 'BMW_코리아_출시모델.xlsx', 'KG모빌리티(쌍용)': 'KG모빌리티(쌍용)_models.xlsx', '기아': '기아_트랜스폰더_칩코드_DBnew.xlsx',
         '르노(르노삼성)': '르노_models.xlsx', '벤츠': '벤츠_models.xlsx', '쉐보레(GM대우)': '쉐보레_models.xlsx', '아우디': '아우디_models.xlsx'}

if __name__ == '__main__':
    p = os.path.join(ROOT, 'research', 'recheck', 'overrides.json')
    ovs = json.load(open(p, encoding='utf-8'))
    ovs = [o for o in ovs if not o.get('r4')]
    newkeys = {(o['brand'], o['model'], str(y)) for o in NEW for y in o['years']}
    for o in ovs:
        if 'flag' in o and not o.get('delete'):
            o['years'] = [y for y in o['years'] if (o['brand'], o['model'], str(y)) not in newkeys]
    for o in NEW:
        o['r4'] = True
    ovs = [o for o in ovs if o['years']] + NEW
    json.dump(ovs, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('overrides', len(ovs))
    for b in sorted({o['brand'] for o in NEW}):
        print(b, recheck.apply_file(os.path.join(ROOT, FILES[b]), ovs))

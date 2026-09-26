# 3차 전 브랜드 재검색(2026.9) — 정확성 우선. overrides.json에 추가하고 각 파일에 적용.
# 사용: python3 research/recheck3.py
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'recheck'))
import apply as recheck
CHIP = '칩코드 (예: ID46(PCF7936))'; IMMO = '이모빌라이저 시스템'
R = lambda a, b: list(range(a, b + 1))
def O(brand, model, years, **kw): return dict(brand=brand, model=model, years=years, **kw)
NEW = []
# ── BMW ──
B = lambda *a, **k: NEW.append(O('BMW', *a, **k))
for m, ys in [('5시리즈 (G60/G61, 8세대)', R(2023, 2026)), ('i5 (G60)', R(2023, 2026)), ('M5 (G90)', R(2024, 2026)), ('X7 (G07)', R(2024, 2026))]:
    B(m, ys, set={IMMO: 'BDC3'}, flag='')
NEW[-1]['guide'] = 'BMW G60·i5·M5·X7 LCI: 키 프로그래머 업체(Autel·KeyDIY·Xhorse)가 G섀시(G30/G31/G60 2020.7~)를 BDC3, U섀시를 BCP로 구분 — G60은 BDC3 Add Key 대상으로 명시(obdii365·obd2.ltd)'
B('XM (G09)', R(2023, 2026), set={IMMO: 'BDC3'}, flag='', guide='BMW XM G09: IYZBK1 키(X5·X6·X7·XM 공용, UWB) — G섀시 BDC3 키 복사·추가 대상(Xhorse G chassis BDC3)')
B('X4 (F26, 1세대)', [2016], set={CHIP: 'ID49(PCF7953)'}, flag='', guide='BMW X4 F26 2016: 순정 CAS4+ 키 칩은 PCF7953(ID49) — PCF7945P는 "CAS4 modified type" 애프터마켓 키 칩(mk3·vvdi)이라 뺌')
B('3시리즈 (E90/E91/E92/E93, 5세대)', [2010], set={CHIP: 'ID46(PCF7945), ID46(PCF7943), ID46(PCF7944)'}, flag='', guide='BMW E90 CAS3+: 순정 키 칩 PCF7945·PCF7943·PCF7944 모두 ID46(Hitag2) 계열로 병존(bimmerfest·keyecu) — 자료 상충 아님')
B('X3 (G45, 4세대)', R(2024, 2026), set={IMMO: 'BCP'}, flag='', guide='BMW X3 G45: Lonsdor K518 PRO "2025 BMW X3 UWB에 BCP 키 추가" 절차(U섀시 BCP) 확인 — 이모빌라이저 BCP 확정')
B('X3 (F25, 2세대)', [2013], set={CHIP: 'ID49(PCF7953)'}, flag='', guide='BMW X3 F25 2013: CAS4+ 순정 키 칩 PCF7953(ID49) — 같이 적혀 있던 PCF7945P는 중국산 CAS4 호환 키 칩(mr-key·tlkeys 판매품)이라 뺌(X4 F26과 같은 판단)')

# ── 쉐보레 ──
C = lambda *a, **k: NEW.append(O('쉐보레(GM대우)', *a, **k))
C('스파크 (쉐보레, M300)', [2013], flag='', guide='스파크 2013: 2013년형은 이모빌라이저 없음, 2014년형(2013.5.14 출시)부터 이모빌라이저 폴딩키 적용(나무위키 스파크 2세대·차프라이스 2013.5 가격표) — 전환기라 색 없음')
C('토스카 (GM대우/쉐보레)', [2006], flag='', guide='토스카 2006: 2007년형(2006.11 출시)부터 이모빌라이저 신규 적용(이투데이 "GM대우 2007년형 토스카 출시") — 전환기라 색 없음')
C('서버번 (쉐보레)', [2023], delete=True)
C('서버번 (쉐보레)', R(2024, 2026), flag='', guide='서버번: 한국GM이 2024.10부터 국내 정식 판매(위키백과) — 2023년식 행 삭제. 키는 타호와 같은 스마트키(YG0G21TB2, 433MHz, ID49)')
C('캡티바 (쉐보레, 2세대, 리뱃지)', [2024], delete=True)
C('이쿼녹스 EV (쉐보레)', [2024], delete=True, guide='캡티바 2세대·이쿼녹스 EV: 국내 미출시(이쿼녹스 EV는 2024.12 인증 후 출시 철회, EBN) — 행 삭제')

# ── 아우디 ──
A = lambda *a, **k: NEW.append(O('아우디', *a, **k))
for m, ys in [('A3 (8V, 3세대)', [2020]), ('S3 (8V)', [2019]), ('A5 (B9, 2세대)', [2020]), ('A7 (C7, 1세대)', [2014]),
              ('A8 (D3/D4)', [2008]), ('Q2', [2022]), ('Q3 (F3, 2세대)', [2023]), ('Q5 (8R, 1세대)', [2011]),
              ('Q7 (4L, 1세대)', [2006]), ('Q7 (4M, 2세대)', [2017]), ('TT (8J, 2세대)', [2014]), ('TTS', [2021]), ('R8 (42, 1세대)', [2009])]:
    A(m, ys, flag='')
NEW[-1]['guide'] = '아우디 A3 8V 2020·S3 2019·A5 B9 2020·A7 C7 2014·A8 D3 2008·Q2 2022·Q3 F3 2023·Q5 8R 2011·Q7 4L 2006·Q7 4M 2017·TT 8J 2014·TTS 2021·R8 42 2009: 같은 세대 안의 연식이라 키(부품번호)·칩이 앞뒤 확정 연식과 같음 — 연식별 판매처 표기 차이는 세대 구분 오류로 보고 색 지움'
A('Q4 e-트론', R(2022, 2026), set={CHIP: 'ID49[추정]'}, flag='orange', note='Q4 전용 칩 자료 없음 — 같은 MEB 플랫폼 VW ID.3·ID.4 키(5HG959753B, MQB49 Hitag Pro, 골프8 공용) 기준 추정')

FILES = {'BMW': 'BMW_코리아_출시모델.xlsx', 'KG모빌리티(쌍용)': 'KG모빌리티(쌍용)_models.xlsx', '기아': '기아_트랜스폰더_칩코드_DBnew.xlsx',
         '르노(르노삼성)': '르노_models.xlsx', '벤츠': '벤츠_models.xlsx', '쉐보레(GM대우)': '쉐보레_models.xlsx', '아우디': '아우디_models.xlsx'}

if __name__ == '__main__':
    p = os.path.join(ROOT, 'research', 'recheck', 'overrides.json')
    ovs = json.load(open(p, encoding='utf-8'))
    # 이미 들어간 3차 항목은 지우고, 같은 (브랜드, 모델, 연식)의 이전 색 지정은 새 결과로 대체
    ovs = [o for o in ovs if not o.get('r3')]
    newkeys = {(o['brand'], o['model'], str(y)) for o in NEW for y in o['years']}
    for o in ovs:
        if 'flag' in o and not o.get('delete'):
            o['years'] = [y for y in o['years'] if (o['brand'], o['model'], str(y)) not in newkeys]
    for o in NEW:
        o['r3'] = True
    ovs = [o for o in ovs if o['years']] + NEW
    json.dump(ovs, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('overrides', len(ovs))
    for b in sorted({o['brand'] for o in NEW}):
        print(b, recheck.apply_file(os.path.join(ROOT, FILES[b]), ovs))

# 5차(2026.9) — 애프터마켓 번호를 지워 순정 부품번호가 빈 BMW 행에 순정 번호 채우기
#   한국 사양(KO) 번호의 적용 차종은 확인 못 해, 적용 차대가 확인된 해외(ECE+RoW) 순정 번호를 [해외 공용 품번]으로 기재
#   근거: hubauer-shop.de·schmiedmann.com·recambiosyaccesoriosbmw.com·BMW 딜러 부품몰(차대 목록), 868MHz(유럽)·US 전용 번호는 제외
# 사용: python3 research/recheck5.py
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'recheck'))
import apply as recheck
SK = '스마트키(부품번호)'; BL = '키블레이드(부품번호)'
NEW = []
def B(model, years, col, val, guide=None):
    NEW.append(dict(brand='BMW', model=model, years=years, append={col: val}, **({'guide': guide} if guide else {})))

MS = '[M 스포츠, 해외 공용 품번]'
B('1시리즈 (F40, 3세대)', [2023], BL, '51215A4FBE5[비상키, 해외 공용 품번]',
  guide='BMW 순정 부품번호(애프터마켓 대체): 비상키 51215A4FBE5 = F40·F44·G20·G22·G26·G42·G80·G82 등 인서트 키(recambiosyaccesoriosbmw), '
        '51215A65D30 = U06·U10·U11·G60·G70·I20 등 인서트 키, 리모컨 66125A473F4(M 스포츠, ECE+RoW+US) = F40·F44·F9x·G01·G42·G87·G80·G82(hubauer·딜러몰), '
        '66125A47402(기본, ECE+RoW) = G01·G02·G08·G11·G12·G30(schmiedmann), 66125A56076(기본, ECE+RoW) = F15·F16·F39·F45·F46·F48(hubauer), '
        '66128708328(기본, ECE+RoW+US) = F40·G29(hubauer), 66125B3E8E1(M, ECE+RoW) = G60·G70·I20·U06·U10·U11 등, 66129362173 = i3 I01 434MHz(66126805980 대체), '
        '51217127047 = X3 E83 도어·점화 키 — 한국 사양(KO) 번호 적용 차종은 미확인이라 [해외 공용 품번]')
B('2시리즈 쿠페 (G42, 2세대)', [2025, 2026], SK, '66125A473F4' + MS)
B('M2 (G87)', [2024], BL, '51215A4FBE5[비상키, 추정]')
B('M2 (G87)', [2025, 2026], SK, '66125A473F4' + MS)
B('M4 (G82)', [2025, 2026], SK, '66125A473F4' + MS)
B('X3 (E83, 1세대)', [2005, 2006], BL, '51217127047[해외 공용 품번]')
B('5시리즈 (G60/G61, 8세대)', [2026], SK, '66125B3E8E1' + MS)
B('8시리즈 (G15/G16, 2세대)', [2025], SK, '66125A473F4[M 스포츠, 추정]')
B('M8 (G15/G16)', [2025], SK, '66125A473F4' + MS)
B('X4 (G02, 2세대)', [2023], SK, '66125A47402[해외 공용 품번]')
B('X5 (F15, 3세대)', [2017, 2018], SK, '66125A56076[해외 공용 품번]')
B('Z4 (G29, 3세대)', [2026], SK, '66128708328[해외 공용 품번]')
B('i3 (I01)', [2016, 2017], SK, '66129362173[해외 공용 품번]')
B('iX (I20)', [2023], BL, '51215A65D30[비상키, 해외 공용 품번]')
B('iX (I20)', [2026], SK, '66125B3E8E1' + MS)

if __name__ == '__main__':
    p = os.path.join(ROOT, 'research', 'recheck', 'overrides.json')
    ovs = [o for o in json.load(open(p, encoding='utf-8')) if not o.get('r5')]
    for o in NEW:
        o['r5'] = True
    ovs += NEW
    json.dump(ovs, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('overrides', len(ovs))
    print('BMW', recheck.apply_file(os.path.join(ROOT, 'BMW_코리아_출시모델.xlsx'), ovs))

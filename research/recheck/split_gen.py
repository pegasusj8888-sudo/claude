# 세대가 바뀌는 해를 세대별 행으로 나누기
#   한 연식 행에 구세대[TF]·신세대[JF] 값이 같이 적혀 있으면, 그 연식을 세대마다 1행씩 만든다.
#   같은 세대 안의 전환(부분변경·생산 시기·키 변경)은 한 행에 전·후 값을 함께 적는 기존 규칙 유지.
#   apply.apply_file()이 끝에서 호출(빌드 뒤에도 유지). 이미 나뉜 파일에서는 할 일이 없음.
import re
from copy import copy
from openpyxl.styles import PatternFill

# (모델명, 연식 앞 4자리, [(세대 태그, 새 모델명, 추가 설정)], 옵션)
#   새 모델명 None → 그 세대 행은 이미 따로 있으므로 만들지 않음
#   옵션 strip=False → 모델명에 세대가 없어서 [세대] 표기를 칸에 남김
#   옵션 manual={값: 태그} → 세대 표기가 없는 값의 세대 지정(없으면 모든 세대에 넣음)
SPLITS = [
    ('K3 (Forte, YD/BD)', '2018', [('YD', 'K3 (Forte, YD 페이스리프트)', {}), ('BD', 'K3 (Forte, BD)', {})], {}),
    ('K5 (Optima, TF/JF)', '2015', [('TF', 'K5 (Optima, TF)', {}), ('JF', 'K5 (Optima, JF)', {})], {}),
    ('K5 (Optima, JF/DL3)', '2019', [('JF', None, {}), ('DL3', 'K5 (Optima, DL3)', {})], {}),
    ('K7 (Cadenza, VG)', '2015', [('VG', 'K7 (Cadenza, VG)', {}), ('YG', 'K7 (Cadenza, YG)', {})],
     {'manual': {'81996-F6100': 'YG'}}),
    ('K9 (K900/Quoris, KH/RJ)', '2018', [('KH', 'K9 (K900/Quoris, KH)', {}), ('RJ', 'K9 (K900, RJ)', {})], {}),
    ('프라이드 JB/UB', '2011', [('JB', '프라이드 JB', {}), ('UB', '프라이드 UB', {})], {}),
    ('모닝 (Morning, TA/JA)', '2017', [('TA', '모닝 (Morning, TA)', {}), ('JA', '모닝 (Morning, JA)', {})], {}),
    ('스포티지 (Sportage, SL)', '2015', [('SL', '스포티지 (Sportage, SL)', {}), ('QL', '스포티지 (Sportage, QL)', {})], {}),
    ('스포티지 (Sportage, QL)', '2021', [('QL', '스포티지 (Sportage, QL)', {}), ('NQ5', '스포티지 (Sportage, NQ5)', {})], {}),
    ('쏘렌토 (Sorento, BL)', '2009', [('BL', '쏘렌토 (Sorento, BL)', {}), ('XM', '쏘렌토 (Sorento, XM)', {})], {}),
    ('쏘렌토 (Sorento, XM/UM)', '2014', [('XM', '쏘렌토 (Sorento, XM)', {}), ('UM', '쏘렌토 (Sorento, UM)', {})], {}),
    ('쏘렌토 (Sorento, UM/MQ4)', '2020', [('UM', '쏘렌토 (Sorento, UM 페이스리프트)', {}), ('MQ4', '쏘렌토 (Sorento, MQ4)', {})],
     {'manual': {'95440-P2000[5버튼]': 'MQ4', '95440-P2010': 'MQ4'}}),
    ('니로 (Niro, DE/SG2)', '2022', [('DE', '니로 (Niro, DE)', {}), ('SG2', '니로 (Niro, SG2)', {})], {}),
    ('카렌스 (Carens, UN/RP)', '2013', [('UN', '카렌스 (Carens, UN)', {}), ('RP', '카렌스 (Carens, RP)', {})], {}),
    ('카니발 (Carnival, VQ/YP)', '2014', [('VQ', '카니발 (Carnival, VQ)', {}), ('YP', '카니발 (Carnival, YP)', {})], {}),
    ('카니발 (Carnival, YP)', '2020', [('YP', '카니발 (Carnival, YP)', {}), ('KA4', '카니발 (Carnival, KA4)', {})], {}),
    ('A6 (C6, 6세대)', '2004', [('C5', 'A6 (C5, 5세대)', {}), ('C6', 'A6 (C6, 6세대)', {})], {}),
    ('TT (8S, 3세대)', '2015', [('8J', 'TT (8J, 2세대)', {'키종류': '폴딩키', '연식': '2015(단종)'}),
                                ('8S', 'TT (8S, 3세대)', {'키종류': '스마트키'})],
     {'manual': {'HU162T': '8S'}}),
    ('Q3 (F3, 2세대)', '2026', [('F3', 'Q3 (F3, 2세대)', {}),
                               ('3세대', 'Q3 (3세대)', {'키종류': None, 'flag': 'red', 'note': '3세대 Q3(2026.06~) 키 칩 자료 없음'})],
     {'manual': {'HU66': 'F3', 'HU162T': 'F3', '81A837220AG': 'F3'}, 'flag': ''}),
    ('S5', '2025', [('B9', 'S5', {}), ('B10', 'S5', {'flag': 'red', 'note': 'B10(2025.07~) 신형 키 칩 자료 없음'})],
     {'strip': False, 'flag': ''}),
    ('SQ5', '2025', [('FY', 'SQ5', {}), ('3세대', 'SQ5', {'flag': 'red', 'note': '3세대 SQ5 신형 키 칩 자료 없음'})],
     {'strip': False, 'flag': '', 'manual': {'HU66': 'FY'}}),
    ('콜로라도 (쉐보레)', '2024', [('2세대', '콜로라도 (쉐보레)', {'키종류': '막대키'}),
                              ('3세대', '콜로라도 (쉐보레)', {'키종류': '스마트키'})],
     {'strip': False, 'manual': {'FCC YG0G21TB2': '3세대'}}),
    ('SM7', '2011', [('1세대', 'SM7', {'키종류': '막대키,카드키'}),
                     ('2세대', 'SM7', {'키종류': '카드키', 'flag': 'orange',
                                      'note': '2세대(2011.8~) ID46 카드와 삼성 전용 AES 카드 병존 — 적용 구분 자료 없음'})],
     {'strip': False, 'flag': ''}),
    ('카렌스 (Carens, RS)', '2006', [('RS', '카렌스 (Carens, RS)', {'키종류': '막대키', 'flag': 'orange', 'note': '해외 카탈로그 상충(transpondery·keyclick: 카렌스 2001-2005 Texas 4D60, 다른 판매처: 2001-2012 ID46) — 국내 부품번호 원문 없음'}),
                                     ('UN', '카렌스 (Carens, UN)', {'키종류': '폴딩키', 'flag': 'orange', 'note': '954301D100 적용 시점은 954301D101(2007.7.2~) 이전 부품으로 추정'})], {}),
    ('셀토스 (SP2 PE)', '2026', [('SP2 PE', '셀토스 (SP2 PE)', {'flag': ''}),
                               ('SP3', '셀토스 (SP3)', {'키종류': None, 'flag': 'red', 'note': '디 올 뉴 셀토스(SP3, 2026.1~) 스마트키 품번·칩 자료 없음'})], {}),
]

# 같은 세대 안에서 연식 중간에 바뀐 경우(생산 시기·부분변경·키 변경)도 시기별 행으로 나눔.
#   모델명은 그대로(부분변경 이름이 따로 있으면 그 이름), 칸 안의 [시기] 표기는 남겨서 행을 구분.
def P(model, year, t1, t2, e1=None, e2=None, name2=None, **opt):
    opt.setdefault('strip', False)
    SPLITS.append((model, year, [(t1, model, e1 or {}), (t2, name2 or model, e2 or {})], opt))


for m, y in [('1시리즈 (E87, 1세대)', '2009'), ('3시리즈 (E90/E91/E92/E93, 5세대)', '2008'), ('5시리즈 (E60/E61, 5세대)', '2008'),
             ('M5 (E60)', '2008'), ('6시리즈 (E63/E64, 2세대)', '2008'), ('X5 (E70, 2세대)', '2008'), ('X6 (E71, 1세대)', '2008')]:
    P(m, y, '2008 중반 이전 생산', '2008 중반 이후 생산')
for m in ('5시리즈 (E60/E61, 5세대)', 'M5 (E60)', '6시리즈 (E63/E64, 2세대)'):
    P(m, '2007', '2007.3 LCI 이전 생산', '2007.3 LCI 이후 생산')
for m in ('5시리즈 GT (F07)', '5시리즈 (F10/F11, 6세대)', 'M5 (F10)', '6시리즈 (F12/F13/F06, 3세대)', 'M6 (F06/F12/F13)',
          '7시리즈 (F01/F02, 5세대)', 'X3 (F25, 2세대)'):
    P(m, '2012', '2012 중반 이전 생산', '2012 중반 이후 생산')
for m in ('5시리즈 (G30/G31, 7세대)', 'M5 (F90)', '6시리즈 그란 투리스모 (G32)'):
    P(m, '2020', '2020.6 이전 생산', '2020.7 이후 생산')
for m in ('X3 (G01, 3세대)', 'X3 M (F97)', 'X4 (G02, 2세대)', 'X4 M (F98)'):
    P(m, '2021', '2021.7 이전 생산', '2021.8 이후 생산')
P('iX3 (G08, 1세대)', '2021', '2021.8 이전 생산', '2021.9 이후 생산')
P('7시리즈 (E65/E66, 4세대)', '2005', '2005 LCI 이전 생산', '2005 LCI 이후 생산')
P('7시리즈 (G11/G12, 6세대)', '2019', '2019.2 이전 생산', '2019.3 이후 생산')
P('X3 (E83, 1세대)', '2006', '2006 중반 이전 생산', '2006 중반 이후 생산')
# 벤츠 FBS3 → FBS4
for m, y, mo in [('CLA (C117, 1세대)', '2014', '2014.11'), ('CLA45 AMG (C117/C118)', '2014', '2014.11'),
                 ('GLA (X156, 1세대)', '2014', '2014.11'), ('GLA35/45 AMG', '2014', '2014.11'),
                 ('E클래스 (W212, 9세대)', '2013', '2013.4'), ('E클래스 쿠페 (C207)', '2013', '2013.7'),
                 ('E클래스 카브리올레 (A207)', '2013', '2013.7'), ('M클래스 (W166, 3세대)', '2013', '2013.7'),
                 ('GL클래스 (X164/X166)', '2013', '2013.7'), ('CLS (C218, 2세대)', '2014', '2014.9'),
                 ('CLS53/63 AMG', '2014', '2014.9'), ('SLK/SLC (R172)', '2015', '2015.4')]:
    P(m, y, mo + ' 이전 생산', mo + ' 이후 생산')
P('GLK (X204)', '2015', '2015 초기 생산', '2015 후기 생산')
for m in ('A클래스 (W176, 3세대 해치백)', 'A45 AMG (W176/W177)', 'B클래스 (W246)'):   # MFA — CLA·GLA와 같은 2014.11 전환
    P(m, '2014', '2014.11 이전 생산', '2014.11 이후 생산')
for m, y in [('G클래스 (W463, 구형 바디)', '2016'), ('G63 AMG', '2016')]:
    P(m, y, 'A', 'B', manual={'FBS3': 'A', 'FBS4': 'B'})   # 전환 월 미확인 — 주황 유지
# 현대
P('쏘나타 (DN8, 8세대)', '2023', '~2023.2', '2023.3~')
P('아반떼 (XD, 3세대)', '2004', '~2004.6', '2004.7~', manual={'81996-25010[해외 공용 품번]': '2004.7~'},
  alias={'2005년형': '2004.7~'})
P('베르나 (MC, 2세대)', '2009', '~2009.5', '2009.6~', manual={'81996-1E010[이모빌라이저키]': '~2009.5'})
P('i40 (VF)', '2012', '~2012.4.2', '95440-3Z001 키', manual={'95440-3Z001': '95440-3Z001 키'})
P('스타렉스 (A1)', '2005', '~2005.6', '2005.7~', alias={'2006년형': '2005.7~', '2006년형~': '2005.7~'})
P('싼타페 (SM, 1세대)', '2004', '~2004.7', '2004.8~', alias={'2005년형~': '2004.8~', '2005년형': '2004.8~'})
P('투싼 (NX4, 4세대)', '2023', '~2023.10', '2023.11~', alias={'더 뉴 투싼': '2023.11~'})
P('제네시스 G70 (IK)', '2023', '이전 키', '95440-G9720 키', manual={'95440-G9720[5버튼]': '95440-G9720 키'})
P('제네시스 일렉트리파이드 GV70 (JK1 EV)', '2025', '~2025.1', '부분변경', e1={'flag': ''},
  e2={'flag': 'orange', 'note': '부분변경(2025.1) 스마트키 품번·칩 원문 없음 — GV70 부분변경(ID4A) 기준 추정'})
# 기아
P('K3 (Forte, BD)', '2021', '~4.26', '4.5~', name2='K3 (Forte, BD 페이스리프트)',
  manual={'95440-M6501[4버튼, ~3.24]': '~4.26', '95430-M6000[~4.21]': '~4.26'})
P('카니발 (Carnival, KV-II/GQ)', '2001', 'A', '2001.6.11~', manual={'ID48': 'A', 'ID60(4D60)': 'A'})
# 쉐보레
P('스파크 (쉐보레, M300)', '2013', '2013년형', '2014년형~', e1={'키종류': '막대키'}, e2={'키종류': '폴딩키'},
  manual={'HU100[M400 폴딩키 기준]': '2014년형~'})
P('토스카 (GM대우/쉐보레)', '2006', '2006년형', '2007년형~', alias={'2007년형': '2007년형~'})
# KGM
for m in ('액티언 (1세대)', '액티언 스포츠 (픽업)', '카이런'):
    P(m, '2007', '2007.3 이전 생산', '2007.4 이후 생산')
P('렉스턴 (1세대)', '2006', '2006.1 이전 생산', '2006.2 이후 생산')
P('G4 렉스턴 (2세대)', '2020', '2020.11 이전 생산', '2020.11 이후 생산',
  alias={'2017.07~2020.11': '2020.11 이전 생산', '2020.11~': '2020.11 이후 생산'}, e1={'flag': ''},
  e2={'flag': 'orange', 'note': '2020.11 이후 생산분 신형 스마트키(NXP 부품 표기) 칩 ID 자료 없음'})

# 1행만 남기거나 이름만 바꿀 때 연식 표기를 옮길 행: (모델명, 원래 연식) → 새 연식
RELABEL = {('TT (8J, 2세대)', '2014(단종)'): '2014'}
SKIP = ('브랜드', '모델명', '연식', 'XT27A/A66 호환', 'XT27B 호환', 'XT57B 호환', '출처', '비고', '키종류')


def _vals(s):
    out, depth, cur = [], 0, ''
    for ch in s:
        if ch in '([': depth += 1
        elif ch in ')]': depth -= 1
        if ch == ',' and depth == 0:
            out.append(cur.strip()); cur = ''
        else:
            cur += ch
    if cur.strip(): out.append(cur.strip())
    return out


def _tag_of(v, tags, alias=None):
    alias = alias or {}
    m = re.search(r'\[([^\[\]]*)\]$', v)
    if not m: return None, v
    toks = [t.strip() for t in m.group(1).split(',')]
    for t in toks:
        if t in tags or t in alias:
            rest = [x for x in toks if x != t]
            return alias.get(t, t), v[:m.start()] + ('[' + ', '.join(rest) + ']' if rest else '')
    return None, v


def split_cell(s, tags, strip, manual, alias=None):
    res = {t: [] for t in tags}
    for v in _vals(s):
        t, bare = _tag_of(v, tags, alias)
        if t is None and v in manual:
            t = manual[v]
        if t is None:
            for k in res: res[k].append(v)
        else:
            res[t].append(bare if strip else v)
    return {t: ', '.join(x) for t, x in res.items()}


def split_ws(ws, hr, hdr, xt, FILL, FONT, XTFILL, CHIP):
    n = 0
    for (old, y4, parts, opt) in SPLITS:
        r = next((r for r in range(hr + 1, ws.max_row + 1)
                  if ws.cell(r, hdr['모델명']).value == old and str(ws.cell(r, hdr['연식']).value or '')[:4] == y4), None)
        if r is None:
            continue
        tags = [p[0] for p in parts]
        alias = opt.get('alias', {})
        # 세대·시기 표기가 2개 이상 들어 있는 행만(이미 나뉜 행은 건너뜀)
        seen = {_tag_of(v, tags, alias)[0] or opt.get('manual', {}).get(v)
                for c, col in hdr.items() if c not in SKIP
                for v in _vals(str(ws.cell(r, col).value or ''))}
        if len(seen - {None}) < 2:
            continue
        strip = opt.get('strip', True); manual = opt.get('manual', {})
        src = {c: ws.cell(r, col).value for c, col in hdr.items()}
        style = {col: copy(ws.cell(r, col)._style) for col in hdr.values()}
        cells = {c: split_cell(str(v), tags, strip, manual, alias) for c, v in src.items() if c not in SKIP and v not in (None, '')}
        rows = []
        for tag, name, extra in parts:
            if name is None: continue
            d = dict(src); d['모델명'] = name
            for c in cells: d[c] = cells[c][tag] or None
            d.update({k: v for k, v in extra.items() if k not in ('flag', 'note')})
            fl = extra.get('flag', opt.get('flag'))
            rows.append((d, fl, extra.get('note')))
        # 전에 나눈 행이 남아 있으면(재조사 항목이 원래 행 값을 다시 넣은 경우) 지우고 다시 나눔
        names = {p[1] for p in parts if p[1]}
        for rr in range(ws.max_row, hr, -1):
            if rr != r and ws.cell(rr, hdr['모델명']).value in names and \
                    str(ws.cell(rr, hdr['연식']).value or '')[:4] == y4:
                ws.delete_rows(rr)
                if rr < r: r -= 1
        ws.delete_rows(r)
        if rows:
            ws.insert_rows(r, len(rows))
        for i, (d, fl, note) in enumerate(rows):
            rr = r + i
            for c, col in hdr.items():
                cell = ws.cell(rr, col); cell._style = copy(style[col]); cell.value = d.get(c)
            if CHIP in hdr and 'XT27A/A66 호환' in hdr:
                for c, v in zip(('XT27A/A66 호환', 'XT27B 호환', 'XT57B 호환'), xt(d.get(CHIP))):
                    cell = ws.cell(rr, hdr[c]); cell.value = v or None
                    if v in XTFILL:
                        cell.fill = PatternFill('solid', fgColor=XTFILL[v][0])
                        f = copy(cell.font); f.color = XTFILL[v][1]; cell.font = f
                    else:
                        cell.fill = PatternFill(fill_type=None)
            if fl is not None:
                for c in (CHIP, '이모빌라이저 시스템', '비고'):
                    if c not in hdr: continue
                    cell = ws.cell(rr, hdr[c])
                    if fl and not str(cell.value or '').strip():
                        cell.fill = PatternFill(fill_type=None); continue
                    cell.fill = PatternFill('solid', fgColor=FILL[fl]) if fl else PatternFill(fill_type=None)
                    f = copy(cell.font); f.color = FONT.get(fl, 'FF000000'); cell.font = f
                if '비고' in hdr:
                    ws.cell(rr, hdr['비고']).value = (note or None) if fl else None
        n += 1
    for r in range(hr + 1, ws.max_row + 1):
        k = (ws.cell(r, hdr['모델명']).value, str(ws.cell(r, hdr['연식']).value))
        if k in RELABEL:
            ws.cell(r, hdr['연식']).value = RELABEL[k]; n += 1
    return n

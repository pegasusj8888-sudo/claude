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
]
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


def _tag_of(v, tags):
    m = re.search(r'\[([^\[\]]*)\]$', v)
    if not m: return None, v
    toks = [t.strip() for t in m.group(1).split(',')]
    for t in toks:
        if t in tags:
            rest = [x for x in toks if x != t]
            return t, v[:m.start()] + ('[' + ', '.join(rest) + ']' if rest else '')
    return None, v


def split_cell(s, tags, strip, manual):
    res = {t: [] for t in tags}
    for v in _vals(s):
        t, bare = _tag_of(v, tags)
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
        # 세대 표기가 2개 이상 들어 있는 행만(이미 나뉜 행은 건너뜀)
        seen = {_tag_of(v, tags)[0] for c, col in hdr.items() if c not in SKIP
                for v in _vals(str(ws.cell(r, col).value or ''))}
        if len(seen - {None}) < 2:
            continue
        strip = opt.get('strip', True); manual = opt.get('manual', {})
        src = {c: ws.cell(r, col).value for c, col in hdr.items()}
        style = {col: copy(ws.cell(r, col)._style) for col in hdr.values()}
        cells = {c: split_cell(str(v), tags, strip, manual) for c, v in src.items() if c not in SKIP and v not in (None, '')}
        rows = []
        for tag, name, extra in parts:
            if name is None: continue
            d = dict(src); d['모델명'] = name
            for c in cells: d[c] = cells[c][tag] or None
            d.update({k: v for k, v in extra.items() if k not in ('flag', 'note')})
            fl = extra.get('flag', opt.get('flag'))
            rows.append((d, fl, extra.get('note')))
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

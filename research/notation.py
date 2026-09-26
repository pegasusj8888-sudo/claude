# 칩코드·부품번호·키웨이·이모빌라이저 칸 표기 통일
#   - 여러 값은 ", "로만 구분 ("/", "·", "또는", 범위 줄임 안 씀)
#   - ( ) 안에는 부품번호(칩 번호·모듈 품번)만:  ID49(PCF7953), SKM(87570-36010)
#   - [ ] 안에는 적용 조건만(키 종류·버튼 수·옵션·생산 시기·차종 코드·추정)
#   - 부품번호 칸은 부품번호만. FCC ID는 "FCC ", 한국 전파인증은 "KC " 접두
# 사용: python3 research/notation.py            → 저장소 루트의 모든 .xlsx에 적용
#       python3 research/notation.py --check    → 규칙 위반 값만 출력(파일 안 바꿈)
#       build_xlsx.py에서는 apply_file(경로) 호출
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CHIP = '칩코드 (예: ID46(PCF7936))'
IMMO = '이모빌라이저 시스템'
KEYWAY = '키블레이드(키웨이)'
PN_COLS = ('키블레이드(부품번호)', '카드키(부품번호)', '스마트키(부품번호)', '폴딩키(부품번호)')
COLS = (CHIP, IMMO, KEYWAY) + PN_COLS


def load_manual():
    m, col = {}, None
    for line in open(os.path.join(HERE, 'notation_manual.txt'), encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('## '):
            col = line[3:].strip()
            m.setdefault(col, {})
        elif ' ⇒' in line and col:
            old, new = line.split(' ⇒', 1)
            m[col][old] = new.strip()
    return m


MANUAL = load_manual()

# ───── 기아 부품번호 칸: 규칙 변환 ─────
_PN = r'(?:\d{5}-[0-9A-Z]{5}|\d{6}[0-9A-Z]{4}(?:CA)?|\d{5}[A-Z0-9]{5}|[0-9A-Z]{2}\d{3}[A-Z0-9]{5})'
_MC = r'(?:[A-Z]{2}\d?|[A-Z]{1,3}\d[A-Z]?\d?|SP2 PE)'  # 차종 코드(YD, JF, DL3, SG2, NQ5 …)
_DROP = re.compile(r'원문|미확인|확인 필요')


def _split_top(s, sep):
    out, depth, cur, i = [], 0, '', 0
    while i < len(s):
        if s.startswith(sep, i) and depth == 0:
            out.append(cur); cur = ''; i += len(sep); continue
        ch = s[i]; depth += ch == '('; depth -= ch == ')'; cur += ch; i += 1
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def _conds(txt):
    txt = re.sub(r'\(([^()]*)\)', r' \1', txt)
    out = []
    for x in re.split(r',\s*|·|/', txt):
        x = x.strip()
        if not x or _DROP.search(x):
            continue
        m = re.match(r'^(' + _MC + r')\s+(.+)$', x)
        out += [m.group(1), m.group(2)] if m else [x]
    return out


def _is_mc(c):
    return re.fullmatch(_MC, c.strip()) is not None


def kia_pn(s):
    segs = []
    for big in _split_top(s, ' // '):
        prefix = []
        for seg in _split_top(big, ' / '):
            m = re.match(r'^((?:(?!' + _PN + r')[^:])+):\s*(.*)$', seg)
            if m:
                prefix = _conds(m.group(1)); seg = m.group(2)
            items = []
            for it in _split_top(seg, ', '):
                m = re.match(r'^(' + _PN + r')(?:\s*계열)?((?:\([^()]*\))*)$', it)
                if not m:
                    return None
                items.append([m.group(1), re.findall(r'\(([^()]*)\)', m.group(2))])
            grp, last = [], items[-1][1]
            if len(last) == 2:  # "A(x), B(y)(공통)" → 공통 조건은 모두에
                grp = _conds(last.pop())
            elif (len(items) > 1 and len(last) == 1 and all(not p[1] for p in items[:-1])
                  and not re.search(r'\d+년형', last[0])):  # "A, B(조건)" → 둘 다
                grp = _conds(last.pop())
            segs.append({'items': items, 'grp': grp, 'prefix': list(prefix)})
    # 차종 코드(YD, JF …)는 코드 없는 앞 세그먼트에도 적용
    for i, sg in enumerate(segs):
        codes = [c for c in sg['grp'] if _is_mc(c)]
        j = i - 1
        while codes and j >= 0:
            own = segs[j]['grp'] + [c for it in segs[j]['items'] for p in it[1] for c in _conds(p)]
            if any(_is_mc(c) for c in own):
                break
            segs[j]['grp'] = segs[j]['grp'] + codes
            j -= 1
    out = []
    for sg in segs:
        for pn, ps in sg['items']:
            cs = [c for p in ps for c in _conds(p)] + sg['grp'] + sg['prefix']
            cs = [c for c in cs if _is_mc(c)] + [c for c in cs if not _is_mc(c)]
            uniq = []
            for c in cs:
                if c not in uniq:
                    uniq.append(c)
            out.append(pn + ('[' + ', '.join(uniq) + ']' if uniq else ''))
    return ', '.join(out)


# ───── 변환·검사 ─────
def normalize(col, value, brand=''):
    if value is None:
        return value
    v = str(value)
    if not v.strip() or col not in COLS:
        return value
    man = MANUAL.get(col, {})
    if v in man:
        return man[v]
    if col in PN_COLS and brand.startswith('기아'):
        r = kia_pn(v)
        if r is not None:
            return r
    return v


def _top_items(v):
    out, depth, cur = [], 0, ''
    for ch in v:
        depth += ch == '['; depth -= ch == ']'
        if ch == ',' and depth == 0:
            out.append(cur.strip()); cur = ''
        else:
            cur += ch
    out.append(cur.strip())
    return out


def problems(col, v):
    """규칙에 어긋나는 점 목록(빈 목록이면 통과)"""
    v = str(v or '')
    if not v.strip() or col not in COLS:
        return []
    p = []
    outside = re.sub(r'\[[^\]]*\]', '', v)
    if re.search(r'/|·| 또는 |—', outside):
        p.append('구분자(/ · 또는 —)')
    if 'MHz' in v:
        p.append('주파수 표기')
    if v.count('[') != v.count(']') or v.count('(') != v.count(')'):
        p.append('괄호 짝')
    if re.search(r'\[[^\]]*[()]', v):
        p.append('[ ] 안 괄호')
    for it in _top_items(v):
        if not it:
            p.append('빈 항목'); continue
        base = re.sub(r'\[[^\]]*\]$', '', it)
        if '[' in base or ']' in base:
            p.append('조건 위치: ' + it)
        if col in PN_COLS + (KEYWAY,) and '(' in base:
            p.append('부품번호 칸 괄호: ' + it)
        m = re.search(r'\(([^()]*)\)', base)
        if m and ' ' in m.group(1).strip():
            p.append('( ) 안 설명: ' + it)
    return p


# ───── 안내 시트 ─────
GUIDE_FIX = {  # 예전 표기를 설명하던 문장 고치기
    "- 복수 칩이 확인된 경우 'ID46(PCF7952) / ID47(NCF2951)' 처럼 '/'로 나열합니다. 다른 컬럼도 동일 규칙 적용.":
        "- 복수 칩이 확인된 경우 'ID46(PCF7952), ID47(NCF2951)'처럼 쉼표로 나열합니다. 다른 컬럼도 같은 규칙입니다(아래 '표기 규칙' 참고).",
    "'(카드키용)'으로 구분해": "'[카드키용]'으로 구분해",
    "부품번호 뒤 괄호의 'N버튼'": "부품번호 뒤 대괄호 [ ]의 'N버튼'",
    "- 이모빌라이저는 EIS(EZS, 전자식 점화 스위치 모듈)이며 칸에 FBS3/FBS4 세대를 함께 적었습니다.":
        "- 이모빌라이저는 EIS(EZS, 전자식 점화 스위치 모듈)입니다. FBS3/FBS4 세대는 칩코드 칸에 적었습니다.",
    "(예: FBS3(2013.4 이전 생산) / FBS4(2013.4 이후 생산))": "(예: FBS3[2013.4 이전 생산], FBS4[2013.4 이후 생산])",
    "(예: TT 2015 = 8J ID48 / 8S MQB)": "(예: TT 2015 = ID48[8J, 2015.10 이전], ID88[8S])",
    "- CAS4/CAS4+ 키의 칩은 PCF7953(Hitag Pro, ID49, EWS5)입니다(이전 초안의 'Hitag2' 표기는 오류였음).":
        "- CAS4/CAS4+ 키의 칩은 ID49(PCF7953)입니다(Hitag Pro 계열, 이전 초안의 'Hitag2' 표기는 오류였음). 일부 판매처는 이 칩을 'EWS5'로 부르지만 이모빌라이저 이름(EWS)과 헷갈려 쓰지 않았습니다.",
}
GUIDE_BLOCK = [
    '',
    '※ 표기 규칙 (칩코드·부품번호·키웨이·이모빌라이저 칸 공통)',
    "- 한 칸에 값이 여러 개면 ', '(쉼표)로만 구분합니다. '/', '·', '또는'은 쓰지 않고, 줄임(예: 4F0837220M/T, 5WK49145~49147)도 모두 풀어서 따로 적었습니다.",
    "- ( ) 안에는 부품번호만 적습니다. 칩코드 'ID49(PCF7953)' = ID49 칩, 칩 부품번호 PCF7953. 이모빌라이저 'SKM(87570-36010)' = SKM 모듈, 품번 87570-36010. 칩 부품번호를 모르면 'ID46'처럼 ID만 적었습니다.",
    "- [ ] 안에는 그 값이 적용되는 조건을 적습니다(키 종류·버튼 수·옵션·생산 시기·차종 코드). 예: ID46(PCF7936)[폴딩키], ID46(PCF7952A)[스마트키] → 폴딩키는 PCF7936, 스마트키는 PCF7952A.",
    "- [추정] = 추정값, [일부 자료] = 일부 자료에만 나오는 값, [자료 상충] = 자료마다 달라 둘 중 무엇인지 미확정, [해외 공용 품번] = 해외 공용 품번(국내 순정 품번 미확인).",
    "- 부품번호 칸에는 부품번호만 적습니다. 'FCC ' = 미국 FCC 인증번호(키 모델 식별용), 'KC ' = 한국 전파인증번호, [애프터마켓] = 순정이 아닌 호환품 번호. 설명·판매처·주파수(모두 국내 433/434MHz)는 적지 않았고, 부품번호가 없으면 공란입니다.",
    "- Hitag2·Hitag Pro·Megamos·DST80 같은 칩 방식 이름은 ID 코드와 같은 뜻이라 칸에 따로 적지 않았습니다(아래 표).",
    '',
    '※ 칩 ID 코드 뜻',
    '- ID13: Megamos 13(고정 코드)  |  ID44: Philips Crypto(PCF7935, BMW EWS 구형)  |  ID48: Megamos Crypto',
    '- ID46: Philips Hitag2 계열(PCF7936·PCF7941·PCF7945·PCF7952 등). [Extended] = Hitag2 Extended, [Circle Plus] = GM Circle Plus',
    '- ID47: NXP Hitag3(NCF2951·NCF2952·NCF2971·PCF7938 등)  |  ID49: NXP Hitag Pro(PCF7953P·NCF2951·NCF295X 등)  |  ID4A: NXP Hitag AES(NCF29A1M·PCF7953M·PCF7961M 등)',
    '- ID60: Texas 4D60(40bit)  |  4D60x80: Texas 4D60 80bit(DST80 계열)  |  ID70: Texas 4D70  |  ID6E-MA: Texas DST80(현대·기아 표기)',
    '- ID6A·ID8A: Texas Crypto AES(DST-AES)  |  ID75: Texas AES(판매처 표기)  |  ID88: Megamos AES(VW·아우디 MQB)  |  ID8E: 아우디 8E Crypto(Sokymat 8E)',
    '- FBS3·FBS4: 벤츠 NEC 프로세서 키(ID 칩이 아님)  |  MLB 전용 칩·MLB evo 전용 칩: 아우디 MLB 플랫폼 전용 키 칩',
    '- 확인 불가 = 자료로 확인하지 못함  |  해당 없음 = 이모빌라이저 미적용',
]


def fix_guide(wb):
    from copy import copy
    from openpyxl.styles import Alignment
    if '안내' not in wb.sheetnames:
        return 0
    g, n = wb['안내'], 0
    for c in g['A']:
        v = c.value
        if isinstance(v, str):
            nv = v
            for a, b in GUIDE_FIX.items():
                nv = nv.replace(a, b)
            if nv != v:
                c.value = nv; n += 1
    if not any(c.value == GUIDE_BLOCK[1] for c in g['A']):
        ref = g.cell(g.max_row, 1)
        for line in GUIDE_BLOCK:
            r = g.max_row + 1
            g.cell(r, 1).value = line or None
            g.cell(r, 1)._style = copy(ref._style)
            g.cell(r, 1).alignment = Alignment(wrap_text=False, vertical='top')
            n += 1
    return n


# ───── 엑셀 적용 ─────
def apply_file(path):
    sys.path.insert(0, HERE)
    from add_brand import _load, _header_row
    wb = _load(path)
    changed, bad = 0, []
    for ws in wb.worksheets:
        hr, _ = _header_row(ws)
        if hr is None:
            continue
        hdr = {str(c.value).strip(): c.column for c in ws[hr] if c.value}
        bcol = hdr.get('브랜드')
        for r in range(hr + 1, ws.max_row + 1):
            brand = str(ws.cell(r, bcol).value or '') if bcol else os.path.basename(path)
            for col in COLS:
                if col not in hdr:
                    continue
                cell = ws.cell(r, hdr[col])
                new = normalize(col, cell.value, brand)
                if new != cell.value:
                    cell.value = new if new != '' else None
                    changed += 1
                for pr in problems(col, cell.value):
                    bad.append((os.path.basename(path), r, col, cell.value, pr))
    changed += fix_guide(wb)
    if changed:
        wb.save(path)
    return changed, bad


if __name__ == '__main__':
    check = '--check' in sys.argv
    files = [a for a in sys.argv[1:] if not a.startswith('--')] or \
        [os.path.join(ROOT, f) for f in sorted(os.listdir(ROOT)) if f.endswith('.xlsx')]
    total_bad = []
    for f in files:
        if check:
            sys.path.insert(0, HERE)
            from add_brand import _load, _header_row
            wb = _load(f)
            for ws in wb.worksheets:
                hr, _ = _header_row(ws)
                if hr is None:
                    continue
                hdr = {str(c.value).strip(): c.column for c in ws[hr] if c.value}
                for r in range(hr + 1, ws.max_row + 1):
                    for col in COLS:
                        if col in hdr:
                            for pr in problems(col, ws.cell(r, hdr[col]).value):
                                total_bad.append((os.path.basename(f), r, col, ws.cell(r, hdr[col]).value, pr))
        else:
            n, bad = apply_file(f)
            total_bad += bad
            print(os.path.basename(f), '변경', n, '칸')
    for b in total_bad:
        print('규칙 위반:', *b, sep=' | ')
    print('규칙 위반', len(total_bad), '건')

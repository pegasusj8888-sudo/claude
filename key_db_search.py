# -*- coding: utf-8 -*-
"""트랜스폰더 DB 검색·수정 프로그램

실행하면 엑셀 파일이 있는 폴더를 고르고, 그 폴더의 모든 .xlsx 파일
(파일명 구분 없음)에서 모델명·연식으로 검색합니다.
- 모델명/연식 중 하나만 넣어도 되고 둘 다 넣어도 됩니다(입력값을 포함하는 행 모두 표시).
- 모델명 칸에는 브랜드도 함께 넣을 수 있습니다(예: "기아 K5" → 기아 K5, "기아" → 기아 모든 차).
- 결과를 고르고 [수정](또는 더블클릭)하면 값을 고칠 수 있고, 원본 엑셀 파일에 바로 저장됩니다.
- 검색 결과는 엑셀에서 주황·빨강으로 칠한 칸(불완전한 항목)만 같은 색으로 보여 줍니다(행 전체가 아님).
- 파이썬 표준 라이브러리만 사용합니다(openpyxl 불필요). 저장할 때는 고친 셀만 바꾸고
  서식·색·다른 시트는 그대로 둡니다(한셀·엑셀에서 저장한 파일 모두 가능).
"""
import os, sys, re, json, shutil, tempfile, zipfile, posixpath
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

NS_MAIN = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
NS_REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS_PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
NS_MC = 'http://schemas.openxmlformats.org/markup-compatibility/2006'
M = '{%s}' % NS_MAIN

MODEL_ALIASES = ('모델명', '모델이름', '모델', '차종', '차명')
YEAR_ALIASES = ('연식', '년식', '연도', '년도')
BRAND_ALIASES = ('브랜드', '제조사', '메이커')
MODEL, YEAR, BRAND = '모델명', '연식', '브랜드'
FILE_COL = '파일'
# 설정(마지막 폴더·컬럼 너비)은 이 파이썬 파일과 같은 폴더에 저장
_HERE = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
CONFIG = os.path.join(_HERE, 'key_db_search_config.json')
FLAG_COLORS = {'FFD599': 'orange', 'FFC7CE': 'red'}


# ───────────────────────── 엑셀 읽기 ─────────────────────────
def col_to_idx(col):
    n = 0
    for ch in col:
        n = n * 26 + ord(ch) - 64
    return n


def idx_to_col(n):
    s = ''
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def split_ref(ref):
    m = re.match(r'([A-Z]+)(\d+)$', ref)
    return col_to_idx(m.group(1)), int(m.group(2))


def _text(el):
    """<si>/<is> 안의 모든 <t> 글자를 이어 붙임(서식 있는 글자 포함, 발음 표기 제외)."""
    skip = {id(t) for ph in el.iter(M + 'rPh') for t in ph.iter(M + 't')}
    return ''.join(t.text or '' for t in el.iter(M + 't') if id(t) not in skip)


def _xf_list(parent):
    """cellXfs/fills 등의 자식 목록. mc:AlternateContent는 Fallback(없으면 Choice)의 첫 요소로 1개로 셈."""
    items = []
    for ch in parent:
        if ch.tag == '{%s}AlternateContent' % NS_MC:
            pick = ch.find('{%s}Fallback' % NS_MC)
            if pick is None or len(pick) == 0:
                pick = ch.find('{%s}Choice' % NS_MC)
            items.append(pick[0] if pick is not None and len(pick) else None)
        else:
            items.append(ch)
    return items


def _style_flags(z):
    """스타일 번호 → 'orange'/'red' (주황·빨강 채우기인 경우만)."""
    try:
        root = ET.fromstring(z.read('xl/styles.xml'))
    except Exception:
        return {}
    fills_el, xfs_el = root.find(M + 'fills'), root.find(M + 'cellXfs')
    if fills_el is None or xfs_el is None:
        return {}
    fills = []
    for f in _xf_list(fills_el):
        rgb = ''
        if f is not None:
            fg = f.find('.//' + M + 'fgColor')
            if fg is not None:
                rgb = (fg.get('rgb') or '')[-6:].upper()
        fills.append(rgb)
    out = {}
    for i, xf in enumerate(_xf_list(xfs_el)):
        if xf is None:
            continue
        try:
            rgb = fills[int(xf.get('fillId', 0))]
        except (ValueError, IndexError):
            continue
        if rgb in FLAG_COLORS:
            out[i] = FLAG_COLORS[rgb]
    return out


def _sheet_paths(z):
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    target = {r.get('Id'): r.get('Target') for r in rels.iter('{%s}Relationship' % NS_PKG)}
    out = []
    for s in wb.iter(M + 'sheet'):
        t = target.get(s.get('{%s}id' % NS_REL), '')
        path = t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join('xl', t))
        out.append((s.get('name'), path))
    return out


def read_sheet(z, path, shared):
    """시트 → {행번호: {열번호: (값, 스타일번호)}}"""
    root = ET.fromstring(z.read(path))
    data = {}
    rno = 0
    for row in root.iter(M + 'row'):
        rno = int(row.get('r')) if row.get('r') else rno + 1
        cells, cno = {}, 0
        for c in row.findall(M + 'c'):
            if c.get('r'):
                cno, _ = split_ref(c.get('r'))
            else:
                cno += 1
            t = c.get('t')
            v = c.find(M + 'v')
            if t == 's':
                val = shared[int(v.text)] if v is not None and v.text else ''
            elif t == 'inlineStr':
                isel = c.find(M + 'is')
                val = _text(isel) if isel is not None else ''
            elif t == 'b':
                val = 'TRUE' if v is not None and v.text == '1' else 'FALSE'
            else:
                val = v.text if v is not None and v.text is not None else ''
                if t in (None, 'n') and re.fullmatch(r'-?\d+\.0+', val):
                    val = val.split('.')[0]
            cells[cno] = (val, int(c.get('s', 0)))
        data[rno] = cells
    return data


def _canon(h):
    h = (h or '').strip()
    if h in MODEL_ALIASES:
        return MODEL
    if h in YEAR_ALIASES:
        return YEAR
    if h in BRAND_ALIASES:
        return BRAND
    return h


def load_workbook_rows(fpath):
    """파일 하나에서 모델명·연식 머리행이 있는 시트의 모든 데이터 행을 읽음."""
    recs = []
    with zipfile.ZipFile(fpath) as z:
        names = set(z.namelist())
        shared = []
        if 'xl/sharedStrings.xml' in names:
            sroot = ET.fromstring(z.read('xl/sharedStrings.xml'))
            shared = [_text(si) for si in sroot.findall(M + 'si')]
        flags = _style_flags(z)
        for sname, spath in _sheet_paths(z):
            if spath not in names:
                continue
            data = read_sheet(z, spath, shared)
            hdr_row = None
            for r in sorted(data)[:10]:
                vals = {_canon(v) for v, _ in data[r].values()}
                if MODEL in vals and YEAR in vals:
                    hdr_row = r
                    break
            if hdr_row is None:
                continue  # 안내 시트 등
            header = {c: _canon(v) for c, (v, _) in data[hdr_row].items() if str(v).strip()}
            cols = [header[c] for c in sorted(header)]
            for r in sorted(data):
                if r <= hdr_row:
                    continue
                cells = data[r]
                values = {header[c]: cells[c][0] for c in header if c in cells}
                if not any(str(v).strip() for v in values.values()):
                    continue
                cflags = {}  # 칸별 색: {컬럼명: 'orange'/'red'} — 엑셀에서 칠한 칸만
                for c in header:  # XT 호환 칸의 'X' 빨강은 호환 표시라 제외
                    if header[c].startswith('XT'):
                        continue
                    if c in cells and cells[c][1] in flags:
                        cflags[header[c]] = flags[cells[c][1]]
                flag = 'red' if 'red' in cflags.values() else 'orange' if cflags else ''
                recs.append({'file': fpath, 'sheet': sname, 'sheet_path': spath,
                             'row': r, 'cols': cols,
                             'colidx': {h: c for c, h in header.items()},
                             'values': values, 'flag': flag, 'flags': cflags})
    return recs


def load_folder(folder):
    recs, errors, files = [], [], []
    for fn in sorted(os.listdir(folder)):
        if not fn.lower().endswith(('.xlsx', '.xlsm')) or fn.startswith('~$'):
            continue
        fp = os.path.join(folder, fn)
        try:
            rs = load_workbook_rows(fp)
            files.append(fn)
            recs.extend(rs)
        except Exception as e:  # 손상/암호 파일 등
            errors.append('%s: %s' % (fn, e))
    return recs, files, errors


def all_columns(recs):
    """파일마다 다른 컬럼을 엑셀 순서를 유지하며 합침(예: 기아 파일엔 '키종류' 없음)."""
    cols = []
    for r in recs:
        prev = -1
        for h in r['cols']:
            if h in cols:
                prev = cols.index(h)
            else:
                cols.insert(prev + 1, h)
                prev += 1
    return cols


def _norm(s):
    return re.sub(r'\s+', '', str(s)).lower()


def _match_model(query, brand, model):
    """모델명 칸 검색: 띄어 쓴 낱말 중 브랜드에 들어 있는 낱말은 브랜드로 보고,
    나머지 낱말을 이어 붙인 글자가 모델명에 들어 있으면 일치.
    예) '기아 K5', '쌍용 렉스턴', '기아'(기아 전체), 'a 6'(A6)"""
    b, mo = _norm(brand), _norm(model)
    if _norm(query) in mo:
        return True
    words = [_norm(w) for w in query.split() if w.strip()]
    rest = [w for w in words if not (b and w in b)]
    if len(rest) == len(words):  # 브랜드 낱말이 없음
        return False
    return ''.join(rest) in mo


def search(recs, model='', year=''):
    m, y = _norm(model), _norm(year)
    if not m and not y:  # 빈 검색은 결과 없음
        return []
    return [r for r in recs
            if (not m or _match_model(model, r['values'].get(BRAND, ''), r['values'].get(MODEL, '')))
            and (not y or y in _norm(r['values'].get(YEAR, '')))]


# ───────────────────────── 엑셀 쓰기 ─────────────────────────
_ILLEGAL = re.compile('[\x00-\x08\x0b\x0c\x0e-\x1f]')
_ATTR = re.compile(r'([\w:]+)\s*=\s*("[^"]*"|\'[^\']*\')')


def _cell_xml(pfx, ref, attrs, value, keep_number):
    a = {k: v for k, v in attrs if k not in ('r', 't')}
    head = '<%sc r="%s"' % (pfx, ref) + ''.join(' %s=%s' % (k, v) for k, v in a.items())
    value = _ILLEGAL.sub('', value)
    if value == '':
        return head + '/>'
    if keep_number and re.fullmatch(r'-?\d+(\.\d+)?', value):
        return head + '><%sv>%s</%sv></%sc>' % (pfx, value, pfx, pfx)
    return head + ' t="inlineStr"><%sis><%st xml:space="preserve">%s</%st></%sis></%sc>' % (
        pfx, pfx, escape(value), pfx, pfx, pfx)


def _patch_row(xml, rownum, changes):
    """시트 XML 텍스트에서 rownum 행의 셀들만 바꿈. changes = {열번호: 새 값}"""
    m = re.search(r'<((?:\w+:)?)row\b[^>]*?\br=["\']%d["\'][^>]*?(/?)>' % rownum, xml)
    if not m:
        raise ValueError('%d행을 파일에서 찾을 수 없습니다' % rownum)
    pfx = m.group(1)
    if m.group(2):  # <row .../> → 빈 행을 열고 닫는 형태로
        start_tag = m.group(0)[:-2].rstrip() + '>'
        xml = xml[:m.start()] + start_tag + '</%srow>' % pfx + xml[m.end():]
        body_start = m.start() + len(start_tag)
    else:
        body_start = m.end()
    body_end = xml.index('</%srow>' % pfx, body_start)
    body = xml[body_start:body_end]
    cell_re = re.compile(r'<(?:\w+:)?c\b([^>]*?)(?:/>|>.*?</(?:\w+:)?c>)', re.S)
    cells = []  # (열번호, start, end, attrs)
    for cm in cell_re.finditer(body):
        attrs = _ATTR.findall(cm.group(1))
        ad = dict(attrs)
        ref = ad.get('r', '').strip('"\'')
        if not ref:
            raise ValueError('셀 주소(r)가 없는 형식이라 수정할 수 없습니다')
        cells.append((split_ref(ref)[0], cm.start(), cm.end(), attrs))
    for col in sorted(changes, reverse=True):
        value = changes[col]
        ref = '%s%d' % (idx_to_col(col), rownum)
        hit = [c for c in cells if c[0] == col]
        if hit:
            _, s, e, attrs = hit[0]
            t = dict(attrs).get('t', '"n"').strip('"\'')
            new = _cell_xml(pfx, ref, attrs, value, keep_number=(t == 'n'))
            body = body[:s] + new + body[e:]
        else:
            if value == '':
                continue
            pos = next((c[1] for c in cells if c[0] > col), len(body))
            new = _cell_xml(pfx, ref, [], value, keep_number=False)
            body = body[:pos] + new + body[pos:]
        # 뒤쪽부터 바꾸므로 앞쪽 셀 위치는 그대로
    return xml[:body_start] + body + xml[body_end:]


def save_changes(rec, changes):
    """rec(검색 결과 한 행)의 값 중 changes={컬럼명: 새 값}을 원본 파일에 저장."""
    fpath = rec['file']
    # 불러온 뒤 파일이 바뀌지 않았는지 확인(모델명·연식이 그대로인지)
    fresh = [r for r in load_workbook_rows(fpath)
             if r['sheet'] == rec['sheet'] and r['row'] == rec['row']]
    if not fresh or any(fresh[0]['values'].get(k, '') != rec['values'].get(k, '')
                        for k in (MODEL, YEAR)):
        raise RuntimeError('불러온 뒤 파일 내용이 바뀌었습니다. [다시 불러오기] 후 수정하세요.')
    colchanges = {rec['colidx'][h]: v for h, v in changes.items()}
    with zipfile.ZipFile(fpath) as zin:
        xml = zin.read(rec['sheet_path']).decode('utf-8')
        xml = _patch_row(xml, rec['row'], colchanges)
        ET.fromstring(xml.encode('utf-8'))  # 깨진 XML이면 여기서 중단(원본 보존)
        fd, tmp = tempfile.mkstemp(suffix='.xlsx', dir=os.path.dirname(fpath))
        os.close(fd)
        try:
            with zipfile.ZipFile(tmp, 'w') as zout:
                for info in zin.infolist():
                    data = xml.encode('utf-8') if info.filename == rec['sheet_path'] else zin.read(info)
                    zout.writestr(info, data, compress_type=info.compress_type)
        except Exception:
            os.remove(tmp)
            raise
    try:
        shutil.copymode(fpath, tmp)
        os.replace(tmp, fpath)
    except PermissionError:
        os.remove(tmp)
        raise PermissionError('파일이 엑셀/한셀에서 열려 있어 저장할 수 없습니다. 파일을 닫고 다시 시도하세요.')
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
    rec['values'].update(changes)


# ───────────────────────── 화면 ─────────────────────────
CELL_BG = {'orange': '#FFD599', 'red': '#FFC7CE'}
SEL_BG = '#CCE4FF'


def run_gui():
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    import tkinter.font as tkfont

    class CellTable(ttk.Frame):
        """칸마다 배경색을 줄 수 있는 표(ttk.Treeview는 행 단위 색만 가능해서 Canvas로 그림).
        보이는 행만 그려서 결과가 많아도 빠름. 머리글 경계를 끌어 컬럼 너비 조절."""
        PAD = 4

        def __init__(self, master, on_double=None, on_resize=None):
            super().__init__(master)
            self.font = tkfont.nametofont('TkDefaultFont')
            self.hfont = self.font.copy()
            self.hfont.configure(weight='bold')
            self.rowh = self.font.metrics('linespace') + 8
            self.cols, self.widths, self.rows, self.sel = [], [], [], None
            self.on_double, self.on_resize = on_double, on_resize
            self._drag = None
            self._fit_cache = {}
            self.head = tk.Canvas(self, height=self.rowh, bg='#E8E8E8', highlightthickness=0)
            self.body = tk.Canvas(self, bg='white', highlightthickness=0, takefocus=1)
            self.ys = ttk.Scrollbar(self, orient='vertical', command=self._yview)
            self.xs = ttk.Scrollbar(self, orient='horizontal', command=self._xview)
            self.body.configure(yscrollcommand=self.ys.set, xscrollcommand=self._xset)
            self.head.grid(row=0, column=0, sticky='ew')
            self.body.grid(row=1, column=0, sticky='nsew')
            self.ys.grid(row=1, column=1, sticky='ns')
            self.xs.grid(row=2, column=0, sticky='ew')
            self.rowconfigure(1, weight=1)
            self.columnconfigure(0, weight=1)
            self.body.bind('<Configure>', lambda e: self.redraw())
            self.body.bind('<Button-1>', self._click)
            self.body.bind('<Double-1>', self._double)
            for w in (self.body, self.head):
                w.bind('<MouseWheel>', self._wheel)
                w.bind('<Shift-MouseWheel>', lambda e: self._xview('scroll', -int(e.delta / 120) or -1, 'units'))
                w.bind('<Button-4>', lambda e: self._yview('scroll', -3, 'units'))
                w.bind('<Button-5>', lambda e: self._yview('scroll', 3, 'units'))
            self.body.bind('<Up>', lambda e: self._move(-1))
            self.body.bind('<Down>', lambda e: self._move(1))
            self.head.bind('<Motion>', self._head_motion)
            self.head.bind('<Button-1>', self._head_press)
            self.head.bind('<B1-Motion>', self._head_drag)
            self.head.bind('<ButtonRelease-1>', self._head_release)

        # ── 데이터 ──
        def set_columns(self, cols, widths):
            self.cols, self.widths = list(cols), [max(40, int(w)) for w in widths]
            self._layout()

        def set_rows(self, rows):
            """rows = [(값 목록, {컬럼 번호: 'orange'/'red'})]"""
            self.rows, self.sel = rows, None
            self.body.yview_moveto(0)
            self._layout()

        def update_row(self, i, values):
            self.rows[i] = (values, self.rows[i][1])
            self.redraw()

        def selected(self):
            return self.sel

        def column_widths(self):
            return dict(zip(self.cols, self.widths))

        # ── 그리기 ──
        def _xs(self):
            xs, x = [], 0
            for w in self.widths:
                xs.append(x); x += w
            return xs, x

        def _layout(self):
            _, total = self._xs()
            self.body.configure(scrollregion=(0, 0, total, len(self.rows) * self.rowh))
            self.head.configure(scrollregion=(0, 0, total, self.rowh))
            self.redraw()

        def _fit(self, text, width, font):
            text = str(text).replace('\n', ' ')
            key = (text, width, str(font))
            if key in self._fit_cache:
                return self._fit_cache[key]
            avail = width - 2 * self.PAD
            out = text
            if font.measure(text) > avail:
                lo, hi = 0, len(text)
                while lo < hi:  # 말줄임표까지 들어가는 가장 긴 앞부분
                    mid = (lo + hi + 1) // 2
                    if font.measure(text[:mid] + '…') <= avail:
                        lo = mid
                    else:
                        hi = mid - 1
                out = text[:lo] + '…' if lo else ''
            if len(self._fit_cache) > 20000:
                self._fit_cache.clear()
            self._fit_cache[key] = out
            return out

        def redraw(self):
            xs, total = self._xs()
            h = self.head
            h.delete('all')
            for i, c in enumerate(self.cols):
                x, w = xs[i], self.widths[i]
                h.create_rectangle(x, 0, x + w, self.rowh, fill='#E8E8E8', outline='#B0B0B0')
                h.create_text(x + self.PAD, self.rowh / 2, anchor='w', font=self.hfont,
                              text=self._fit(c, w, self.hfont))
            b = self.body
            b.delete('all')
            if not self.rows:
                return
            top = b.canvasy(0)
            first = max(0, int(top // self.rowh))
            last = min(len(self.rows), int((top + b.winfo_height()) // self.rowh) + 2)
            left, right = b.canvasx(0), b.canvasx(b.winfo_width())
            vis = [i for i in range(len(self.cols)) if xs[i] + self.widths[i] >= left and xs[i] <= right]
            for r in range(first, last):
                vals, colors = self.rows[r]
                y = r * self.rowh
                for i in vis:
                    x, w = xs[i], self.widths[i]
                    bg = CELL_BG.get(colors.get(i), SEL_BG if r == self.sel else 'white')
                    b.create_rectangle(x, y, x + w, y + self.rowh, fill=bg, outline='#D9D9D9')
                    v = vals[i] if i < len(vals) else ''
                    if v != '':
                        b.create_text(x + self.PAD, y + self.rowh / 2, anchor='w', font=self.font,
                                      text=self._fit(v, w, self.font))
                if r == self.sel:
                    b.create_rectangle(0, y, total, y + self.rowh, outline='#3875D7', width=2)

        # ── 스크롤 ──
        def _yview(self, *a):
            self.body.yview(*a); self.redraw()

        def _xview(self, *a):
            self.body.xview(*a); self.head.xview(*a); self.redraw()

        def _xset(self, lo, hi):
            self.xs.set(lo, hi)
            self.head.xview_moveto(lo)

        def _wheel(self, e):
            self._yview('scroll', -int(e.delta / 120) * 3 or (-3 if e.delta > 0 else 3), 'units')

        # ── 선택 ──
        def _row_at(self, e):
            r = int(self.body.canvasy(e.y) // self.rowh)
            return r if 0 <= r < len(self.rows) else None

        def _click(self, e):
            self.body.focus_set()
            self.sel = self._row_at(e)
            self.redraw()

        def _double(self, e):
            self._click(e)
            if self.sel is not None and self.on_double:
                self.on_double()

        def _move(self, d):
            if not self.rows:
                return
            self.sel = 0 if self.sel is None else min(len(self.rows) - 1, max(0, self.sel + d))
            top, bot = self.body.canvasy(0), self.body.canvasy(self.body.winfo_height())
            y = self.sel * self.rowh
            n = len(self.rows) * self.rowh
            if y < top:
                self.body.yview_moveto(y / n)
            elif y + self.rowh > bot:
                self.body.yview_moveto((y + self.rowh - self.body.winfo_height()) / n)
            self.redraw()

        # ── 컬럼 너비 조절 ──
        def _edge(self, e):
            x = self.head.canvasx(e.x)
            xs, _ = self._xs()
            for i in range(len(self.cols)):
                if abs(xs[i] + self.widths[i] - x) <= 4:
                    return i
            return None

        def _head_motion(self, e):
            self.head.configure(cursor='sb_h_double_arrow' if self._edge(e) is not None else '')

        def _head_press(self, e):
            i = self._edge(e)
            self._drag = (i, self.head.canvasx(e.x), self.widths[i]) if i is not None else None

        def _head_drag(self, e):
            if self._drag:
                i, x0, w0 = self._drag
                self.widths[i] = max(40, int(w0 + self.head.canvasx(e.x) - x0))
                self._layout()

        def _head_release(self, e):
            if self._drag and self.on_resize:
                self.on_resize()
            self._drag = None

    class App:
        def __init__(self, root):
            self.root = root
            root.title('트랜스폰더 DB 검색')
            root.geometry('1400x700')
            self.recs, self.shown, self.folder = [], {}, ''

            top = ttk.Frame(root, padding=6)
            top.pack(fill='x')
            ttk.Label(top, text='모델명').pack(side='left')
            self.e_model = ttk.Entry(top, width=28)
            self.e_model.pack(side='left', padx=(4, 12))
            ttk.Label(top, text='연식').pack(side='left')
            self.e_year = ttk.Entry(top, width=12)
            self.e_year.pack(side='left', padx=(4, 12))
            ttk.Button(top, text='검색', command=self.do_search).pack(side='left')
            ttk.Button(top, text='초기화', command=self.clear).pack(side='left', padx=4)
            ttk.Button(top, text='수정', command=self.edit).pack(side='left', padx=(16, 4))
            ttk.Button(top, text='다시 불러오기', command=self.reload).pack(side='right')
            ttk.Button(top, text='폴더 변경', command=self.pick_folder).pack(side='right', padx=4)
            for e in (self.e_model, self.e_year):
                e.bind('<Return>', lambda ev: self.do_search())

            # 결과 표: 엑셀에서 주황·빨강으로 칠한 칸만 같은 색으로 표시
            self.table = CellTable(root, on_double=self.edit, on_resize=self.save_cfg)
            self.table.pack(fill='both', expand=True)
            self.cols = []

            self.status = tk.StringVar()
            ttk.Label(root, textvariable=self.status, anchor='w', padding=4).pack(fill='x')

            # 저장된 설정(마지막 폴더·컬럼 너비) 불러오기
            self.cfg = {}
            try:
                with open(CONFIG, encoding='utf-8') as f:
                    self.cfg = json.load(f)
            except Exception:
                pass
            self.cfg.setdefault('widths', {})
            # 컬럼 너비를 바꾸면(마우스 놓을 때)·프로그램을 닫을 때 저장
            root.protocol('WM_DELETE_WINDOW', self.on_close)
            last = self.cfg.get('folder', '')
            if last and os.path.isdir(last):
                self.folder = last
                root.after(100, self.reload)  # 저장된 폴더는 바로 불러옴
            else:
                root.after(100, lambda: self.pick_folder(initial=last, first=True))

        def save_cfg(self):
            try:
                for c, w in self.table.column_widths().items():
                    self.cfg['widths'][c] = int(w)
                self.cfg['folder'] = self.folder
                with open(CONFIG, 'w', encoding='utf-8') as f:
                    json.dump(self.cfg, f, ensure_ascii=False, indent=1)
            except Exception:
                pass

        def on_close(self):
            self.save_cfg()
            self.root.destroy()

        def pick_folder(self, initial='', first=False):
            d = filedialog.askdirectory(title='엑셀 파일이 있는 폴더를 고르세요',
                                        initialdir=initial or self.folder or os.getcwd())
            if not d:
                if first and not self.folder:
                    self.status.set('폴더를 고르지 않았습니다. [폴더 변경]을 누르세요.')
                return
            self.save_cfg()  # 바꾸기 전 폴더의 컬럼 너비 저장
            self.folder = d
            self.reload()
            self.save_cfg()

        def reload(self):
            if not self.folder:
                return
            self.root.config(cursor='watch')
            self.root.update_idletasks()
            try:
                self.recs, files, errors = load_folder(self.folder)
            finally:
                self.root.config(cursor='')
            self.cols = all_columns(self.recs) + [FILE_COL]
            self.table.set_columns(self.cols, [
                self.cfg['widths'].get(c) or (
                    260 if c in (MODEL, '출처', '비고') else 90 if c.startswith('XT') or c == YEAR else 170)
                for c in self.cols])
            msg = '폴더: %s  |  파일 %d개, 행 %d개' % (self.folder, len(files), len(self.recs))
            if errors:
                msg += '  |  읽기 실패: ' + '; '.join(errors)
            self.status.set(msg)
            self.base_status = msg
            self.do_search()

        def clear(self):
            self.e_model.delete(0, 'end')
            self.e_year.delete(0, 'end')
            self.do_search()

        def do_search(self):
            self.shown = []
            if not self.e_model.get().strip() and not self.e_year.get().strip():
                self.table.set_rows([])
                self.status.set('%s  |  모델명 또는 연식을 입력하고 검색하세요' % getattr(self, 'base_status', ''))
                return
            res = search(self.recs, self.e_model.get(), self.e_year.get())
            rows = []
            for r in res:
                colors = {i: r['flags'][c] for i, c in enumerate(self.cols) if c in r.get('flags', {})}
                rows.append((self.row_values(r), colors))
            self.shown = res
            self.table.set_rows(rows)
            self.status.set('%s  |  검색 결과 %d행' % (getattr(self, 'base_status', ''), len(res)))

        def row_values(self, r):
            return [r['values'].get(c, '') for c in self.cols[:-1]] + [os.path.basename(r['file'])]

        def edit(self):
            iid = self.table.selected()
            if iid is None:
                messagebox.showinfo('수정', '수정할 행을 먼저 고르세요.')
                return
            rec = self.shown[iid]
            win = tk.Toplevel(self.root)
            win.title('수정 - %s / %s' % (os.path.basename(rec['file']), rec['sheet']))
            win.transient(self.root)
            win.grab_set()
            ttk.Label(win, text='%s  [%s]  %d행' % (os.path.basename(rec['file']), rec['sheet'], rec['row']),
                      padding=6).grid(row=0, column=0, columnspan=2, sticky='w')
            entries = {}
            for i, h in enumerate(rec['cols'], start=1):
                ttk.Label(win, text=h).grid(row=i, column=0, sticky='e', padx=6, pady=2)
                e = ttk.Entry(win, width=90)
                e.insert(0, rec['values'].get(h, ''))
                e.grid(row=i, column=1, sticky='we', padx=6, pady=2)
                entries[h] = e
            win.columnconfigure(1, weight=1)

            def save():
                changes = {h: e.get() for h, e in entries.items() if e.get() != rec['values'].get(h, '')}
                if not changes:
                    win.destroy()
                    return
                try:
                    save_changes(rec, changes)
                except Exception as ex:
                    messagebox.showerror('저장 실패', str(ex), parent=win)
                    return
                self.table.update_row(iid, self.row_values(rec))
                win.destroy()
                self.status.set('%s  |  저장됨: %s %d행 (%s)' % (
                    self.base_status, os.path.basename(rec['file']), rec['row'], ', '.join(changes)))

            bf = ttk.Frame(win, padding=6)
            bf.grid(row=len(rec['cols']) + 1, column=0, columnspan=2, sticky='e')
            ttk.Button(bf, text='저장', command=save).pack(side='left', padx=4)
            ttk.Button(bf, text='취소', command=win.destroy).pack(side='left')
            win.bind('<Return>', lambda ev: save())
            win.bind('<Escape>', lambda ev: win.destroy())

    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    run_gui()

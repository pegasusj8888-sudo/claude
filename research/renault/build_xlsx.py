# research/renault/rows.jsonl → 르노_models.xlsx (기아 트랜스폰더 DB와 동일 14컬럼)
import json, openpyxl, os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows=[json.loads(l) for l in open(os.path.join(ROOT,'research','renault','rows.jsonl'))]
order=[l.strip() for l in open(os.path.join(ROOT,'research','renault','model_order.txt'))]
import sys; sys.path.insert(0,os.path.join(ROOT,'research')); from finalize import process
rows=process('renault',rows)
rows.sort(key=lambda r:(order.index(r['model']),int(r['year'][:4])))

def xt(chip):
    if chip.startswith(('확인','해당')) or not chip: return ('','','')
    new=any(k in chip for k in ('ID4A','ID47','ID49','ID8A','AES'))
    old=any(k in chip for k in ('ID46','ID44','ID60','ID70','DST80','4D70','4D60x80'))
    if 'ID48' in chip:
        return ('△','△','O') if old else ('△','△','△')
    if old and new: return ('△','△','O')
    if old: return ('O','O','O')
    if new: return ('X','△','O')
    return ('','','')

HDR=['모델명','연식','XT27A/A66 호환','XT27B 호환','XT57B 호환','칩코드 (예: ID46(PCF7936))','키종류','키블레이드(부품번호)','키블레이드(키웨이)','카드키(부품번호)','스마트키(부품번호)','폴딩키(부품번호)','이모빌라이저 시스템','출처','비고']
wb=openpyxl.Workbook(); ws=wb.active; ws.title='르노 트랜스폰더 DB'
thin=Side(style='thin',color='FFBFBFBF'); bd=Border(left=thin,right=thin,top=thin,bottom=thin)
ws.append(HDR)
for c in ws[1]:
    c.font=Font(name='Arial',size=11,bold=True,color='FFFFFFFF'); c.fill=PatternFill('solid',fgColor='FF7A1F1F')
    c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=False); c.border=bd
F=lambda c:PatternFill('solid',fgColor=c)
XT={'O':(F('FFC6EFCE'),'FF006100'),'△':(F('FFFFEB9C'),'FF9C6500'),'X':(F('FFFFC7CE'),'FF9C0006')}
FLAG={'orange':(F('FFFFD599'),'FF000000'),'red':(F('FFFFC7CE'),'FF9C0006'),'gen':(F('FFDDEBF7'),'FF000000')}
for r in rows:
    a,b,c=xt(r['chip'])
    ws.append([r['model'],r['year'],a,b,c,r['chip'],r['ktype'],r['blade_pn'],r['keyway'],r['card'],r['smart'],r['fold'],r['immo'],r['src'],r['note']])
    i=ws.max_row
    for cell in ws[i]:
        cell.font=Font(name='Arial',size=10); cell.border=bd; cell.alignment=Alignment(vertical='center',wrap_text=False)
    for col in (3,4,5):
        cell=ws.cell(i,col); cell.alignment=Alignment(horizontal='center',vertical='center')
        if cell.value in XT: cell.fill,fc=XT[cell.value]; cell.font=Font(name='Arial',size=10,bold=True,color=fc)
    fl=r.get('flag')
    if fl:
        fill,fc=FLAG[fl]
        cols=(6,13,15) if fl in ('orange','red') else range(6,16)
        for col in cols:
            ws.cell(i,col).fill=fill; ws.cell(i,col).font=Font(name='Arial',size=10,color=fc)
for col,w in zip('ABCDEFGHIJKLMNO',[30,14,12,11,11,26,16,26,22,12,36,12,22,48,48]): ws.column_dimensions[col].width=w
ws.freeze_panes='B2'; ws.auto_filter.ref=f'A1:O{ws.max_row}'

g=wb.create_sheet('안내')
notes=['이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.','',
'※ 구성',
"- '키종류'는 그 연식에 나온 키 형태(막대키·폴딩키·스마트키·카드키)를 모두 적었습니다. 트림별로 다른 경우 함께 적었습니다(예: 폴딩키,스마트키).",
"- 키 부품번호는 국내 사양(433/434MHz)만 적었습니다. 미국(315MHz)·유럽(868MHz) 사양 키는 뺐습니다.",
"- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
"- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 동일합니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다(SM5 1세대 1998년 출시분도 2000년식부터).",
"- 원본 목록의 연식 범위가 실제 국내 판매와 다른 모델은 실제 기준으로 적었습니다(SM3 2세대 2009~, SM6·QM6 2025 단종, 클리오는 4세대 2018~2019, 조에 2022 수입 중단, 마스터 밴 2018~).",
"- '이모빌라이저 시스템': 르노 계열은 UCH(메간3/플루언스/래티튜드 세대) → BCM(클리오4·캡처 이후 Hitag AES 세대), 닛산 기반 구형 삼성 차종은 NATS(르노삼성 12자리 코드)로 적었습니다.",
"- 카드형 스마트키(르노 카드)는 '카드키(부품번호)' 칸에 적었습니다. 부품번호는 동일 플랫폼 르노 차종의 순정 번호(285975779R, 285977147R 등)이며 국내 순정 품번은 대부분 확인되지 않았습니다 — 르노코리아 부품은 VIN(KNMA…)별로 상이.",
"- '키블레이드(부품번호)'는 해당 연식 검색에서 직접 나온 경우에만 적었고 나머지는 공란입니다(기아 파일 규칙). 키웨이는 카드 비상키 블레이드 기준(VA2/NSN14 등)입니다.",
"- 'XT27A/A66·XT27B·XT57B 호환'은 기아 파일 표기 규칙을 따랐습니다: ID46·ID60(4D60) → O/O/O, ID4A(Hitag AES)·ID47·ID49·ID8A → X/△/O, 구형(ID46)·신형(AES) 칩이 병기된 행 → △/△/O(기아 파일 혼재 행 규칙). 실제 적용 전 장비로 재확인하세요.",
"- 출처 칸은 해당 연식 검색에서 근거로 쓴 페이지입니다. 이 환경에서는 원문 페이지를 직접 열 수 없어 검색 결과 요약을 근거로 했습니다.",
'',
'※ 색상',
"- 주황색: 국내 차종 자료가 없어 닛산/르노 동일 플랫폼 기준으로 추정했거나, 자료 연식 범위 밖이거나, 출처가 상충하는 경우 — 실물 키/VIN으로 재확인.",
'',
'※ 조사하며 확인된 주요 사항',
"- [재조사] SM3 CF는 르노삼성이 생산한 닛산 알메라 클래식(러시아)·써니(중동)와 같은 차라 ID46 PCF7936·NSN14로 확인했습니다. SM3 1세대는 같은 차체라 동일 가능성이 높으나 직접 자료는 없습니다.",
"- SM5 1·2세대, SM7 1세대는 한국어·러시아·중남미·중동 자료를 다시 찾았지만 칩을 밝힌 자료가 없어 닛산 기준 추정(주황)으로 남겼습니다.",
"- [재조사] SM5 3세대·SM7 2세대는 래티튜드용 ID46 카드와 삼성 전용 AES(PCF7945M, 434MHz) 카드가 함께 판매되어 두 칩을 병기했습니다(주황). 285975779R 카드도 후기 순정품에 PCF7953M(4A) 사양이 있습니다.",
"- [재조사] 마스터3는 ID46 PCF7947, 블레이드 VA6 리모컨키입니다(이전 초안의 ID4A 추정은 오류). 그랑 콜레오스는 지리 몬자로 순정 키(Hitag AES 4A / DST AES 8A) 기준입니다.",
"- SM5 2세대·SM7 1세대 카드형 스마트키: 0156 타입(2005~2007)과 T002 타입(2008~, 뉴아트·임프레션)은 서로 호환되지 않습니다. FCC TFWB1J637(312.4MHz).",
"- SM3 2세대(플루언스), SM5 3세대·SM7 2세대(래티튜드): ID46 PCF7952 카드 285975779R, VA2, UCH. 2011년경부터 UCH 소프트웨어 변경으로 OBD 등록 제한 자료 있음.",
"- QM5(콜레오스 H45): ID46 PCF7952 카드 285979045R(핸즈프리)/285970036R(비핸즈프리), 비상키 NSN14 또는 VA2 두 종류. QM5용 AES(PCF7953) 카드도 존재(적용 연식 미확인).",
"- QM3·클리오4: 285971998R(핸즈프리 PCF7953M 4A) / 285974100R(비핸즈프리). SM6·QM6: 285977147R(PCF7953M/NCF29A1M 4A). 캡처2·조에·XM3·아르카나: 285979827R/285973979R(NCF29A1M 4A).",
"- 그랑 콜레오스는 지리 싱웨L(몬자로) 기반으로, 키 칩 자료가 없어 지리 자료 기준 추정입니다."]
for n in notes: g.append([n])
g.column_dimensions['A'].width=150
for c in g['A']: c.font=Font(name='Arial',size=10); c.alignment=Alignment(wrap_text=False,vertical='top')
wb.save(os.path.join(ROOT,'르노_models.xlsx'))
print(len(rows),'rows written')

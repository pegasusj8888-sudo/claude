# research/bmw_rows.jsonl → BMW_코리아_출시모델.xlsx (기아 트랜스폰더 DB와 동일 14컬럼)
import json, openpyxl, os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows=[json.loads(l) for l in open(os.path.join(ROOT,'research','bmw_rows.jsonl'))]
order=[l.strip() for l in open(os.path.join(ROOT,'research','model_order.txt'))]
rows.sort(key=lambda r:(order.index(r['model']),int(r['year'][:4])))

def xt(chip):
    if chip.startswith('확인'): return ('','','')
    if 'ID49' in chip: return ('X','△','O')
    if 'ID46' in chip or 'ID44' in chip: return ('O','O','O')
    return ('','','')

HDR=['모델명','연식','XT27A/A66 호환','XT27B 호환','XT57B 호환','칩코드 (예: ID46(PCF7936))','키블레이드(부품번호)','키블레이드(키웨이)','카드키(부품번호)','스마트키(부품번호)','폴딩키(부품번호)','이모빌라이저 시스템','출처','비고']
wb=openpyxl.Workbook(); ws=wb.active; ws.title='BMW 트랜스폰더 DB'
thin=Side(style='thin',color='FFBFBFBF'); bd=Border(left=thin,right=thin,top=thin,bottom=thin)
ws.append(HDR)
for c in ws[1]:
    c.font=Font(name='Arial',size=11,bold=True,color='FFFFFFFF'); c.fill=PatternFill('solid',fgColor='FF7A1F1F')
    c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True); c.border=bd
F=lambda c:PatternFill('solid',fgColor=c)
XT={'O':(F('FFC6EFCE'),'FF006100'),'△':(F('FFFFEB9C'),'FF9C6500'),'X':(F('FFFFC7CE'),'FF9C0006')}
FLAG={'orange':(F('FFFFD599'),'FF000000'),'red':(F('FFFFC7CE'),'FF9C0006'),'gen':(F('FFDDEBF7'),'FF000000')}
for r in rows:
    a,b,c=xt(r['chip'])
    ws.append([r['model'],r['year'],a,b,c,r['chip'],r['blade_pn'],r['keyway'],r['card'],r['smart'],r['fold'],r['immo'],r['src'],r['note']])
    i=ws.max_row
    for cell in ws[i]:
        cell.font=Font(name='Arial',size=10); cell.border=bd; cell.alignment=Alignment(vertical='center',wrap_text=True)
    for col in (3,4,5):
        cell=ws.cell(i,col); cell.alignment=Alignment(horizontal='center',vertical='center')
        if cell.value in XT: cell.fill,fc=XT[cell.value]; cell.font=Font(name='Arial',size=10,bold=True,color=fc)
    fl=r.get('flag')
    if fl:
        fill,fc=FLAG[fl]
        cols=(6,12,14) if fl in ('orange','red') else range(6,15)
        for col in cols:
            ws.cell(i,col).fill=fill; ws.cell(i,col).font=Font(name='Arial',size=10,color=fc)
for col,w in zip('ABCDEFGHIJKLMN',[30,14,12,11,11,26,26,22,12,36,12,22,48,48]): ws.column_dimensions[col].width=w
ws.row_dimensions[1].height=30; ws.freeze_panes='B2'; ws.auto_filter.ref=f'A1:N{ws.max_row}'

g=wb.create_sheet('안내')
notes=['이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.','',
'※ 구성',
"- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 동일합니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다(1990년대 출시 모델도 2000년식부터).",
"- 연식이 '현재'인 모델은 2026년식까지, 단종 모델의 마지막 연식은 '2012(단종)' 형식으로 표기했습니다.",
"- '이모빌라이저 시스템'은 차량 쪽 모듈(EWS3/EWS4, CAS1~CAS4+, FEM, BDC/BDC2/BDC3, BCP)을 적었습니다.",
"- '스마트키(부품번호)'에는 BMW 순정 부품번호(66 12 …, 9xxxxxx-xx 등)와 FCC ID(KR55WK…, YGOHUF…, N5F-ID21A, IYZBK1 등)를 함께 적었습니다. CAS1~CAS3의 삽입식 리모컨키도 이 칸에 적고 괄호로 구분했습니다.",
"- '키블레이드(부품번호)'는 비상키 블레이드 부품번호(순정/애프터마켓)를 적었습니다. 카드키·폴딩키는 BMW에 해당 형태가 없어 비워 두었습니다(E65 CAS1 슬롯형 키는 스마트키 칸에 기재).",
"- 'XT27A/A66·XT27B·XT57B 호환'은 칩 종류 기준으로 기아 파일의 표기 규칙을 그대로 따랐습니다: ID46·ID44 → O/O/O, ID49(Hitag Pro) → X/△/O. (근거: Xhorse 슈퍼칩 비교 — XT27A는 ID49 미지원, XT27B·XT57B는 ID49 지원 표기) 실제 차량 적용 전 장비로 재확인하세요.",
"- 출처 칸의 사이트명은 해당 연식 검색에서 근거로 쓴 페이지입니다. 이 환경에서는 부품몰 원문을 직접 열 수 없어 검색 결과 요약을 근거로 했습니다.",
'',
'※ 색상',
"- 빨간색: 확인 불가/확인 필요 — 절대 그대로 신뢰해서 작업하지 마세요.",
"- 주황색: 출처가 서로 상충하거나 원문으로 직접 확인되지 않은 경우 — 작업 전 VIN/실물 모듈로 재확인.",
"- 전환기(CAS3→CAS3+, CAS4→CAS4+, FEM→BDC, BDC2→BDC3)는 색 표시 없이 이모빌라이저 칸에 전환 전·후를 함께 적었습니다(예: CAS3(2008 중반 이전 생산) / CAS3+(2008 중반 이후 생산)).",
"- 하늘색: 연식별 개별 검색을 끝내지 못한 행(웹 검색 한도 200회 도달). 앞서 받은 세대 단위 검색결과로 임시 기입했으며, 다음 작업에서 연식별로 재검색해야 합니다.",
"   대상: X3(F25 2013~, G01, G45), X3 M, X4 전 세대, X4 M, X5 전 세대, X5 M, X6 전 세대, X6 M, X7, XM, Z4 전 세대, i3, i8, i4, iX, iX3, 1M 쿠페",
'',
'※ 조사하며 확인된 주요 사항',
"- CAS4/CAS4+ 키의 칩은 PCF7953(Hitag Pro, ID49, EWS5)입니다(이전 초안의 'Hitag2' 표기는 오류였음).",
"- CAS4+ 도입 시점은 자료마다 다릅니다(2012 중반 이후 생산분 vs 2013년 F10부터) — 2012년식은 주황색.",
"- BDC3는 G30/G31 기준 2020.7 이후 생산분부터(Autel 자료). BDC2 키: N5F-ID21A(9367401-01), 2022년 이후 순정 키: IYZBK1.",
"- U섀시(U06/U10/U11)는 BCP 이모빌라이저 + UWB 키(NCF2951/Hitag Pro/ID49, FCC IYZBK1).",
"- F40·F44는 G시리즈 전장이라 BDC2/BDC3 표기가 자료마다 다릅니다(주황색)."]
for n in notes: g.append([n])
g.column_dimensions['A'].width=150
for c in g['A']: c.font=Font(name='Arial',size=10); c.alignment=Alignment(wrap_text=True,vertical='top')
wb.save(os.path.join(ROOT,'BMW_코리아_출시모델.xlsx'))
print(len(rows),'rows written')

# research/bmw_rows.jsonl → BMW_코리아_출시모델.xlsx (기아 트랜스폰더 DB와 동일 14컬럼)
import json, openpyxl, os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows=[json.loads(l) for l in open(os.path.join(ROOT,'research','bmw_rows.jsonl'))]
order=[l.strip() for l in open(os.path.join(ROOT,'research','model_order.txt'))]
import sys; sys.path.insert(0,os.path.join(ROOT,'research')); from finalize import process
rows=process('bmw',rows)
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
wb=openpyxl.Workbook(); ws=wb.active; ws.title='BMW 트랜스폰더 DB'
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
"- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 동일합니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다(1990년대 출시 모델도 2000년식부터).",
"- 연식이 '현재'인 모델은 2026년식까지, 단종 모델의 마지막 연식은 '2012(단종)' 형식으로 표기했습니다.",
"- '이모빌라이저 시스템'은 차량 쪽 모듈(EWS3/EWS4, CAS1~CAS4+, FEM, BDC/BDC2/BDC3, BCP)을 적었습니다.",
"- '스마트키(부품번호)'에는 BMW 순정 부품번호(66 12 …, 9xxxxxx-xx 등)와 FCC ID(KR55WK…, YGOHUF…, N5F-ID21A, IYZBK1 등)를 함께 적었습니다. CAS1~CAS3의 삽입식 리모컨키도 이 칸에 적고 괄호로 구분했습니다.",
"- '키블레이드(부품번호)'는 해당 연식 검색 결과에 직접 나온 경우에만 적었고, 나오지 않은 칸은 공란입니다(기아 파일 규칙과 동일). 카드키·폴딩키는 BMW에 해당 형태가 없어 비워 두었습니다(E65 CAS1 슬롯형 키는 스마트키 칸에 기재).",
"- '키블레이드(키웨이)'에 '(세대 기준)'이 붙은 칸은 그 연식 검색에서 키웨이가 직접 확인되지 않아 같은 세대 기준으로 적은 값입니다. '(추정)'은 신형 차종에서 근거가 약한 값입니다.",
"- 'XT27A/A66·XT27B·XT57B 호환'은 칩 종류 기준으로 기아 파일의 표기 규칙을 그대로 따랐습니다: ID46·ID44 → O/O/O, ID49(Hitag Pro) → X/△/O, ID46·ID49 병기 → △/△/O. (근거: Xhorse 슈퍼칩 비교 — XT27A는 ID49 미지원, XT27B·XT57B는 ID49 지원 표기) 실제 차량 적용 전 장비로 재확인하세요.",
"- 출처 칸의 사이트명은 해당 연식 검색에서 근거로 쓴 페이지입니다. 이 환경에서는 부품몰 원문을 직접 열 수 없어 검색 결과 요약을 근거로 했습니다.",
'',
'※ 색상',
"- 빨간색: 확인 불가/확인 필요 — 절대 그대로 신뢰해서 작업하지 마세요.",
"- 주황색: 출처가 서로 상충하거나 원문으로 직접 확인되지 않은 경우 — 작업 전 VIN/실물 모듈로 재확인.",
"- 전환기(EWS3→EWS4, CAS1→CAS2, CAS2→CAS3, CAS3→CAS3+, CAS4→CAS4+, BDC2→BDC3)는 색 표시 없이 이모빌라이저 칸에 전환 전·후를 함께 적었습니다(예: CAS3(2008 중반 이전 생산) / CAS3+(2008 중반 이후 생산)).",
'',
'※ 조사하며 확인된 주요 사항',
"- CAS4/CAS4+ 키의 칩은 PCF7953(Hitag Pro, ID49, EWS5)입니다(이전 초안의 'Hitag2' 표기는 오류였음).",
"- CAS4+ 도입 시점은 자료마다 다릅니다(2012 중반 이후 생산분 vs 2013년 F10부터) — 2012년식은 주황색.",
"- [이모빌라이저 재검증] F20/F22/F30/F32/F80/F82/F87은 LCI 이후에도 FEM(딜러 부품 FEM 61355A7FB57 등) — BDC가 아닙니다. F15/F16/F85/F86/F45/F48/F39/i3/i8은 BDC.",
"- BDC2(BDC_G11): G11/G12(~2019.2), G30/G31/G32/F90(~2020.6), G01/G02/F97/F98(~2021.7), G08(~2021.8). 이후 생산분은 BDC3.",
"- BDC3(BDC_G05): G05/G06/G07/G20/G15/G29/F40/F44/G42/G22/G80/G82/G87/F95/F96은 출시부터 BDC3.",
"- BCP: i7/7시리즈 G70·iX(딜러 부품 'Control u.basic computing platform (BCP)' 61355A9A210), U06/U10/U11, G45. G60/i5/G90은 BDC3·BCP 자료 상충(주황색).",
"- BDC2 키: N5F-ID21A(9367401-01), 2022년 이후 순정 키: IYZBK1.",
"- U섀시(U06/U10/U11)는 BCP 이모빌라이저 + UWB 키(NCF2951/Hitag Pro/ID49, FCC IYZBK1).",
"- E65는 2005 LCI 전 CAS1, 이후 CAS2. E60/E61/E63은 2007.3 LCI 전 CAS2, 이후 CAS3. E83은 2006 중 EWS3→EWS4."]
for n in notes: g.append([n])
g.column_dimensions['A'].width=150
for c in g['A']: c.font=Font(name='Arial',size=10); c.alignment=Alignment(wrap_text=False,vertical='top')
wb.save(os.path.join(ROOT,'BMW_코리아_출시모델.xlsx'))
print(len(rows),'rows written')

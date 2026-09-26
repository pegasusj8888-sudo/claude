# research/chevy/rows.jsonl → 쉐보레_models.xlsx (기아 트랜스폰더 DB와 동일 14컬럼)
import json, openpyxl, os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows=[json.loads(l) for l in open(os.path.join(ROOT,'research','chevy','rows.jsonl'))]
order=[l.strip() for l in open(os.path.join(ROOT,'research','chevy','model_order.txt'))]
import sys; sys.path.insert(0,os.path.join(ROOT,'research')); from finalize import process
rows=process('chevy',rows)
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
wb=openpyxl.Workbook(); ws=wb.active; ws.title='쉐보레(GM대우) 트랜스폰더 DB'
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
    ws.append([r['model'],r['year'],a,b,c,r['chip'],r['ktype'],r['blade_pn'],r['keyway'],r['card'],r['smart'],r['fold'],r['immo'],r['src'],r['note']])
    i=ws.max_row
    for cell in ws[i]:
        cell.font=Font(name='Arial',size=10); cell.border=bd; cell.alignment=Alignment(vertical='center',wrap_text=True)
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
ws.row_dimensions[1].height=30; ws.freeze_panes='B2'; ws.auto_filter.ref=f'A1:O{ws.max_row}'

g=wb.create_sheet('안내')
notes=['이 표는 락스미스(자동차 키 제작/프로그래밍) 참고용입니다.','',
'※ 구성',
"- '키종류'는 그 연식에 나온 키 형태(막대키·폴딩키·스마트키·카드키)를 모두 적었습니다. 트림별로 다른 경우 함께 적었습니다(예: 폴딩키,스마트키).",
"- 키 부품번호는 국내 사양(433/434MHz)만 적었습니다. 미국(315MHz)·유럽(868MHz) 사양 키는 뺐습니다.",
"- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
"- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 동일합니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다.",
"- 원본 목록 연식이 실제 국내 판매와 다른 모델은 실제 기준으로 적었습니다(마티즈Ⅱ 2000.8~, 매그너스 1999.12~2006.1, 레조 2000.1~2007.6, 크루즈 J300 ~2017.11, 올 뉴 크루즈 2017.1~, 볼트(Volt) 2세대 2016.8~2019.3, 임팔라 ~2020, G2X ~2008.9, 트랙스 ~2022.11, 이쿼녹스 ~2024.4, 트래버스·타호 ~2025.3, 콜로라도 3세대 2024.7~).",
"- 캡티바 2세대(리뱃지)·이쿼녹스 EV는 국내에 출시되지 않아 '국내 미출시' 한 행만 남겼습니다(빨간색). 삭제할지 알려주세요.",
"- 콜벳 C7·C8, 서버번은 한국GM 공식 판매 자료가 없고 수입업체 판매만 확인되어 주황색으로 표시했습니다.",
"- 'XT27A/A66·XT27B·XT57B 호환'은 기아 파일 규칙을 따랐습니다: ID46·ID60(4D60) → O/O/O, ID49(Hitag Pro) → X/△/O, ID48(Megamos Crypto) → △/△/△, ID46·ID49 병기 → △/△/O. 실제 적용 전 장비로 재확인하세요.",
"- 출처 칸은 해당 연식 검색에서 근거로 쓴 페이지입니다. 원문 페이지는 이 환경에서 열 수 없어 검색 결과 요약을 근거로 했습니다.",
'',
'※ 색상',
"- 빨간색: 확인 불가 또는 국내 미출시 — 마티즈Ⅱ(국내형 이모빌라이저 적용 자료 없음), 캡티바 2세대·이쿼녹스 EV(국내 미출시).",
"- 주황색: 추정이거나 자료가 서로 다르거나, 수출형 자료로 대신 채운 값 — 실물 키/VIN으로 재확인.",
'',
'※ 조사하며 확인된 주요 사항',
"- GM대우 국내형은 이모빌라이저가 없거나 트림/연식별로 달랐습니다: 올 뉴 마티즈 국내형 미적용, 마티즈 크리에이티브/스파크 M300은 2013년형까지 미적용·2014년형부터 이모빌라이저 폴딩키, 토스카는 2007년형(2006.11)부터 이모빌라이저 적용.",
"- 칼로스·젠트라·레조·매그너스·라세티 J200은 국내형 적용 자료를 찾지 못해 같은 차의 수출형 자료로 채웠습니다: 칼로스/아베오 T250/타쿠마 ID48(DWO4R, TMPro 모듈113 대우 이모박스), 에반다(매그너스) ID48(DWO5), 라세티/옵트라 2004-2013 4D60(DWO4R).",
"- 2011년 이후 쉐보레(아베오·크루즈·올란도·트랙스·말리부): 폴딩키 ID46 Hitag2(PCF7937/PCF7941E) HU100 433MHz, 이모빌라이저는 BCM 통합. 스마트키는 PCF7952 계열 ID46.",
"- 2016년 이후 스마트키 HYQ4EA(433MHz, ID46): 말리부 9세대·카마로 6세대·올 뉴 크루즈·이쿼녹스·트래버스. HYQ4ES(ID46): 트레일블레이저·트랙스 크로스오버.",
"- 2021년 이후 대형 SUV/픽업(타호·서버번·콜로라도 3세대)·콜벳 C8: Hitag Pro ID49(YG0G21TB2 / YG0G20TB1).",
"- 콜로라도 2세대(2019~2024.4)는 버튼시동 없이 키 시동(트랜스폰더 키 23209427, B119/HU100, ID46), 3세대(2024.7~)부터 스마트키.",
"- 트레일블레이저·트랙스 크로스오버는 LS 트림이 키 시동, LT 이상이 스마트키입니다."]
for n in notes: g.append([n])
g.column_dimensions['A'].width=150
for c in g['A']: c.font=Font(name='Arial',size=10); c.alignment=Alignment(wrap_text=True,vertical='top')
wb.save(os.path.join(ROOT,'쉐보레_models.xlsx'))
print(len(rows),'rows written')

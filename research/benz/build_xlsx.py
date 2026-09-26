# research/kgm/rows.jsonl → 벤츠_models.xlsx (기아 트랜스폰더 DB와 동일 14컬럼)
import json, openpyxl, os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows=[json.loads(l) for l in open(os.path.join(ROOT,'research','benz','rows.jsonl'))]
order=[l.strip() for l in open(os.path.join(ROOT,'research','benz','model_order.txt'))]
import sys; sys.path.insert(0,os.path.join(ROOT,'research')); from finalize import process
rows=process('benz',rows)
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
wb=openpyxl.Workbook(); ws=wb.active; ws.title='벤츠 트랜스폰더 DB'
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
"- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 같고, 칩코드 뒤에 '키종류'를 추가했습니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다(G클래스 구형은 2000년식부터).",
"- '키종류'는 그 연식에 나온 키 형태(막대키·폴딩키·스마트키·카드키)를 모두 적었습니다. 벤츠는 EIS(EZS)에 꽂는 크롬키·키리스고 키 모두 '스마트키'로 적었고, 폴딩키·카드키는 없습니다.",
"- 키 부품번호는 국내 사양(433MHz)만 적었습니다. 미국(315MHz) 사양 키(FCC IYZ3312·NBGDM3 등)는 뺐습니다.",
"- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
"- 연식이 '현재'인 모델은 2026년식까지, 단종 모델의 마지막 연식은 '2019(단종)' 형식입니다. 원본 목록 연식을 그대로 따랐습니다.",
"- 벤츠 키는 ID46 같은 일반 트랜스폰더가 아니라 NEC 프로세서 키(FBS3/FBS4)라서 'XT27A/A66·XT27B·XT57B 호환' 칸은 비어 있습니다(기아 파일 규칙상 해당 칩 없음). ",
"- 이모빌라이저는 EIS(EZS, 전자식 점화 스위치 모듈)이며 칸에 FBS3/FBS4 세대를 함께 적었습니다.",
"- 키블레이드(키웨이)는 비상키 블레이드 HU64입니다(1997~2014 인서트 및 2019+ FBS4 비상키 모두 HU64 표기). 키블레이드 부품번호는 찾지 못해 비웠습니다.",
"- 출처 칸은 검색에서 근거로 쓴 페이지입니다. 원문은 이 환경에서 열 수 없어 검색 결과 요약을 근거로 했습니다.",
'',
'※ 색상',
"- 주황색: 추정이거나 자료가 서로 다른 값, 또는 해당 연식 검색 자료가 없어 이전 연식 기준으로 채운 값 — 실물 키/VIN(SA코드 803/804 = FBS4)으로 재확인.",
"- 전환 연식(FBS3→FBS4)은 색 없이 칩코드·이모빌라이저 칸에 전환 전·후를 함께 적었습니다(예: FBS3(2013.4 이전 생산) / FBS4(2013.4 이후 생산)).",
'',
'※ 조사하며 확인된 주요 사항',
"- 모델마다 연식별로 검색했고 연식별 검색 기록은 research/benz/yearly.md에 있습니다. 같은 세대 안에서도 FBS3→FBS4 전환, 페이스리프트 후 신형 키 디자인, 키리스고 옵션 여부가 달라집니다.",
"- 신형 키 디자인: E클래스 W213 2017~, S클래스 2018 페이스리프트~, G클래스 2019~, A·C·CLA·CLS·GLB·GLC·GLS 2020~(Gen3), GLE W167 2019~(티어드롭), 2021~ W223·W206·W214·X254·EQS/EQE는 MS5 계열 신형 키. 구형 키와 호환 안 됨.",
"- 확인된 국내 사양(433/434MHz) 순정 품번: W205 A2059053609(3버튼)·A2059050000/A2059050600(2버튼), W222·C217·X222 A2229059610, W177 A1779057902, EQA·EQB A1779054606, FBS4 공용 보드 IYZDC12B.",
"- FBS4 적용 시점: W212 2013.4~, 166(ML·GL)·207(E쿠페/카브리올레)·V212 2013.7~, 218(CLS) 2014.9~, 117(CLA)·156(GLA) 2014.11~, 172(SLK) 2015.4~, 205·217·222·231은 처음부터 FBS4. A클래스 W176은 2014년부터 FBS4.",
"- FBS3 키는 로컬 장비(NEC/BGA 등)로 키 제작이 가능하지만, FBS4는 독일 벤츠 서버 인증이 필요해 사실상 딜러(또는 XENTRY 계정 보유 업체) 작업입니다.",
"- 2021년 이후 신형(W206·W223·W214·X254·EQS/EQE 등)도 FBS4 딜러 전용으로 분류됩니다. 비상키는 Gen4 인서트(HU64).",
"- FBS3/FBS4 키 구분: 키 기판 번호 문자열에 'K'가 앞에 있으면 FBS3 풀 스마트키, 중간에 있으면 FBS4 풀 스마트키. FBS4 기판에는 오른쪽에 트랜지스터가 있고 칩이 더 작습니다.",
"- 순정 FBS4 스마트키(433MHz, 3버튼) IYZDC12B는 2014-2023년식 적용 표기, W222 S클래스 FBS4 키리스고 키 A2229059610(433MHz).",
"- G클래스(W463) 구형: 2000~2001년식 키 자료 상충, 2002~2005년식 IR 스마트키·트랜스폰더 막대키 병존, 2006년식 검정 키, 2007년형부터 크롬 키, 2016년식 FBS3/FBS4 자료 상충."]
for n in notes: g.append([n])
g.column_dimensions['A'].width=150
for c in g['A']: c.font=Font(name='Arial',size=10); c.alignment=Alignment(wrap_text=False,vertical='top')
wb.save(os.path.join(ROOT,'벤츠_models.xlsx'))
sys.path.insert(0,os.path.join(ROOT,'research')); from add_brand import add_brand; add_brand(os.path.join(ROOT,'벤츠_models.xlsx'))  # 맨 앞 '브랜드' 컬럼
print(len(rows),'rows written')

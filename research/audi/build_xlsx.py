# research/kgm/rows.jsonl → 아우디_models.xlsx (기아 트랜스폰더 DB와 동일 14컬럼)
import json, openpyxl, os
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows=[json.loads(l) for l in open(os.path.join(ROOT,'research','audi','rows.jsonl'))]
order=[l.strip() for l in open(os.path.join(ROOT,'research','audi','model_order.txt'))]
import sys; sys.path.insert(0,os.path.join(ROOT,'research')); from finalize import process
rows=process('audi',rows)
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
wb=openpyxl.Workbook(); ws=wb.active; ws.title='아우디 트랜스폰더 DB'
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
"- 컬럼은 '기아_트랜스폰더_칩코드_DBnew.xlsx'와 같고, 칩코드 뒤에 '키종류'를 추가했습니다. 모델마다 연식별로 한 행씩, 2000년식부터 기록했습니다.",
"- 연식은 실제 국내 판매 기준입니다. 원본 목록 연식과 국내 출시 시점이 다른 모델은 국내 기준으로 바꿨습니다(아래 목록). 단종 모델의 마지막 연식은 '2016(단종)' 형식입니다.",
"- '키종류'는 그 연식에 나온 키 형태(막대키·폴딩키·스마트키·카드키)를 모두 적었습니다. 카드키는 PPE/PPC 차량의 NFC 키카드(Audi connect Key Card)입니다.",
"- 키 부품번호는 국내 사양(433/434MHz)만 적었습니다. 미국형(315MHz, FCC IYZFBSB802·IYZ-AK01/AK2·NBG009272T 등 미국 딜러 품번)과 유럽 868MHz 사양은 뺐습니다.",
"- '비고'에는 주황색·빨간색 칸의 이유만 적었습니다.",
"- 칩코드는 세대별 방식입니다: ID48 Megamos(구형 폴딩키) / ID8E(A6 C6·Q7 4L) / ID46 Hitag2(A8 D3) / BCM2 PCF7945AC(2008~2018 B8·C7·D4·8R) / MQB Megamos AES(MQB48) / MQB-Evo Hitag Pro(MQB49, 8Y) / MLB·MLB evo 전용 키 / PPE·PPC·MEB 신형 키.",
"- BCM2·MLB·MLB evo 키는 일반 트랜스폰더(ID46 등)로 복제하는 방식이 아니라서 'XT27A/A66·XT27B·XT57B 호환' 칸을 비웠습니다.",
"- 키블레이드(키웨이)는 비상키 블레이드입니다(HU66, Q2·Q3 F3·TT 8S·Q8은 HU162T 표기 병존). 키블레이드 부품번호는 MLB 비상키 4M0837216A만 찾았습니다.",
"- 출처 칸은 검색에서 근거로 쓴 페이지입니다. 원문은 이 환경에서 열 수 없어 검색 결과 요약을 근거로 했습니다. 부품 판매처는 대부분 미국·유럽 사이트입니다.",
'',
'※ 색상',
"- 주황색: 추정이거나 자료가 서로 다른 값, 해당 연식 칩 자료가 없어 같은 세대 기준으로 채운 값, 또는 국내 미판매 모델(해외 사양 기준) — 실물 키로 재확인.",
"- 빨간색: 확인 불가 — PPE·PPC·MEB 신형 키(A5·S5 B10, Q5·SQ5 3세대, A6·S6 e-트론, Q6 e-트론, Q4 e-트론, 3세대 Q3)는 칩·이모빌라이저 자료가 없습니다.",
"- 전환 연식은 칩코드·이모빌라이저 칸에 전·후를 함께 적었습니다(예: TT 2015 = 8J ID48 / 8S MQB). 후속 모델 칩이 확인 불가면 빨간색입니다.",
'',
'※ 목록과 국내 판매 연식이 다른 모델',
"- A1: 2015.06 첫 출시, 2016 디젤게이트로 판매 중단 → 2015~2016만 기록(목록 2012-2018).",
"- A3 8P: 스포트백 2008.10 출시 → 2008~2012 / A3 8Y: 2022.07 출시 → 2022~ / S3 8Y: 2022.12 출시 → 2022~ / RS3: 8V 국내 미판매, 8Y 2023.07 출시 → 2023~.",
"- A5 B10: 2025.07 출시(목록 2024~) / A7 C8: 2020.03 / S7: 2020.07 / A8 D5: 2019.12 / S6 C8: 2020.07 / S8: D4는 2017까지, D5 S8 L은 2023.07 출시.",
"- RS6 아반트·RS7: C7 2014.08 출시, C8 2021.08 출시 → 2019~2020년식 없음.",
"- Q2: 2020.09 출시(2018 부산모터쇼 공개 후 연기) / Q3 F3: 2020.05 / Q5·SQ5 FY: 2020.05.13 / Q7 4L: 2006.07 판매 시작 / Q7 4M: 2016.03 / SQ7: 2024.01 첫 출시.",
"- Q8: 2020.04.01 첫 출시 / RS Q8: 2021.06 / e-트론 55: 2020.07.01 / SQ8 e-트론: 2024.06.10 / R8 2세대: 2017.11(1세대 국내 판매는 2016.02까지).",
"- 국내 정식 판매 이력이 없는 모델: SQ2, RS Q3, TT RS(2019 인증만). 목록 연식대로 남기고 주황색(해외 사양 기준)으로 표시했습니다.",
'',
'※ 조사하며 확인된 주요 사항',
"- 모델마다 연식별로 검색했고 연식별 검색 기록은 research/audi/yearly.md에 있습니다.",
"- BCM2(2008~2018): 키 주파수는 BCM2 코드로 구분(5D1=433MHz, 5D2~5D4=315MHz, 5D7=868MHz). 2013년경부터 공장 잠김(locked) BCM2가 나와 올키로스트는 OBD만으로 안 되고 온라인 해제(Abrites VN020 등)나 벤치 읽기가 필요합니다.",
"- MQB(8V·Q2·Q3 F3·TT 8S)는 Megamos AES(ID88), 8Y(A3·S3·RS3 2021~)는 Hitag Pro MQB49(NCF295X)이며 GeKo 온라인 로그인이 필요합니다. 일부 판매처는 8Y를 AES ID88로 표기합니다.",
"- MLB(B9·Q5 FY·Q7 4M): 국내형 순정 스마트키 4M0959754BA(433MHz, 5M 칩, 2017-2021), 2016 Q7 4M0959754BC(434MHz). 중고 키는 VIN 잠금이라 재등록이 어렵습니다.",
"- MLB evo(C8·D5·Q8·e-트론·e-트론 GT): Q8 4N0959754BL(434MHz), RS6·RS7·RS Q8·RS e-트론 GT 4N0959754BC(433.92MHz). 미국 딜러 품번 4N0959754AM/K/BF는 뺐습니다.",
"- 구형 국내형 폴딩키: A3 8P·TT 8J 8P0837220D(434MHz), A1·Q3 8U 8X0837220D(434MHz), A4 B7 8E0837220E/Q/K(433MHz), A6 C6·Q7 4L 4F0837220M/T(434MHz), A8 D3 4E0837220M/D(433MHz), R8 1세대 420837220(433MHz).",
"- Q2 81A837220D(434MHz, Megamos AES), Q3 F3 81A837220AG(434MHz), TT 8S 8S0959754AK(434MHz, ID88), A3/S3 8V 8V0837220D(434MHz), A3/S3/RS3 8Y 8Y0959754AN(434MHz).",
"- PPE(A6 e-트론·Q6 e-트론)·PPC(A5·Q5 3세대)는 UWB/NFC 디지털 키가 표준이고 NFC 키카드가 제공됩니다. Q4 e-트론은 RSAD UWB(릴레이 공격 탐지) 키입니다."]
for n in notes: g.append([n])
g.column_dimensions['A'].width=150
for c in g['A']: c.font=Font(name='Arial',size=10); c.alignment=Alignment(wrap_text=False,vertical='top')
wb.save(os.path.join(ROOT,'아우디_models.xlsx'))
sys.path.insert(0,os.path.join(ROOT,'research')); from add_brand import add_brand; add_brand(os.path.join(ROOT,'아우디_models.xlsx'))  # 맨 앞 '브랜드' 컬럼
from notation import apply_file; apply_file(os.path.join(ROOT,'아우디_models.xlsx'))  # 칩코드·부품번호 표기 통일
sys.path.insert(0,os.path.join(ROOT,'research','recheck')); import apply as recheck; recheck.apply_file(os.path.join(ROOT,'아우디_models.xlsx'))  # 2005+ 불확실 행 재조사 결과
print(len(rows),'rows written')

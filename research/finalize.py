# 모든 브랜드 공통 후처리: 해외 주파수 키 제거, 키종류 판정, 비고(주황/빨강 사유만) 정리
import re

TYPES=['막대키','폴딩키','스마트키','카드키']
def join(ts): return ','.join(t for t in TYPES if t in ts)
def y4(r): return int(r['year'][:4])

# ---------- 해외 주파수(315·868MHz) 키 제거 ----------
FOREIGN=re.compile(r'315(?!\d)|868MHz|미국형|US 리모컨|사양 존재')
def clean_tokens(v):
    out=[]
    for t in v.split(' / '):
        t2=re.sub(r'315/43([34])MHz',r'43\1MHz',t).replace('315/433/868MHz','433MHz')
        if FOREIGN.search(t2): continue
        out.append(t2)
    return ' / '.join(out)
def strip_foreign(brand,r):
    for k in ('smart','fold','card','blade_pn'):
        v=r.get(k,'')
        if not v: continue
        if brand=='chevy':
            if FOREIGN.search(v): r[k]=''
        else:
            r[k]=clean_tokens(v)

# ---------- 키종류 ----------
def kt_bmw(r):
    ts={'막대키'} if r['immo'].startswith('EWS') else {'스마트키'}
    if '카드' in r['smart']: ts.add('카드키')
    return ts
REN_BAR={'SM5 (1세대)','SM3 (1세대, N17)','SM3 뉴 제너레이션 (1세대 페이스리프트, CF)'}
def kt_renault(r):
    m=r['model']
    if m in REN_BAR: return {'막대키'}
    if m=='SM5 (2세대)' or (m=='SM7' and y4(r)<=2011): return {'막대키','카드키'}
    if m=='그랑 콜레오스': return {'스마트키'}
    if m=='마스터 (LCV)': return {'폴딩키'}
    return {'카드키'}
KGM_BAR={'체어맨 (1세대, H)','코란도 (2세대)','뉴 코란도','무쏘','무쏘 스포츠 (픽업)','렉스턴 (1세대)','이스타나 (밴)',
         '액티언 (1세대)','액티언 스포츠 (픽업)','카이런','뉴 렉스턴'}
def kt_kgm(r):
    m=r['model']; ts=set()
    if m in KGM_BAR: ts.add('막대키')
    if m=='로디우스': ts.add('막대키')
    if '리모컨키' in r['fold'] or '리모컨키' in r['blade_pn']: ts.add('막대키')
    if '폴딩' in r['fold']: ts.add('폴딩키')
    if r['smart'] or m in ('체어맨 (2세대, W)','코란도 e-모션 (전기차)'): ts.add('스마트키')
    return ts
CH={'마티즈 II (GM대우, M150)':'막대키','올 뉴 마티즈 (GM대우, M200)':'막대키','마티즈 크리에이티브 (GM대우, M300)':'막대키',
    '칼로스 (GM대우)':'막대키','젠트라 (GM대우)':'막대키','라세티 (GM대우, J200, 1세대)':'막대키','매그너스 (GM대우)':'막대키',
    '토스카 (GM대우/쉐보레)':'막대키','레조 (GM대우, Rezzo)':'막대키','G2X (GM대우)':'막대키',
    '아베오 (쉐보레, T300)':'폴딩키','트랙스 (쉐보레, 1세대)':'폴딩키','카마로 (쉐보레, 5세대)':'폴딩키',
    '윈스톰 (GM대우)':'폴딩키','윈스톰 맥스 (GM대우)':'폴딩키',
    '라세티 프리미어 (GM대우, J300)':'폴딩키,스마트키','크루즈 (쉐보레, J300, 1세대)':'폴딩키,스마트키','크루즈 (쉐보레, D2XX, 2세대)':'폴딩키,스마트키',
    '말리부 (쉐보레, 8세대)':'폴딩키,스마트키','알페온 (GM대우→쉐보레)':'폴딩키,스마트키','임팔라 (쉐보레)':'폴딩키,스마트키',
    '올란도 (쉐보레)':'폴딩키,스마트키','캡티바 (쉐보레, 1세대)':'폴딩키,스마트키',
    '트랙스 크로스오버 (쉐보레, 2세대)':'폴딩키,스마트키','트레일블레이저 (쉐보레, 소형 SUV)':'폴딩키,스마트키',
    '볼트 (쉐보레, Volt, 플러그인 하이브리드)':'스마트키','말리부 (쉐보레, 9세대)':'스마트키','카마로 (쉐보레, 6세대)':'스마트키',
    '콜벳 (쉐보레, C7)':'스마트키','콜벳 (쉐보레, C8)':'스마트키','볼트 EV (쉐보레)':'스마트키','볼트 EUV (쉐보레)':'스마트키',
    '이쿼녹스 (쉐보레, 가솔린)':'스마트키','트래버스 (쉐보레)':'스마트키','타호 (쉐보레)':'스마트키','서버번 (쉐보레)':'스마트키',
    '캡티바 (쉐보레, 2세대, 리뱃지)':'','이쿼녹스 EV (쉐보레)':''}
def kt_chevy(r):
    m,y=r['model'],y4(r)
    if m=='스파크 (쉐보레, M300)': return {'막대키'} if y<=2012 else ({'막대키','폴딩키'} if y==2013 else {'폴딩키'})
    if m=='콜로라도 (쉐보레)': return {'막대키'} if y<=2023 else ({'막대키','스마트키'} if y==2024 else {'스마트키'})
    return set(CH[m].split(',')) if CH[m] else set()
KT={'benz':lambda r:set(r['ktype_hint'].split(',')),'bmw':kt_bmw,'renault':kt_renault,'kgm':kt_kgm,'chevy':kt_chevy}

# ---------- 비고: 주황/빨강 칸의 이유만 ----------
def R_bmw(r):
    m,y=r['model'],y4(r)
    if m.startswith(('1시리즈 (F70','2시리즈 그란 쿠페 (F74')): return '신형 섀시(F70/F74) 전용 칩·이모빌라이저 자료 없음'
    if m.startswith(('5시리즈 (E39','7시리즈 (E38')): return '블레이드 HU92(2트랙)·HU58(4트랙) 병존, EWS3/EWS4 공용 칩 — 실물 확인 필요'
    if m.startswith(('5시리즈 (G60','i5 (G60')): return '이모빌라이저 BDC3·BCP 출처 상충'
    if m.startswith(('M5 (G90','X7 (G07')): return '이 연식 이모빌라이저 BDC3·BCP 자료 상충(확인 필요)'
    if m.startswith('X3 (F25'): return '블레이드 표기 HU127 vs HU100R 상충'
    if m.startswith('X3 (G45'): return {2024:'2024년식 BDC3 vs BCP 자료 상충, 칩은 U섀시 기준 추정',2025:'칩 세부형식 직접 확인 안 됨(U섀시 기준 추정)'}.get(y,'2026년식 칩 자료 없음')
    if m.startswith(('X3 M (F97','X4 (G02','X4 M (F98')): return '해당 섀시 생산 종료 후 연식 — 국내 해당 연식 존재 여부 확인 불가'
    if m.startswith('Z4 (E89'): return 'E89 생산 2016.8 종료 — 국내 해당 연식 존재 여부 확인 불가'
    if m.startswith('XM'): return 'XM 전용 이모빌라이저 자료 없음 — G09 섀시 분류로 추정'+(' / 2026년식 자료 없음' if y==2026 else '')
    if m.startswith('iX3 (NA5'): return '신규 구조(ZSM) — 칩 형식 자료 없음'
    return '이 연식 이모빌라이저 원문 없음 — 이전 연식 기준 추정'
def R_renault(r):
    m,y=r['model'],y4(r)
    if m.startswith('SM3 (2세대'): return '같은 품번 카드가 PCF7952(Hitag2)·PCF7953M(AES) 두 사양으로 유통 — 전환 시점 자료 없음'
    if m.startswith('SM5 (3세대') or (m=='SM7' and y>=2012): return 'ID46 카드와 삼성 전용 AES 카드 병존 — 적용 연식 구분 자료 없음'
    if m=='QM5': return 'Hitag2·AES 카드 두 종류 판매 — AES 전환 연식 자료 없음'
    if m=='SM5 (1세대)': return '칩 직접 자료 없음 — 닛산 맥시마(A33) 기준 추정'
    if m.startswith('SM3 (1세대'): return '1세대 칩 직접 자료 없음 — 같은 차체 페이스리프트(CF) 기준 추정'
    if m in ('SM5 (2세대)','SM7'): return '국내 카드키 칩 직접 자료 없음 — 닛산 티아나 J31 기준 추정'
    if m in ('SM6','QM6'): return '순정 카드 자료가 2024년식까지 — 동일 카드로 추정'
    if m.startswith('아르카나'): return '신형 로고 차량용 카드 품번 미확인(285979827R 불일치 안내 있음)'
    if m=='그랑 콜레오스': return '전용 자료 없음 — 원형 지리 몬자로 키가 ID4A·ID8A 두 종류'
    if m.startswith('마스터'): return '칩 자료가 2020년까지 — 이후 연식 추정'
    return None
def R_kgm(r):
    m,y=r['model'],y4(r)
    d={'체어맨 (1세대, H)':'체어맨 칩 직접 자료 없음 — 쌍용 공용 4D60 기준 추정',
       '체어맨 (2세대, W)':'스마트키 칩 자료 없음 — 추정값',
       '코란도 (2세대)':'이모박스 자료가 2002년부터 — 2000·2001년식 직접 확인 안 됨',
       '무쏘':'이모박스 자료가 2002년부터 — 2000·2001년식 직접 확인 안 됨',
       '코란도 (4세대, C313)':'칩·블레이드 해외 판매처 1곳 기준, 이모빌라이저 명칭은 티볼리·G4 렉스턴 기준 추정',
       '코란도 e-모션 (전기차)':'키 칩 직접 자료 없음 — 코란도 C300 기준 추정',
       '무쏘 스포츠 (픽업)':'직접 자료 없음 — 무쏘 기준 추정',
       '코란도 스포츠 (픽업)':'폴딩키 자료가 2014.01부터 — 2012·2013년식 직접 확인 안 됨',
       '렉스턴 스포츠 & 칸 (픽업)':'2022 이후 스마트키 칩 자료 없음',
       'G4 렉스턴 (2세대)':'2020.11 이후 신형 스마트키 칩 자료 없음',
       '이스타나 (밴)':'키 칩 자료 없음',
       '로디우스':'1세대 키(4D60)와 로디우스 II 폴딩키(4D60x80) 병존 — 키로 구분 필요',
       '토레스 EVX (전기차)':'키 칩 직접 자료 없음 — 토레스 47칩 기준 추정',
       '액티언 (2세대, J120)':'키 칩 직접 자료 없음 — 토레스 47칩 기준 추정',
       '무쏘 EV (픽업, 전기차)':'키 칩 직접 자료 없음 — 토레스 47칩 기준 추정'}
    if m=='티볼리': return '2020.02 이후 스마트키 칩 자료 없음'+(' (2022~ 폴딩키도 미확인)' if y>=2022 else '')
    if m=='토레스': return '페이스리프트 신형 키 칩 자료 없음 — 기존 47칩 기준 추정' if y>=2026 else '이모빌라이저 모듈 명칭은 G4 렉스턴·티볼리 기준 추정'
    return d.get(m)
def R_chevy(r):
    m,y=r['model'],y4(r)
    X='국내형 이모빌라이저 적용 자료 없음 — 수출형 '
    d={'마티즈 II (GM대우, M150)':'국내형 이모빌라이저 적용 자료 없음(후속 올뉴마티즈 국내형은 미적용)',
       '칼로스 (GM대우)':X+'칼로스 ID48 기준','젠트라 (GM대우)':X+'아베오 T250 ID48 기준',
       '레조 (GM대우, Rezzo)':X+'타쿠마 ID48 기준','매그너스 (GM대우)':X+'에반다 ID48 기준',
       '라세티 (GM대우, J200, 1세대)':X+'라세티/옵트라(2004~) 4D60 기준',
       '라세티 프리미어 (GM대우, J300)':'칩은 같은 차 수출형(크루즈 J300) 기준 — 국내 품번 미확인',
       '볼트 (쉐보레, Volt, 플러그인 하이브리드)':'국내형(433MHz) 스마트키 자료 없음 — 칩은 미국형 기준',
       '알페온 (GM대우→쉐보레)':'칩은 뷰익 라크로스 기준 — 국내 품번 미확인',
       '올란도 (쉐보레)':'스마트키 칩 표기 상충(PCF7952 계열 vs PCF7938X)',
       '카마로 (쉐보레, 6세대)':'국내 판매 종료 연도 자료 상충(2022~2024)',
       '콜벳 (쉐보레, C7)':'한국GM 공식 판매 자료 없음(수입업체 판매만)','콜벳 (쉐보레, C8)':'한국GM 공식 판매 자료 없음(수입업체 판매만)',
       '서버번 (쉐보레)':'한국GM 공식 판매 자료 없음(수입업체 판매만)',
       '볼트 EUV (쉐보레)':'칩 표기 상충(ID46 vs ID49)','윈스톰 맥스 (GM대우)':'윈스톰 기준 추정',
       '캡티바 (쉐보레, 1세대)':'국내 스마트키 적용·품번 자료 없음, 블레이드 표기 상충(DWO5/HU100)',
       '캡티바 (쉐보레, 2세대, 리뱃지)':'국내 미출시','이쿼녹스 EV (쉐보레)':'국내 미출시(인증 후 출시 철회)',
       '이쿼녹스 (쉐보레, 가솔린)':'HYQ4EA 적용 자료가 2022년까지 — 이후 연식 추정',
       '트래버스 (쉐보레)':'2021년 이후 키(HYQ4ES)는 해외 판매처 적용표 기준 — 국내 확인 안 됨'}
    if m=='스파크 (쉐보레, M300)': return '2014년형(2013 하반기)부터 이모빌라이저 — 연식만으로 구분 불가' if y==2013 else 'M300 폴딩키 자료 없음 — M400 폴딩키 기준 추정'
    if m=='토스카 (GM대우/쉐보레)': return ('2006년형 미적용·2007년형(2006.11~) 적용 — ' if y==2006 else '')+'칩은 같은 차 수출형(에피카) 4D60 기준'
    if m=='볼트 EV (쉐보레)': return '칩 표기 상충(ID46 vs ID49)' if y>=2022 else '국내형(433MHz) 스마트키 자료 없음 — 칩은 미국형 기준'
    return d.get(m)
RS={'benz':lambda r:r['note'],'bmw':R_bmw,'renault':R_renault,'kgm':R_kgm,'chevy':R_chevy}

def process(brand,rows):
    for r in rows:
        strip_foreign(brand,r)
        if brand=='kgm' and '87170' in r['fold'] and '폴딩' not in r['fold']:
            r['blade_pn']=r['fold']+' — 리모컨 일체형 막대키' if '리모컨키' not in r['fold'] else r['fold']; r['fold']=''
        if brand=='kgm' and r['fold'].startswith('2버튼 리모컨키'):
            bar,fold=r['fold'].split(' / ',1); r['blade_pn']=bar; r['fold']=fold
        r['ktype']=join(KT[brand](r))
        if r.get('flag') in ('orange','red'):
            why=RS[brand](r)
            if not why: raise SystemExit(f'사유 없음: {brand} {r["model"]} {r["year"]}')
            r['note']=why
        else:
            r['note']=''
    return rows

# 6차 세대별 보완 규칙 (research/recheck/fill6.py가 사용)
#   RULES: dict(file, model(정규식), y0, y1, col, val, src[, chip(정규식)])  — 빈 칸만 채움
#   FUNCS: dict(file, model, col, fn(row)→값, src) — 행 내용(칩·키종류)으로 값을 정하는 규칙
import re

H = '현대_트랜스폰더_칩코드_DB.xlsx'
K = '기아_트랜스폰더_칩코드_DBnew.xlsx'
KW = '키블레이드(키웨이)'
IM = '이모빌라이저 시스템'
BP = '키블레이드(부품번호)'
SP = '스마트키(부품번호)'

TPH = 'transpondery(Hyundai Catalog {})'
TPK = 'transpondery(Kia Catalog {})'
SAME = '같은 세대 다른 연식 행 키웨이와 동일'
GEN_LXP = 'American Key Supply(Genesis G80·G90 2017-2020 비상키 LXP90, 순정 81996-D2000)'
GEN_KK = 'Locksmith Keyless·Royal Key Supply(Genesis G70·G80·GV70·GV80 2020-2023 비상키 KK12, 순정 81996-AR000·81996-T6000), Your Car Key Guys(2023-2026 Genesis 비상키 81996-CU000)'


def R(file, model, y0, y1, col, val, src, **k):
    return dict(file=file, model=model, y0=y0, y1=y1, col=col, val=val, src=src, **k)


RULES = [
 # ── 현대 키웨이 ──
 R(H, r'그랜저 \(IG, 6세대\)', 2016, 2018, KW, 'KK12', TPH.format('Azera·Grandeur 2018–2022 Hitag3 ID47 95440-G8000·G8100, 비상키 KK12')),
 R(H, r'아반떼 \(XD, 3세대\)', 2000, 2003, KW, 'HYN6', SAME + '(XD 2004~2006 HYN6)'),
 R(H, r'아반떼 \(MD, 5세대\)', 2010, 2012, KW, 'HY15[ILCO]', SAME + '(MD 2013~2015 HY15)'),
 R(H, r'아반떼 \(CN7, 7세대\)', 2020, 2022, KW, 'KK12[ILCO]', SAME + '(CN7 2023~ KK12), ' + TPH.format('Avante·Elantra 2021–2026 Hitag AES ID4A 95440-AA000, KK12')),
 R(H, r'아반떼 N \(CN7\)', 2021, 2023, KW, 'KK12[ILCO]', SAME + '(아반떼 N 2024~ KK12)'),
 R(H, r'베르나 \((LC, 1세대|MC, 2세대)\)', 2000, 2010, KW, 'HYN14R', TPH.format('Verna·Accent 1999–2011 Hitag2 ID46 PCF7936, HYN14R·HYN14')),
 R(H, r'i30 \(FD, 1세대\)', 2007, 2011, KW, 'HYN14R', TPH.format('i30 2007–2011 Hitag2 ID46 95430-2L000·95440-2L000, HYN14R')),
 R(H, r'i30 \(GD, 2세대\)', 2011, 2016, KW, 'HYN14R', TPH.format('i30 2012–2016 DST80 ID6E-MA, HYN14R·비상키')),
 R(H, r'i30 \(PD, 3세대\)', 2016, 2020, KW, 'HY22, KK12', TPH.format('i30·i30N 2017–2024 Hitag3 ID47 95440-G3000·G3100, 비상키 HY22·KK12')),
 R(H, r'벨로스터 \(FS, 1세대\)', 2011, 2017, KW, 'HYN14R', TPH.format('Veloster 2011–2017 95430-2V000·95440-2V000, HYN14R·비상키')),
 R(H, r'벨로스터 \(JS, 2세대\)', 2018, 2022, KW, 'HY22, KK12', TPH.format('Veloster·Veloster N 2018–2022 95440-J3000·J3100·K9000, 비상키 HY22·KK12')),
 R(H, r'제네시스 \(BH, 1세대\)', 2008, 2013, KW, 'HYN14R, HYN17B', TPH.format('Genesis·Genesis Coupe 2009–2014 Hitag2 ID46 95440-3M000·2M100, HYN14R·HYN17B')),
 R(H, r'제네시스 \(DH, 2세대\)', 2016, 2016, KW, 'KK12[ILCO], KIA9[Silca]', SAME + '(DH 2013~2015 KK12·KIA9)'),
 R(H, r'제네시스 쿠페 \(BK\)', 2008, 2010, KW, 'HY15R[ILCO], HY17[ILCO]', SAME + '(BK 2011~2016 HY15R·HY17)'),
 R(H, r'아이오닉 \(AE\)', 2016, 2022, KW, 'HY22, KK12', TPH.format('IONIQ 2016–2022 Hitag3 ID47 95440-G2000·G2100·G2500, HY22·KK12')),
 R(H, r'아이오닉 5 (N )?\(NE\)', 2021, 2026, KW, 'KK12[ILCO]', SAME + '(아이오닉 5 2021~2023 KK12), ' + TPH.format('IONIQ 5 2021–2026 Hitag AES ID4A 95440-GI000, KK12')),
 R(H, r'아이오닉 9 \(ME\)', 2025, 2026, KW, 'KK12', TPH.format('IONIQ 9 2024–2026 Hitag AES ID4A UWB 95440-N0000, KK12')),
 R(H, r'싼타페 \(SM, 1세대\)', 2000, 2003, KW, 'HYN7, HYN7R[Silca], HY-6D.P1[JMA], HY12[ILCO]', SAME + '(SM 2004~2005)'),
 R(H, r'싼타페 \(TM, 4세대\)', 2018, 2019, KW, 'KK12[ILCO]', SAME + '(TM 2020~2023 KK12), ' + TPH.format('Santa Fe 2019–2023 Hitag3 ID47 95440-S1000, KK12')),
 R(H, r'팰리세이드 \(LX2, 1세대\)', 2018, 2021, KW, 'KK12[ILCO]', SAME + '(LX2 2022~2024 KK12), ' + TPH.format('Palisade 2020–2022 Hitag3 ID47 95440-S8000, KK12')),
 R(H, r'팰리세이드 \(LX3, 2세대\)', 2025, 2026, KW, 'KK12', TPH.format('Palisade 2023–2026 Hitag AES ID4A 95440-S8500·S8600, KK12')),
 R(H, r'투싼ix \(LM, 2세대\)', 2009, 2012, KW, 'HY22', SAME + '(LM 2013~2015 HY22)'),
 R(H, r'투싼 \(NX4, 4세대\)', 2020, 2026, KW, 'KK12', TPH.format('Tucson 2022–2026 Hitag AES ID4A 95440-N9000·N9100, KK12')),
 R(H, r'코나 (일렉트릭 )?\(SX2(, 2세대)?\)', 2023, 2026, KW, 'KK12', TPH.format('Kona·Kona Electric 2024–2026 Hitag AES ID4A 95440-BE000·BE100, KK12')),
 R(H, r'캐스퍼 (일렉트릭 )?\(AX1( EV)?\)', 2021, 2026, KW, 'KK12', TPH.format('Casper 2021–2026 Hitag AES 95440-CW000, KK12')),
 R(H, r'스타렉스 \(A1\)', 2000, 2004, KW, 'HYN6', SAME + '(A1 2005~2007 HYN6)'),
 R(H, r'그랜드 스타렉스 \(TQ\)', 2007, 2021, KW, 'HYN14R', TPH.format('Starex·H-1 2011–2016 Hitag2 ID46, 2017–2021, HYN14R')),
 R(H, r'포터2 \(HR\)', 2004, 2026, KW, 'HYN14', TPH.format('Porter II 2004–2016 HYN14') + ', abkeys(Porter 2014+ 리모컨 키 블레이드 HYN14 순정 81996-4F500)'),
 R(H, r'포터2 일렉트릭', 2019, 2026, BP, '81996-CN000[비상키]', 'auto-keys.eu(Porter 2 스마트키 95440-CN100 433MHz AES 6A, 비상키 블레이드 81996-CN000)'),
 R(H, r'제네시스 G80 \(DH\)', 2016, 2020, KW, 'LXP90', GEN_LXP),
 R(H, r'제네시스 EQ900/G90 \(HI\)', 2015, 2022, KW, 'LXP90', GEN_LXP),
 R(H, r'제네시스 (일렉트리파이드 )?G80 \(RG3( EV)?\)', 2020, 2026, KW, 'KK12', GEN_KK),
 R(H, r'제네시스 G90 \(RS4\)', 2022, 2026, KW, 'KK12', GEN_KK),
 R(H, r'제네시스 G70 \(IK\)', 2024, 2026, KW, 'KK12', GEN_KK),
 R(H, r'제네시스 GV80( 쿠페)? \(JX1\)', 2020, 2026, KW, 'KK12', GEN_KK),
 R(H, r'제네시스 (일렉트리파이드 )?GV70 \(JK1( EV)?\)', 2020, 2026, KW, 'KK12', GEN_KK),
 R(H, r'제네시스 GV60 \(JW1\)', 2021, 2026, KW, 'KK12', GEN_KK),
 # ── 기아 키웨이 ──
 R(K, r'옵티마 \(Optima, MS\)', 2000, 2000, KW, 'HY12[ILCO], HYN7R-HY7R-HY16[Lishi]', SAME + '(MS 2001~2005)'),
 R(K, r'로체 \(Optima, MG\)', 2005, 2009, KW, 'HYN14R, HY22[ILCO]', TPK.format('Optima·Magentis MG 2006–2010 Hitag2 ID46, HYN14R') + ', ' + SAME + '(로체 2010 HY22)'),
 R(K, r'K5 \(Optima, TF\)', 2014, 2015, KW, 'HY22[ILCO]', SAME + '(TF 2010~2013 HY22)'),
 R(K, r'K5 \(Optima, JF\)', 2015, 2019, KW, 'HYN17B', TPK.format('Optima JF 2015–2020 Hitag3 NCF2951 95440-D4000·D4100, HYN17B')),
 R(K, r'K7 \(Cadenza, YG 프리미어\)', 2020, 2021, KW, 'LXP90[ILCO], TOYO-18[JMA]', SAME + '(YG 2015~2019)'),
 R(K, r'프라이드 JB', 2005, 2011, KW, 'HYN14R', TPK.format('Rio JB 2005–2011 Hitag2 ID46 PCF7936AS, HYN14R')),
 R(K, r'프라이드 UB', 2011, 2013, KW, 'HY22[ILCO]', SAME + '(UB 2014~2017 HY22)'),
 R(K, r'오피러스 \(Opirus, GH( 프리미엄)?\)', 2003, 2012, KW, 'HYN14R', TPK.format('Opirus·Amanti GH 2004–2010 4D60·ID46, HYN14R')),
 R(K, r'스팅어 \(Stinger, CK( 페이스리프트)?\)', 2017, 2023, KW, 'HYN17B, KK12', TPK.format('Stinger CK 2018–2023 Hitag3 NCF2951 95440-J5000·J5210, HYN17B·KK12')),
 R(K, r'스토닉', 2017, 2026, KW, 'KK12, HYN17B', TPK.format('Stonic YB 2017–2026 DST80·AES, KK12·HYN17B')),
 R(K, r'쏘울 \(Soul, AM\)', 2008, 2013, KW, 'HYN14R, HYN17B', TPK.format('Soul AM 2008–2013 Hitag2 ID46 95440-2K200, HYN14R·HYN17B')),
 R(K, r'쏘울 \(Soul, PS\)', 2014, 2019, KW, 'HYN17B', TPK.format('Soul PS 2014–2019 DST80 95440-B2000, HYN17B')),
 R(K, r'쏘울 부스터 \(Soul, SK3\)', 2019, 2025, KW, 'KK12', TPK.format('Soul SK3 2019–2026 AES ID4A 95440-K0000, KK12')),
 R(K, r'레이 \(Ray, TAM\)', 2023, 2025, KW, 'KK10[ILCO], KIA7[Silca]', SAME + '(TAM 2018~2022 KK10·KIA7)'),
 R(K, r'모닝 \(Morning, SA\)', 2004, 2010, KW, 'HYN14R', TPK.format('Picanto SA 2004–2011 Hitag2 ID46 PCF7936AS, HYN14R')),
 R(K, r'모닝 \(Morning, TA\)', 2011, 2017, KW, 'HYN17BT', TPK.format('Picanto TA 2011–2017 DST80 95440-1Y100, HYN17BT')),
 R(K, r'모닝 \(Morning, JA\)', 2017, 2025, KW, 'KK12, HYN17B', TPK.format('Picanto JA 2017–2026 DST80·AES 95440-G6000, KK12·HYN17B')),
 R(K, r'EV[369]( .*)?', 2021, 2026, KW, 'KK12', TPK.format('EV3·EV6·EV9 Hitag AES ID4A, 비상키 KK12')),
 R(K, r'EV4 \(CT1\)', 2025, 2026, KW, 'KK12', TPK.format('EV3·EV6·EV9 Hitag AES ID4A, 비상키 KK12') + ' — EV4 같은 세대 기준'),
 R(K, r'스포티지 \(Sportage, NB-Ⅶ\)', 2000, 2002, KW, 'HYN6', TPK.format('Sportage JA 1999–2001 ID48, HYN6')),
 R(K, r'스포티지 \(Sportage, JE/KM\)', 2004, 2010, KW, 'HYN14R', TPK.format('Sportage KM 2004–2010 Hitag2 ID46 PCF7936AS, HYN14R')),
 R(K, r'스포티지 \(Sportage, NQ5\)', 2025, 2026, KW, 'KK12[ILCO]', SAME + '(NQ5 2021~2024 KK12)'),
 R(K, r'쏘렌토 \(Sorento, BL\)', 2002, 2009, KW, 'HYN14R', TPK.format('Sorento BL 2002–2009 Hitag2 ID46 PCF7936AS, HYN14R')),
 R(K, r'쏘렌토 \(Sorento, XM\)', 2009, 2009, KW, 'HY22[ILCO]', SAME + '(XM 2010~2012 HY22)'),
 R(K, r'쏘렌토 \(Sorento, UM 페이스리프트\)', 2018, 2020, KW, 'HY18R[ILCO]', SAME + '(UM 2014~2017 HY18R), ' + TPK.format('Sorento UM Facelift 2018–2020 95440-C6000, HYN17B·KK12')),
 R(K, r'쏘렌토 \(Sorento, MQ4( 페이스리프트)?\)', 2020, 2026, KW, 'KK12', TPK.format('Sorento MQ4 2020–2026 Hitag AES ID4A 95440-P2000·P2020, KK12')),
 R(K, r'모하비 \(Mohave, HM 더마스터\)', 2020, 2025, KW, 'HY22[ILCO]', SAME + '(더마스터 2019 HY22)'),
 R(K, r'니로 \(Niro, DE\)', 2016, 2018, KW, 'KK12[ILCO]', SAME + '(DE 2019~2022 KK12)'),
 R(K, r'카렌스 \(Carens, (RS|UN)\)', 2000, 2013, KW, 'HYN14R', TPK.format('Carens RS 2001–2005·UN 2006–2012, HYN14R')),
 R(K, r'카니발 \(Carnival, KV-II/GQ\)', 2002, 2005, KW, 'HYN14R', TPK.format('Carnival GQ 2000–2005 4D60, HYN14R')),
 R(K, r'카니발 \(Carnival, KV-II/GQ\)', 2000, 2001, KW, 'HYN6, HYN14R', TPK.format('Carnival GQ 1998–2001 ID48 HYN6, 2000–2005 4D60 HYN14R')),
 R(K, r'카니발 \(Carnival, VQ\)', 2006, 2014, KW, 'HYN14R', TPK.format('Carnival VQ 2006–2014 Hitag2 ID46 PCF7936AS, HYN14R')),
 R(K, r'카니발 \(Carnival, KA4( PE)?\)', 2020, 2026, KW, 'KK12', TPK.format('Carnival KA4 2021–2026 Hitag AES ID4A 95440-R0000, KK12')),
 R(K, r'봉고3 \(Bongo3, J\)', 2003, 2025, KW, 'HYN14', 'abkeys·MK3(Kia Bongo 2006+ 순정 리모컨 키 블레이드 81996-4E030 HYN14)'),
 R(K, r'봉고3 \(Bongo3, J\)', 2006, 2025, BP, '81996-4E030[폴딩키]', 'abkeys·MK3(Kia Bongo 2006+ 순정 리모컨 키 블레이드 81996-4E030 HYN14)'),
 R(K, r'봉고3 EV \(전기차\)', 2020, 2025, BP, '81996-CP000[비상키]', 'VVDI(Kia Bongo 순정 스마트키 블레이드 81996-CP000)'),
 R(H, r'i40 \(VF\)', 2011, 2011, IM, 'SMK', 'transpondery(Kia Catalog DST80 스마트키 세대: SMARTRA 80bit & SMK), 같은 세대 i40 스마트키'),
]

# ── 아우디 ──
A = '아우디_models.xlsx'
CH = '칩코드 (예: ID46(PCF7936))'
MLBE = r'(A6 \(C8, 8세대\)|S6|RS6 아반트|A7 \(C8, 2세대\)|S7|RS7|A8 \(D5, 5세대\)|S8|SQ8|RS Q8|e-트론/Q8 e-트론|SQ8 e-트론|(RS )?e-트론 GT)'
SRC_MLBE = 'auto-keys.eu(Audi A8·A6·Q8 2018+ 스마트키 4N0959754AL·e-tron 4M0959754BF 비상키 HU162T), keyshop-online(Audi MLB 2016+ 비상키 HU162T)'
SRC_PPE = 'Audi USA 순정 부품(2025 Q6 e-tron·Q5·A5·SQ5 스마트키 4M0959754CG 공용 — 북미형이라 품번 뺌) — MLB evo 계열 키 기준 추정'
NEWAUDI = r'(A5 \(B10, 3세대\)|S5|RS5|A6 e-트론 \(GH\)|S6|Q5 \(GU, 3세대\)|SQ5|Q6 e-트론)'
RULES += [
 R(A, MLBE, 2019, 2026, KW, 'HU162T', SRC_MLBE, chip='MLB evo'),
 R(A, r'R8 \(4S, 2세대\)', 2017, 2024, KW, 'HU66, HU162T', 'auto-keys.eu(Audi R8 2021+ 순정 스마트키 4H0959754FK 비상키 HU162T), key4·Keymall(R8 HU66 비상키)'),
 R(A, r'Q4 e-트론', 2022, 2026, KW, 'HU66', 'MEB 플랫폼 키(폭스바겐 ID.4와 공용) — 비상키 HU66'),
 R(A, NEWAUDI, 2025, 2026, CH, 'MLB evo 전용 칩[추정]', SRC_PPE, chip='확인', force=True, flag='orange', note='2025년 이후 신형(PPE·PPC) 전용 칩 자료 없음 — MLB evo 공용 키 기준 추정'),
 R(A, NEWAUDI, 2025, 2026, KW, 'HU162T', SRC_PPE, chip='확인'),
]

# ── KGM(쌍용) ──
KG = 'KG모빌리티(쌍용)_models.xlsx'
SRC_TOY48 = 'Keystation(SsangYong Rexton 2버튼 리모컨 키 케이스 TOY48 블레이드), Autokeymaster(Rexton·Actyon 4D60x80 키 TOY40·TOY48)'
RULES += [
 R(KG, r'무쏘( 스포츠 \(픽업\))?', 2000, 2005, KW, 'SSY2', 'Autokeymaster(SsangYong Musso 1993-2011 ID48 키 블레이드 SSY2)'),
 R(KG, r'G4 렉스턴 \(2세대\)|렉스턴 스포츠 & 칸 \(픽업\)', 2017, 2026, KW, 'TOY48', SRC_TOY48),
 R(KG, r'토레스( EVX \(전기차\))?|액티언 \(2세대, J120\)|무쏘 EV \(픽업, 전기차\)', 2022, 2026, KW, 'TOY48[추정]', SRC_TOY48 + ' — 같은 회사 스마트키 비상키 기준 추정(신형 전용 자료 없음)'),
]

# ── 쉐보레(GM대우) ──
CV = '쉐보레_models.xlsx'
RULES += [
 R(CV, r'(마티즈 II \(GM대우, M150\)|올 뉴 마티즈 \(GM대우, M200\)|마티즈 크리에이티브 \(GM대우, M300\)|스파크 \(쉐보레, M300\))', 2000, 2013, KW, 'DWO4R', 'Eurocarkeyshop(Chevrolet Matiz 2005-2012 키 블레이드 DWO4R), UHS(Daewoo DWO4RAP 기계식 키)', chip='^(해당|확인)'),
 R(CV, r'스파크 \(쉐보레, M300\)', 2013, 2013, CH, 'ID46(PCF7937E)', 'transpondery(Chevrolet Spark 2013+ Hitag2 Extended ID46E PCF7937E·NCF2951E)', chip='^$'),
 R(CV, r'스파크 \(쉐보레, M300\)', 2013, 2013, KW, 'HU100', SAME + '(스파크 폴딩키 2014~ HU100)', chip='PCF7937E|^$'),
 R(CV, r'토스카 \(GM대우/쉐보레\)', 2006, 2011, KW, 'DWO5', 'CLK Supplies·Ilco(Chevrolet Epica 2004-2007 트랜스폰더 키 DW05T5), car-keys-online(Epica·Evanda DWO5 ID60) — 토스카는 수출명 Epica(V250)'),
 R(CV, r'콜벳 \(쉐보레, C8\)', 2022, 2026, KW, 'HU100', 'UHS·American Key Supply(Corvette C8 2020-2024 스마트키 13538852 YG0G20TB1, 비상키 HU100)'),
]

# ── 벤츠 2019년 이후 신형(EPC 범위 밖) — 같은 플랫폼 순정 433MHz 키 품번 [추정] ──
BZ = '벤츠_models.xlsx'
AKM = 'auto-keys.eu(메르세데스 순정 스마트키 433.92MHz: {})'
def gz(*p): return ', '.join(x + '[추정, 해외 공용 품번]' for x in p)
RULES += [
 R(BZ, r'CLA \(C118, 2세대\)|CLA45 AMG \(C117/C118\)|GLA \(H247, 2세대\)|GLA35/45 AMG|GLB \(X247, 1세대\)|GLB35 AMG', 2019, 2026, SP,
   gz('A1779057902', 'A2479054303'), AKM.format('W177 A클래스 2019 A1779057902·W247 A2479054303, HELLA 제조 키리스고') + ' — 같은 MFA2 플랫폼(A·B·CLA·GLA·GLB) 키 기준 추정'),
 R(BZ, r'E클래스 \(W214, 11세대\)|E53 AMG \(W214\)|CLE \(C236\)|GLC \(X254/C254, 2세대\)|GLC63 AMG \(X254\)', 2023, 2026, SP,
   gz('A2069057403'), AKM.format('C클래스 W206 2020+ A2069057403 HU64 키리스고') + ' — 같은 MRA2 플랫폼(W206·W214·X254·C236) 키 기준 추정'),
 R(BZ, r'메르세데스-마이바흐 S클래스 \(Z223\)|EQS 세단 \(V297\)|EQE 세단 \(V295\)|EQS SUV \(X296\)|EQE SUV \(X294\)', 2021, 2026, SP,
   gz('A2239057507', 'A2239054408'), AKM.format('S클래스 2020+ A2239057507·A2239054408') + ' — S클래스(W223)와 같은 세대 키 기준 추정'),
 R(BZ, r'GLS \(X167, 2세대\)|메르세데스-마이바흐 GLS \(X167\)', 2020, 2026, SP,
   gz('A1679053303', 'A1679054203'), AKM.format('FBS4 A1679053303·A1679054203 HU64 키리스고') + ' — GLE(W167)와 같은 MHA 플랫폼 키 기준 추정'),
]

# ── BMW: ETK(03.2019) 이후 연식 — 같은 세대·같은 칩 앞 연식의 스마트키 품번 이어 쓰기 ──
BM = 'BMW_코리아_출시모델.xlsx'
def _bmw_prev():
    import openpyxl, os
    ws = openpyxl.load_workbook(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), BM)).worksheets[0]
    hdr = [str(c.value).strip() if c.value else '' for c in ws[1]]
    ix = {h: i for i, h in enumerate(hdr)}
    last = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[ix['스마트키(부품번호)']] and not r[ix['비고']]:
            last.setdefault((r[ix['모델명']], str(r[ix['칩코드 (예: ID46(PCF7936))']])), []).append((int(str(r[ix['연식']])[:4]), r[ix['스마트키(부품번호)']]))
    return last
_BP = _bmw_prev()
def _bmw_carry(row):
    chip = str(row.get('칩코드 (예: ID46(PCF7936))'))
    if 'BDC3' in chip or '추정' in chip or row.get('비고'):
        return ''
    y = int(str(row['연식'])[:4])
    prev = sorted(v for v in _BP.get((row['모델명'], chip), []) if v[0] < y)
    return prev[-1][1] if prev else ''
FUNCS = [] if 'FUNCS' not in globals() else FUNCS


# ── 이모빌라이저: 칩·키종류로 세대별 시스템 판정 ──
def _immo(row, brand):
    chip = str(row.get('칩코드 (예: ID46(PCF7936))') or '')
    kt = str(row.get('키종류') or '')
    if not chip or chip.startswith('확인'):
        return ''
    if chip.startswith('해당 없음') or chip == 'None':
        return '해당 없음'
    toks = [t.strip() for t in re.split(r',\s*(?![^\[]*\])', chip) if t.strip()]
    smart_kw = ('스마트키' in kt or '카드키' in kt)
    blade_kw = ('막대키' in kt or '폴딩키' in kt)
    bl, sm = set(), set()
    for t in toks:
        base = re.sub(r'\[.*?\]', '', t)
        is_smart_tok = '스마트키' in t or re.search(r'PCF795[23]|ID8A|ID47|ID4A|ID6A|ID75', base)
        is_blade_tok = '폴딩키' in t or '플립키' in t or '이모빌라이저' in t or re.search(r'ID60|4D60|ID48|PCF7936|ID6E', base)
        if re.search(r'ID60|4D60|ID48', base):
            bl.add('SHINCHANG 이모빌라이저' if brand == '기아' else 'SMARTRA')
        elif re.search(r'ID6E', base) and not is_smart_tok:
            bl.add('SMARTRA 80bit')
        elif re.search(r'ID46', base) and (is_blade_tok or not smart_kw) and not re.search(r'PCF795[23]', base):
            bl.add('SMARTRA2, SMARTRA3')
        if re.search(r'PCF795[23]', base) or (re.search(r'ID46', base) and smart_kw and not blade_kw) or (re.search(r'ID8A', base)):
            sm.add('SMK')
        elif re.search(r'ID47|ID4A|ID6A|ID75', base):
            sm.add('IBU')
    if blade_kw and smart_kw and not bl and sm == {'SMK'} and 'ID46' in chip:
        bl.add('SMARTRA3')  # 같은 세대 폴딩키(ID46)는 SMARTRA3 (Kia Catalog TF·XM·SL·AM: SMARTRA 3 & SMK)
    if not smart_kw:
        sm = set()
    if not blade_kw:
        bl = set()
    flat = lambda S: [x for y in sorted(S) for x in y.split(', ')]
    if bl and sm:
        return ', '.join([f'{x}[일반 키]' for x in flat(bl)] + [f'{x}[스마트키]' for x in flat(sm)])
    return ', '.join(flat(bl) + flat(sm))


IMSRC = ('transpondery(Kia Catalog 세대별 이모빌라이저: Shinchang Immobox(4D60)·SMARTRA 2·3(ID46)·SMARTRA 80bit(DST80)·SMK(스마트키 유닛)·IBU), '
         'UHS(Hyundai·Kia 2008-2016 SMARTRA 2·3), ECUBUG(SMARTRA 1·2·3 → 2010 이후 DST80), 현대모비스(SMK 스마트키 시스템)')
FUNCS = [
 dict(file=H, model=r'.*', col=IM, fn=lambda r: _immo(r, '현대'), src=IMSRC),
 dict(file=K, model=r'.*', col=IM, fn=lambda r: _immo(r, '기아'), src=IMSRC),
 dict(file=BM, model=r'.*', col=SP, fn=_bmw_carry, src='같은 세대·같은 칩 앞 연식 스마트키 품번과 동일(BMW ETK 03.2019판 이후 연식이라 이어 씀)'),
]

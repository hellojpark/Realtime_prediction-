# 네이버 부동산 API 설정 및 상수 정의

# API 엔드포인트
NAVER_LAND_URL = 'https://m.land.naver.com/cluster/ajax/articleList'

# API 요청 파라미터
DEFAULT_PARAMS = {
    'rletTpCd': 'OR:APT:JGC:OPST:ABYG:OBYG:VL:YR:DSD:JWJT:SGJT:HOJT:DDDGG',
    'tradTpCd': 'B2',
    'z': '13',
    'lat': '37.563475',
    'lon': '127.036838',
    'btm': '37.5116815',
    'lft': '126.9807906',
    'top': '37.6152325',
    'rgt': '127.0928854',
    'showR0': '',
    'totCnt': '2310',
    'cortarNo': '1120000000',  # 성동구 전체
}

# 네이버 부동산 접속 시 필요한 기본 쿠키 설정
COOKIES = {
    'NNB': '5VDY3KETRZCGO',
    'ASID': '798225530000019364b933cf0000006e',
    'NID_JKL': 'ZSQxx6uaA+FvYjVXX6PHhupC/AZuHseEaQ6b+Bukyho=',
    'NID_AUT': '8i2ZhfMFnsrbTeu9yQRSbMPj+Lb2pRuDqfv17lXKyIPxvpmVblIcliIX5hlACBl5',
    'nhn.realestate.article.rlet_type_cd': 'A01',
    'nhn.realestate.article.ipaddress_city': '1100000000',
    'landHomeFlashUseYn': 'Y',
}

# 성동구 지역 코드 매핑
REGION_CODES = {
    '1120010100': '왕십리도선동',
    '1120010200': '왕십리제2동',
    '1120010300': '마장동',
    '1120010400': '사근동',
    '1120010500': '행당제1동',
    '1120010600': '행당제2동',
    '1120010700': '응봉동',
    '1120010800': '금호1가동',
    '1120010900': '금호2가동',
    '1120011000': '금호3가동',
    '1120011100': '금호4가동',
    '1120011200': '옥수동',
    '1120011300': '성수1가제1동',
    '1120011400': '성수1가제2동',
    '1120011500': '성수2가제1동',
    '1120011600': '성수2가제3동',
    '1120011700': '송정동',
    '1120011800': '용답동'
}

# 저장할 컬럼 정의
COLUMNS_TO_SAVE = [
    'atclNo',  # 매물 번호
    'atclNm',  # 건물명
    'region',  # 지역명 (변환된)
    'rletTpNm',  # 매물 종류
    'tradTpNm',  # 거래 종류
    'flrInfo',   # 층수 정보
    'prc',       # 보증금
    'rentPrc',   # 월세
    'spc1',      # 공급면적
    'spc2',      # 전용면적
    'direction', # 방향
    'atclCfmYmd', # 확인 일자
    'lat',       # 위도
    'lng',       # 경도
    'atclFetrDesc', # 특징 설명
    'bildNm',    # 동
    'rltrNm',    # 부동산 이름
]

# 크롤링 설정
MAX_RETRIES = 3  # 최대 재시도 횟수
REQUEST_DELAY = (3, 5)  # 요청 간 대기 시간 범위 (초)
RETRY_DELAY = (5, 10)   # 재시도 시 대기 시간 범위 (초)

# 출력 파일 설정
OUTPUT_FILE = 'naver_real_estate_with_region.csv' 
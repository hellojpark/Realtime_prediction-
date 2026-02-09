import time
import random
from fake_useragent import UserAgent
from config import REGION_CODES

def get_region_name(cortarNo):
    """지역 코드를 지역명으로 변환"""
    return REGION_CODES.get(cortarNo, f'기타지역({cortarNo})')

def get_random_headers():
    """랜덤 헤더 생성"""
    ua = UserAgent()
    return {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': ua.random,
        'referer': 'https://m.land.naver.com/',
        'sec-ch-ua-mobile': '?1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-requested-with': 'XMLHttpRequest',
    }

def random_sleep(min_sec, max_sec):
    """랜덤한 시간 동안 대기"""
    time.sleep(random.uniform(min_sec, max_sec)) 
import requests
import pandas as pd
from typing import Optional, List, Dict, Any

from config import (
    NAVER_LAND_URL, DEFAULT_PARAMS, COOKIES,
    MAX_RETRIES, REQUEST_DELAY, RETRY_DELAY,
    COLUMNS_TO_SAVE, OUTPUT_FILE
)
from utils import get_region_name, get_random_headers, random_sleep

class NaverLandCrawler:
    """네이버 부동산 크롤러 클래스"""
    
    def __init__(self):
        self.all_articles: List[Dict[str, Any]] = []
        self.current_page = 1
    
    def get_real_estate_data(self, page_no: int) -> Optional[Dict]:
        """특정 페이지의 부동산 데이터를 가져오는 함수"""
        params = DEFAULT_PARAMS.copy()
        params['page'] = page_no
        
        # 랜덤 딜레이 추가
        random_sleep(*REQUEST_DELAY)
        
        try:
            response = requests.get(
                NAVER_LAND_URL,
                params=params,
                cookies=COOKIES,
                headers=get_random_headers()
            )
            
            if response.status_code != 200:
                print(f"API 요청 실패: 상태 코드 {response.status_code}")
                return None
                
            if "비정상적인 접근" in response.text:
                print("CAPTCHA 감지: 서비스 이용이 제한되었습니다.")
                return None
                
            return response.json()
            
        except Exception as e:
            print(f"요청 중 에러 발생: {e}")
            return None
    
    def collect_data(self) -> bool:
        """전체 데이터 수집"""
        while True:
            retry_count = 0
            success = False
            
            while retry_count < MAX_RETRIES and not success:
                try:
                    print(f"\n페이지 {self.current_page} 수집 중... (시도 {retry_count + 1}/{MAX_RETRIES})")
                    data = self.get_real_estate_data(self.current_page)
                    
                    if data is None:
                        print(f"재시도 중... ({retry_count + 1}/{MAX_RETRIES})")
                        retry_count += 1
                        random_sleep(*RETRY_DELAY)
                        continue
                        
                    success = True
                    
                except Exception as e:
                    print(f"에러 발생: {e}")
                    retry_count += 1
                    if retry_count < MAX_RETRIES:
                        random_sleep(*RETRY_DELAY)
                        continue
                    break
            
            if not success:
                print("최대 재시도 횟수 초과")
                return False
                
            if not data.get('body', []):
                print("더 이상 데이터가 없습니다.")
                break
                
            self.all_articles.extend(data['body'])
            
            if not data.get('more', False):
                print("마지막 페이지입니다.")
                break
                
            self.current_page += 1
        
        return True
    
    def process_data(self) -> Optional[pd.DataFrame]:
        """수집된 데이터 처리"""
        if not self.all_articles:
            return None
            
        # 데이터프레임 생성
        df = pd.DataFrame(self.all_articles)
        
        # 지역 코드를 지역명으로 변환
        print("\n지역 정보 변환 중...")
        if 'cortarNo' in df.columns:
            df['region'] = df['cortarNo'].apply(get_region_name)
        else:
            print("경고: 'cortarNo' 컬럼을 찾을 수 없습니다.")
            df['region'] = '지역정보없음'
        
        # 필요한 컬럼만 선택
        available_columns = [col for col in COLUMNS_TO_SAVE if col in df.columns]
        return df[available_columns]
    
    def save_data(self, df: pd.DataFrame) -> None:
        """데이터프레임을 CSV 파일로 저장"""
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"\n데이터 저장 완료: {OUTPUT_FILE}")
        print(f"총 {len(df)}개의 매물이 저장되었습니다.")
    
    def run(self) -> None:
        """크롤링 실행"""
        print("네이버 부동산 데이터 수집 시작...")
        
        if not self.collect_data():
            print("데이터 수집 실패")
            return
            
        print(f"\n총 {self.current_page}페이지 수집 완료")
        print(f"수집된 매물 수: {len(self.all_articles)}")
        
        df = self.process_data()
        if df is not None:
            self.save_data(df)
            print("\n데이터 미리보기:")
            preview_columns = ['atclNm', 'region', 'rletTpNm', 'tradTpNm']
            available_preview = [col for col in preview_columns if col in df.columns]
            print(df[available_preview].head().to_string()) 
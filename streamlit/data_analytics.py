"""
부동산 데이터 분석 모듈
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import streamlit as st


class EstateDataAnalyzer:
    """부동산 데이터 분석 클래스"""
    
    def __init__(self):
        """데이터 로드 및 초기화"""
        self.data_path = Path(__file__).parent.parent / "estate_data"
        self.raw_data = None
        self.region_stats = None
        
    @st.cache_data
    def load_estate_data(_self):
        """부동산 데이터 로드 (캐시 적용)"""
        try:
            # 원본 데이터 로드
            raw_data_path = _self.data_path / "naver_region_name_estate.csv"
            _self.raw_data = pd.read_csv(raw_data_path)
            
            # 기본 데이터 정리
            _self._clean_data()
            
            # 지역별 통계 계산
            _self._calculate_region_stats()
            
            return True
            
        except Exception as e:
            st.error(f"데이터 로드 중 오류 발생: {e}")
            return False
    
    def _clean_data(self):
        """데이터 정리"""
        if self.raw_data is None:
            return
            
        # 가격 데이터를 숫자형으로 변환
        price_columns = ['prc', 'rentPrc']
        for col in price_columns:
            if col in self.raw_data.columns:
                self.raw_data[col] = pd.to_numeric(self.raw_data[col], errors='coerce')
        
        # 면적 데이터를 숫자형으로 변환
        area_columns = ['spc1', 'spc2']
        for col in area_columns:
            if col in self.raw_data.columns:
                self.raw_data[col] = pd.to_numeric(self.raw_data[col], errors='coerce')
        
        # 결측값 제거
        self.raw_data = self.raw_data.dropna(subset=['region', 'prc', 'rentPrc'])
        
    def _calculate_region_stats(self):
        """지역별 통계 계산"""
        if self.raw_data is None:
            return
            
        # 지역별 기본 통계
        self.region_stats = self.raw_data.groupby('region').agg({
            'prc': ['mean', 'median', 'count', 'min', 'max'],
            'rentPrc': ['mean', 'median', 'count', 'min', 'max'],
            'spc1': ['mean', 'median'],
            'spc2': ['mean', 'median'],
            'rletTpNm': lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A'
        }).round(0)
        
        # 컬럼명 정리
        self.region_stats.columns = [
            'avg_deposit', 'median_deposit', 'count_deposit', 'min_deposit', 'max_deposit',
            'avg_rent', 'median_rent', 'count_rent', 'min_rent', 'max_rent',
            'avg_area1', 'median_area1', 'avg_area2', 'median_area2', 'popular_type'
        ]
        
        # 평수 계산 (평 = 제곱미터 / 3.3)
        self.region_stats['avg_pyeong1'] = (self.region_stats['avg_area1'] / 3.3).round(1)
        self.region_stats['avg_pyeong2'] = (self.region_stats['avg_area2'] / 3.3).round(1)
        
        # 지역별 + 매물유형별 상세 통계 추가
        self.region_type_stats = self.raw_data.groupby(['region', 'rletTpNm']).agg({
            'prc': ['mean', 'median', 'count', 'min', 'max'],
            'rentPrc': ['mean', 'median', 'count', 'min', 'max'],
            'spc1': ['mean', 'median'],
            'spc2': ['mean', 'median']
        }).round(0)
        
        # 컬럼명 정리
        self.region_type_stats.columns = [
            'avg_deposit', 'median_deposit', 'count_deposit', 'min_deposit', 'max_deposit',
            'avg_rent', 'median_rent', 'count_rent', 'min_rent', 'max_rent',
            'avg_area1', 'median_area1', 'avg_area2', 'median_area2'
        ]
        
        # 평수 계산
        self.region_type_stats['avg_pyeong1'] = (self.region_type_stats['avg_area1'] / 3.3).round(1)
        self.region_type_stats['avg_pyeong2'] = (self.region_type_stats['avg_area2'] / 3.3).round(1)
        
        # 인덱스 리셋
        self.region_type_stats = self.region_type_stats.reset_index()
    
    def get_region_list(self):
        """지역 목록 반환"""
        if self.raw_data is None:
            return []
        return sorted(self.raw_data['region'].unique())
    
    def get_region_summary(self, region):
        """특정 지역의 요약 정보 반환"""
        if self.region_stats is None or region not in self.region_stats.index:
            return None
            
        stats = self.region_stats.loc[region]
        
        return {
            'region': region,
            'avg_deposit': int(stats['avg_deposit']),
            'avg_rent': int(stats['avg_rent']),
            'avg_pyeong1': stats['avg_pyeong1'],
            'avg_pyeong2': stats['avg_pyeong2'],
            'total_count': int(stats['count_deposit']),
            'popular_type': stats['popular_type'],
            'price_range': {
                'deposit_min': int(stats['min_deposit']),
                'deposit_max': int(stats['max_deposit']),
                'rent_min': int(stats['min_rent']),
                'rent_max': int(stats['max_rent'])
            }
        }
    
    def create_region_comparison_chart(self, selected_regions):
        """지역 비교 차트 생성"""
        if self.region_stats is None or not selected_regions:
            return None
            
        # 선택된 지역들의 데이터 추출
        comparison_data = self.region_stats.loc[selected_regions]
        
        # 보증금 비교 차트
        fig_deposit = go.Figure()
        fig_deposit.add_trace(go.Bar(
            name='평균 보증금',
            x=selected_regions,
            y=comparison_data['avg_deposit'],
            text=comparison_data['avg_deposit'].astype(int),
            textposition='auto',
            marker_color='#667eea'
        ))
        
        fig_deposit.update_layout(
            title="지역별 평균 보증금 비교",
            xaxis_title="지역",
            yaxis_title="보증금 (만원)",
            height=450,
            width=None,
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=100),
            xaxis=dict(tickangle=-45)
        )
        
        # 월세 비교 차트
        fig_rent = go.Figure()
        fig_rent.add_trace(go.Bar(
            name='평균 월세',
            x=selected_regions,
            y=comparison_data['avg_rent'],
            text=comparison_data['avg_rent'].astype(int),
            textposition='auto',
            marker_color='#764ba2'
        ))
        
        fig_rent.update_layout(
            title="지역별 평균 월세 비교",
            xaxis_title="지역",
            yaxis_title="월세 (만원)",
            height=450,
            width=None,
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=100),
            xaxis=dict(tickangle=-45)
        )
        
        # 평수 비교 차트
        fig_area = go.Figure()
        fig_area.add_trace(go.Scatter(
            name='공급면적',
            x=selected_regions,
            y=comparison_data['avg_pyeong1'],
            mode='markers+lines',
            marker=dict(size=10, color='#84fab0'),
            line=dict(color='#84fab0', width=2)
        ))
        fig_area.add_trace(go.Scatter(
            name='전용면적',
            x=selected_regions,
            y=comparison_data['avg_pyeong2'],
            mode='markers+lines',
            marker=dict(size=10, color='#8fd3f4'),
            line=dict(color='#8fd3f4', width=2)
        ))
        
        fig_area.update_layout(
            title="지역별 평균 평수 비교",
            xaxis_title="지역",
            yaxis_title="평수 (평)",
            height=450,
            width=None,
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=100),
            xaxis=dict(tickangle=-45),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return {
            'deposit': fig_deposit,
            'rent': fig_rent,
            'area': fig_area
        }
    
    def create_price_distribution_chart(self, region):
        """특정 지역의 가격 분포 차트"""
        if self.raw_data is None:
            return None
            
        region_data = self.raw_data[self.raw_data['region'] == region]
        
        if region_data.empty:
            return None
        
        # 보증금 분포
        fig_deposit_dist = px.histogram(
            region_data, 
            x='prc', 
            title=f"{region} 보증금 분포",
            labels={'prc': '보증금 (만원)', 'count': '매물 수'},
            color_discrete_sequence=['#667eea']
        )
        
        # 월세 분포
        fig_rent_dist = px.histogram(
            region_data, 
            x='rentPrc', 
            title=f"{region} 월세 분포",
            labels={'rentPrc': '월세 (만원)', 'count': '매물 수'},
            color_discrete_sequence=['#764ba2']
        )
        
        return {
            'deposit_dist': fig_deposit_dist,
            'rent_dist': fig_rent_dist
        }
    
    def get_property_types(self, region=None):
        """매물 유형 목록 반환"""
        if self.raw_data is None:
            return []
        
        if region:
            region_data = self.raw_data[self.raw_data['region'] == region]
            return sorted(region_data['rletTpNm'].unique())
        else:
            return sorted(self.raw_data['rletTpNm'].unique())
    
    def get_region_type_summary(self, region, property_type=None):
        """지역별 + 매물유형별 상세 통계"""
        if self.region_type_stats is None:
            return None
        
        if property_type:
            # 특정 지역 + 특정 매물 유형
            filtered_stats = self.region_type_stats[
                (self.region_type_stats['region'] == region) & 
                (self.region_type_stats['rletTpNm'] == property_type)
            ]
            
            if filtered_stats.empty:
                return None
                
            stats = filtered_stats.iloc[0]
            
            return {
                'region': region,
                'property_type': property_type,
                'avg_deposit': int(stats['avg_deposit']),
                'avg_rent': int(stats['avg_rent']),
                'median_deposit': int(stats['median_deposit']),
                'median_rent': int(stats['median_rent']),
                'avg_pyeong1': stats['avg_pyeong1'],
                'avg_pyeong2': stats['avg_pyeong2'],
                'avg_area1': stats['avg_area1'],
                'avg_area2': stats['avg_area2'],
                'total_count': int(stats['count_deposit']),
                'price_range': {
                    'deposit_min': int(stats['min_deposit']),
                    'deposit_max': int(stats['max_deposit']),
                    'rent_min': int(stats['min_rent']),
                    'rent_max': int(stats['max_rent'])
                }
            }
        else:
            # 특정 지역의 모든 매물 유형 통계
            region_stats = self.region_type_stats[
                self.region_type_stats['region'] == region
            ]
            
            if region_stats.empty:
                return None
                
            return region_stats.to_dict('records')
    
    def get_property_type_stats(self, region):
        """지역별 매물 유형 통계 (기존 호환성 유지)"""
        region_stats = self.get_region_type_summary(region)
        
        if not region_stats:
            return None
        
        # DataFrame 형태로 변환
        df_stats = pd.DataFrame(region_stats)
        df_stats = df_stats.rename(columns={
            'rletTpNm': 'property_type',
            'avg_deposit': 'prc',
            'avg_rent': 'rentPrc',
            'avg_area2': 'spc2',
            'total_count': 'count',
            'avg_pyeong2': 'avg_pyeong'
        })
        
        return df_stats[['property_type', 'prc', 'rentPrc', 'spc2', 'count', 'avg_pyeong']]
    
    def create_region_type_comparison_chart(self, region, property_types=None):
        """지역 내 매물유형별 비교 차트"""
        if self.region_type_stats is None:
            return None
        
        region_data = self.region_type_stats[
            self.region_type_stats['region'] == region
        ]
        
        if region_data.empty:
            return None
        
        # 특정 매물 유형만 필터링
        if property_types:
            region_data = region_data[
                region_data['rletTpNm'].isin(property_types)
            ]
        
        if region_data.empty:
            return None
        
        # 보증금 비교 차트
        fig_deposit = go.Figure()
        fig_deposit.add_trace(go.Bar(
            name='평균 보증금',
            x=region_data['rletTpNm'],
            y=region_data['avg_deposit'],
            text=region_data['avg_deposit'].astype(int),
            textposition='auto',
            marker_color='#667eea'
        ))
        
        fig_deposit.update_layout(
            title=f"{region} 매물유형별 평균 보증금",
            xaxis_title="매물 유형",
            yaxis_title="보증금 (만원)",
            height=450,
            width=None,
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        # 월세 비교 차트
        fig_rent = go.Figure()
        fig_rent.add_trace(go.Bar(
            name='평균 월세',
            x=region_data['rletTpNm'],
            y=region_data['avg_rent'],
            text=region_data['avg_rent'].astype(int),
            textposition='auto',
            marker_color='#764ba2'
        ))
        
        fig_rent.update_layout(
            title=f"{region} 매물유형별 평균 월세",
            xaxis_title="매물 유형",
            yaxis_title="월세 (만원)",
            height=450,
            width=None,
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        # 평수 및 매물 수 차트
        fig_combined = go.Figure()
        
        # 평수 (좌측 y축)
        fig_combined.add_trace(go.Bar(
            name='평균 평수',
            x=region_data['rletTpNm'],
            y=region_data['avg_pyeong2'],
            text=region_data['avg_pyeong2'],
            textposition='auto',
            marker_color='#84fab0',
            yaxis='y'
        ))
        
        # 매물 수 (우측 y축)
        fig_combined.add_trace(go.Scatter(
            name='매물 수',
            x=region_data['rletTpNm'],
            y=region_data['count_deposit'],
            mode='markers+lines',
            marker=dict(size=10, color='#ff6b6b'),
            line=dict(color='#ff6b6b', width=3),
            yaxis='y2'
        ))
        
        fig_combined.update_layout(
            title=f"{region} 매물유형별 평수 및 매물 수",
            xaxis_title="매물 유형",
            yaxis=dict(
                title="평수 (평)",
                side="left"
            ),
            yaxis2=dict(
                title="매물 수 (건)",
                side="right",
                overlaying="y"
            ),
            height=450,
            width=None,
            autosize=True,
            margin=dict(l=60, r=60, t=50, b=50),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return {
            'deposit_by_type': fig_deposit,
            'rent_by_type': fig_rent,
            'area_count_by_type': fig_combined
        }
    
    def search_properties(self, filters):
        """조건에 맞는 매물 검색"""
        if self.raw_data is None:
            return pd.DataFrame()
        
        filtered_data = self.raw_data.copy()
        
        # 지역 필터
        if filters.get('region'):
            filtered_data = filtered_data[filtered_data['region'] == filters['region']]
        
        # 가격 범위 필터
        if filters.get('min_deposit'):
            filtered_data = filtered_data[filtered_data['prc'] >= filters['min_deposit']]
        if filters.get('max_deposit'):
            filtered_data = filtered_data[filtered_data['prc'] <= filters['max_deposit']]
        
        if filters.get('min_rent'):
            filtered_data = filtered_data[filtered_data['rentPrc'] >= filters['min_rent']]
        if filters.get('max_rent'):
            filtered_data = filtered_data[filtered_data['rentPrc'] <= filters['max_rent']]
        
        # 면적 필터
        if filters.get('min_area'):
            filtered_data = filtered_data[filtered_data['spc2'] >= filters['min_area']]
        if filters.get('max_area'):
            filtered_data = filtered_data[filtered_data['spc2'] <= filters['max_area']]
        
        # 매물 유형 필터
        if filters.get('property_type'):
            filtered_data = filtered_data[filtered_data['rletTpNm'] == filters['property_type']]
        
        return filtered_data.head(20)  # 상위 20개만 반환
    
    def get_seongdong_overview_stats(self):
        """성동구 전체 매물유형별 통계"""
        if self.raw_data is None:
            return None
        
        # 성동구 전체 매물유형별 통계
        seongdong_stats = self.raw_data.groupby('rletTpNm').agg({
            'prc': ['mean', 'median', 'count', 'min', 'max'],
            'rentPrc': ['mean', 'median', 'count', 'min', 'max'],
            'spc1': ['mean', 'median'],
            'spc2': ['mean', 'median']
        }).round(0)
        
        # 컬럼명 정리
        seongdong_stats.columns = [
            'avg_deposit', 'median_deposit', 'count_deposit', 'min_deposit', 'max_deposit',
            'avg_rent', 'median_rent', 'count_rent', 'min_rent', 'max_rent',
            'avg_area1', 'median_area1', 'avg_area2', 'median_area2'
        ]
        
        # 평수 계산
        seongdong_stats['avg_pyeong1'] = (seongdong_stats['avg_area1'] / 3.3).round(1)
        seongdong_stats['avg_pyeong2'] = (seongdong_stats['avg_area2'] / 3.3).round(1)
        
        # 인덱스 리셋하여 매물유형을 컬럼으로 만들기
        seongdong_stats = seongdong_stats.reset_index()
        
        return seongdong_stats
    
    def create_seongdong_overview_charts(self):
        """성동구 전체 매물유형별 차트"""
        seongdong_stats = self.get_seongdong_overview_stats()
        
        if seongdong_stats is None or seongdong_stats.empty:
            return None
        
        # 매물유형별 보증금 비교
        fig_deposit = go.Figure()
        fig_deposit.add_trace(go.Bar(
            name='평균 보증금',
            x=seongdong_stats['rletTpNm'],
            y=seongdong_stats['avg_deposit'],
            text=seongdong_stats['avg_deposit'].astype(int),
            textposition='auto',
            marker_color='#667eea'
        ))
        
        fig_deposit.update_layout(
            title="성동구 매물유형별 평균 보증금",
            xaxis_title="매물 유형",
            yaxis_title="보증금 (만원)",
            height=400,
            width=None,
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=80),
            xaxis=dict(tickangle=-30)
        )
        
        # 매물유형별 월세 비교
        fig_rent = go.Figure()
        fig_rent.add_trace(go.Bar(
            name='평균 월세',
            x=seongdong_stats['rletTpNm'],
            y=seongdong_stats['avg_rent'],
            text=seongdong_stats['avg_rent'].astype(int),
            textposition='auto',
            marker_color='#764ba2'
        ))
        
        fig_rent.update_layout(
            title="성동구 매물유형별 평균 월세",
            xaxis_title="매물 유형",
            yaxis_title="월세 (만원)",
            height=400,
            width=None,
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=80),
            xaxis=dict(tickangle=-30)
        )
        
        # 매물유형별 매물 수 파이차트
        fig_pie = go.Figure()
        fig_pie.add_trace(go.Pie(
            labels=seongdong_stats['rletTpNm'],
            values=seongdong_stats['count_deposit'],
            hole=0.3,
            textinfo='label+percent',
            textposition='outside'
        ))
        
        fig_pie.update_layout(
            title="성동구 매물유형별 분포",
            height=400,
            width=None,
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        # 매물유형별 평수 및 매물 수 복합 차트
        fig_combined = go.Figure()
        
        # 평수 (좌측 y축)
        fig_combined.add_trace(go.Bar(
            name='평균 평수',
            x=seongdong_stats['rletTpNm'],
            y=seongdong_stats['avg_pyeong2'],
            text=seongdong_stats['avg_pyeong2'],
            textposition='auto',
            marker_color='#84fab0',
            yaxis='y'
        ))
        
        # 매물 수 (우측 y축)
        fig_combined.add_trace(go.Scatter(
            name='매물 수',
            x=seongdong_stats['rletTpNm'],
            y=seongdong_stats['count_deposit'],
            mode='markers+lines',
            marker=dict(size=12, color='#ff6b6b'),
            line=dict(color='#ff6b6b', width=3),
            yaxis='y2'
        ))
        
        fig_combined.update_layout(
            title="성동구 매물유형별 평수 및 매물 수",
            xaxis_title="매물 유형",
            yaxis=dict(
                title="평수 (평)",
                side="left"
            ),
            yaxis2=dict(
                title="매물 수 (건)",
                side="right",
                overlaying="y"
            ),
            height=400,
            width=None,
            autosize=True,
            margin=dict(l=60, r=60, t=50, b=80),
            xaxis=dict(tickangle=-30),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return {
            'deposit_by_type': fig_deposit,
            'rent_by_type': fig_rent,
            'distribution': fig_pie,
            'area_count_combined': fig_combined
        }
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Load real estate data
@st.cache_data

def load_real_estate_data():
    # 거래량 데이터 로드
    df_region_type_count = pd.read_csv('estate_data/df_region_type_count.csv')
    
    # 가격 데이터 로드
    df_region_type_price = pd.read_csv('estate_data/df_region_type_price.csv', index_col=0)
    
    # 첫 번째 행이 컬럼명이 되도록 처리
    df_region_type_price.columns = df_region_type_price.iloc[0]
    df_region_type_price = df_region_type_price.iloc[1:]
    
    # 'prc' 컬럼만 선택
    price_columns = [col for col in df_region_type_price.columns if col.startswith('prc')]
    df_region_type_price = df_region_type_price[price_columns]
    
    # 컬럼명을 부동산 유형으로 변경
    property_types = df_region_type_count.columns[1:].tolist()  # region 컬럼 제외
    column_mapping = dict(zip(price_columns, property_types))
    df_region_type_price = df_region_type_price.rename(columns=column_mapping)
    
    # 숫자형으로 변환
    for col in df_region_type_price.columns:
        df_region_type_price[col] = pd.to_numeric(df_region_type_price[col], errors='coerce')
    
    return {
        'region_type_count': df_region_type_count,
        'region_type_price': df_region_type_price
    }

def load_raw_estate_data():
    # 거래량 데이터 로드
    df = pd.read_csv('../estate_data/naver_region_name_estate.csv')
    
    return df
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils import load_real_estate_data, load_raw_estate_data

# Load environment variables
load_dotenv()

@st.cache_data

def load_real_estate_data():
    # 거래량 데이터 로드
    df_region_type_count = pd.read_csv('../estate_data/df_region_type_count.csv')
    
    # 가격 데이터 로드
    df_region_type_price = pd.read_csv('../estate_data/df_region_type_price.csv', index_col=0)
    
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


# Initialize ChatOpenAI
llm = ChatOpenAI(
    temperature=0.1,
    model_name="gpt-3.5-turbo",
    max_tokens=2048
)

# Define prompt template for real estate recommendations
real_estate_template = """
당신은 부동산 매물 추천 전문가 AI 어시스턴트입니다. 사용자의 질문을 바탕으로 적절한 매물을 추천해주세요.

현재 검색 조건:
- 지역: {region}
- 매물 유형: {property_type}

사용자 질문: {question}

참고 정보:
- 해당 지역 평균 매물가: {price}만원
- 현재 거래량: {volume}건

답변 시 주의사항:
1. 사용자의 질문을 고려하여 구체적인 매물 추천을 해주세요.
2. 해당 지역의 특성과 장단점을 설명해주세요.
3. 실거주/투자 목적에 따른 조언을 제공해주세요.
4. 주변 편의시설, 교통, 학군 등 관련 정보도 함께 제공해주세요.
"""

# Function to save prompt to file
def save_prompt(prompt):
    timestamp = datetime.now().strftime("%Y-%m-%d / %H:%M:%S")
    with open('prompts.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n[{timestamp}]\n{prompt}\n')

# 페이지 설정
st.set_page_config(
    page_title="AI 종합 분석 대시보드",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #2d3748;
        font-weight: 500;
    }
    .recommendation-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 사이드바 메뉴
with st.sidebar:
    st.markdown("### 🤖 AI 종합 분석 대시보드")
    st.markdown("---")
    menu = st.selectbox(
        "📍 메뉴 선택",
        ["🏠 대시보드", "🏘️ 부동산 매물 추천", "📈 주식 분석", "₿ 가상자산 분석"],
        index=1
    )

# 부동산 매물 추천 페이지
if menu == "🏘️ 부동산 매물 추천":
    # Load data
    real_estate_data = load_real_estate_data()
    # real_estate_data = load_raw_estate_data()
    
    st.markdown("""
    <div class="main-header">
        <h1>🏘️ AI 부동산 매물 추천</h1>
        <p>데이터 기반 맞춤형 매물 추천 서비스</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 검색 필터
    col1, col2 = st.columns(2)
    with col1:
        unique_regions = real_estate_data['region_type_count']['region'].unique()
        region = st.selectbox("🌍 지역 선택", unique_regions)
    with col2:
        property_types = real_estate_data['region_type_count'].columns[1:].tolist()
        property_type = st.selectbox("🏠 매물 유형 선택", property_types)
    
    # 선택된 지역과 유형에 대한 데이터 가져오기
    selected_count = real_estate_data['region_type_count'].loc[
        real_estate_data['region_type_count']['region'] == region,
        property_type
    ].values[0]
    
    # 가격 데이터 가져오기
    try:
        selected_price = float(real_estate_data['region_type_price'].loc[region, property_type])
    except:
        selected_price = 0
    
    # 현재 매물 정보 표시
    col1, col2 = st.columns(2)
    with col1:
        st.metric("평균 매물가", f"₩{selected_price:,.0f}만원", "시세 정보")
    with col2:
        st.metric("현재 거래량", f"{selected_count}건", "실거래 정보")
    
    st.markdown("---")
    
    # AI 매물 추천 섹션
    st.markdown("### 🤖 AI 매물 추천")
    
    # 사용자 입력 받기
    user_question = st.text_input(
        "원하시는 조건을 자유롭게 입력해주세요",
        placeholder="예: 역세권 아파트 중에서 신축이면서 주변에 학교가 있는 매물 추천해주세요"
    )
    
    if user_question:
        # 프롬프트 저장
        save_prompt(f"지역: {region}\n유형: {property_type}\n질문: {user_question}")
        
        # 프롬프트 템플릿 생성
        prompt = PromptTemplate.from_template(real_estate_template)
        
        # 체인 생성
        chain = prompt | llm | StrOutputParser()
        
        # 현재 선택된 정보로 컨텍스트 생성
        context = {
            "region": region,
            "property_type": property_type,
            "question": user_question,
            "price": f"{selected_price:,.0f}",
            "volume": str(selected_count)
        }
        
        # 로딩 표시
        with st.spinner('AI가 매물을 분석하고 있습니다...'):
            # 답변 생성
            response = chain.invoke(context)
            
            # 답변 표시
            st.markdown(f"""
            <div class="recommendation-box">
                <h4>🏠 추천 매물 분석</h4>
                {response}
            </div>
            """, unsafe_allow_html=True)
    
    # 지역 정보 시각화
    st.markdown("### 📊 지역 매물 현황")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 매물 유형별 분포
        property_distribution = real_estate_data['region_type_count'][
            real_estate_data['region_type_count']['region'] == region
        ].iloc[0, 1:]
        
        fig = go.Figure(data=go.Pie(
            labels=property_distribution.index,
            values=property_distribution.values,
            hole=0.4
        ))
        fig.update_layout(title=f"{region} 매물 유형 분포")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 매물 가격 비교
        price_comparison = real_estate_data['region_type_price'].loc[region]
        
        fig = go.Figure(data=go.Bar(
            x=price_comparison.index,
            y=price_comparison.values,
            text=price_comparison.values.round(0),
            textposition='auto',
        ))
        fig.update_layout(
            title=f"{region} 유형별 평균 매물가",
            xaxis_title="매물 유형",
            yaxis_title="가격 (만원)"
        )
        st.plotly_chart(fig, use_container_width=True)

elif menu == "🏠 대시보드":
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI 종합 분석 대시보드</h1>
        <p>실시간 데이터 기반 투자 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 여기에 대시보드 메인 페이지 내용 추가

elif menu == "📈 주식 분석":
    st.markdown("""
    <div class="main-header">
        <h1>📈 AI 주식 분석</h1>
        <p>실시간 주가 분석 및 예측</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 여기에 주식 분석 페이지 내용 추가

elif menu == "₿ 가상자산 분석":
    st.markdown("""
    <div class="main-header">
        <h1>₿ AI 가상자산 분석</h1>
        <p>암호화폐 시장 분석 및 예측</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 여기에 가상자산 분석 페이지 내용 추가

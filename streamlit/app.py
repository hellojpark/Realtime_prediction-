"""
부동산 RAG 시스템 Streamlit UI
"""

import streamlit as st
import sys
import os
from pathlib import Path
import time
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Windows 환경에서 한글 처리를 위한 인코딩 설정
import locale
if sys.platform.startswith('win'):
    try:
        os.environ['PYTHONIOENCODING'] = 'utf-8'
    except:
        pass

# RAG 모듈 경로 추가
sys.path.append(str(Path(__file__).parent.parent / "rag"))

from rag_system import EstateRAGSystem
from data_analytics import EstateDataAnalyzer
from streamlit_components import (
    setup_page_config, 
    render_sidebar, 
    render_chat_interface,
    render_system_status,
    display_sample_questions
)
from streamlit_utils import (
    initialize_session_state,
    check_system_ready,
    format_response
)


def main():
    """메인 앱 함수"""
    
    # 페이지 설정
    st.set_page_config(
        page_title="AI 부동산 분석 플랫폼",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 커스텀 CSS (strealit_ui 스타일)
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
        .stats-card {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 0.5rem 0;
        }
        .chat-message {
            background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #667eea;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 세션 상태 초기화
    initialize_session_state()
    
    # 데이터 분석기 초기화
    if 'data_analyzer' not in st.session_state:
        st.session_state.data_analyzer = EstateDataAnalyzer()
        st.session_state.data_analyzer.load_estate_data()
    
    # 사이드바 메뉴
    with st.sidebar:
        st.markdown("### 🏠 AI 부동산 분석 플랫폼")
        st.markdown("---")
        menu = st.selectbox(
            "📍 메뉴 선택",
            ["🏠 대시보드", "🤖 AI 매물 추천", "📊 지역 분석", "⚙️ 시스템 설정"],
            index=1
        )
        
        # RAG 시스템 상태 표시
        st.markdown("---")
        st.subheader("🤖 RAG 시스템")
        if st.session_state.system_initialized:
            st.success("✅ 시스템 준비 완료")
            
            # 캐시 정보 표시
            if hasattr(st.session_state, 'rag_system') and st.session_state.rag_system:
                cache_info = st.session_state.rag_system.get_cache_info()
                if cache_info.get("exists", False):
                    st.info(f"💾 캐시: {cache_info.get('size_mb', 'N/A')} MB")
        else:
            st.warning("⏳ 시스템 대기 중")
    
    # 메인 헤더
    st.markdown("""
    <div class="main-header">
        <h1>🏠 AI 부동산 분석 플랫폼</h1>
        <p>데이터 기반 맞춤형 매물 추천 및 시장 분석 서비스</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 메뉴별 페이지 렌더링
    if menu == "🤖 AI 매물 추천":
        render_ai_recommendation_page()
    elif menu == "📊 지역 분석":
        render_region_analysis_page()
    elif menu == "🏠 대시보드":
        render_dashboard_page()
    elif menu == "⚙️ 시스템 설정":
        render_system_settings_page()


def render_ai_recommendation_page():
    """AI 매물 추천 페이지"""
    
    # AI 질문 섹션을 최상단에 배치
    st.subheader("🤖 AI 매물 추천 질문")
    
    # RAG 시스템 상태에 따른 분기
    if not st.session_state.system_initialized:
        st.markdown("""
        <div class="success-box">
            <h4>🤖 AI 시스템 준비</h4>
            <p>AI 매물 추천을 위해 시스템을 초기화해야 합니다.</p>
            <p><strong>첫 실행 시 1-2분 정도 소요됩니다.</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 AI 시스템 초기화", type="primary", use_container_width=True):
            with st.spinner("AI 시스템을 초기화하는 중입니다..."):
                try:
                    # RAG 시스템 초기화 (캐시 활용)
                    rag_system = EstateRAGSystem()
                    rag_system.setup()
                    
                    # 세션 상태 업데이트
                    st.session_state.rag_system = rag_system
                    st.session_state.system_initialized = True
                    
                    st.success("✅ AI 시스템이 성공적으로 초기화되었습니다!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ 시스템 초기화 중 오류가 발생했습니다: {str(e)}")
                    st.error("💡 .env 파일에 OPENAI_API_KEY가 올바르게 설정되어 있는지 확인해주세요.")
    else:
        # AI 질문 입력 섹션 (최상단)
        render_ai_question_section()
        
        # AI 대화 히스토리 (질문창 바로 아래)
        render_ai_chat_history()
    
    st.markdown("---")
    
    # RAG 시스템이 준비되지 않은 경우 여기서 종료
    if not st.session_state.system_initialized:
        return
    
    # 성동구 전체 요약 정보 (확장 가능한 섹션)
    with st.expander("🏘️ 성동구 전체 시장 현황", expanded=False):
        render_seongdong_overview()
    
    st.markdown("---")
    
    # 지역 및 매물 유형 선택
    st.subheader("📍 지역별 상세 분석")
    
    col1, col2 = st.columns(2)
    with col1:
        regions = st.session_state.data_analyzer.get_region_list()
        selected_region = st.selectbox("관심 지역을 선택하세요", regions)
    
    with col2:
        if selected_region:
            property_types = st.session_state.data_analyzer.get_property_types(selected_region)
            selected_property_type = st.selectbox("매물 유형을 선택하세요", ["전체"] + property_types)
        else:
            selected_property_type = None
    
    # 상세 통계 표시
    if selected_region:
        if selected_property_type and selected_property_type != "전체":
            # 특정 지역 + 특정 매물 유형
            detailed_info = st.session_state.data_analyzer.get_region_type_summary(selected_region, selected_property_type)
            
            if detailed_info:
                st.markdown("### 📊 상세 통계")
                
                # 메트릭 표시
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("평균 보증금", f"{detailed_info['avg_deposit']:,}만원", 
                             f"({detailed_info['median_deposit']:,}만원)")
                with col2:
                    st.metric("평균 월세", f"{detailed_info['avg_rent']:,}만원",
                             f"({detailed_info['median_rent']:,}만원)")
                with col3:
                    st.metric("평균 면적", f"{detailed_info['avg_pyeong2']}평",
                             f"({detailed_info['avg_area2']:.0f}㎡)")
                with col4:
                    st.metric("매물 수", f"{detailed_info['total_count']:,}건")
                with col5:
                    deposit_range = detailed_info['price_range']
                    st.metric("보증금 범위", 
                             f"{deposit_range['deposit_min']:,}~{deposit_range['deposit_max']:,}만원")
                
                # 상세 정보 카드
                st.markdown(f"""
                <div class="stats-card">
                    <h4>🏠 {selected_region} - {selected_property_type} 상세 정보</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div>
                            <p><strong>💰 가격 정보</strong></p>
                            <p>• 평균 보증금: {detailed_info['avg_deposit']:,}만원</p>
                            <p>• 중간값 보증금: {detailed_info['median_deposit']:,}만원</p>
                            <p>• 평균 월세: {detailed_info['avg_rent']:,}만원</p>
                            <p>• 중간값 월세: {detailed_info['median_rent']:,}만원</p>
                        </div>
                        <div>
                            <p><strong>📐 면적 정보</strong></p>
                            <p>• 공급면적: {detailed_info['avg_pyeong1']}평 ({detailed_info['avg_area1']:.0f}㎡)</p>
                            <p>• 전용면적: {detailed_info['avg_pyeong2']}평 ({detailed_info['avg_area2']:.0f}㎡)</p>
                            <p>• 총 매물 수: {detailed_info['total_count']:,}건</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            # 지역의 매물유형별 상세 표시 (전체 평균은 제거)
            all_types_stats = st.session_state.data_analyzer.get_region_type_summary(selected_region)
            
            if all_types_stats:
                st.markdown(f"### 📊 {selected_region} 지역 개요")
                
                # 기본 정보만 표시
                total_properties = sum([stats['count_deposit'] for stats in all_types_stats])
                total_types = len(all_types_stats)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("총 매물 수", f"{total_properties:,}건")
                with col2:
                    st.metric("매물 유형 수", f"{total_types}개 유형")
                
                # 매물 유형별 상세 표
                st.markdown("### 📋 매물 유형별 상세 통계")
                
                # DataFrame으로 변환하여 표시
                import pandas as pd
                df_display = pd.DataFrame(all_types_stats)
                df_display = df_display[['rletTpNm', 'avg_deposit', 'avg_rent', 'avg_pyeong2', 'count_deposit']]
                df_display.columns = ['매물유형', '평균보증금(만원)', '평균월세(만원)', '평균면적(평)', '매물수(건)']
                
                # 숫자 포맷팅
                df_display['평균보증금(만원)'] = df_display['평균보증금(만원)'].apply(lambda x: f"{x:,.0f}")
                df_display['평균월세(만원)'] = df_display['평균월세(만원)'].apply(lambda x: f"{x:,.0f}")
                df_display['매물수(건)'] = df_display['매물수(건)'].apply(lambda x: f"{x:,.0f}")
                
                st.dataframe(df_display, use_container_width=True)
                
                # 매물 유형별 비교 차트
                st.markdown("### 📈 매물 유형별 비교 차트")
                
                charts = st.session_state.data_analyzer.create_region_type_comparison_chart(selected_region)
                if charts:
                    # 컨테이너 고정 크기로 차트 안정성 확보
                    chart_container = st.container()
                    with chart_container:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.plotly_chart(charts['deposit_by_type'], use_container_width=True, config={'responsive': True})
                        with col2:
                            st.plotly_chart(charts['rent_by_type'], use_container_width=True, config={'responsive': True})
                    
                    st.plotly_chart(charts['area_count_by_type'], use_container_width=True, config={'responsive': True})


def render_ai_question_section():
    """AI 질문 섹션 렌더링 (최상단)"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 질문 입력
        user_question = st.text_area(
            "원하시는 조건을 자유롭게 입력해주세요",
            placeholder="예: 성동구에서 월세 60만원 이하, 6평 이상 매물을 5곳 추천해주세요. 추천 이유와 매물 정보도 함께 알려주세요.",
            height=100,
            key="ai_question_input"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🚀 AI 추천 받기", type="primary", use_container_width=True):
                if user_question:
                    # 질문을 채팅 히스토리에 추가
                    st.session_state.chat_history.append({
                        "role": "user", 
                        "content": user_question,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    
                    # AI 답변 생성
                    with st.spinner("🤖 AI가 매물을 분석하고 있습니다..."):
                        try:
                            response = st.session_state.rag_system.ask(user_question)
                            
                            # 답변을 채팅 히스토리에 추가
                            st.session_state.chat_history.append({
                                "role": "assistant", 
                                "content": response,
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            })
                            
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ 답변 생성 중 오류가 발생했습니다: {str(e)}")
                else:
                    st.warning("질문을 입력해주세요.")
        
        with col_btn2:
            if st.button("🗑️ 채팅 초기화", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
    
    with col2:
        # 빠른 질문 템플릿
        st.markdown("**💡 빠른 질문 템플릿**")
        
        quick_questions = [
            "월세 60만원 이하 매물 추천",
            "6평 이상 원룸 추천", 
            "한양대 근처 매물 추천",
            "신축 아파트 추천"
        ]
        
        for i, q in enumerate(quick_questions):
            if st.button(f"📝 {q}", key=f"quick_q_{i}", use_container_width=True):
                st.session_state.ai_question_input = q
                st.rerun()


def render_ai_chat_history():
    """AI 대화 히스토리 렌더링 (질문창 바로 아래)"""
    if st.session_state.chat_history:
        st.markdown("### 💬 AI 대화 히스토리")
        
        # 채팅 히스토리 표시 (최신 대화가 위로)
        for message in st.session_state.chat_history[-4:]:  # 최근 4개만 표시
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message">
                    <strong>👤 질문 ({message.get('timestamp', '')}):</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="recommendation-box">
                    <strong>🤖 AI 답변 ({message.get('timestamp', '')}):</strong><br>
                    {format_response(message["content"])}
                </div>
                """, unsafe_allow_html=True)
        
        # 더 많은 대화가 있으면 표시
        if len(st.session_state.chat_history) > 8:  # 4쌍(8개) 초과 시
            st.info(f"💡 총 {len(st.session_state.chat_history)//2}개의 대화 중 최근 4개를 표시 중입니다.")
    else:
        st.info("💡 아직 대화가 없습니다. 위에서 질문을 입력해보세요!")


def render_seongdong_overview():
    """성동구 전체 개요 렌더링"""
    
    # 성동구 전체 통계 계산
    if st.session_state.data_analyzer.raw_data is not None:
        total_data = st.session_state.data_analyzer.raw_data
        
        # 기본 통계만 표시 (평균은 매물유형별로 다르므로 제외)
        total_stats = {
            'total_count': len(total_data),
            'unique_regions': total_data['region'].nunique(),
            'property_types_count': total_data['rletTpNm'].nunique(),
            'property_types': total_data['rletTpNm'].value_counts().to_dict()
        }
        
        # 핵심 메트릭만 표시 (3개 컬럼)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("전체 매물 수", f"{total_stats['total_count']:,}건")
        with col2:
            st.metric("분석 지역 수", f"{total_stats['unique_regions']}개 동")
        with col3:
            st.metric("매물 유형 수", f"{total_stats['property_types_count']}개 유형")
        
        # 성동구 매물유형별 상세 분석 탭
        tab1, tab2 = st.tabs(["📋 상세 통계표", "📊 시각화 차트"])
        
        with tab1:
            # 매물유형별 상세 데이터 테이블
            seongdong_stats = st.session_state.data_analyzer.get_seongdong_overview_stats()
            
            if seongdong_stats is not None and not seongdong_stats.empty:
                st.markdown("#### 성동구 매물유형별 상세 통계")
                
                # 테이블 표시용 데이터 가공
                display_data = seongdong_stats.copy()
                display_data = display_data[['rletTpNm', 'avg_deposit', 'avg_rent', 'avg_pyeong2', 'count_deposit', 'min_deposit', 'max_deposit']]
                display_data.columns = ['매물유형', '평균보증금(만원)', '평균월세(만원)', '평균면적(평)', '매물수(건)', '최저보증금(만원)', '최고보증금(만원)']
                
                # 숫자 포맷팅
                for col in ['평균보증금(만원)', '평균월세(만원)', '매물수(건)', '최저보증금(만원)', '최고보증금(만원)']:
                    display_data[col] = display_data[col].apply(lambda x: f"{x:,.0f}")
                
                # 매물수 기준으로 정렬 (내림차순)
                display_data = display_data.sort_values('매물수(건)', ascending=False, key=lambda x: x.str.replace(',', '').astype(int))
                
                st.dataframe(display_data, use_container_width=True, hide_index=True)
                
                # 주요 인사이트 요약
                top_type = seongdong_stats.loc[seongdong_stats['count_deposit'].idxmax(), 'rletTpNm']
                expensive_type = seongdong_stats.loc[seongdong_stats['avg_deposit'].idxmax(), 'rletTpNm']
                
                st.markdown(f"""
                <div class="stats-card">
                    <h4>💡 주요 인사이트</h4>
                    <p>• <strong>가장 많은 매물 유형:</strong> {top_type}</p>
                    <p>• <strong>평균 보증금이 가장 높은 유형:</strong> {expensive_type}</p>
                    <p>• <strong>전체 매물 유형 수:</strong> {len(seongdong_stats)}개</p>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            # 성동구 매물유형별 시각화
            st.markdown("#### 성동구 매물유형별 시장 분석")
            
            charts = st.session_state.data_analyzer.create_seongdong_overview_charts()
            
            if charts:
                # 첫 번째 행: 보증금과 월세 비교
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(charts['deposit_by_type'], use_container_width=True, config={'responsive': True})
                with col2:
                    st.plotly_chart(charts['rent_by_type'], use_container_width=True, config={'responsive': True})
                
                # 두 번째 행: 매물 분포와 평수+매물수 복합 차트
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(charts['distribution'], use_container_width=True, config={'responsive': True})
                with col2:
                    st.plotly_chart(charts['area_count_combined'], use_container_width=True, config={'responsive': True})


def render_region_analysis_page():
    """지역 분석 페이지"""
    st.subheader("📊 지역별 부동산 시장 분석")
    
    # 지역 및 매물 유형 선택
    col1, col2, col3 = st.columns(3)
    
    regions = st.session_state.data_analyzer.get_region_list()
    
    with col1:
        selected_region = st.selectbox("분석할 지역 선택", regions)
    
    with col2:
        if selected_region:
            property_types = st.session_state.data_analyzer.get_property_types(selected_region)
            selected_types = st.multiselect("매물 유형 선택 (다중선택 가능)", property_types, default=property_types[:3] if len(property_types) >= 3 else property_types)
        else:
            selected_types = []
    
    with col3:
        comparison_regions = st.multiselect("비교할 지역들 선택", regions, default=[selected_region] if selected_region else [])
    
    if selected_region:
        # 지역 기본 정보만 표시 (평균은 매물유형별로 편차가 크므로 제거)
        all_types_stats = st.session_state.data_analyzer.get_region_type_summary(selected_region)
        if all_types_stats:
            st.markdown(f"### 🏘️ {selected_region} 지역 개요")
            
            total_properties = sum([stats['count_deposit'] for stats in all_types_stats])
            total_types = len(all_types_stats)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("총 매물 수", f"{total_properties:,}건")
            with col2:
                st.metric("매물 유형 수", f"{total_types}개 유형")
            
            st.markdown("---")
            
            # 선택된 매물 유형별 상세 분석
            if selected_types:
                st.markdown("### 🏠 매물 유형별 상세 분석")
                
                # 매물 유형별 통계 테이블
                type_stats_list = []
                for prop_type in selected_types:
                    type_info = st.session_state.data_analyzer.get_region_type_summary(selected_region, prop_type)
                    if type_info:
                        type_stats_list.append({
                            '매물유형': prop_type,
                            '평균보증금': f"{type_info['avg_deposit']:,}만원",
                            '평균월세': f"{type_info['avg_rent']:,}만원",
                            '평균면적': f"{type_info['avg_pyeong2']}평",
                            '매물수': f"{type_info['total_count']:,}건",
                            '보증금범위': f"{type_info['price_range']['deposit_min']:,}~{type_info['price_range']['deposit_max']:,}만원"
                        })
                
                if type_stats_list:
                    import pandas as pd
                    df_types = pd.DataFrame(type_stats_list)
                    st.dataframe(df_types, use_container_width=True)
                
                # 매물 유형별 비교 차트
                st.markdown("### 📈 매물 유형별 비교 차트")
                
                charts = st.session_state.data_analyzer.create_region_type_comparison_chart(selected_region, selected_types)
                if charts:
                    # 안정적인 차트 렌더링을 위한 컨테이너 사용
                    chart_container = st.container()
                    with chart_container:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.plotly_chart(charts['deposit_by_type'], use_container_width=True, config={'responsive': True})
                        with col2:
                            st.plotly_chart(charts['rent_by_type'], use_container_width=True, config={'responsive': True})
                    
                    st.plotly_chart(charts['area_count_by_type'], use_container_width=True, config={'responsive': True})
            
            st.markdown("---")
            
            # 가격 분포 차트
            st.markdown("### 📊 가격 분포 분석")
            charts = st.session_state.data_analyzer.create_price_distribution_chart(selected_region)
            if charts:
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(charts['deposit_dist'], use_container_width=True)
                with col2:
                    st.plotly_chart(charts['rent_dist'], use_container_width=True)
    
    # 지역 비교 분석
    if len(comparison_regions) > 1:
        st.markdown("---")
        st.subheader("🔄 지역 간 비교 분석")
        
        # 지역별 요약 통계 테이블
        comparison_stats = []
        for region in comparison_regions:
            # 지역별 매물유형 통계로 기본 정보 계산
            region_types = st.session_state.data_analyzer.get_region_type_summary(region)
            if region_types:
                total_properties = sum([stats['count_deposit'] for stats in region_types])
                total_types = len(region_types)
                most_popular_type = max(region_types, key=lambda x: x['count_deposit'])['rletTpNm'] if region_types else 'N/A'
                
                comparison_stats.append({
                    '지역': region,
                    '총매물수': f"{total_properties:,}건",
                    '매물유형수': f"{total_types}개 유형",
                    '인기유형': most_popular_type
                })
        
        if comparison_stats:
            st.markdown("#### 📋 지역별 기본 비교")
            import pandas as pd
            df_comparison = pd.DataFrame(comparison_stats)
            st.dataframe(df_comparison, use_container_width=True)
        
        # 참고: 지역별 전체 평균 비교는 매물유형별 편차가 크므로 
        # 각 지역의 매물유형별 상세 통계를 확인하시기 바랍니다.
        st.info("💡 지역별 정확한 비교를 위해서는 각 지역의 '매물 유형별 상세 통계'를 확인해주세요.")


def render_dashboard_page():
    """대시보드 페이지"""
    st.subheader("🏠 부동산 시장 대시보드")
    
    # 전체 시장 개요
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("전체 지역 수", len(st.session_state.data_analyzer.get_region_list()))
    with col2:
        st.metric("시스템 상태", "온라인" if st.session_state.system_initialized else "오프라인")
    with col3:
        st.metric("캐시 상태", "활성" if st.session_state.get('rag_system') else "비활성")
    with col4:
        st.metric("총 대화 수", len(st.session_state.chat_history) // 2)
    
    st.markdown("---")
    
    # 최근 활동
    st.subheader("📈 최근 활동")
    
    if st.session_state.chat_history:
        recent_questions = [msg["content"] for msg in st.session_state.chat_history if msg["role"] == "user"][-5:]
        
        for i, question in enumerate(reversed(recent_questions), 1):
            st.markdown(f"**{i}.** {question[:100]}{'...' if len(question) > 100 else ''}")
    else:
        st.info("아직 질문이 없습니다. AI 매물 추천을 시작해보세요!")


def render_system_settings_page():
    """시스템 설정 페이지"""
    st.subheader("⚙️ 시스템 설정")
    
    # RAG 시스템 관리
    st.markdown("### 🤖 RAG 시스템 관리")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.system_initialized:
            st.success("✅ RAG 시스템 활성")
            
            if st.button("🔄 시스템 재시작"):
                st.session_state.system_initialized = False
                st.session_state.rag_system = None
                st.success("시스템이 재설정되었습니다.")
                st.rerun()
        else:
            st.warning("⏳ RAG 시스템 비활성")
            
            if st.button("🚀 시스템 시작"):
                with st.spinner("시스템을 시작하는 중..."):
                    try:
                        rag_system = EstateRAGSystem()
                        rag_system.setup()
                        st.session_state.rag_system = rag_system
                        st.session_state.system_initialized = True
                        st.success("✅ 시스템이 시작되었습니다!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 시스템 시작 실패: {str(e)}")
    
    with col2:
        if st.session_state.system_initialized and hasattr(st.session_state, 'rag_system'):
            cache_info = st.session_state.rag_system.get_cache_info()
            
            if cache_info.get("exists", False):
                st.info(f"💾 캐시 크기: {cache_info.get('size_mb', 'N/A')} MB")
                
                if st.button("🗑️ 캐시 삭제"):
                    st.session_state.rag_system.clear_cache()
                    st.success("캐시가 삭제되었습니다.")
                    st.rerun()
                    
                if st.button("🔄 캐시 재구축"):
                    with st.spinner("캐시를 재구축하는 중..."):
                        st.session_state.rag_system.rebuild_vectorstore()
                    st.success("캐시가 재구축되었습니다!")
                    st.rerun()
            else:
                st.info("💾 캐시 없음")
    
    st.markdown("---")
    
    # 채팅 관리
    st.markdown("### 💬 채팅 관리")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("총 대화 수", len(st.session_state.chat_history) // 2)
        
        if st.button("🗑️ 채팅 내역 삭제"):
            st.session_state.chat_history = []
            st.success("채팅 내역이 삭제되었습니다.")
            st.rerun()
    
    with col2:
        if st.session_state.chat_history:
            last_chat = st.session_state.chat_history[-1].get("timestamp", "N/A")
            st.metric("마지막 대화", last_chat)


if __name__ == "__main__":
    main()
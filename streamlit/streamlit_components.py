"""
Streamlit UI 컴포넌트들
"""

import streamlit as st
from streamlit_utils import format_response


def setup_page_config():
    """Streamlit 페이지 설정"""
    st.set_page_config(
        page_title="부동산 RAG 시스템",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 커스텀 CSS
    st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    
    .stChat > div {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .user-message {
        background-color: #e3f2fd !important;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background-color: #f1f8e9 !important;
        border-left: 4px solid #4caf50;
    }
    
    .sample-question {
        background-color: #fff3e0;
        border: 1px solid #ffcc02;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        cursor: pointer;
    }
    
    .sample-question:hover {
        background-color: #ffe0b2;
    }
    
    .status-box {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.header("📋 시스템 정보")
        
        # 시스템 상태
        if st.session_state.system_initialized:
            st.success("✅ 시스템 준비 완료")
        else:
            st.warning("⏳ 시스템 대기 중")
        
        st.markdown("---")
        
        # 사용 통계
        st.subheader("📊 사용 통계")
        st.metric("총 질문 수", len(st.session_state.chat_history) // 2)
        
        if st.session_state.chat_history:
            st.metric("마지막 질문 시간", 
                     st.session_state.chat_history[-1].get("timestamp", "N/A"))
        
        st.markdown("---")
        
        # 설정
        st.subheader("⚙️ 설정")
        
        # 응답 형식 설정
        response_style = st.selectbox(
            "응답 스타일",
            ["상세형", "간단형", "목록형"],
            key="response_style"
        )
        
        # 검색 결과 수 설정
        max_results = st.slider(
            "최대 검색 결과 수",
            min_value=3,
            max_value=10,
            value=5,
            key="max_results"
        )
        
        st.markdown("---")
        
        # 캐시 관리
        st.subheader("💾 캐시 관리")
        
        if st.session_state.system_initialized:
            # 캐시 정보 표시
            cache_info = st.session_state.rag_system.get_cache_info()
            
            if cache_info.get("exists", False):
                st.success("✅ 벡터스토어 캐시 활성")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("크기", f"{cache_info.get('size_mb', 'N/A')} MB")
                with col2:
                    st.metric("수정일", cache_info.get('modified_time', 'N/A')[-8:] if cache_info.get('modified_time') else 'N/A')
                
                # 캐시 관리 버튼들
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 캐시 재구축", help="벡터스토어를 새로 생성합니다"):
                        with st.spinner("벡터스토어를 재구축하는 중..."):
                            st.session_state.rag_system.rebuild_vectorstore()
                        st.success("캐시가 재구축되었습니다!")
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ 캐시 삭제", help="저장된 벡터스토어를 삭제합니다"):
                        st.session_state.rag_system.clear_cache()
                        st.session_state.system_initialized = False
                        st.session_state.rag_system = None
                        st.success("캐시가 삭제되었습니다!")
                        st.rerun()
            else:
                st.info("ℹ️ 캐시 없음")
        else:
            st.info("시스템 초기화 후 이용 가능")
        
        st.markdown("---")
        
        # 도움말
        st.subheader("❓ 도움말")
        with st.expander("사용법"):
            st.markdown("""
            1. **시스템 초기화**: 먼저 'RAG 시스템 초기화' 버튼을 클릭하세요.
            2. **질문하기**: 부동산 관련 질문을 입력하세요.
            3. **샘플 질문**: 오른쪽의 샘플 질문들을 클릭해서 사용할 수 있습니다.
            4. **캐시 활용**: 두 번째 실행부터는 저장된 벡터스토어를 빠르게 로드합니다.
            """)
        
        with st.expander("팁"):
            st.markdown("""
            - 구체적인 조건을 포함해서 질문하세요 (월세, 면적, 지역 등)
            - "추천해줘", "알려줘" 등의 요청 형태로 질문하세요
            - 여러 조건을 조합해서 질문할 수 있습니다
            - 첫 초기화는 시간이 걸리지만, 이후부터는 빠르게 로드됩니다
            - 데이터가 업데이트되면 '캐시 재구축'을 사용하세요
            """)


def render_chat_interface():
    """채팅 인터페이스 렌더링"""
    st.subheader("💬 질문하기")
    
    # 채팅 히스토리 표시
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(f'<div class="user-message">{message["content"]}</div>', 
                              unsafe_allow_html=True)
                else:
                    formatted_content = format_response(message["content"])
                    st.markdown(f'<div class="assistant-message">{formatted_content}</div>', 
                              unsafe_allow_html=True)
    
    # 새 질문 입력
    if prompt := st.chat_input("부동산 관련 질문을 입력해주세요..."):
        # 사용자 메시지 추가
        st.session_state.chat_history.append({
            "role": "user", 
            "content": prompt,
            "timestamp": st.session_state.get("current_time", "")
        })
        
        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.markdown(f'<div class="user-message">{prompt}</div>', 
                       unsafe_allow_html=True)
        
        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("답변을 생성하는 중..."):
                try:
                    # RAG 시스템으로 답변 생성
                    response = st.session_state.rag_system.ask(prompt)
                    
                    # 응답 포맷팅
                    formatted_response = format_response(response)
                    
                    # 응답 표시
                    st.markdown(f'<div class="assistant-message">{formatted_response}</div>', 
                               unsafe_allow_html=True)
                    
                    # 채팅 히스토리에 추가
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": response,
                        "timestamp": st.session_state.get("current_time", "")
                    })
                    
                except Exception as e:
                    error_msg = f"❌ 답변 생성 중 오류가 발생했습니다: {str(e)}"
                    st.error(error_msg)
                    
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": error_msg,
                        "timestamp": st.session_state.get("current_time", "")
                    })


def render_system_status():
    """시스템 상태 렌더링"""
    st.markdown("""
    <div class="status-box">
        <h3>🤖 RAG 시스템 준비</h3>
        <p>부동산 데이터를 분석하고 질문에 답변하기 위해 시스템을 초기화해야 합니다.</p>
        <p><strong>초기화 과정:</strong></p>
        <ul style="text-align: left; display: inline-block;">
            <li>📄 부동산 데이터 로딩</li>
            <li>✂️ 텍스트 분할 처리</li>
            <li>🧮 벡터 임베딩 생성</li>
            <li>🔍 검색 시스템 구축</li>
            <li>🤖 AI 모델 준비</li>
        </ul>
        <p><em>처음 실행 시 1-2분 정도 소요될 수 있습니다.</em></p>
    </div>
    """, unsafe_allow_html=True)


def display_sample_questions():
    """샘플 질문 표시"""
    st.subheader("💡 샘플 질문")
    
    sample_questions = [
        "월세 60만원 이하, 6평 이상 매물을 추천해주세요.",
        "성수동 지역의 아파트 매물을 알려주세요.",
        "전용면적 20평 이상인 오피스텔을 찾아주세요.",
        "보증금 5000만원 이하인 매물이 있나요?",
        "한양대학교 근처의 월세 매물을 추천해주세요.",
        "남향이면서 월세 50만원 이하인 매물을 찾아주세요."
    ]
    
    for i, question in enumerate(sample_questions):
        if st.button(f"Q{i+1}", key=f"sample_q_{i}", help=question):
            # 샘플 질문을 채팅 입력란에 설정
            st.session_state.sample_question = question
            
        st.markdown(f"""
        <div class="sample-question">
            {question}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 채팅 히스토리 관리
    if st.button("🗑️ 채팅 내역 삭제"):
        st.session_state.chat_history = []
        st.success("채팅 내역이 삭제되었습니다.")
        st.rerun()
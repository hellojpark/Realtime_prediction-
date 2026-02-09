"""
Streamlit 앱 설정
"""

import streamlit as st
from pathlib import Path

# 앱 설정
APP_CONFIG = {
    "page_title": "부동산 RAG 시스템",
    "page_icon": "🏠",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# 색상 테마
COLORS = {
    "primary": "#2196f3",
    "secondary": "#4caf50", 
    "accent": "#ffcc02",
    "background": "#f8f9fa",
    "surface": "#ffffff",
    "error": "#f44336",
    "warning": "#ff9800",
    "success": "#4caf50",
    "info": "#2196f3"
}

# 메시지 스타일
MESSAGE_STYLES = {
    "user": {
        "background": "#e3f2fd",
        "border_color": "#2196f3"
    },
    "assistant": {
        "background": "#f1f8e9",
        "border_color": "#4caf50"
    },
    "system": {
        "background": "#fff3e0", 
        "border_color": "#ffcc02"
    }
}

# UI 텍스트
UI_TEXT = {
    "title": "🏠 부동산 RAG 시스템",
    "subtitle": "AI 기반 부동산 매물 추천 시스템",
    "chat_placeholder": "부동산 관련 질문을 입력해주세요...",
    "system_init_button": "🚀 RAG 시스템 초기화",
    "system_reset_button": "🔄 시스템 재초기화",
    "clear_chat_button": "🗑️ 채팅 내역 삭제",
    "export_chat_button": "📤 채팅 내역 내보내기"
}

# 샘플 질문
SAMPLE_QUESTIONS = [
    {
        "category": "조건별 검색",
        "questions": [
            "월세 60만원 이하, 6평 이상 매물을 추천해주세요.",
            "보증금 5000만원 이하인 매물이 있나요?",
            "전용면적 20평 이상인 오피스텔을 찾아주세요."
        ]
    },
    {
        "category": "지역별 검색", 
        "questions": [
            "성수동 지역의 아파트 매물을 알려주세요.",
            "한양대학교 근처의 월세 매물을 추천해주세요.",
            "성동구에서 가장 저렴한 매물을 찾아주세요."
        ]
    },
    {
        "category": "특성별 검색",
        "questions": [
            "남향이면서 월세 50만원 이하인 매물을 찾아주세요.",
            "신축 건물의 매물을 추천해주세요.",
            "주차 가능한 매물이 있나요?"
        ]
    }
]

# 도움말 텍스트
HELP_TEXT = {
    "usage_guide": """
    ### 📖 사용법
    
    1. **시스템 초기화**: 먼저 'RAG 시스템 초기화' 버튼을 클릭하세요.
    2. **질문하기**: 부동산 관련 질문을 입력하세요.
    3. **샘플 질문**: 제공된 샘플 질문들을 참고하세요.
    4. **결과 확인**: AI가 생성한 추천 결과를 확인하세요.
    """,
    
    "tips": """
    ### 💡 효과적인 질문 팁
    
    - **구체적인 조건 포함**: 월세, 면적, 지역 등
    - **명확한 요청**: "추천해줘", "알려줘" 등
    - **복합 조건**: 여러 조건을 조합해서 질문
    - **우선순위 명시**: 가장 중요한 조건을 먼저 언급
    
    ### 🎯 질문 예시
    - "성수동에서 월세 70만원 이하 원룸 추천해줘"
    - "한양대 도보 10분 거리, 보증금 3000만원 이하 매물"
    - "남향이고 20평 이상인 아파트 매물 있나요?"
    """,
    
    "data_info": """
    ### 📊 데이터 정보
    
    현재 시스템은 다음 정보를 포함합니다:
    - **지역**: 성동구 일대 (한양대학교 인근)
    - **매물 유형**: 아파트, 원룸, 오피스텔 등
    - **거래 유형**: 월세, 전세, 매매
    - **상세 정보**: 면적, 층수, 방향, 가격 등
    
    모든 데이터는 실제 부동산 사이트에서 수집된 정보입니다.
    """
}

# 시스템 메시지
SYSTEM_MESSAGES = {
    "initializing": "🔄 RAG 시스템을 초기화하는 중입니다...",
    "loading_documents": "📄 부동산 데이터를 로딩하는 중...",
    "creating_embeddings": "🧮 텍스트 임베딩을 생성하는 중...",
    "building_vectorstore": "🔍 벡터 데이터베이스를 구축하는 중...",
    "preparing_model": "🤖 AI 모델을 준비하는 중...",
    "system_ready": "✅ 시스템이 준비되었습니다!",
    "generating_response": "💭 답변을 생성하는 중...",
    "error_occurred": "❌ 오류가 발생했습니다"
}

# 경로 설정
PATHS = {
    "rag_modules": Path(__file__).parent.parent / "rag",
    "data_dir": Path(__file__).parent.parent / "estate_data",
    "logs_dir": Path(__file__).parent / "logs"
}
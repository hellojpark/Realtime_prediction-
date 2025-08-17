"""
Streamlit 유틸리티 함수들
"""

import streamlit as st
import re
from datetime import datetime
from typing import Dict, Any


def initialize_session_state():
    """세션 상태 초기화"""
    
    # RAG 시스템 관련
    if "rag_system" not in st.session_state:
        st.session_state.rag_system = None
    
    if "system_initialized" not in st.session_state:
        st.session_state.system_initialized = False
    
    # 채팅 관련
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "sample_question" not in st.session_state:
        st.session_state.sample_question = ""
    
    # 설정 관련
    if "response_style" not in st.session_state:
        st.session_state.response_style = "상세형"
    
    if "max_results" not in st.session_state:
        st.session_state.max_results = 5
    
    # 현재 시간 업데이트
    st.session_state.current_time = datetime.now().strftime("%H:%M:%S")


def check_system_ready() -> bool:
    """시스템 준비 상태 확인"""
    return (
        st.session_state.system_initialized and 
        st.session_state.rag_system is not None
    )


def format_response(response: str) -> str:
    """응답 텍스트 포맷팅"""
    
    # 응답 스타일에 따른 포맷팅
    response_style = st.session_state.get("response_style", "상세형")
    
    if response_style == "간단형":
        # 간단형: 첫 번째 문단만 표시
        paragraphs = response.split('\n\n')
        response = paragraphs[0] if paragraphs else response
    
    elif response_style == "목록형":
        # 목록형: 번호나 불릿 포인트 강조
        response = enhance_list_format(response)
    
    # 기본 포맷팅 적용
    formatted_response = apply_basic_formatting(response)
    
    return formatted_response


def apply_basic_formatting(text: str) -> str:
    """기본 텍스트 포맷팅 적용"""
    
    # 매물명을 굵게 표시
    text = re.sub(r'\*\*(매물 이름:[^*]+)\*\*', r'**\1**', text)
    text = re.sub(r'(매물 이름:\s*[^\n]+)', r'**\1**', text)
    
    # 월세, 보증금 등 중요 정보 강조
    text = re.sub(r'(월세:\s*[^\n]+)', r'💰 **\1**', text)
    text = re.sub(r'(보증금:\s*[^\n]+)', r'💳 **\1**', text)
    text = re.sub(r'(중개하는 부동산 이름:\s*[^\n]+)', r'🏢 **\1**', text)
    
    # 숫자 패턴 강조 (만원 단위)
    text = re.sub(r'(\d+만\s*원)', r'**\1**', text)
    
    # 추천 이유 강조
    text = re.sub(r'(추천 이유:\s*[^\n]+)', r'✅ *\1*', text)
    
    return text


def enhance_list_format(text: str) -> str:
    """목록 형식 강화"""
    
    # 숫자 목록 강조
    text = re.sub(r'^(\d+\.\s)', r'📍 **\1**', text, flags=re.MULTILINE)
    
    # 불릿 포인트 추가
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('매물 이름:'):
            formatted_lines.append(f"🏠 **{line}**")
        elif line.startswith('월세:'):
            formatted_lines.append(f"💰 {line}")
        elif line.startswith('보증금:'):
            formatted_lines.append(f"💳 {line}")
        elif line.startswith('추천 이유:'):
            formatted_lines.append(f"✅ {line}")
        elif line.startswith('중개하는 부동산'):
            formatted_lines.append(f"🏢 {line}")
        else:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)


def get_chat_statistics() -> Dict[str, Any]:
    """채팅 통계 계산"""
    
    chat_history = st.session_state.get("chat_history", [])
    
    total_messages = len(chat_history)
    user_messages = len([msg for msg in chat_history if msg["role"] == "user"])
    assistant_messages = len([msg for msg in chat_history if msg["role"] == "assistant"])
    
    return {
        "total_messages": total_messages,
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "conversation_count": user_messages
    }


def export_chat_history() -> str:
    """채팅 히스토리를 텍스트로 내보내기"""
    
    chat_history = st.session_state.get("chat_history", [])
    
    if not chat_history:
        return "채팅 내역이 없습니다."
    
    export_text = "=== 부동산 RAG 시스템 채팅 내역 ===\n\n"
    export_text += f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    export_text += f"총 대화 수: {len(chat_history) // 2}\n\n"
    
    for i, message in enumerate(chat_history):
        role = "사용자" if message["role"] == "user" else "AI"
        timestamp = message.get("timestamp", "")
        
        export_text += f"[{timestamp}] {role}:\n"
        export_text += f"{message['content']}\n\n"
        export_text += "-" * 50 + "\n\n"
    
    return export_text


def validate_api_key() -> bool:
    """API 키 유효성 검증"""
    import os
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return False
    
    if not api_key.startswith("sk-"):
        return False
    
    if len(api_key) < 40:
        return False
    
    return True


def format_error_message(error: Exception) -> str:
    """에러 메시지 포맷팅"""
    
    error_str = str(error)
    
    # OpenAI API 관련 에러
    if "api" in error_str.lower() or "openai" in error_str.lower():
        return """
        ❌ **OpenAI API 오류가 발생했습니다**
        
        가능한 원인:
        - API 키가 잘못되었거나 만료됨
        - API 사용량 한도 초과
        - 네트워크 연결 문제
        
        해결 방법:
        1. .env 파일의 OPENAI_API_KEY 확인
        2. API 키 유효성 및 잔액 확인
        3. 네트워크 연결 상태 확인
        """
    
    # 파일 관련 에러
    elif "file" in error_str.lower() or "path" in error_str.lower():
        return """
        ❌ **파일 접근 오류가 발생했습니다**
        
        가능한 원인:
        - CSV 데이터 파일을 찾을 수 없음
        - 파일 권한 문제
        
        해결 방법:
        1. 데이터 파일 경로 확인
        2. 파일 존재 여부 확인
        3. 파일 접근 권한 확인
        """
    
    # 메모리 관련 에러
    elif "memory" in error_str.lower():
        return """
        ❌ **메모리 부족 오류가 발생했습니다**
        
        해결 방법:
        1. 다른 프로그램 종료 후 재시도
        2. 시스템 재시작
        3. 더 작은 데이터셋 사용
        """
    
    # 기타 에러
    else:
        return f"""
        ❌ **예상치 못한 오류가 발생했습니다**
        
        오류 내용: {error_str}
        
        해결 방법:
        1. 페이지 새로고침 후 재시도
        2. 시스템 재초기화
        3. 문제가 지속되면 관리자에게 문의
        """
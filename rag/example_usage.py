"""
RAG 시스템 사용 예시
"""

from rag_system import EstateRAGSystem


def main():
    """메인 실행 함수"""
    
    # RAG 시스템 초기화 및 설정
    print("부동산 RAG 시스템을 초기화합니다...")
    rag_system = EstateRAGSystem()
    rag_system.setup()
    
    # 예시 질문들
    questions = [
        "월세 60이하, 6평 이상, 그리고 한양대학교와의 거리를 고려해서 월세 방을 5곳 추천해줘. 추천한 이유와 추천된 곳의 매물 이름, 월세, 보증금, 중개하는 부동산 이름을 같이 알려줘.",
        "성수동 지역의 아파트 중에서 보증금 5000만원 이하인 매물을 알려줘.",
        "전용면적 20평 이상인 오피스텔 매물을 추천해줘.",
        "월세 50만원 이하이고 남향인 매물이 있나요?"
    ]
    
    # 각 질문에 대해 답변 생성
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"질문 {i}: {question}")
        print('='*60)
        
        try:
            # 검색 테스트 (선택사항)
            print("\n[검색된 관련 문서들]")
            rag_system.test_retrieval(question)
            
            # 최종 답변 생성
            print("\n[AI 답변]")
            response = rag_system.ask(question)
            print(response)
            
        except Exception as e:
            print(f"오류 발생: {e}")
        
        print("\n" + "-"*60)


if __name__ == "__main__":
    main()
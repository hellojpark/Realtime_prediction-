"""
RAG 시스템 통합 모듈
"""

import os
from dotenv import load_dotenv

from document_loader import EstateDocumentLoader
from text_processor import TextProcessor
from vector_store import VectorStoreManager
from rag_chain import RAGChain

# .env 파일에서 환경변수 로드
load_dotenv()


class EstateRAGSystem:
    """부동산 RAG 시스템 통합 클래스"""
    
    def __init__(self, csv_path: str = None):
        """
        Args:
            csv_path: CSV 파일 경로 (None이면 기본값 사용)
        """
        self.csv_path = csv_path
        self.document_loader = None
        self.text_processor = None
        self.vector_store_manager = None
        self.rag_chain = None
        
    def setup(self, force_rebuild: bool = False):
        """RAG 시스템 전체 설정
        
        Args:
            force_rebuild: True이면 캐시를 무시하고 새로 구축
        """
        print("=== RAG 시스템 설정 시작 ===")
        
        # 벡터스토어 매니저 초기화
        self.vector_store_manager = VectorStoreManager()
        
        # 캐시 확인
        cache_info = self.vector_store_manager.get_cache_info()
        
        if cache_info["exists"] and not force_rebuild:
            print(f"📦 기존 벡터스토어 캐시 발견!")
            print(f"   - 경로: {cache_info.get('path', 'N/A')}")
            print(f"   - 크기: {cache_info.get('size_mb', 'N/A')} MB")
            print(f"   - 수정일: {cache_info.get('modified_time', 'N/A')}")
            
            # 캐시된 벡터스토어 로드
            print("\n🚀 저장된 벡터스토어를 로드하는 중...")
            self.vector_store_manager.load_or_create_vectorstore()
            
        else:
            if force_rebuild:
                print("🔄 강제 재구축 모드: 새로운 벡터스토어를 생성합니다...")
            else:
                print("📦 캐시된 벡터스토어가 없습니다. 새로 생성합니다...")
                
            # 1. 문서 로드
            print("\n1. 문서 로딩...")
            self.document_loader = EstateDocumentLoader(self.csv_path) if self.csv_path else EstateDocumentLoader()
            documents = self.document_loader.load_documents()
            
            # 2. 텍스트 분할
            print("\n2. 텍스트 분할...")
            self.text_processor = TextProcessor()
            split_documents = self.text_processor.split_documents(documents)
            
            # 3. 벡터스토어 생성 및 저장
            print("\n3. 벡터스토어 생성 및 저장...")
            if force_rebuild:
                self.vector_store_manager.clear_cache()
            self.vector_store_manager.load_or_create_vectorstore(split_documents)
        
        # 4. RAG 체인 생성
        print("\n4. RAG 체인 생성...")
        retriever = self.vector_store_manager.get_retriever()
        self.rag_chain = RAGChain(retriever)
        
        print("\n=== RAG 시스템 설정 완료 ===")
        
        # 최종 캐시 정보 출력
        final_cache_info = self.vector_store_manager.get_cache_info()
        if final_cache_info["exists"]:
            print(f"💾 벡터스토어 캐시: {final_cache_info.get('size_mb', 'N/A')} MB")
    
    def ask(self, question: str) -> str:
        """
        질문하기
        
        Args:
            question: 질문 문자열
            
        Returns:
            str: 생성된 답변
        """
        if self.rag_chain is None:
            raise ValueError("RAG 시스템이 설정되지 않았습니다. setup()을 먼저 호출하세요.")
            
        return self.rag_chain.invoke(question)
    
    def test_retrieval(self, question: str):
        """검색 테스트"""
        if self.rag_chain is None:
            raise ValueError("RAG 시스템이 설정되지 않았습니다. setup()을 먼저 호출하세요.")
            
        self.rag_chain.test_retrieval(question)
    
    def rebuild_vectorstore(self):
        """벡터스토어 강제 재구축"""
        print("🔄 벡터스토어를 재구축합니다...")
        self.setup(force_rebuild=True)
    
    def clear_cache(self):
        """벡터스토어 캐시 삭제"""
        if self.vector_store_manager:
            self.vector_store_manager.clear_cache()
        else:
            print("벡터스토어 매니저가 초기화되지 않았습니다.")
    
    def get_cache_info(self) -> dict:
        """캐시 정보 반환"""
        if self.vector_store_manager:
            return self.vector_store_manager.get_cache_info()
        else:
            return {"exists": False, "error": "벡터스토어 매니저가 초기화되지 않았습니다."}


if __name__ == "__main__":
    # 사용 예시
    rag_system = EstateRAGSystem()
    rag_system.setup()
    
    # 테스트 질문
    test_question = ("월세 60이하, 6평 이상, 그리고 한양대학교와의 거리를 고려해서 월세 방을 5곳 추천해줘. "
                    "추천한 이유와 추천된 곳의 매물 이름, 월세, 보증금, 중개하는 부동산 이름을 같이 알려줘.")
    
    print("\n=== 질문 ===")
    print(test_question)
    
    print("\n=== 답변 ===")
    response = rag_system.ask(test_question)
    print(response)
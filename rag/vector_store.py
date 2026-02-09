"""
벡터 스토어 모듈
"""

import os
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever
from typing import List, Optional
from langchain_core.documents import Document


class VectorStoreManager:
    """벡터 스토어 관리 클래스"""
    
    def __init__(self, cache_dir: str = "vectorstore_cache"):
        """
        Args:
            cache_dir: 벡터스토어 캐시 디렉토리 경로
        """
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_path = self.cache_dir / "faiss_index"
    
    def load_or_create_vectorstore(self, documents: Optional[List[Document]] = None) -> FAISS:
        """
        저장된 벡터스토어를 로드하거나, 없으면 새로 생성
        
        Args:
            documents: 벡터화할 문서 리스트 (새로 생성할 때만 필요)
            
        Returns:
            FAISS: 로드되거나 생성된 벡터스토어
        """
        # 기존 벡터스토어가 있으면 로드
        if self.cache_path.exists():
            try:
                print("저장된 벡터스토어를 로드하는 중...")
                self.vectorstore = FAISS.load_local(
                    str(self.cache_path), 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print("✅ 벡터스토어를 성공적으로 로드했습니다!")
                return self.vectorstore
            except Exception as e:
                print(f"⚠️ 벡터스토어 로드 실패: {e}")
                print("새로운 벡터스토어를 생성합니다...")
        
        # 새로 생성
        if documents is None:
            raise ValueError("문서가 제공되지 않았습니다. 새 벡터스토어 생성을 위해 documents가 필요합니다.")
        
        print("새로운 벡터스토어를 생성하는 중...")
        self.vectorstore = FAISS.from_documents(
            documents=documents, 
            embedding=self.embeddings
        )
        
        # 저장
        self.save_vectorstore()
        print("✅ 벡터스토어가 성공적으로 생성되고 저장되었습니다!")
        
        return self.vectorstore
    
    def create_vectorstore(self, documents: List[Document]) -> FAISS:
        """
        문서로부터 FAISS 벡터스토어 생성 (호환성을 위해 유지)
        
        Args:
            documents: 벡터화할 문서 리스트
            
        Returns:
            FAISS: 생성된 벡터스토어
        """
        return self.load_or_create_vectorstore(documents)
    
    def save_vectorstore(self):
        """현재 벡터스토어를 디스크에 저장"""
        if self.vectorstore is None:
            raise ValueError("저장할 벡터스토어가 없습니다.")
        
        self.vectorstore.save_local(str(self.cache_path))
        print(f"벡터스토어가 {self.cache_path}에 저장되었습니다.")
    
    def clear_cache(self):
        """벡터스토어 캐시 삭제"""
        import shutil
        
        if self.cache_path.exists():
            shutil.rmtree(self.cache_path)
            print("벡터스토어 캐시가 삭제되었습니다.")
            self.vectorstore = None
        else:
            print("삭제할 캐시가 없습니다.")
    
    def cache_exists(self) -> bool:
        """캐시 존재 여부 확인"""
        return self.cache_path.exists()
    
    def get_cache_info(self) -> dict:
        """캐시 정보 반환"""
        if not self.cache_exists():
            return {"exists": False}
        
        try:
            # 캐시 디렉토리 크기 계산
            total_size = sum(f.stat().st_size for f in self.cache_path.rglob('*') if f.is_file())
            
            # 수정 시간
            mtime = self.cache_path.stat().st_mtime
            from datetime import datetime
            modified_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            return {
                "exists": True,
                "path": str(self.cache_path),
                "size_mb": round(total_size / (1024 * 1024), 2),
                "modified_time": modified_time
            }
        except Exception as e:
            return {"exists": True, "error": str(e)}
    
    def get_retriever(self) -> VectorStoreRetriever:
        """
        벡터스토어에서 검색기 생성
        
        Returns:
            VectorStoreRetriever: 검색기 객체
        """
        if self.vectorstore is None:
            raise ValueError("벡터스토어가 생성되지 않았습니다. create_vectorstore()를 먼저 호출하세요.")
            
        retriever = self.vectorstore.as_retriever()
        print("검색기가 성공적으로 생성되었습니다.")
        
        return retriever
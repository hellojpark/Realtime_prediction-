"""
텍스트 처리 모듈
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document

from rag_config import CHUNK_SIZE, CHUNK_OVERLAP


class TextProcessor:
    """텍스트 분할 처리 클래스"""
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        """
        Args:
            chunk_size: 청크 크기
            chunk_overlap: 청크 겹침 크기
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        문서를 청크 단위로 분할
        
        Args:
            documents: 분할할 문서 리스트
            
        Returns:
            List[Document]: 분할된 문서 리스트
        """
        split_documents = self.text_splitter.split_documents(documents)
        print(f"분할된 청크의 수: {len(split_documents)}")
        
        return split_documents
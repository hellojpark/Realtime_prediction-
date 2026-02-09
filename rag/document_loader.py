"""
문서 로딩 모듈
"""

from langchain_community.document_loaders.csv_loader import CSVLoader
from pathlib import Path
from typing import List
from langchain_core.documents import Document

from rag_config import DEFAULT_CSV_PATH, DEFAULT_ENCODING


class EstateDocumentLoader:
    """부동산 데이터 CSV 파일을 로드하는 클래스"""
    
    def __init__(self, file_path: str = DEFAULT_CSV_PATH, encoding: str = DEFAULT_ENCODING):
        """
        Args:
            file_path: CSV 파일 경로
            encoding: 파일 인코딩
        """
        self.file_path = file_path
        self.encoding = encoding
        
    def load_documents(self) -> List[Document]:
        """
        CSV 파일을 로드하여 Document 객체 리스트로 반환
        
        Returns:
            List[Document]: 로드된 문서 리스트
        """
        if not Path(self.file_path).exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.file_path}")
            
        loader = CSVLoader(file_path=self.file_path, encoding=self.encoding)
        docs = loader.load()
        
        print(f"로드된 문서 수: {len(docs)}")
        if docs:
            print(f"첫 번째 문서 예시:\n{docs[0]}")
            
        return docs
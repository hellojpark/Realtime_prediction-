"""
RAG 체인 모듈
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import VectorStoreRetriever

from rag_config import MODEL_NAME, TEMPERATURE, RAG_PROMPT_TEMPLATE


class RAGChain:
    """RAG 체인 클래스"""
    
    def __init__(self, retriever: VectorStoreRetriever):
        """
        Args:
            retriever: 문서 검색기
        """
        self.retriever = retriever
        self.prompt = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
        self.llm = ChatOpenAI(model_name=MODEL_NAME, temperature=TEMPERATURE)
        self.chain = self._create_chain()
    
    def _create_chain(self):
        """RAG 체인 생성"""
        chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm    
            | StrOutputParser()
        )
        print("RAG 체인이 성공적으로 생성되었습니다.")
        return chain
    
    def invoke(self, question: str) -> str:
        """
        질문에 대한 답변 생성
        
        Args:
            question: 질문 문자열
            
        Returns:
            str: 생성된 답변
        """
        response = self.chain.invoke(question)
        return response
    
    def test_retrieval(self, question: str):
        """
        검색 결과 테스트
        
        Args:
            question: 테스트 질문
        """
        retrieved_docs = self.retriever.invoke(question)
        print(f"검색된 문서 수: {len(retrieved_docs)}")
        for i, doc in enumerate(retrieved_docs[:3]):  # 상위 3개만 출력
            print(f"\n검색 결과 {i+1}:")
            print(doc.page_content[:200] + "...")
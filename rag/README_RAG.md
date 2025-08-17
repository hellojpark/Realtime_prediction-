# 부동산 RAG 시스템

`rag.ipynb` 노트북을 모듈화한 부동산 RAG(Retrieval-Augmented Generation) 시스템입니다.

## 파일 구조

```
├── rag_config.py          # 설정 상수 및 프롬프트 템플릿
├── document_loader.py     # CSV 문서 로딩 모듈
├── text_processor.py      # 텍스트 분할 처리 모듈
├── vector_store.py        # FAISS 벡터스토어 관리 모듈
├── rag_chain.py          # RAG 체인 구성 모듈
├── rag_system.py         # 전체 시스템 통합 모듈
├── example_usage.py      # 사용 예시
├── requirements_rag.txt  # 의존성 패키지
└── README_RAG.md        # 문서 (이 파일)
```

## 설치

```bash
pip install -r requirements_rag.txt
```

## 환경 설정

OpenAI API 키를 설정하는 방법:

### 방법 1: .env 파일 사용 (권장)
```bash
# 1. 템플릿 파일을 .env로 복사
cp env_template.txt .env

# 2. .env 파일을 편집하여 실제 API 키 입력
# OPENAI_API_KEY=your_actual_api_key_here
```

### 방법 2: 환경변수 직접 설정
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 사용법

### 기본 사용법

```python
from rag_system import EstateRAGSystem

# RAG 시스템 초기화
rag_system = EstateRAGSystem()
rag_system.setup()

# 질문하기
question = "월세 60이하, 6평 이상 매물을 추천해주세요."
answer = rag_system.ask(question)
print(answer)
```

### 커스텀 CSV 파일 사용

```python
# 다른 CSV 파일 사용
rag_system = EstateRAGSystem(csv_path="./your_estate_data.csv")
rag_system.setup()
```

### 개별 모듈 사용

```python
from document_loader import EstateDocumentLoader
from text_processor import TextProcessor
from vector_store import VectorStoreManager
from rag_chain import RAGChain

# 1. 문서 로드
loader = EstateDocumentLoader("./test_estate.csv")
documents = loader.load_documents()

# 2. 텍스트 분할
processor = TextProcessor()
split_docs = processor.split_documents(documents)

# 3. 벡터스토어 생성
vs_manager = VectorStoreManager()
vs_manager.create_vectorstore(split_docs)
retriever = vs_manager.get_retriever()

# 4. RAG 체인 실행
rag_chain = RAGChain(retriever)
answer = rag_chain.invoke("질문 내용")
```

## 주요 기능

1. **문서 로딩**: CSV 형태의 부동산 데이터를 로드
2. **텍스트 분할**: 긴 텍스트를 적절한 크기로 분할
3. **벡터화**: OpenAI 임베딩을 사용하여 텍스트를 벡터로 변환
4. **벡터 검색**: FAISS를 사용한 유사도 기반 문서 검색
5. **답변 생성**: GPT-4o를 사용하여 자연어 답변 생성

## 설정 커스터마이징

`rag_config.py` 파일에서 다음 설정들을 수정할 수 있습니다:

- `CHUNK_SIZE`: 텍스트 분할 크기 (기본값: 2000)
- `CHUNK_OVERLAP`: 청크 간 겹침 크기 (기본값: 50)
- `MODEL_NAME`: 사용할 LLM 모델 (기본값: "gpt-4o")
- `TEMPERATURE`: 모델 창의성 수준 (기본값: 0)
- `RAG_PROMPT_TEMPLATE`: 프롬프트 템플릿

## 예시 실행

```bash
python example_usage.py
```

## 데이터 형식

CSV 파일은 다음 컬럼들을 포함해야 합니다:
- `prc`: 보증금
- `rentPrc`: 월세
- `spc1`: 공급면적
- `spc2`: 전용면적
- `rletTpNm`: 매물 유형
- `region`: 지역
- `atclNm`: 매물명
- 기타 부동산 관련 정보

## 주의사항

- OpenAI API 키가 필요합니다
- 충분한 메모리가 필요합니다 (벡터스토어 생성 시)
- 인터넷 연결이 필요합니다 (OpenAI API 호출)
# 🏠 AI 부동산 분석 플랫폼

성동구 부동산 시장 데이터를 기반으로 한 **AI 매물 추천 및 분석 플랫폼**입니다.  
RAG(Retrieval-Augmented Generation) 기술과 데이터 분석을 결합하여 개인화된 부동산 매물을 추천하고 시장 분석을 제공합니다.

## 📋 프로젝트 구조

```
estate_project/
├── .env                   # 환경변수 (OpenAI API 키)
├── requirements.txt       # 통합 의존성 목록
├── README.md             # 프로젝트 가이드 (이 파일)
│
├── data_crawling/        # 네이버 부동산 데이터 크롤링
│   ├── config.py         # 크롤링 설정
│   ├── crawler.py        # 메인 크롤러
│   ├── main.py          # 실행 스크립트
│   └── utils.py         # 유틸리티 함수
│
├── estate_data/          # 수집된 부동산 데이터
│   ├── naver_region_name_estate.csv  # 메인 데이터
│   └── 기타 분석 데이터...
│
├── rag/                  # RAG 시스템 (검색 증강 생성)
│   ├── rag_config.py     # RAG 설정
│   ├── document_loader.py # 문서 로더
│   ├── text_processor.py # 텍스트 처리
│   ├── vector_store.py   # 벡터 저장소 (FAISS)
│   ├── rag_chain.py      # RAG 체인
│   ├── rag_system.py     # 통합 RAG 시스템
│   ├── example_usage.py  # 사용 예시
│   └── vectorstore_cache/ # 벡터스토어 캐시
│
└── streamlit/            # 웹 UI 애플리케이션
    ├── app.py            # 메인 Streamlit 앱
    ├── run_app.py        # 앱 실행 스크립트 (권장)
    ├── data_analytics.py # 데이터 분석 모듈
    ├── streamlit_components.py # UI 컴포넌트
    ├── streamlit_utils.py # 유틸리티 함수
    ├── config.py         # Streamlit 설정
    └── .streamlit/       # Streamlit 내부 설정
        └── config.toml
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화 (conda 권장)
conda create -n estate_recom python=3.11
conda activate estate_recom

# 통합 의존성 설치
pip install -r requirements.txt
```

### 2. OpenAI API 키 설정

프로젝트 루트에 `.env` 파일을 생성하고 OpenAI API 키를 설정하세요:

```bash
# 방법 1: .env 파일 편집 (권장)
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# 방법 2: 시스템 환경변수 설정
# Windows:
set OPENAI_API_KEY=your_openai_api_key_here

# Mac/Linux:
export OPENAI_API_KEY=your_openai_api_key_here
```

⚠️ **중요**: OpenAI API 키는 [OpenAI 플랫폼](https://platform.openai.com/api-keys)에서 발급받을 수 있습니다.

### 3. 웹 애플리케이션 실행

```bash
# 프로젝트 루트에서 실행
cd streamlit

# 방법 1: 실행 스크립트 사용 (권장 - 사전 검사 포함)
python run_app.py

# 방법 2: 직접 실행 (개발자용)
streamlit run app.py
```

### 4. 브라우저 접속

http://localhost:8501 에서 앱에 접속할 수 있습니다.

## 🎯 주요 기능

### 📊 데이터 분석
- **성동구 전체 시장 현황**: 매물유형별 상세 통계
- **지역별 분석**: 각 동별 부동산 시장 분석
- **매물유형별 비교**: 원룸, 투룸, 아파트 등 유형별 분석
- **인터랙티브 차트**: Plotly 기반 시각화

### 🤖 AI 매물 추천
- **자연어 질의**: 편리한 한국어 질문
- **맞춤형 추천**: 예산, 면적, 위치 기반 추천
- **상세한 분석**: 추천 이유와 시장 분석 제공
- **실시간 대화**: 채팅 형태의 인터랙티브 AI

### 📈 시각화 기능
- **매물 분포 차트**: 지역별, 유형별 매물 분포
- **가격 비교 차트**: 보증금, 월세 비교 분석
- **트렌드 분석**: 시장 동향 파악

## 🛠 기술 스택

- **Frontend**: Streamlit
- **AI/ML**: LangChain, OpenAI GPT-4
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Vector Database**: FAISS
- **Web Scraping**: Selenium (Playwright MCP)

## 📚 사용 예시

### AI 질문 예시:
```
"성동구에서 월세 60만원 이하, 6평 이상 원룸을 5곳 추천해주세요. 
추천 이유와 매물 정보도 함께 알려주세요."

"한양대 근처에서 신축 아파트 중에 투룸 매물을 찾고 있어요. 
보증금 1억 이하로 추천해주세요."
```

## 🔧 환경 변수

RAG 시스템 사용을 위해 다음 환경 변수가 필요합니다:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 📝 라이선스

이 프로젝트는 개인 학습 및 연구 목적으로 제작되었습니다.

## 🤝 기여

프로젝트에 기여하고 싶으시다면 Issue나 Pull Request를 열어주세요!

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 GitHub Issues를 통해 연락해주세요.
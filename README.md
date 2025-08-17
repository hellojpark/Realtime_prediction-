# 🏠 AI 부동산 분석 플랫폼

성동구 부동산 시장 데이터를 기반으로 한 AI 매물 추천 및 분석 플랫폼입니다.

## 📋 프로젝트 구조

```
estate_project/
├── data_crawling/          # 네이버 부동산 데이터 크롤링
│   ├── config.py          # 크롤링 설정
│   ├── crawler.py         # 메인 크롤러
│   ├── main.py           # 실행 스크립트
│   └── utils.py          # 유틸리티 함수
├── rag/                   # RAG 시스템 (검색 증강 생성)
│   ├── rag_config.py     # RAG 설정
│   ├── document_loader.py # 문서 로더
│   ├── text_processor.py # 텍스트 처리
│   ├── vector_store.py   # 벡터 저장소
│   ├── rag_chain.py      # RAG 체인
│   ├── rag_system.py     # 통합 RAG 시스템
│   └── requirements_rag.txt # RAG 의존성
└── streamlit/             # 웹 UI 애플리케이션
    ├── app.py            # 메인 Streamlit 앱
    ├── data_analytics.py # 데이터 분석 모듈
    ├── streamlit_components.py # UI 컴포넌트
    ├── streamlit_utils.py # 유틸리티
    ├── config.py         # Streamlit 설정
    ├── run_app.py        # 앱 실행 스크립트
    └── requirements.txt  # 의존성
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 생성 (conda 사용)
conda create -n estate_recom python=3.11
conda activate estate_recom

# 의존성 설치
pip install -r streamlit/requirements.txt
pip install -r rag/requirements_rag.txt
pip install -r requirements.txt
```

### 2. API 키 설정

```bash
# rag 폴더에 .env 파일 생성
cd rag
cp env_template.txt .env

# .env 파일에 OpenAI API 키 입력
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### 3. 웹 애플리케이션 실행

```bash
cd streamlit
python run_app.py
```

또는

```bash
streamlit run app.py
```

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
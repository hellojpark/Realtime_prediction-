"""
RAG 시스템 설정 모듈
"""

# 파일 경로 설정
DEFAULT_CSV_PATH = '../estate_data/naver_region_name_estate.csv'
DEFAULT_ENCODING = 'utf-8-sig'

# 텍스트 분할 설정
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 50

# LLM 설정
MODEL_NAME = "gpt-4o"
TEMPERATURE = 0

# 프롬프트 템플릿
RAG_PROMPT_TEMPLATE = """You are an assistant for question-answering tasks.
User the following peices of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Anser in Korean.
retrieved context includes information of Deposit(column anme 'prc'), Monthly Rent(column name 'rentPrc'),
Total Floor Area(in Korean, 공급면적. column name 'spc1'), Exclusive Use Area(in Korean, 전용면적. column name 'spc2'),
Listing type(or Housing type. It includes 'apartment, studio aparmtent, officetel etc'. column name 'rletTpNm').
District(column name 'region)'.
And also include 'prc per spc1 and spc2 (column name 'prc/spc1' and 'prc/spc2)',
'rentPrc per spc1 and spc2 (column name 'rentPrc/spc1' and 'rentPrc/spc2')'.
All data come from Real Estat Listing Website. And I extract about Seongdong-Gu list, which is closed to Hanyang University, Korea.
And all data is related to region District and Listing type.

#Question:
{question}

#Context:
{context}

#Answer:
"""
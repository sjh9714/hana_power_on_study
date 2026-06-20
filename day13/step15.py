# FAISS 버전 전체 코드
# pip install langchain-openai langchain-community langchain-core faiss-cpu

import os

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. OpenAI API Key
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# 2. Embedding Model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# 3. 데이터 준비
raw_documents = [
    "파이썬을 활용한 머신러닝과 딥러닝 실무 가이드. 데이터 전처리부터 모델 배포까지 다룹니다.",
    "자바 스프링 부트 기반의 엔터프라이즈 웹 애플리케이션 아키텍처 및 백엔드 개발.",
    "쿠버네티스와 도커를 이용한 마이크로서비스 아키텍처 구축 및 Devops 인프라 실무.",
    "시간 흐름에 따른 데이터 분석과 LSTM, RNN 기반의 시계열 딥러닝 예측 모델링.",
    "맛있는 이탈리아 파스타 요리 레시피와 토마토 소스 숙성 비법 가이드."
]

metadatas = [
    {"category": "AI/Data", "year": 2025},
    {"category": "Backend", "year": 2024},
    {"category": "DevOps", "year": 2026},
    {"category": "AI/Data", "year": 2026},
    {"category": "Cooking", "year": 2023}
]

docs = [
    Document(page_content=text, metadata=meta)
    for text, meta in zip(raw_documents, metadatas)
]

# 4. FAISS 인덱스 생성
print(">> FAISS 인덱싱 중...")

vector_store = FAISS.from_documents(
    documents=docs,
    embedding=embedding_model
)

print(">> 인덱싱 완료!\n")

# 5. 로컬 경로에 저장
vector_store.save_local("./my_faiss_db")

print(">> 저장 완료\n")

# 6. 검색
query_text = "컨테이너 기반의 클라우드 배포 인프라를 공식 공부하고 싶어"

print(f"🔍 질문: {query_text}")
print("-" * 50)

results = vector_store.similarity_search_with_score(
    query_text,
    k=2
)

# 7. 결과 출력
for i, (doc, score) in enumerate(results):
    print(f"[순위 {i+1}]")
    print(f"거리 점수 : {score:.4f}")
    print(f"카테고리 : {doc.metadata['category']}")
    print(f"발행년도 : {doc.metadata['year']}")
    print(f"내용 : {doc.page_content}")
    print("-" * 50)
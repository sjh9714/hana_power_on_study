import os
import chromadb
from openai import OpenAI

# -----------------------------------
# OpenAI Client
# -----------------------------------

client_openai = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# -----------------------------------
# ChromaDB
# -----------------------------------

client_chroma = chromadb.PersistentClient(
    path="./my_native_openai_db"
)

collection = client_chroma.get_or_create_collection(
    name="book_recommendation_native"
)

# -----------------------------------
# 원본 문서
# -----------------------------------

documents = [
    "파이썬을 활용한 머신러닝과 딥러닝 실무 가이드. 데이터 전처리부터 모델 배포까지 다룹니다.",
    "자바 스프링 부트 기반의 엔터프라이즈 웹 애플리케이션 아키텍처 및 백엔드 개발.",
    "쿠버네티스와 도커를 이용한 마이크로서비스 아키텍처 구축 및 DevOps 인프라 실무.",
    "시간 흐름에 따른 데이터 분석과 LSTM, RNN 기반의 시계열 딥러닝 예측 모델링.",
    "맛있는 이탈리아 파스타 요리 레시피와 토마토 소스 숙성 비법 가이드."
]

ids = [
    "book_01",
    "book_02",
    "book_03",
    "book_04",
    "book_05"
]

metadatas = [
    {"category": "AI/Data", "year": 2025},
    {"category": "Backend", "year": 2024},
    {"category": "DevOps", "year": 2026},
    {"category": "AI/Data", "year": 2026},
    {"category": "Cooking", "year": 2023}
]

# -----------------------------------
# OpenAI Embedding 생성
# -----------------------------------

print("임베딩 생성 중...")

response = client_openai.embeddings.create(
    model="text-embedding-3-large",
    input=documents
)

embeddings = [
    item.embedding
    for item in response.data
]

print("임베딩 완료")

# -----------------------------------
# Chroma 저장
# -----------------------------------

collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings
)

print("저장 완료")

query_text = "컨테이너 기반의 클라우드 인프라를 공부하고 싶어"

# 질문에 대한 Embedding 객체를 OpenAI로 사용하여 생성
query_embedding = (
    client_openai.embeddings.create(
        model="text-embedding-3-large",
        input=query_text
    )
    .data[0]
    .embedding
)

# 질문 Embedding 객체를 사용하여 Chroma 검색
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print("\n검색 결과")

for i in range(len(results["documents"][0])):
    doc = results['documents'][0][i]
    doc_id = results['ids'][0][i]
    meta = results['metadatas'][0][i]
    distance = results['distances'][0][i]  # 거리가 가까울수록(작을수록) 유사도가 높음
    
    print(f"[순위 {i+1}] ID: {doc_id} (거리 점수: {distance:.4f})")
    print(f"카테고리: {meta['category']} / 발행년도: {meta['year']}")
    print(f"내용 요약: {doc}")
    print("-" * 50)


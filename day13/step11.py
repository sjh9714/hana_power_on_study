# pip install langchain-openai langchain-chroma langchain-core
# 
import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings  # OpenAI 임베딩 모듈 임포트

# 1. OpenAI API 키 설정 (환경 변수 또는 직접 입력)
# 시스템 환경 변수에 이미 등록되어 있다면 이 라인은 생략 가능합니다.
#os.environ["OPENAI_API_KEY"] = "자신의 OPENAI_API_KEY"

# 2. 임베딩 모델 정의 (OpenAI text-embedding-3-large 활용)
# 기본적으로 text-embedding-3-large 모델은 3072 차원의 벡터를 생성합니다.
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# 3. 데이터 준비 (랭체인 규격인 Document 객체 형태로 변환)
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

# 4. 크로마DB 생성 및 데이터 인덱싱
print(">> 데이터를 벡터 데이터베이스에 인덱싱하는 중...")
vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    collection_name="book_recommendation_openai",  # 모델이 바뀌었으므로 컬렉션 이름을 새로 지정하는 것이 좋습니다.
    persist_directory="./my_langchain_openai_db"    # 새로운 DB 저장 경로
)
print(">> 인덱싱 완료!\n")


# 5. 유사도 검색 수행
query_text = "컨테이너 기반의 클라우드 배포 인프라를 공식 공부하고 싶어"

print(f"🔍 유저 질문: '{query_text}'")
print("-" * 50)

results = vector_store.similarity_search_with_score(query_text, k=2)

# 6. 결과 출력
for i, (doc, score) in enumerate(results):
    print(f"[순위 {i+1}] (거리 점수: {score:.4f})")
    print(f"카테고리: {doc.metadata.get('category')} / 발행년도: {doc.metadata.get('year')}")
    print(f"내용 요약: {doc.page_content}")
    print("-" * 50)
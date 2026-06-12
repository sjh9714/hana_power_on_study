# pip install langchain-chroma langchain-community langchain-core sentence-transformers
# 1. 랭체인과 크로마DB 임포트

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. 임베딩 모델 정의 (HuggingFace의 오픈소스 모델 활용)
# 앞서 chromadb가 내부적으로 다운로드했던 'all-MiniLM-L6-v2' 모델을 랭체인 규격으로 선언합니다.
# 이 모델 역시 로컬 캐시에 저장되므로 외부 API 비용이 들지 않습니다.
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. 데이터 준비 (랭체인 규격인 Document 객체 형태로 변환)
# 텍스트 내용(page_content)과 메타데이터(metadata)를 하나의 객체로 묶습니다.
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

# List Comprehension을 사용하여 Document 객체 리스트 생성
docs = [
    Document(page_content=text, metadata=meta) 
    for text, meta in zip(raw_documents, metadatas)
]

# 3. 크로마DB 생성 및 데이터 인덱싱 (VectorStore 인터페이스 구현체 사용)
# 기존 PersistentClient와 collection 설정을 from_documents() 메서드 하나로 통합 처리합니다.
print(">> 데이터를 벡터 데이터베이스에 인덱싱하는 중...")
vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    collection_name="book_recommendation",
    persist_directory="./my_langchain_db"  # 로컬 영구 저장 경로
)
print(">> 인덱싱 완료!\n")


# 4. 유사도 검색 수행 (VectorStore 표준 인터페이스 활용)
query_text = "컨테이너 기반의 클라우드 배포 인프라를 공식 공부하고 싶어"

print(f"🔍 유저 질문: '{query_text}'")
print("-" * 50)

# 구조화된 유사도 검색 호출 (가장 유사한 상위 2개 문서 요청)
# 검색 결과로 랭체인의 Document 객체와 거리(Distance) 점수가 튜플 형태로 반환됩니다.
results = vector_store.similarity_search_with_score(query_text, k=2)

# 5. 결과 출력
for i, (doc, score) in enumerate(results):
    print(f"[순위 {i+1}] (거리 점수: {score:.4f})")
    print(f"카테고리: {doc.metadata.get('category')} / 발행년도: {doc.metadata.get('year')}")
    print(f"내용 요약: {doc.page_content}")
    print("-" * 50)
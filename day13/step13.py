# pip install langchain-google-genai langchain-chroma langchain-core
# 
import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # 추천받은 올바른 이름 사용
from google import genai

# 1. Gemini API 키 설정 (환경 변수 또는 직접 입력)
#client = genai.Client(
#    api_key=os.environ["GOOGLE_API_KEY"]
#)

# 모델 리스트 출력 (사용 가능한 모델 확인용)
#for model in client.models.list():
#    print(model.name)

# 1. Gemini API 키 설정 (환경 변수 또는 직접 입력)
# 구글 AI 스튜디오(Google AI Studio)에서 발급받은 API 키를 입력합니다.
#os.environ["GOOGLE_API_KEY"] = "자신의 GOOGLE_API_KEY 입력"

# 2. 임베딩 모델 정의 (Google text-embedding-004 활용)
# model 인자에 사용할 모델명을 정확히 적어줍니다.
embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

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
    collection_name="book_recommendation_google",  # 구글 모델용 컬렉션 이름 변경
    persist_directory="./my_langchain_google_db"    # 구글 모델용 새로운 DB 저장 경로
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
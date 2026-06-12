import chromadb

# 1. 크로마DB 클라이언트 생성 (데이터를 파일로 저장할 경로 지정)
# 데이터를 휘발시키지 않고 './my_chroma_db' 폴더에 영구 보관합니다.
client = chromadb.PersistentClient(path="./my_chroma_db")

# 2. 컬렉션(Collection) 생성 또는 가져오기
# RDBMS의 테이블(Table)에 해당하는 개념입니다.
collection = client.get_or_create_collection(name="book_recommendation")

# 3. 데이터 준비 (도서 요약 정보)
# 문서 데이터, 각 문서의 고유 ID, 검색 필터링을 위한 메타데이터를 준비합니다.
documents = [
    "파이썬을 활용한 머신러닝과 딥러닝 실무 가이드. 데이터 전처리부터 모델 배포까지 다룹니다.",
    "자바 스프링 부트 기반의 엔터프라이즈 웹 애플리케이션 아키텍처 및 백엔드 개발.",
    "쿠버네티스와 도커를 이용한 마이크로서비스 아키텍처 구축 및 Devops 인프라 실무.",
    "시간 흐름에 따른 데이터 분석과 LSTM, RNN 기반의 시계열 딥러닝 예측 모델링.",
    "맛있는 이탈리아 파스타 요리 레시피와 토마토 소스 숙성 비법 가이드."
]

ids = ["book_01", "book_02", "book_03", "book_04", "book_05"]

metadatas = [
    {"category": "AI/Data", "year": 2025},
    {"category": "Backend", "year": 2024},
    {"category": "DevOps", "year": 2026},
    {"category": "AI/Data", "year": 2026},
    {"category": "Cooking", "year": 2023}
]

# 4. 컬렉션에 데이터 추가
# 따로 임베딩 모델을 지정하지 않으면 내장된 SentenceTransformer 모델이 
# 자동으로 텍스트를 고차원 벡터로 변환(임베딩)하여 저장합니다.
print(">> 데이터를 벡터 데이터베이스에 인덱싱하는 중...")
collection.add(
    documents=documents,
    ids=ids,
    metadatas=metadatas
)
print(">> 인덱싱 완료!\n")


# 5. 유사도 검색 수행 (Semantic Search)
# 사용자는 구체적인 단어 대신 '의미적 맥락'으로 질문을 던집니다.
query_text = "컨테이너 기반의 클라우드 배포 인프라를 공부하고 싶어"

print(f"🔍 유저 질문: '{query_text}'")
print("-" * 50)

# 쿼리 전송 (가장 유사한 상위 2개의 결과를 요청)
results = collection.query(
    query_texts=[query_text],
    n_results=2
)

# 6. 결과 출력
for i in range(len(results['documents'][0])):
    doc = results['documents'][0][i]
    doc_id = results['ids'][0][i]
    meta = results['metadatas'][0][i]
    distance = results['distances'][0][i]  # 거리가 가까울수록(작을수록) 유사도가 높음
    
    print(f"[순위 {i+1}] ID: {doc_id} (거리 점수: {distance:.4f})")
    print(f"카테고리: {meta['category']} / 발행년도: {meta['year']}")
    print(f"내용 요약: {doc}")
    print("-" * 50)
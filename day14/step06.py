from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

##############################################################################
# 설정 정보
##############################################################################

# ChromaDB Collection 이름
COLLECTION_NAME = "pdf_collection"

# ChromaDB가 저장된 디렉토리
PERSIST_DIRECTORY = "./chroma_db"

# 문장을 벡터로 변환할 임베딩 모델
EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

##############################################################################
# 임베딩 모델 생성
##############################################################################

def get_embedding_model():
    """
    HuggingFace 임베딩 모델 생성

    역할:
        텍스트를 숫자 벡터(Vector)로 변환

    예)
        "스마트 농업"
            ↓
        [0.123, 0.456, 0.789, ...]

    Retriever는 질문과 문서를 같은 벡터 공간으로 변환한 후
    유사도를 계산하여 검색을 수행한다.
    """

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

##############################################################################
# Chroma Vector DB 로드
##############################################################################

def load_vector_store():
    """
    이미 생성된 ChromaDB를 로드

    ChromaDB 내부 구조

    ChromaDB
    ├── 문서 Chunk
    ├── Embedding Vector
    └── Metadata

    Retriever는 이 Vector DB를 이용하여 검색한다.
    """

    embedding_model = get_embedding_model()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model
    )

    return vector_store

##############################################################################
# Retriever 생성
##############################################################################

def create_retriever():
    """
    Retriever 객체 생성

    search_type="similarity"

        질문과 가장 유사한 문서를 검색

    k=3

        상위 3개 문서를 반환

    반환 형태

        List[Document]
    """

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 3
        }
    )

    return retriever

##############################################################################
# Retriever 검색
##############################################################################

def search(query):
    """
    Retriever를 이용한 검색

    입력:
        사용자 질문

    예)
        "노지 스마트농업 시범사업이 무엇인가?"

    처리 과정

        질문
            ↓
        Embedding 생성
            ↓
        ChromaDB 검색
            ↓
        상위 3개 문서 반환

    반환 형태

        [
            Document(...),
            Document(...),
            Document(...)
        ]
    """

    retriever = create_retriever()

    return retriever.invoke(query)

##############################################################################
# 점수(score)까지 확인하는 검색
##############################################################################

def search_with_score(query, k=3):
    """
    Retriever 대신 ChromaDB를 직접 사용

    similarity_search_with_score()

    반환 형태

        [
            (Document, score),
            (Document, score),
            (Document, score)
        ]

    score 의미

        Chroma는 Distance 값을 반환

        값이 작을수록 유사도가 높음

        예)

        0.12 ← 매우 유사
        0.35 ← 유사
        0.78 ← 관련성 낮음
        1.20 ← 거의 무관
    """

    vector_store = load_vector_store()

    return vector_store.similarity_search_with_score(
        query,
        k=k
    )

##############################################################################
# 실행 테스트
##############################################################################

# 사용자 질문
query = "농작물 재배관리 의사결정에 대해 알려줘"

# 검색 수행
docs = search_with_score(query)

print(f"질문: {query}")

##############################################################################
# 검색 결과 출력
##############################################################################

for idx, (doc, score) in enumerate(docs):

    print("=" * 80)

    print(f"검색 결과 #{idx+1}")

    print(f"유사도 거리(score): {score:.4f}")

    print(f"페이지 번호: {doc.metadata.get('page')}")

    print(f"파일명: {doc.metadata.get('source')}")

    print("\n[문서 내용 일부]\n")

    print(doc.page_content[:300])

    print("\n")
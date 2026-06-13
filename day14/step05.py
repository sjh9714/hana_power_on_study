import re
import unicodedata
from pathlib import Path

from langchain_chroma import Chroma

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

##############################################################################
# 설정
##############################################################################

COLLECTION_NAME = "pdf_collection"

PERSIST_DIRECTORY = "./chroma_db"

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


##############################################################################
# PDF 읽기
##############################################################################

def load_pdf(pdf_path: str):
    """
    PDF 파일 로드

    Returns:
        List[Document]
    """

    loader = PyMuPDFLoader(pdf_path)

    documents = loader.load()

    print(f"페이지 수 : {len(documents)}")

    return documents


##############################################################################
# 텍스트 정제
##############################################################################

def clean_text(text: str) -> str:
    """
    PDF 텍스트 정제

    처리 항목
    ----------
    1. Unicode 정규화
    2. 제어문자 제거
    3. 특수 공백 제거
    4. 연속 공백 제거
    5. 연속 줄바꿈 제거
    6. 페이지 번호 제거
    """

    # Unicode 정규화
    text = unicodedata.normalize("NFKC", text)

    # 제어문자 제거
    text = "".join(
        ch
        for ch in text
        if not unicodedata.category(ch).startswith("C")
        or ch in ["\n", "\t", "\r"]
    )

    # 특수 공백 제거
    text = text.replace("\u00A0", " ")
    text = text.replace("\u200B", "")

    # 연속 공백 제거
    text = re.sub(r"[ \t]+", " ", text)

    # 연속 줄바꿈 제거
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

##############################################################################
# 페이지별 전처리
##############################################################################

def preprocess_documents(documents):

    cleaned_documents = []

    for doc in documents:

        doc.page_content = clean_text(
            doc.page_content
        )

        cleaned_documents.append(doc)

    return cleaned_documents


##############################################################################
# Chunk 생성
##############################################################################

def create_chunks(
    documents,
    chunk_size=1000,
    chunk_overlap=100
):
    """
    Chunk 생성
    """

    # RecursiveCharacterTextSplitter를 사용하여 문서를 청크로 분할합니다.
    # 한글처리 `다. 요.`  로 끝나는 부분에 분할을 하는 것이 좋습니다
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "다.",
            "요.",
            " ",
            ""
        ]
    )

    # 문서를 청크로 분할합니다.
    chunks = splitter.split_documents(documents)

    print(f"[INFO] Chunk 수 : {len(chunks)}")

    return chunks


##############################################################################
# 전체 파이프라인
##############################################################################

def process_pdf(
    pdf_path,
    chunk_size=1000,
    chunk_overlap=100
):
    """
    PDF -> Clean -> Chunk
    """

    # PDF 읽기
    documents = load_pdf(pdf_path)

    # PDF 전체 전처리 (병합 + 정제)
    documents = preprocess_documents(documents)

    # Chunk 생성
    chunks = create_chunks(
        documents,
        chunk_size,
        chunk_overlap
    )

    return chunks


##############################################################################
# 임베딩 모델
##############################################################################

def get_embedding_model():
    # HuggingFaceEmbeddings를 사용하여 지정된 모델로 임베딩 객체를 생성합니다.
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


##############################################################################
# Chroma 저장
##############################################################################

def save_to_chroma(chunks):

    # 임베딩 모델 객체를 생성합니다.
    embedding_model = get_embedding_model()

    # Chroma.from_documents() 메서드를 사용하여 청크 리스트를 Chroma 벡터 데이터베이스에 저장합니다.
    vector_store = Chroma.from_documents(
        documents=chunks,           # 청크 리스트 (각 청크는 Document 객체)
        embedding=embedding_model,  # 임베딩 모델 객체 (HuggingFaceEmbeddings)
        collection_name=COLLECTION_NAME,    # Chroma 컬렉션 이름 (COLLECTION_NAME)
        persist_directory=PERSIST_DIRECTORY # Chroma 데이터베이스가 저장될 디렉토리 경로 (PERSIST_DIRECTORY)
    )

    return vector_store


##############################################################################
# 전체 파이프라인
##############################################################################
# PDF -> Clean -> Chunk
# PDF을 읽고, 텍스트를 정제한 후, 청크로 분할하는 전체 파이프라인을 실행합니다.
# 결과로 생성된 청크 리스트는 이후 임베딩 및 벡터 데이터베이스 저장에 사용됩니다.
def build_vector_store(pdf_path):

    # PDF 읽기
    documents = load_pdf(pdf_path)

    # PDF 전체 전처리 (병합 + 정제)
    documents = preprocess_documents(documents)
    
    # Chunk 생성
    chunks = create_chunks(documents)

    # Chroma 저장
    save_to_chroma(chunks)

    print(
        f"총 {len(chunks)}개 Chunk 저장 완료"
    )


##############################################################################
# 실행
##############################################################################
# PDF 파일 경로를 지정하여 전체 파이프라인을 실행합니다.
PDF_PATH = "data/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축.pdf"

build_vector_store(PDF_PATH)
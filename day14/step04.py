import re
import unicodedata

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


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
# 실행 예제
##############################################################################
PDF_PATH = "data/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축.pdf"

chunks = process_pdf(
    pdf_path=PDF_PATH,
    chunk_size=1000,
    chunk_overlap=100
)

print("\n===== 첫 번째 Chunk =====\n")

print(chunks[0].page_content[:1000])

print("\n===== Metadata =====\n")

for chunk in chunks:
    print(chunk.metadata)
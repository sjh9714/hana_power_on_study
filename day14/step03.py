# PDF 로딩을 위해 필요한 패키지 설치
# pip install langchain langchain-community pymupdf langchain-text-splitters

# LangChain Community 패키지에서 PDF Loader를 가져옵니다.
# PyMuPDFLoader는 PyMuPDF(fitz)를 사용하여 PDF를 읽습니다.
from langchain_community.document_loaders import PyMuPDFLoader

# 문서를 일정 크기의 청크(Chunk)로 분할하기 위한 Text Splitter를 가져옵니다.
from langchain_text_splitters import RecursiveCharacterTextSplitter

# -----------------------------------------------------------------------------
# 1. PDF 파일 로드
# -----------------------------------------------------------------------------

# PDF 파일을 읽기 위한 Loader 객체를 생성합니다.
# 지정한 PDF 파일의 내용을 LangChain Document 객체로 변환합니다.
loader = PyMuPDFLoader(
    "data/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축.pdf"
)

# PDF를 읽어 Document 객체 리스트로 반환합니다.
# PDF가 20페이지라면 Document 객체도 20개 생성됩니다.
documents = loader.load()

# PDF 페이지 수 확인
print(f"페이지 수: {len(documents)}")

# -----------------------------------------------------------------------------
# 2. Text Splitter 생성
# -----------------------------------------------------------------------------

# RecursiveCharacterTextSplitter 생성
#
# chunk_size:
#   하나의 청크에 포함될 최대 문자 수
#
# chunk_overlap:
#   이전 청크와 다음 청크가 공유할 문자 수
#
# overlap을 사용하는 이유:
# 문장이 청크 경계에서 잘릴 경우 문맥(Context)이 끊어지는 것을 방지
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 청크 최대 크기
    chunk_overlap=200     # 청크 간 중복 영역
)

# -----------------------------------------------------------------------------
# 3. 문서 분할 (Chunking)
# -----------------------------------------------------------------------------

# PDF 전체 문서를 여러 개의 청크로 분할합니다.
#
# 예)
# 원본 문서
#   10,000자
#
# 결과
#   Chunk1 (1000자)
#   Chunk2 (1000자)
#   Chunk3 (1000자)
#   ...
#
# 이렇게 분할된 청크는 이후 Embedding 및 Vector DB 저장에 사용됩니다.
chunks = splitter.split_documents(documents)

# -----------------------------------------------------------------------------
# 4. 결과 확인
# -----------------------------------------------------------------------------

# 생성된 청크 개수 출력
print(f"청크 개수: {len(chunks)}")

# 첫 번째 청크 내용 일부 출력
print("\n===== 첫 번째 청크 =====")
print(chunks[0].page_content[:500])

# 첫 번째 청크 메타데이터 출력
print("\n===== 메타데이터 =====")
print(chunks[0].metadata)
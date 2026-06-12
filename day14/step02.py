# pip install langchain langchain-community pymupdf

# LangChain Community 패키지에서 PDF 로더를 가져옵니다.
from langchain_community.document_loaders import PyMuPDFLoader

# PDF 파일을 읽기 위한 Loader 객체를 생성합니다.
# "data/sample.pdf" 경로의 PDF 파일을 대상으로 합니다.
loader = PyMuPDFLoader("data/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축.pdf")

# PDF 파일을 로드합니다.
# 각 페이지가 Document 객체로 변환되어 리스트 형태로 반환됩니다.
documents = loader.load()

# Document 객체 개수 확인 (PDF 페이지 수와 동일)
print(f"PDF 페이지 = {len(documents)}\n")

# 첫 번째 페이지의 메타데이터 확인
print(f"메타데이터: {documents[0].metadata}\n")

# 첫 번째 페이지(인덱스 0)의 텍스트 내용을 출력합니다.
# page_content 속성에는 해당 페이지에서 추출된 텍스트가 저장됩니다.
print(f"텍스트 내용: {documents[0].page_content}")
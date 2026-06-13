from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 샘플 텍스트 준비 (긴 문서라고 가정)
sample_text = """
Large Language Models (LLMs) are incredibly powerful tools for natural language processing.
They can generate essays, write code, and summarize complex texts.

However, to use them effectively with personal documents, we need Retrieval-Augmented Generation (RAG).
RAG allows us to fetch relevant documents and inject them into the LLM's prompt context.

This process requires splitting documents into smaller, meaningful pieces called 'chunks'.
Using the right text splitter ensures that semantic meaning is preserved across boundaries.
"""

# 2. Splitter 객체 생성
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,       # 하나의 청크는 최대 150자 내외
    chunk_overlap=30,     # 청크 간에 30자는 서로 겹치도록 설정
    length_function=len,  # 글자 수 기준 계산
    separators=["\n\n", "\n", " ", ""] # 분할 기준 순서
)

# 3. 텍스트 분할 실행
# 문자열을 바로 쪼갤 때는 split_text를 사용합니다.
chunks = text_splitter.split_text(sample_text)

# 4. 결과 확인
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} (Length: {len(chunk)}) ---")
    print(chunk)
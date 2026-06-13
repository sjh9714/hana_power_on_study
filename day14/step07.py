from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

import os

##############################################################################
# 설정
##############################################################################

COLLECTION_NAME = "pdf_collection"
PERSIST_DIRECTORY = "./chroma_db"

EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

##############################################################################
# Embedding
##############################################################################

def get_embedding_model():

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

##############################################################################
# Vector Store
##############################################################################

def load_vector_store():

    embedding_model = get_embedding_model()

    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model
    )

##############################################################################
# Retriever
##############################################################################

def search(query, k=3):

    vector_store = load_vector_store()

    return vector_store.similarity_search(
        query,
        k=k
    )

##############################################################################
# LLM
##############################################################################

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

##############################################################################
# RAG
##############################################################################

def ask_pdf(query):

    ####################################################
    # 1. Retriever 검색
    ####################################################

    docs = search(query)

    ####################################################
    # 2. Context 생성
    ####################################################

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    ####################################################
    # 3. 페이지 정보 추출
    ####################################################

    pages = sorted(
        list(
            set(
                doc.metadata.get("page")
                for doc in docs
            )
        )
    )

    page_text = ", ".join(
        str(page)
        for page in pages
    )

    ####################################################
    # 4. Prompt 생성
    ####################################################

    prompt = f"""
당신은 스마트농업 전문가입니다.

반드시 제공된 문서 내용만 사용하여 답변하세요.

문서:
{context}

질문:
{query}

답변 작성 규칙:

1. 문서에 있는 내용만 사용한다.
2. 문서에 없는 내용은 추측하지 않는다.
3. 핵심 내용을 요약한다.
4. 문서에 없는 경우
   "문서에서 찾을 수 없습니다."
   라고 답변한다.
5. 답변 마지막에 참고 페이지를 표시한다.

참고 페이지:
{page_text}
"""

    ####################################################
    # 5. LLM 호출
    ####################################################

    response = llm.invoke(prompt)

    return response.content

##############################################################################
# 실행
##############################################################################

query = "농작물 재배관리 의사결정에 대해 알려줘"

answer = ask_pdf(query)

print(answer)


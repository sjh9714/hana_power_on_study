COLLECTION_NAME = "pdf_collection"

# ChromaDB에 저장된 문서에서 검색할 때 사용할 키입니다. 일반적으로 "text"로 설정하여, 문서의 텍스트 내용을 검색하도록 합니다.
PERSIST_DIRECTORY = "./data/chroma_db"

# 문서 임베딩에 사용할 모델입니다. "sentence-transformers/all-MiniLM-L6-v2"는 문서의 의미를 벡터로 변환하는 데 사용되는 사전 학습된 모델입니다. 
# 이 모델을 사용하여 문서의 의미를 벡터로 변환하고, 이를 기반으로 유사한 문서를 검색할 수 있습니다.   
EMBEDDING_MODEL = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

TOP_K = 3

DEFAULT_TEMPERATURE = 0.7

MODEL_CONFIG = {

    "GPT-4.1 Mini": {
        "provider": "openai",
        "model": "gpt-4.1-mini"
    },

    "Gemini 2.5 Flash": {
        "provider": "gemini",
        "model": "gemini-2.5-flash"
    }

}

CHATBOT_TITLE = "스마트농업 RAG 챗봇"
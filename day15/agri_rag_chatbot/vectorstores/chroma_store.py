from langchain_chroma import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from day15.agri_rag_chatbot.config.settings import *

# Chroma DB에 저장된 벡터 스토어를 로드하는 함수입니다. 이 함수는 Chroma DB에 연결하여, 지정된 컬렉션에서 벡터 스토어를 로드합니다. 
# 이렇게 로드된 벡터 스토어는 문서 임베딩과 검색 기능을 제공하는 객체입니다. 
# 이후 get_retriever() 함수에서 이 벡터 스토어를 사용하여 리트리버 객체를 생성할 때 활용됩니다.
# load_vector_store() 함수에서는 HuggingFaceEmbeddings를 사용하여 임베딩 모델을 설정하고, Chroma 객체를 생성하여 벡터 스토어를 로드합니다.
def load_vector_store():
    """
    Chroma DB 연결
    """
    
    embedding_model = (
        HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )
    )

    return Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model
    )
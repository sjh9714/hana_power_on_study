from langchain_chroma import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from day15.retrievers_refactoring.config.settings import *

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
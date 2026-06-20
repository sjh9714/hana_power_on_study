from day15.retrievers_refactoring.vectorstores.chroma_store import (
    load_vector_store
)

def get_retriever():

    vector_store = (
        load_vector_store()
    )

    return vector_store.as_retriever(
        search_kwargs={
            "k": 3
        }
    )
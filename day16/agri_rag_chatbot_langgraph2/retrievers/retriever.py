from config.settings import TOP_K
from vectorstores.chroma_store import (
    load_vector_store
)

# get_retriever() 함수는 ChromaDB에 저장된 문서에서 검색할 때 사용할 리트리버 객체를 생성하여 반환하는 역할을 합니다.

# load_vector_store() 함수를 사용하여 ChromaDB에 저장된 벡터 스토어를 로드합니다. 이렇게 로드된 벡터 스토어는 문서 임베딩과 검색 기능을 제공하는 객체입니다.
def get_retriever():

    vector_store = (
        load_vector_store()
    )

    return vector_store.as_retriever(
        search_kwargs={
            "k": TOP_K  # TOP_K는 config/settings.py 파일에서 정의된 상수로, 검색 시 반환할 유사한 문서의 개수를 지정하는 값입니다.
                        # 일반적으로 3과 같은 값이 사용됩니다. 이렇게 설정함으로써, 
                        # 검색 결과로 반환되는 문서의 수를 제한하여, 모델이 보다 관련성 높은 문서에 집중하여 응답을 생성할 수 있도록 합니다.
        }
    )
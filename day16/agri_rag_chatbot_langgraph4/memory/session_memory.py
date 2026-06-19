from langchain_core.chat_history import (
    InMemoryChatMessageHistory
)

# 세션 메모리를 관리하는 모듈입니다. 세션 메모리는 각 사용자의 대화 히스토리를 저장하고 관리하는 역할을 합니다.
store = {}

# get_session_history() 함수는 세션 ID를 입력으로 받아서, 해당 세션의 대화 히스토리를 반환하는 역할을 합니다.
def get_session_history(session_id):
    
    # 세션 ID가 store 딕셔너리에 존재하지 않는 경우, 새로운 InMemoryChatMessageHistory 객체를 생성하여 해당 세션 ID에 할당합니다. 이렇게 함으로써, 각 세션마다 고유한 대화 히스토리를 관리할 수 있도록 합니다.
    if session_id not in store: 
        # InMemoryChatMessageHistory는 langchain_core 라이브러리에서 제공하는 클래스입니다. 이 클래스는 메모리에 대화 메시지를 저장하는 역할을 합니다. 각 세션마다 InMemoryChatMessageHistory 객체를 생성하여, 해당 세션의 대화 히스토리를 관리할 수 있도록 합니다. 
        store[session_id] = (InMemoryChatMessageHistory())

    # 세션 ID에 해당하는 대화 히스토리를 반환합니다. 이렇게 반환된 대화 히스토리는 이후 체인 실행 시 참조되어, 사용자 질문과 모델 응답을 대화 히스토리에 저장하고 관리하는 데 사용됩니다.
    return store[session_id]

# clear_session() 함수는 세션 ID를 입력으로 받아서, 해당 세션의 대화 히스토리를 삭제하는 역할을 합니다. 이렇게 함으로써, 특정 세션의 대화 히스토리를 초기화하거나 삭제할 수 있도록 합니다.
# 세션 ID가 store 딕셔너리에 존재하는 경우, del 키워드를 사용하여 해당 세션 ID에 할당된 대화 히스토리를 삭제합니다. 이렇게 하면, 해당 세션의 대화 히스토리가 초기화되어, 
# 이후 새로운 대화가 시작될 때 빈 대화 히스토리로 시작할 수 있도록 합니다.   
def clear_session(session_id):

    if session_id in store:
        del store[session_id]
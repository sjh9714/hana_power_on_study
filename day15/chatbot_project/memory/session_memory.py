from langchain_core.chat_history import (
    InMemoryChatMessageHistory
)

store = {}

def get_session_history(session_id):

    if session_id not in store:

        store[session_id] = (
            InMemoryChatMessageHistory()
        )

    return store[session_id]


def clear_session(session_id):

    if session_id in store:
        del store[session_id]
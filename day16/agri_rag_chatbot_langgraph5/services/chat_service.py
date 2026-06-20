
from chains.router_chain import create_chain


def chat(message,           # 사용자 입력 메시지
         history,           # 대화 히스토리 (이전 메시지와 응답을 포함하는 리스트)
         selected_model,    # 사용자가 선택한 모델 (예: "GPT-4.1 Mini", "Gemini 2.5 Flash" 등)
         selected_mode,     # 사용자가 선택한 처리 방식 (예: "AUTO", "REACT", "RAG", "GPT" 등)
         session_id):       # 세션 ID (사용자 고유 상태값 관리)

    if history is None:
        history = []

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": ""})

    partial = ""

    # 모드에 관계없이 create_chain()이 적절한 체인/어댑터를 반환합니다.
    # AUTO, REACT  → ReactChainAdapter (LangGraph ReAct Agent)
    # RAG          → RAG 체인
    # GPT          → 일반 GPT 체인
    chain = create_chain(selected_model, selected_mode, message)

    for chunk in chain.stream(
        {"query": message},
        config={
            "configurable": {
                "session_id": session_id
            }
        }
    ):
        partial += str(chunk)
        history[-1]["content"] = partial
        yield history, ""

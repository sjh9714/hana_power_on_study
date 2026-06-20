
from prompts.router_prompt import router_prompt
from chains.rag_chain import create_chain as create_rag_chain
from chains.general_chain import create_chain as create_general_chain
from agents.react_rag_agent import create_graph
from llms.llm_factory import get_llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessageChunk
from memory.session_memory import get_session_history


class ReactChainAdapter:
    """
    LangGraph ReAct Agent를 chain.stream() 인터페이스로 감싸는 어댑터.
    chat_service.py가 모드 구분 없이 동일한 방식으로 스트리밍할 수 있도록 한다.
    """

    def __init__(self, selected_model):
        self.selected_model = selected_model

    def stream(self, inputs, config=None):
        session_id = (config or {}).get("configurable", {}).get("session_id", "default")
        message = inputs["query"]

        graph = create_graph(selected_model=self.selected_model, session_id=session_id)
        chat_history = get_session_history(session_id)
        messages = chat_history.messages + [HumanMessage(content=message)]

        full_answer = ""

        # stream_mode="messages" → LLM 토큰 단위로 (chunk, metadata) 스트리밍
        for chunk, _ in graph.stream(
            {
                "messages": messages,
                "session_id": session_id,
                "user_question": message,
                "final_answer": ""
            },
            stream_mode="messages"
        ):
            # LLM이 생성한 텍스트 청크만 처리 (ToolMessage 등 제외)
            if not isinstance(chunk, AIMessageChunk):
                continue
            if not chunk.content:
                continue

            full_answer += chunk.content
            yield chunk.content

        chat_history.add_user_message(message)
        chat_history.add_ai_message(full_answer)


def create_chain(selected_model, selected_mode, question=""):

    if selected_mode in ["AUTO", "REACT"]:
        return ReactChainAdapter(selected_model)

    llm = get_llm(selected_model)

    if selected_mode == "GPT":
        return create_general_chain(llm)

    if selected_mode == "RAG":
        return create_rag_chain(llm)

    # 알 수 없는 모드는 router_prompt로 react/general 자동 선택
    router = router_prompt | llm | StrOutputParser()
    category = router.invoke({"query": question}).strip().lower()

    if category == "react":
        return ReactChainAdapter(selected_model)

    return create_general_chain(llm)

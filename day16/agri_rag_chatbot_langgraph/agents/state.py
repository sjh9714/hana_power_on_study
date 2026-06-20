from typing import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):

    # ReAct Agent 핵심 메모리
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

    # 원본 질문
    user_question: str

    # 최종 응답
    final_answer: str

    # 향후 확장용
    user_id: str
    session_id: str

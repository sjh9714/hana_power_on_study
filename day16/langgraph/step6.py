import os
from typing import TypedDict
from typing import Annotated
from datetime import datetime

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from typing import TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    # BaseMessage은 LangChain에서는 모든 메시지의 부모 클래스
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

llm = ChatOpenAI(
    model="gpt-4.1-mini",   
    api_key=os.getenv("OPENAI_API_KEY"), 
    temperature=0
    )

@tool
def get_time() -> str:
    """현재 시간을 반환"""
    return str(datetime.now())


@tool
def calculator(expression: str) -> str:
    """수식을 계산"""

    try:
        return str(eval(expression))
    except Exception as e:
        return str(e)


@tool
def explain_docker() -> str:
    """Docker 설명"""

    return """
Docker는 컨테이너 기반 애플리케이션
실행 플랫폼입니다.
"""


#tools 관련 함수 배열 선언 
tools = [
    get_time,
    calculator,
    explain_docker
]

# LLM에게 `이런 Tool들이 존재한다` 라고 알려주는 것입니다
llm_with_tools = llm.bind_tools(tools)


#LLM이 요청한 Tool을 실제로 실행 할 수 있는 객체를 생성합니다
tool_node = ToolNode(tools)


def agent_node(state: AgentState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# =====================================================
# Graph 생성
# =====================================================

builder = StateGraph(AgentState)

# Node 등록
builder.add_node(
    "agent",
    agent_node
)

builder.add_node(
    "tools",
    tool_node
)

builder.add_edge(
    START,
    "agent"
)

builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        "__end__": END
    }
)

builder.add_edge(
    "tools",
    "agent"
)

# Graph 컴파일
graph = builder.compile()


# =====================================================
# 실행
# =====================================================
result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="""
현재 시간을 알려주고,
100 * 200을 계산한 다음,
Docker가 무엇인지 설명해줘.
"""
            )
        ]
    }
)

print("\n===================")
print("최종 결과")
print("===================")

print(
    result["messages"][-1].content
)
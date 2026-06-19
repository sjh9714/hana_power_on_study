"""
Hybrid LangGraph Example

Workflow + ReAct Agent

START
  │
  ▼
Preprocess
  │
  ▼
Agent
  │
  ▼
tools_condition
  │
 ┌───────────────┐
 ▼               ▼
ToolNode     Postprocess
 │               │
 └────► Agent ◄──┘
                 │
                 ▼
                END
"""

import os
from datetime import datetime

from typing import TypedDict
from typing import Annotated

from langchain_openai import ChatOpenAI

from langchain_core.tools import tool
from langchain_core.messages import (
    BaseMessage,
    HumanMessage
)

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.graph.message import add_messages

from langgraph.prebuilt import (
    ToolNode
)


# =====================================================
# State
# =====================================================
#
# Workflow Node와 Agent가
# 함께 사용하는 공유 메모리
#
# =====================================================

class AgentState(TypedDict):

    # ReAct Agent의 핵심 메모리
    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

    # Workflow에서 사용할 데이터
    user_question: str

    # 최종 결과
    final_answer: str


# =====================================================
# LLM
# =====================================================

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)


# =====================================================
# Tool 정의
# =====================================================

@tool
def get_time() -> str:
    """
    현재 시간을 반환
    """

    return str(datetime.now())


@tool
def calculator(expression: str) -> str:
    """
    수식을 계산
    """

    try:
        return str(eval(expression))

    except Exception as e:
        return str(e)


@tool
def explain_docker() -> str:
    """
    Docker 설명
    """

    return """
Docker는 컨테이너 기반 애플리케이션
실행 플랫폼입니다.
"""


# =====================================================
# Tool 등록
# =====================================================

tools = [
    get_time,
    calculator,
    explain_docker
]


# =====================================================
# LLM에게 Tool 정보를 제공
# =====================================================

llm_with_tools = llm.bind_tools(
    tools
)


# =====================================================
# Tool 실행 Node
# =====================================================

tool_node = ToolNode(
    tools
)


# =====================================================
# Workflow Node #1
# =====================================================
#
# 사용자 질문 전처리
#
# =====================================================

def preprocess_node(state: AgentState):

    print("\n[Preprocess Node 실행]")

    question = state["messages"][-1].content

    print(f"질문: {question}")

    return {
        "user_question": question
    }


# =====================================================
# ReAct Agent Node
# =====================================================
#
# LLM이
#
# 1. Tool 사용 여부 판단
# 2. Tool Call 생성
# 3. 최종 답변 생성
#
# =====================================================

def agent_node(state: AgentState):

    print("\n[Agent Node 실행]")

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# =====================================================
# Workflow Node #2
# =====================================================
#
# 최종 결과 정리
#
# =====================================================

def postprocess_node(state: AgentState):

    print("\n[Postprocess Node 실행]")

    final_message = state["messages"][-1]

    return {
        "final_answer": final_message.content
    }


# =====================================================
# Conditional Router
# =====================================================
#
# Agent 결과 분석
#
# Tool 호출이 있으면
#   -> ToolNode
#
# 없으면
#   -> Postprocess
#
# =====================================================

def route_after_agent(state: AgentState):

    last_message = state["messages"][-1]

    # Tool 호출 존재
    if hasattr(last_message, "tool_calls"):

        if last_message.tool_calls:

            print(
                "\n[Router] Tool 호출 감지"
            )

            return "tools"

    print(
        "\n[Router] 최종 답변 생성 완료"
    )

    return "postprocess"


# =====================================================
# Graph 생성
# =====================================================

builder = StateGraph(
    AgentState
)


# =====================================================
# Node 등록
# =====================================================

builder.add_node(
    "preprocess",
    preprocess_node
)

builder.add_node(
    "agent",
    agent_node
)

builder.add_node(
    "tools",
    tool_node
)

builder.add_node(
    "postprocess",
    postprocess_node
)


# =====================================================
# Edge 연결
# =====================================================

builder.add_edge(
    START,
    "preprocess"
)

builder.add_edge(
    "preprocess",
    "agent"
)


# =====================================================
# Agent -> Tool 또는 Postprocess
# =====================================================

builder.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tools": "tools",
        "postprocess": "postprocess"
    }
)


# =====================================================
# Tool 실행 후 Agent 재호출
# =====================================================

builder.add_edge(
    "tools",
    "agent"
)


# =====================================================
# 종료
# =====================================================

builder.add_edge(
    "postprocess",
    END
)


# =====================================================
# Compile
# =====================================================

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
Docker가 무엇인지 설명하고,
AI에 대하여 1000자로 설명해줘.
"""
            )
        ]
    }
)


# =====================================================
# 결과 출력
# =====================================================

print("\n")
print("=" * 60)
print("최종 결과")
print("=" * 60)

print(
    result["final_answer"]
)
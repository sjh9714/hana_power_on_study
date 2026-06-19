"""
LangGraph 입문 예제

구조

START
  │
  ▼
Router
  │
  ├─────────► Time
  │
  ├─────────► Calculator
  │
  └─────────► Chat
                    │
                    ▼
                   END

router_node()의 리턴값 명이 add_node() 노드명과 같을 경우 삭제한 예제 

builder.add_conditional_edges(
    "router",
    route_function
)

"""

# TypedDict는 State 구조를 정의하기 위해 사용
from typing import TypedDict

# LangGraph 핵심 클래스
from langgraph.graph import StateGraph
from langgraph.graph import START, END

# 현재 시간 조회용
from datetime import datetime


# =====================================================
# State 정의
# =====================================================
#
# State는 모든 Node가 공유하는 메모장
#
# 예)
#
# {
#     "question": "현재 시간 알려줘",
#     "route": "",
#     "answer": ""
# }
#
# Router Node
# Time Node
# Calculator Node
#
# 모두 같은 State를 사용
#
# =====================================================

class AgentState(TypedDict):

    # 사용자 질문
    question: str

    # Router가 결정한 경로
    route: str

    # 최종 답변
    answer: str


# =====================================================
# Router Node
# =====================================================
#
# 역할
#
# 사용자의 질문을 분석하여 어느 Node로 이동할지 결정
#
# 예)
#
# "현재 시간 알려줘"
#   -> time
#
# "100 * 200"
#   -> calculator
#
# "Docker란?"
#   -> chat
#
# =====================================================

def router_node(state: AgentState):

    question = state["question"]

    # 시간 관련 질문
    if "시간" in question:

        route = "time"

    # 계산 관련 질문
    elif "+" in question or "*" in question:

        route = "calculator"

    # 그 외 일반 질문
    else:

        route = "chat"

    print(f"[Router] route = {route}")

    # State 업데이트
    return {
        "route": route
    }


# =====================================================
# Time Node
# =====================================================
#
# 현재 시간을 반환
#
# =====================================================

def time_node(state: AgentState):

    print("[Time Node 실행]")

    now = datetime.now()

    return {
        "answer": f"현재 시간은 {now}"
    }


# =====================================================
# Calculator Node
# =====================================================
#
# 간단한 계산 수행
#
# 예)
#
# 100 * 200
#
# 결과
#
# 20000
#
# =====================================================

def calculator_node(state: AgentState):

    print("[Calculator Node 실행]")

    question = state["question"]

    try:

        # 교육용 예제
        # 실제 서비스에서는 eval 사용 금지
        result = eval(question)

        return {
            "answer": f"계산 결과 : {result}"
        }

    except Exception:

        return {
            "answer": "계산 실패"
        }


# =====================================================
# Chat Node
# =====================================================
#
# 일반 질문 처리
#
# 실제 프로젝트에서는
#
# ChatOpenAI
# ChatOllama
# Gemini
#
# 등을 호출
#
# =====================================================

def chat_node(state: AgentState):

    print("[Chat Node 실행]")

    question = state["question"]

    return {
        "answer": f"일반 질문 처리 : {question}"
    }


# =====================================================
# Routing Function
# =====================================================
#
# Conditional Edge에서 사용
#
# Router가 저장한 route 값을 읽음
#
# route = time
# route = calculator
# route = chat
#
# =====================================================

def route_function(state: AgentState):

    return state["route"]


# =====================================================
# Graph 생성
# =====================================================

builder = StateGraph(AgentState)


# =====================================================
# Node 등록
# =====================================================

builder.add_node("router", router_node)

builder.add_node("time", time_node)

builder.add_node("calculator", calculator_node)

builder.add_node("chat", chat_node)


# =====================================================
# START -> Router
# =====================================================

builder.add_edge(
    START,
    "router"
)


# =====================================================
# Router 조건 분기
# =====================================================
#
# route 값에 따라 이동
#
# time       -> Time Node
# calculator -> Calculator Node
# chat       -> Chat Node
#
# =====================================================

builder.add_conditional_edges(
    "router",
    route_function
)


# =====================================================
# 각 Node 종료 후 END
# =====================================================

builder.add_edge(
    "time",
    END
)

builder.add_edge(
    "calculator",
    END
)

builder.add_edge(
    "chat",
    END
)


# =====================================================
# Graph 컴파일
# =====================================================
#
# 실제 실행 가능한 Graph 객체 생성
#
# =====================================================

graph = builder.compile()


# =====================================================
# 테스트
# =====================================================

print("\n===== 테스트1 =====")

result = graph.invoke(
    {
        "question": "현재 시간 알려줘",
        "route": "",
        "answer": ""
    }
)

print(result)

print("\n===== 테스트2 =====")

result = graph.invoke(
    {
        "question": "100 * 200",
        "route": "",
        "answer": ""
    }
)

print(result)

print("\n===== 테스트3 =====")

result = graph.invoke(
    {
        "question": "Docker란?",
        "route": "",
        "answer": ""
    }
)

print(result)
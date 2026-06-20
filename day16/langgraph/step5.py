"""
Multi Tool LangGraph Example

질문:
현재 시간을 알려주고,
100 * 200을 계산한 다음,
Docker가 무엇인지 설명해줘.

실행 흐름

START
  │
  ▼
Router
  │
  ├────► Time
  │
  ├────► Calculator
  │
  └────► Chat
          │
          ▼
       Combine
          │
          ▼
         END
"""

from typing import TypedDict, List
from datetime import datetime

from langgraph.graph import StateGraph
from langgraph.graph import START, END


# =====================================================
# State
# =====================================================
#
# 모든 Node가 공유하는 메모장
#
# =====================================================

class AgentState(TypedDict):

    # 사용자 질문
    question: str

    # 실행할 Node 목록
    routes: List[str]

    # 각 Tool 결과 저장
    time_result: str
    calc_result: str
    chat_result: str

    # 최종 답변
    answer: str


# =====================================================
# Router Node
# =====================================================
#
# 질문 분석 후
# 어떤 Tool이 필요한지 결정
#
# =====================================================

def router_node(state: AgentState):

    question = state["question"]

    routes = []

    # 시간 관련
    if "시간" in question:
        routes.append("time")

    # 계산 관련
    if "*" in question or "+" in question:
        routes.append("calculator")

    # Docker 관련
    if "Docker" in question:
        routes.append("chat")

    print(f"[Router] routes = {routes}")

    return {
        "routes": routes
    }


# =====================================================
# Time Node
# =====================================================

def time_node(state: AgentState):

    print("[Time Node 실행]")

    now = datetime.now()

    return {
        "time_result": f"현재 시간 : {now}"
    }


# =====================================================
# Calculator Node
# =====================================================
#
# 교육용 예제
#
# =====================================================

def calculator_node(state: AgentState):

    print("[Calculator Node 실행]")

    question = state["question"]

    try:

        # 예제용
        result = eval("100 * 200")

        return {
            "calc_result": f"계산 결과 : {result}"
        }

    except Exception:

        return {
            "calc_result": "계산 실패"
        }


# =====================================================
# Chat Node
# =====================================================
#
# 실제 프로젝트에서는
#
# ChatOpenAI
# ChatOllama
# Gemini
#
# 호출
#
# =====================================================

def chat_node(state: AgentState):

    print("[Chat Node 실행]")

    return {
        "chat_result":
            "Docker는 컨테이너 기반 애플리케이션 "
            "실행 플랫폼입니다."
    }


# =====================================================
# Combine Node
# =====================================================
#
# 모든 결과를 합쳐서
# 최종 Answer 생성
#
# =====================================================

def combine_node(state: AgentState):

    print("[Combine Node 실행]")

    answer = f"""
{state.get("time_result", "")}

{state.get("calc_result", "")}

{state.get("chat_result", "")}
"""

    return {
        "answer": answer
    }


# =====================================================
# Route Function
# =====================================================
#
# Router 결과에 따라
# 여러 Node 실행
#
# =====================================================

def route_function(state: AgentState):

    routes = state["routes"]

    next_nodes = []

    if "time" in routes:
        next_nodes.append("time")

    if "calculator" in routes:
        next_nodes.append("calculator")

    if "chat" in routes:
        next_nodes.append("chat")

    return next_nodes


# =====================================================
# Graph 생성
# =====================================================

builder = StateGraph(AgentState)

# Node 등록
builder.add_node("router", router_node)

builder.add_node("time", time_node)

builder.add_node("calculator", calculator_node)

builder.add_node("chat", chat_node)

builder.add_node("combine", combine_node)

# 시작
builder.add_edge(
    START,
    "router"
)

# Router → 여러 Node 분기
builder.add_conditional_edges(
    "router",
    route_function
)

# 각 Node → Combine
builder.add_edge(
    "time",
    "combine"
)

builder.add_edge(
    "calculator",
    "combine"
)

builder.add_edge(
    "chat",
    "combine"
)

# Combine → END
builder.add_edge(
    "combine",
    END
)

# Graph 컴파일
graph = builder.compile()


# =====================================================
# 실행
# =====================================================

result = graph.invoke(
    {
        "question":
            "현재 시간을 알려주고 "
            "100 * 200을 계산한 다음 "
            "Docker가 무엇인지 설명해줘.",

        "routes": [],

        "time_result": "",
        "calc_result": "",
        "chat_result": "",

        "answer": ""
    }
)

print("\n===================")
print("최종 결과")
print("===================")

print(result["answer"])
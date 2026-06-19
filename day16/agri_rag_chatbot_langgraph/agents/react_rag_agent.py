from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from agents.state import AgentState
from tools.rag_chain_tool import create_rag_tool
from llms.llm_factory import get_llm
from tools.time_tool import get_time
from tools.calculator_tool import calculator

# =====================================================
# Agent Router
# =====================================================

# 
def route_after_agent(state: AgentState):
    """
    Agent 결과 분석

    Tool 호출 존재 시
        -> tools

    최종 답변이면
        -> postprocess
    """

    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls"):

        if last_message.tool_calls:

            print(
                "\n[Router] Tool 호출 감지"
            )

            return "tools"

    print(
        "\n[Router] 최종 응답 생성"
    )

    return "postprocess"


# =====================================================
# Graph Factory
# =====================================================

def create_graph(selected_model, session_id):


    # ==========================================
    # LLM 초기화
    # ==========================================
    llm = get_llm(selected_model)

    # ==========================================
    # RAG Tool 생성
    # ==========================================
    rag_tool = create_rag_tool(
        llm=llm,
        session_id=session_id
    )

    # =====================================================
    # Tool 목록
    # =====================================================
    TOOLS = [
        rag_tool,
        get_time,
        calculator
    ]

    # ==========================================
    # Tool Binding
    # ==========================================
    llm_with_tools = llm.bind_tools(TOOLS)

    # ==========================================
    # Tool Node 생성
    # ==========================================
    tool_node = ToolNode(TOOLS)

    # ==========================================
    # 전처리
    # ==========================================

    def preprocess_node(state: AgentState):
        """
        사용자 요청 전처리

        향후

        - JWT 인증
        - 사용자 조회
        - 권한 검사
        - 요청 로그

        등을 추가할 위치
        """

        print("\n[Preprocess Node]")

        # state["messages"]의 마지막 메시지(HumanMessage)에서 질문 추출
        question = state["messages"][-1].content

        # state["user_question"] 업데이트
        return {
            "user_question": question
        }

    # ==========================================
    # Agent
    # ==========================================
    def agent_node(state: AgentState):
        """
        ReAct Agent

        역할

        1. Tool 사용 판단
        2. Tool Call 생성
        3. Tool 결과 분석
        4. 최종 답변 생성
        """

        print("\n[Agent Node]")

        # LLM 호출 (Tool Binding된 모델 사용)
        response = llm_with_tools.invoke(
            state["messages"]
        )

        return {
            "messages": [response]
        }

    # ==========================================
    # 후처리
    # ==========================================

    def postprocess_node(state: AgentState):
        """
        최종 응답 정리

        향후

        - DB 저장
        - Audit Log
        - 사용량 기록

        등을 추가할 위치
        """

        print("\n[Postprocess Node]")

        answer = state["messages"][-1].content

        return {
            "final_answer": answer
        }

    # ==========================================
    # Graph 생성
    # ==========================================

    builder = StateGraph(AgentState)

    # ==========================================
    # Node 추가, 사용할 함수 선언이라고 생각하면 됩니다
    # ==========================================
    
    # agent 전처리기 노드 등록
    builder.add_node("preprocess", preprocess_node)

    # agent 노드 등록
    builder.add_node("agent", agent_node)

    # tool 노드 등록 (ToolNode 인스턴스 사용)
    builder.add_node("tools", tool_node)

    # agent 후처리기 노드 등록
    builder.add_node("postprocess", postprocess_node)

    # ==========================================
    # START
    # ==========================================

    builder.add_edge(START, "preprocess")

    builder.add_edge("preprocess", "agent")

    # ==========================================
    # Agent → Tool/Postprocess
    # ==========================================

    builder.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            "postprocess": "postprocess"
        }
    )

    # ==========================================
    # Tool → Agent
    # ==========================================

    builder.add_edge("tools", "agent")

    # ==========================================
    # 종료
    # ==========================================

    builder.add_edge("postprocess", END)

    return builder.compile()
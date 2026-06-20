"""
rag_chain_tool.py

기존 RAG Chain 전체를
ReAct Agent Tool로 감싸는 모듈

중요

Retriever만 사용하는 것이 아니라

기존

    retriever
    rag_prompt
    memory
    llm

전체 체인을 그대로 사용한다.

이렇게 해야

- Session Memory 유지
- RAG Prompt 유지
- 문서 포맷팅 유지

가능하다.
"""

from langchain_core.tools import tool

from chains.rag_chain import create_chain


def create_rag_tool(
    llm,
    session_id: str
):
    """
    RAG Tool Factory

    Parameters
    ----------
    llm
        react_rag_agent..py 에서 생성한 LLM

    session_id
        현재 사용자 세션

    Returns
    -------
    Tool
        ReAct Agent에서 사용할 Tool
    """

    # ==========================================
    # 기존 RAG Chain 생성
    # ==========================================

    rag_chain = create_chain(
        llm
    )

    # ==========================================
    # Tool 정의
    # ==========================================

    @tool
    def rag_answer(
        question: str
    ) -> str:
        """
        농업 관련 전문 문서에서만 정보를 검색하여 답변한다.

        반드시 아래 주제에 해당할 때만 사용하세요.
        - 작물 재배 방법 (밀, 벼, 사과, 고추 등)
        - 병충해 예방 및 대처
        - 농업 의사결정 지원시스템
        - 토양, 비료, 기상 관련 농업 지식

        아래 주제에는 절대 사용하지 마세요.
        - IT 기술, 프로그래밍, 소프트웨어 (Docker, Python, Java 등)
        - 일반 상식, 과학, 역사, 문화
        - 수학 계산 (calculator 툴 사용)
        - 현재 시간 조회 (get_time 툴 사용)
        """

        print(
            "\n[RAG Tool 실행]"
        )

        try:

            result = rag_chain.invoke(
                {
                    "query": question
                },
                config={
                    "configurable": {
                        "session_id": session_id
                    }
                }
            )

            return str(result)

        except Exception as e:

            return (
                f"RAG 검색 중 오류 발생: {str(e)}"
            )

    return rag_answer
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
        농업 문서를 검색하여 답변한다.

        사용 예시

        - 사과 재배 방법 알려줘
        - 토마토 병충해 예방법 알려줘
        - 고추 재배 시 주의사항 알려줘
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
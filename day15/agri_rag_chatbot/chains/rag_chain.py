
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from day15.agri_rag_chatbot.retrievers.retriever import get_retriever
from day15.agri_rag_chatbot.prompts.rag_prompt import rag_prompt
from day15.agri_rag_chatbot.utils.document_utils import format_docs_with_pages
from day15.agri_rag_chatbot.memory.session_memory import get_session_history

# 라우터 체인 생성 함수
# create_chain() 함수는 선택된 모델과 처리 방식에 따라 적절한 체인을 생성하는 역할을 합니다.
# AUTO 모드에서는 router_prompt를 사용하여 사용자 질문을 분석하여 RAG 처리 방식이 필요한지 여부를 판단하고, 그에 따라 RAG 체인 또는 일반 GPT 체인을 생성하여 반환합니다.
# RAG 체인은 문서 검색과 LLM 응답 생성을 포함하는 복합적인 처리 방식을 구현한 체인이고, 일반 GPT 체인은 문서 검색 없이 LLM 응답 생성만을 수행하는 단순한 체인입니다.
# 라우터 체인은 router_prompt를 사용하여 사용자 질문을 분석하여 RAG 처리 방식이 필요한지 여부를 판단하는 역할을 합니다. 
# router_prompt는 LLM에게 질문의 유형을 분석하도록 지시하는 프롬프트입니다. 
# 라우터 체인은 router_prompt와 LLM, 그리고 StrOutputParser로 구성되어 있습니다.
def create_chain(llm):
    retriever = get_retriever()

    # RAG 체인 구성: 사용자 질문을 입력으로 받아서, retriever를 사용하여 관련 문서를 검색하고, rag_prompt와 LLM을 사용하여 최종 응답을 생성하는 체인입니다.
    # 체인은 RunnableLambda로 구성된 여러 단계로 이루어져 있습니다.
    # 첫 번째 단계에서는 retriever를 사용하여 사용자 질문과 관련된 문서를 검색합니다.
    # 두 번째 단계에서는 검색된 문서와 사용자 질문, 대화 히스토리를 rag_prompt에 입력으로 전달하여, LLM이 최종 응답을 생성할 수 있도록 합니다.
    # 세 번째 단계에서는 StrOutputParser를 사용하여 LLM의 응답에서 텍스트만 추출합니다.
    # 최종적으로 RunnableWithMessageHistory로 래핑하여, 대화 히스토리를 관리하면서 사용자 질문에 대한 응답을 생성할 수 있도록 합니다.
    # RunnableWithMessageHistory는 체인 실행 시마다 세션 히스토리를 참조하여, 사용자 질문과 모델 응답을 대화 히스토리에 저장하고 관리할 수 있도록 하는 래퍼입니다.
    # RunnableWithMessageHistory는 get_session_history 함수를 사용하여 세션 히스토리를 참조하고, 
    # input_messages_key와 history_messages_key를 사용하여 대화 히스토리에서 사용자 질문과 모델 응답을 관리할 수 있도록 합니다.  
    # 체인의 각 단계에서 RunnableLambda를 사용하여, 입력값을 받아서 필요한 처리를 수행하고 다음 단계로 전달하는 방식으로 체인을 구성합니다.
    # 예를 들어, 
    # 첫 번째 단계에서는 retriever.invoke(x["query"])를 사용하여 사용자 질문과 관련된 문서를 검색하고, 
    # 두 번째 단계에서는 format_docs_with_pages 함수를 사용하여 검색된 문서를 포맷팅하여 rag_prompt에 입력으로 전달하는 방식으로 체인을 구성합니다. 
    # 최종적으로 StrOutputParser를 사용하여 LLM의 응답에서 텍스트만 추출하는 단계로 체인을 구성합니다.
    # create_chain() 함수는 이렇게 구성된 RAG 체인을 반환하여, 이후 사용자 질문에 대한 응답을 생성하는 데 사용됩니다.
    chain = (
        {
            "docs": RunnableLambda(lambda x: retriever.invoke(x["query"])), # 사용자 질문과 관련된 문서를 검색하는 단계입니다. retriever.invoke() 메서드를 사용하여 사용자 질문을 입력으로 받아서 관련 문서를 검색합니다.   
            "query": RunnableLambda(lambda x: x["query"]),                  # 사용자 질문을 그대로 다음 단계로 전달하는 단계입니다. 입력값에서 "query" 키의 값을 추출하여 다음 단계로 전달합니다.
            "history": RunnableLambda(lambda x: x["history"])               # 대화 히스토리를 그대로 다음 단계로 전달하는 단계입니다. 입력값에서 "history" 키의 값을 추출하여 다음 단계로 전달합니다.
        }
        | RunnableLambda(
            lambda x: {
                # docs는 검색된 문서 리스트를 페이지 단위로 포맷팅하여 rag_prompt에 입력으로 전달할 수 있도록 가공하는 단계입니다.
                **format_docs_with_pages(x["docs"]),  
                "query": x["query"],
                "history": x["history"]
            }
        )
        | rag_prompt   # rag_prompt를 사용하여, 검색된 문서와 사용자 질문, 대화 히스토리를 LLM에 입력으로 전달하여 최종 응답을 생성하는 단계입니다. rag_prompt는 LLM에게 질문의 유형을 분석하도록 지시하는 프롬프트입니다.  
        | llm          # LLM을 사용하여 최종 응답을 생성하는 단계입니다. rag_prompt에서 가공된 입력값을 LLM에 전달하여, 최종 응답을 생성합니다.
        | StrOutputParser()  # LLM의 응답에서 텍스트만 추출하는 단계입니다. StrOutputParser를 사용하여, LLM의 응답에서 텍스트만 추출하여 최종적으로 반환합니다.
    )

    # RunnableWithMessageHistory로 체인을 래핑하여, 대화 히스토리를 관리하면서 사용자 질문에 대한 응답을 생성할 수 있도록 합니다.
    # RunnableWithMessageHistory는 체인 실행 시마다 세션 히스토리를 참조하여, 사용자 질문과 모델 응답을 대화 히스토리에 저장하고 관리할 수 있도록 하는 래퍼입니다.
    # get_session_history 함수를 사용하여 세션 히스토리를 참조하고, input_messages_key와 history_messages_key를 사용하여 대화 히스토리에서 사용자 질문과 모델 응답을 관리할 수 있도록 합니다.
    # 이렇게 래핑된 체인은 이후 사용자 질문에 대한 응답을 생성하는 데 사용됩니다.   
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="query",
        history_messages_key="history"
    )

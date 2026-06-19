
from prompts.general_prompt import general_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from memory.session_memory import get_session_history

# 일반 GPT 체인 생성 함수
# create_chain() 함수는 선택된 모델을 기반으로 일반 GPT 체인을 생성하는 역할을 합니다.
# 일반 GPT 체인은 general_prompt와 LLM, 그리고 StrOutputParser로 구성되어 있습니다.
# general_prompt는 LLM에게 일반적인 질문에 답변하도록 지시하는 프롬프트입니다.
# create_chain() 함수에서는 general_prompt와 LLM, StrOutputParser를 연결하여 체인을 생성하고, RunnableWithMessageHistory로 래핑하여 대화 히스토리를 관리할 수 있도록 합니다.
def create_chain(llm):
    chain = (
        general_prompt   # general_prompt를 사용하여, 사용자 질문에 대해 일반적인 답변을 생성하도록 LLM에 지시하는 단계입니다. general_prompt는 LLM에게 일반적인 질문에 답변하도록 지시하는 프롬프트입니다.
        | llm            # LLM을 사용하여 최종 응답을 생성하는 단계입니다. general_prompt에서 가공된 입력값을 LLM에 전달하여, 최종 응답을 생성합니다.
        | StrOutputParser() # LLM의 응답에서 텍스트만 추출하는 단계입니다. StrOutputParser를 사용하여, LLM의 응답에서 텍스트만 추출하여 최종적으로 반환합니다.
    )
    # RunnableWithMessageHistory로 체인을 래핑하여, get_session_history 함수를 사용하여 세션별 대화 히스토리를 관리할 수 있도록 합니다.
    # input_messages_key와 history_messages_key를 지정하여, 체인 실행 시 입력 메시지와 대화 히스토리를 적절히 연결할 수 있도록 합니다.
    # RunnableWithMessageHistory는 체인 실행 시마다 get_session_history 함수를 호출하여 해당 세션의 대화 히스토리를 가져오고, 체인 실행이 끝난 후에는 대화 히스토리를 업데이트하여 저장하는 역할을 합니다.
    # 이렇게 함으로써, 각 사용자는 고유한 세션 ID를 통해 자신의 대화 히스토리를 관리할 수 있고, 체인 실행 시마다 해당 히스토리를 참조하여 보다 일관된 대화 경험을 제공할 수 있습니다.
    # 또한, 체인 실행 시 config 딕셔너리를 통해 세션 ID를 전달할 수 있도록 하여, 체인 내부에서 세션 관리, 로깅, 디버깅 등에 활용할 수 있도록 합니다.
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="query",
        history_messages_key="history"
    )

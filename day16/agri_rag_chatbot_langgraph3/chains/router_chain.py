
from prompts.router_prompt import router_prompt
from chains.rag_chain import create_chain as create_rag_chain
from chains.general_chain import create_chain as create_general_chain
from llms.llm_factory import get_llm
from langchain_core.output_parsers import StrOutputParser

# 라우터 체인 생성 함수
# create_chain() 함수는 선택된 모델과 처리 방식에 따라 적절한 체인을 생성하는 역할을 합니다.
# AUTO 모드에서는 router_prompt를 사용하여 사용자 질문을 분석하여 RAG 처리 방식이 필요한지 여부를 판단하고, 그에 따라 RAG 체인 또는 일반 GPT 체인을 생성하여 반환합니다.
# RAG 체인은 문서 검색과 LLM 응답 생성을 포함하는 복합적인 처리 방식을 구현한 체인이고, 일반 GPT 체인은 문서 검색 없이 LLM 응답 생성만을 수행하는 단순한 체인입니다.
# 라우터 체인은 router_prompt를 사용하여 사용자 질문을 분석하여 RAG 처리 방식이 필요한지 여부를 판단하는 역할을 합니다. 
# router_prompt는 LLM에게 질문의 유형을 분석하도록 지시하는 프롬프트입니다. 
# 라우터 체인은 router_prompt와 LLM, 그리고 StrOutputParser로 구성되어 있습니다. 
# StrOutputParser는 LLM의 응답에서 텍스트만 추출하는 역할을 합니다. 
# 라우터 체인은 invoke() 메서드를 통해 사용자 질문을 입력으로 받아서, 
# LLM이 분석한 결과에 따라 "RAG" 또는 "GPT"라는 문자열을 반환합니다. 
# create_chain() 함수에서는 이 반환값에 따라 적절한 체인을 생성하여 반환합니다. 
def create_chain(selected_model, selected_mode, question=""):
    
    # 선택된 모델 정보를 기반으로 LLM 객체를 생성합니다.
    llm = get_llm(selected_model)

    if selected_mode == "GPT":
        return create_general_chain(llm)

    if selected_mode == "RAG":
        return create_rag_chain(llm)

    # AUTO 모드
    router = router_prompt | llm | StrOutputParser()

    # 라우터 체인에 사용자 질문을 입력으로 전달하여, LLM이 분석한 결과에 따라 "RAG" 또는 "GPT"라는 문자열을 반환받습니다.
    category = router.invoke(
        {"query": question}
    ).strip().lower()

    # 라우터 체인의 반환값에 따라 적절한 체인을 생성하여 반환합니다.
    if category == "rag":
        return create_rag_chain(llm)

    return create_general_chain(llm)

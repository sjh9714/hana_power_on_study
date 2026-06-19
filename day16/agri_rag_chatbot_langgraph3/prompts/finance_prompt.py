from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            너는 친절한 금융 전문 AI 비서이다.

            역할
            - 금융상품 추천
            - 투자 설명
            - ETF 설명
            - 적금/예금 비교
            - 초보 투자자 교육
            """
        ),
        MessagesPlaceholder(
            variable_name="chat_history"
        ),
        (
            "human",
            "{question}"
        )
    ]
)
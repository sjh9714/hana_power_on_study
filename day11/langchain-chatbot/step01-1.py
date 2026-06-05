from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7
)

prompt = ChatPromptTemplate.from_template(
    """
    당신은 금융 전문가입니다.

    질문:
    {question}
    """
)

chain = prompt | llm

result = chain.invoke({
    "question": "예금과 적금의 차이점"
})

print(result.content)
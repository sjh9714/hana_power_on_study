from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(
    model="gpt-4.1-mini"
)

prompt = PromptTemplate.from_template(
"""
질문:
{question}
"""
)

chain = (
    prompt
    | llm
)

result = chain.invoke(
    {
        "question":"대한민국 수도는?"
    }
)

# 전체 응답 객체 출력
print(result)

# 응답 객체의 content 속성 출력
#print(result.content)


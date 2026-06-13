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
    | StrOutputParser()
)

for chunk in chain.stream({"question":"대한민국 수도는?"}):
    # 스트리밍된 응답을 실시간으로  줄바꿈 하여 출력 
    print(chunk)


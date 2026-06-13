from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

#소문자를 대문자로 변환하는 람다 함수
def upper(text):
    return text.upper()

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
    # 응답을 대문자로 변환하는 람다 함수 추가
    #| RunnableLambda(upper)
)

for chunk in chain.stream({"question":"docker란 무엇인가?"}):
    # 스트리밍된 응답을 실시간으로 줄바꿈 하여 출력 
    print(chunk)


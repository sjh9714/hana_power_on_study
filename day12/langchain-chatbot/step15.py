from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(
    model="gpt-4.1-mini"
)

parser = StrOutputParser()

response = llm.invoke("대한민국 수도는?")

result = parser.invoke(response)

print(result)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(
    model="gpt-4.1-mini"
)

prompt = ChatPromptTemplate.from_template(
    "{topic}에 대해 설명해줘."
)

parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke(
    {"topic": "LangChain"}
)

print(result)

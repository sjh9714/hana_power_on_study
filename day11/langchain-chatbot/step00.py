from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7
)

response = llm.invoke("안녕하세요")

print(response.content)


# 실행
#
# python .\step00.py  
#

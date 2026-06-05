from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro"
)

response = llm.invoke("안녕하세요")

print(response.content)


# 실행
#
# python .\step01.py  
#

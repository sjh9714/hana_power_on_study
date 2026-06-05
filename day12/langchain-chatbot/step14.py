from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4.1-mini"
)

response = llm.invoke("안녕하세요")

print(response)

#응답 객체의 타입과 구조를 확인하기 위해 다음과 같이 출력할 수 있습니다.
#print(f"response type: {type(response)}")

# 응답 문자열을 얻기 위해서는 content 속성을 사용합니다.
#print(response.content)

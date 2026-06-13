from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7
)

while True:

    question = input("사용자 : ")

    if question == "exit":
        break

    response = llm.invoke(question)

    print("AI :", response.content)

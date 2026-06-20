from chains.router_chain import ask

queries = [

    "작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템",
    "작물 생육 예측 플랫폼",
    "Wheat Cultivation Decision Support System",

    "GPT란 무엇인가?",
    "LangChain LCEL이란?",
    "Docker란 무엇인가?"

]

for query in queries:

    answer = ask(query)

    print()
    print(answer)
    print()
    print("=" * 60)


####################################################
# 예제 1 : Query Routing
####################################################


# 질문의 키워드를 분석하여 처리할 경로(라우터)를 결정하는 함수
def route(question):
    # 질문에 "밀"이라는 단어가 포함되어 있으면 RAG(검색 증강 생성) 경로로 지정
    if "밀" in question:
        return "rag"
    # 질문에 "날씨"라는 단어가 포함되어 있으면 웹 검색(Web Search) 경로로 지정
    elif "날씨" in question:
        return "web"
    # 두 조건에 모두 해당하지 않으면 일반 GPT 모델 경로로 지정
    else:
        return "gpt"
    
# RAG(외부 문서 데이터베이스 검색)를 통해 답변을 생성하는 가상의 체인 함수
def rag_chain(question):
    return f"RAG 검색 결과 : {question}"

# 웹 검색을 통해 답변을 생성하는 가상의 체인 함수
def web_chain(question):
    return f"WEB 검색 결과 : {question}"

# 일반 GPT 모델을 통해 답변을 생성하는 가상의 체인 함수
def gpt_chain(question):
    return f"GPT 답변 : {question}"


# 테스트용 질문 설정 ("밀"이라는 키워드가 포함되어 있음)
question = "밀 재배관리 시스템"

# route 함수를 호출하여 질문에 맞는 경로를 결정
path = route(question) 

# 결정된 경로 출력 ("선택경로: rag"가 출력됨)
print("선택경로:", path)

# 분기문을 통해 결정된 경로에 맞는 함수(체인) 실행
if path == "rag":
    # 경로가 "rag"이므로 rag_chain 함수 실행
    answer = rag_chain(question)
else:
    # 경로가 "rag"가 아닌 경우(gpt 또는 web) gpt_chain 함수 실행
    answer = gpt_chain(question)

# 최종 결과물 출력
print(answer)


# 실행 방법 
# python step1.py
# 선택경로: rag

# RAG 검색 결과 :
# 밀 재배관리 시스템

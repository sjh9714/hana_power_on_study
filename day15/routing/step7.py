################################################
# 예제7 Workflow Routing
# ################################################

from typing import TypedDict

# 1. 상태(State) 데이터의 구조를 정의하는 클래스
# Workflow 패턴에서는 이 'State' 객체가 여러 함수를 거쳐 가며 데이터가 업데이트됩니다.
class State(TypedDict):
    question: str  # 사용자의 입력 질문
    workflow: str  # 다음에 실행할 워크플로우 이름 (이 예제에서는 사용되지 않고 조건문으로 분기)
    answer: str    # 최종 결과물이 담길 공간

# 2. 질문(Question)을 분석하여 어떤 워크플로우(경로)로 보낼지 문자열 키를 반환하는 라우터 함수
def workflow_router(state):
    question = state["question"]

    # 질문에 '요약'이 포함되어 있으면 요약 워크플로우 경로 반환
    if "요약" in question:
        return "summary"

    # 질문에 '번역'이 포함되어 있으면 번역 워크플로우 경로 반환
    elif "번역" in question:
        return "translation"

    # 질문에 '코드'가 포함되어 있으면 코딩 워크플로우 경로 반환
    elif "코드" in question:
        return "coding"

    # 어떤 조건에도 맞지 않으면 기본 일반 질의응답(QA) 경로 반환
    return "qa"    

# 3. 각 기능별 워크플로우 함수들 (State를 입력받아 answer를 업데이트한 후 다시 State를 반환)
def qa_workflow(state):
    # 이 예제에서는 단순히 질문을 그대로 답변으로 설정 합니다
    # 실제 구현에서는 LLM 호출, DB 검색 등 복잡한 로직이 들어갈 수 있음
    q = state["question"]
    state["answer"] = f"QA 답변 : {q}"
    return state

def summary_workflow(state):
    text = state["question"]
    # 20글자까지만 자르고 뒤에 ...을 붙여 요약 흉내를 냄
    # 실제 구현에서는 LLM 호출, DB 검색 등 복잡한 로직이 들어갈 수 있음
    state["answer"] = f"요약 결과 : {text[:20]}..."
    return state

def translation_workflow(state):
    # 이 예제에서는 단순히 "영어 번역 결과"라는 고정된 문자열을 반환
    # 실제 구현에서는 번역 API 호출, LLM 번역 등 복잡한 로직이 들어갈 수 있음
    q = state["question"]
    state["answer"] = "영어 번역 결과"
    return state

def coding_workflow(state):
    # 멀티라인 문자열을 활용해 예시 코드 작성
    state["answer"] = """
def hello():
    print("hello")
"""
    return state


# ================================================
# 실행부 (Execution)
# ================================================

# 시스템 전체에서 공유할 초기 상태(State) 정의
state = {
    "question": "이 문서를 요약해줘",
    "workflow": "",
    "answer": ""
}

# 1. 라우터 함수에 상태를 전달하여 어떤 워크플로우로 갈지 결정 (문자열 반환)
# 여기서는 "요약"이 질문에 포함되어 있으므로 "summary"가 반환됨
workflow = workflow_router(state)

# 2. 라우터가 결정해준 워크플로우 이름(문자열)에 따라 적절한 함수를 매칭하여 실행
if workflow == "summary":
    result = summary_workflow(state)      # 주가 실행됨 -> state['answer'] 업데이트
elif workflow == "translation":
    result = translation_workflow(state)
elif workflow == "coding":
    result = coding_workflow(state)
else:
    result = qa_workflow(state)

# 3. 최종적으로 업데이트된 상태(State)의 answer 확인 및 출력
print(result["answer"])  # 출력 결과: "요약 결과 : 이 문서를 요약해줘..."

# 실행 방법
# python step7.py
#
# 결과
#
# 요약 결과 : 이 문서를 요약해줘
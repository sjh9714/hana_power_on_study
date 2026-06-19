from datetime import datetime
import re

# =========================
# Tool 1 : Time, 현재 시간 얻기 
# =========================
def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# =========================
# Tool 2 : Calculator, 계산기 
# =========================
def calculator(question):
    try:
        expr = question.replace("계산", "").strip()

        # 안전하게 숫자와 연산자만 허용
        if not re.fullmatch(r"[0-9+\-*/(). ]+", expr):
            return "계산식이 올바르지 않습니다."

        result = eval(expr)

        return f"결과 = {result}"

    except Exception as e:
        return f"계산 오류 : {e}"


# =========================
# Tool 3 : Chat, 일반 채팅
# =========================
def chat(question):
    return f"일반 대화 처리 : {question}"


# =========================
# Router, 질문으로 다음에 실행할 함수가 어떤 것인지 찾는다 
# 이것은 간단한 예제로 이해를 하면됨 
# =========================
def router(question):

    question = question.lower()

    # Time Routing
    if "시간" in question:
        return "time"

    # Calculator Routing
    if "계산" in question:
        return "calculator"

    # Default
    return "chat"


# =========================
# Main
# =========================
print("=== Simple Router Agent ===")
print("종료 : exit\n")

while True:

    question = input("질문 > ")

    if question.lower() == "exit":
        break

    route = router(question)

    print(f"[Router] → {route}")

    if route == "time":
        answer = get_time()

    elif route == "calculator":
        answer = calculator(question)

    else:
        answer = chat(question)

    print("답변 :", answer)
    print()


#실행 방법
# python step1.py 
# === Simple Router Agent ===
# 종료 : exit

# 질문 > 현재 시간을 알려줘
# [Router] → time
# 답변 : 2026-06-10 12:37:36

# 질문 > 계산 100 + 200 * 3
# [Router] → calculator
# 답변 : 결과 = 20000

# 질문 > 안녕하세요
# [Router] → chat
# 답변 : 일반 대화 처리 : 안녕하세요

# 질문 > exit
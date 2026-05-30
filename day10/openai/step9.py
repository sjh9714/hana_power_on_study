from openai import OpenAI
import gradio as gr
import os
from fastapi import FastAPI

# =========================================
# System Prompt
# =========================================

SYSTEM_PROMPT = """
너는 친절한 금융 전문 AI 비서이다.
답변은 자세하고 이해하기 쉽게 설명해라.
"""

#최대 이력은 이전 5건으로 설정함 
MAX_HISTORY = 5

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def chat(message, history):
    # history 구조 출력합니다
    print(history)

    # 최근 5개만 유지
    history = history[-MAX_HISTORY:]
    messages = [];

    # system role 추가
    messages.append({
        "role": "system",
        "content": SYSTEM_PROMPT
    })

    #이전 질문 및 답변을 추가합니다
    for item in history:
        messages.append({
            "role": item["role"],
            "content": item["content"][0]["text"]
        })

    messages.append({
        "role":"user",
        "content":message
    })

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        stream=True
    )

    partial_message = ""

    # --------------------------------
    # 스트리밍 데이터 수신
    # --------------------------------
    for chunk in response:

        delta = chunk.choices[0].delta.content

        if delta is not None:

            partial_message += delta

            # 실시간 출력
            yield partial_message


demo = gr.ChatInterface(chat)

# -----------------------------
# FastAPI 생성
# -----------------------------
app = FastAPI()

# -----------------------------
# FastAPI에 Gradio 연결
# -----------------------------
app = gr.mount_gradio_app(
    app,
    demo,
    path="/"
)

# 실행 방법
# uvicorn step9:app --reload --host 0.0.0.0 --port 8000
# 질문 : 사회 초년생으로 월 급여는 400만원인 사람으로 장기간 안정적인 투자를 할 수 있는 상품을 추천해줘  
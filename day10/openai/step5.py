from openai import OpenAI
import gradio as gr
import os
from fastapi import FastAPI

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
# uvicorn step5:app --reload --host 0.0.0.0 --port 8000

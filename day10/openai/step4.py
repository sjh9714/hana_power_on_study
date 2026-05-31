from openai import OpenAI
import gradio as gr
import os
from fastapi import FastAPI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def chat(message, history):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"user",
                "content":message
            }
        ],
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
# uvicorn step4:app --reload --host 0.0.0.0 --port 8000

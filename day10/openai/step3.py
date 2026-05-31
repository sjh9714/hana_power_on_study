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
        ]
    )

    return response.choices[0].message.content

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
# uvicorn step3:app --reload --host 0.0.0.0 --port 8000

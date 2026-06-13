from fastapi import FastAPI
from openai import OpenAI
import gradio as gr
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
너는 친절한 금융 전문 AI 비서이다.
답변은 자세하고 이해하기 쉽게 설명해라.
"""

MAX_HISTORY = 5

# ==========================================
# LangChain LLM
# ==========================================

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY"),
    streaming=True
)

# ==========================================
# Chat Function
# ==========================================

def chat(message, history):

    print(history)

    history = history[-MAX_HISTORY:]

    messages = []

    # System Prompt
    messages.append(
        SystemMessage(content=SYSTEM_PROMPT)
    )

    # 이전 대화 추가
    for item in history:

        role = item["role"]
        text = item["content"][0]["text"]

        if role == "user":
            messages.append(
                HumanMessage(content=text)
            )

        elif role == "assistant":
            messages.append(
                AIMessage(content=text)
            )

    # 현재 질문
    messages.append(
        HumanMessage(content=message)
    )

    partial_message = ""

    # 스트리밍 호출
    for chunk in llm.stream(messages):

        if chunk.content:

            partial_message += chunk.content

            yield partial_message


# ==========================================
# Gradio UI
# ==========================================

demo = gr.ChatInterface(chat)

# ==========================================
# FastAPI
# ==========================================

app = FastAPI()

app = gr.mount_gradio_app(
    app,
    demo,
    path="/"
)

# ==========================================
# 실행
# ==========================================

# uvicorn app:app --reload --host 0.0.0.0 --port 8000
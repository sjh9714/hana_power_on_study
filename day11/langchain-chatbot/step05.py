import os
import gradio as gr

from fastapi import FastAPI

# =========================================
# LangChain
# =========================================
from langchain_openai import ChatOpenAI

# LangChain Message 객체
from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

# =========================================
# OpenAI LLM 생성
# =========================================
# streaming=True
# → 응답을 한 번에 받지 않고
# → 토큰 단위로 실시간 수신 가능
# =========================================

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7,
    streaming=True
)

# =========================================
# 채팅 함수
# =========================================
#
# message
#   사용자가 방금 입력한 질문
#
# history
#   이전 대화 내역
#
# Gradio ChatInterface가 자동 전달
# =========================================

def chat(message, history):

    # GPT에 전달할 전체 메시지 저장
    messages = []

    # 최대 5개의 이전 대화 추가
    history = history[-5:]

    # =====================================
    # 이전 대화 추가
    # =====================================
    #
    # history 예시
    #
    # [
    #   {"role":"user","content":"안녕"},
    #   {"role":"assistant","content":"반가워"}
    # ]
    #
    # LangChain Message 객체로 변환
    # =====================================

    for item in history:

        # 사용자 메시지
        if item["role"] == "user":

            messages.append(
                HumanMessage(
                    content=item["content"]
                )
            )

        # AI 메시지
        elif item["role"] == "assistant":

            messages.append(
                AIMessage(
                    content=item["content"]
                )
            )

    # =====================================
    # 현재 질문 추가
    # =====================================

    messages.append(
        HumanMessage(content=message)
    )

    # =====================================
    # 스트리밍 응답 저장 변수
    # =====================================

    partial_message = ""

    # =====================================
    # GPT Streaming 호출
    # =====================================
    #
    # chunk 단위로 응답 수신
    # 예:
    #
    # "안"
    # "녕"
    # "하"
    # "세"
    # "요"
    #
    # =====================================

    for chunk in llm.stream(messages):

        # 빈 토큰 제거
        if chunk.content:

            # 응답 누적
            partial_message += chunk.content

            # Gradio 화면 실시간 갱신
            yield partial_message


# =========================================
# Gradio Chat UI 생성
# =========================================

demo = gr.ChatInterface(
    fn=chat,
    title="LangChain ChatBot",

    # 최신 Gradio 권장 방식
    type="messages"
)

# =========================================
# FastAPI 생성
# =========================================

app = FastAPI()

# =========================================
# FastAPI에 Gradio 연결
# =========================================

app = gr.mount_gradio_app(
    app,
    demo,
    path="/"
)

# =========================================
# 실행
# =========================================
#
# uvicorn step4:app \
#     --reload \
#     --host 0.0.0.0 \
#     --port 8000
#
# 접속
#
# http://localhost:8000
#
# =========================================
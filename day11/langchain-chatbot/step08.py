# goole gemini-2.5-flash 모델을 활용한 금융 상담 챗봇 예제

from fastapi import FastAPI
import gradio as gr
import os

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

# ==================================================
# 설정값
# ==================================================

# 이전 대화 최대 개수
MAX_HISTORY = 5

# ==================================================
# Prompt Template
# ==================================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            너는 친절한 금융 전문 AI 비서이다.

            역할:
            - 금융상품 추천
            - 투자 설명
            - 적금/예금 비교
            - ETF 설명
            - 초보 투자자 교육

            답변 규칙:
            - 쉽게 설명
            - 단계별 설명
            - 예시 포함
            - 표 사용 가능
            - 금융 초보자 기준 설명
            """
        ),

        # 이전 대화 이력 삽입
        MessagesPlaceholder(variable_name="chat_history"),

        # 현재 질문
        (
            "human",
            "{question}"
        )
    ]
)

# ==================================================
# LLM 생성
# ==================================================

llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            streaming=True
        )

# ==================================================
# Chat 함수
# ==================================================

def chat(message, history):

    print("history =", history)

    # 최근 N개만 유지
    history = history[-MAX_HISTORY:]

    chat_history = []

    # ------------------------------------
    # Gradio History -> LangChain Message 변환
    # ------------------------------------
    for item in history:

        role = item["role"]
        text = item["content"][0]["text"]

        if role == "user":
            chat_history.append(
                HumanMessage(content=text)
            )

        elif role == "assistant":
            chat_history.append(
                AIMessage(content=text)
            )

    # ------------------------------------
    # PromptTemplate 적용
    # ------------------------------------
    messages = prompt.format_messages(
        chat_history=chat_history,
        question=message
    )

    # 확인용 출력
    print("messages =", messages)

    partial_message = ""

    # ------------------------------------
    # Streaming 응답
    # ------------------------------------
    for chunk in llm.stream(messages):

        if chunk.content:

            partial_message += chunk.content

            yield partial_message

# ==================================================
# Gradio UI
# ==================================================

demo = gr.ChatInterface(
    fn=chat,
    title="금융 상담 챗봇",
    description="LangChain + openAI + Gemini 예제"
)

# ==================================================
# FastAPI
# ==================================================

app = FastAPI()

app = gr.mount_gradio_app(
    app,
    demo,
    path="/"
)

# ==================================================
# 실행
# ==================================================

# uvicorn step08:app --reload --host 0.0.0.0 --port 8000
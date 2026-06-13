from fastapi import FastAPI
import gradio as gr
import os

from langchain_openai import ChatOpenAI
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
# 설정
# ==================================================

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

        MessagesPlaceholder(variable_name="chat_history"),

        (
            "human",
            "{question}"
        )
    ]
)

# ==================================================
# 모델 설정
# ==================================================

MODEL_CONFIG = {
    "GPT-4.1 Mini": {
        "provider": "openai",
        "model": "gpt-4.1-mini"
    },
    "Gemini 2.5 Flash": {
        "provider": "gemini",
        "model": "gemini-2.5-flash"
    }
}

# ==================================================
# LLM 생성
# ==================================================

def get_llm(model_name):

    config = MODEL_CONFIG[model_name]

    provider = config["provider"]
    model = config["model"]

    if provider == "openai":

        return ChatOpenAI(
            model=model,
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7,
            streaming=True
        )

    elif provider == "gemini":

        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            streaming=True
        )

    raise ValueError("지원하지 않는 모델")

# ==================================================
# Chat 함수
# ==================================================

def chat(message, history, selected_model):

    if not message:
        yield history, ""
        return

    if history is None:
        history = []

    llm = get_llm(selected_model)

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

model_dropdown = gr.Dropdown(
    choices=list(MODEL_CONFIG.keys()),
    value="GPT-4.1 Mini",
    label="모델 선택"
)

demo = gr.ChatInterface(
    fn=chat,

    additional_inputs=[
        model_dropdown
    ],

    title="💰 금융 상담 챗봇",

    description="""

    지원 모델:
    - GPT-4.1 Mini (OpenAI)
    - Gemini 2.5 Flash (Google)

    모델을 선택한 후 질문하세요.
    """
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

"""
환경변수 설정

Linux

export OPENAI_API_KEY="sk-xxxx"
export GOOGLE_API_KEY="xxxx"

Windows

set OPENAI_API_KEY=sk-xxxx
set GOOGLE_API_KEY=xxxx
"""

# 실행
#
# uvicorn step10:app --reload --host 0.0.0.0 --port 8000
#
# 접속
#
# http://localhost:8000
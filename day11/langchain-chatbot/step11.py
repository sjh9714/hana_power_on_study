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

            역할
            - 금융상품 추천
            - 투자 설명
            - ETF 설명
            - 적금/예금 비교
            - 초보 투자자 교육

            답변 규칙
            - 쉽게 설명
            - 단계별 설명
            - 예시 포함
            - 표 사용 가능
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

def get_llm(selected_model):

    config = MODEL_CONFIG[selected_model]

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
# 채팅 함수
# ==================================================
def chat(message, history, selected_model):

    if not message:
        yield history, ""
        return

    if history is None:
        history = []

    llm = get_llm(selected_model)

    # 최근 대화만 사용
    recent_history = history[-MAX_HISTORY * 2:]

    chat_history = []

    # Gradio -> LangChain 변환
    for item in recent_history:

        role = item.get("role")
        content = item.get("content", "")

        if role == "user":
            chat_history.append(
                HumanMessage(content=content)
            )

        elif role == "assistant":
            chat_history.append(
                AIMessage(content=content)
            )

    messages = prompt.format_messages(
        chat_history=chat_history,
        question=message
    )

    # 사용자 메시지 추가
    history.append(
        {
            "role": "user",
            "content": message
        }
    )

    # 빈 assistant 메시지 추가
    history.append(
        {
            "role": "assistant",
            "content": ""
        }
    )

    partial_response = ""

    try:

        for chunk in llm.stream(messages):

            content = ""

            if hasattr(chunk, "content"):
                content = chunk.content

            if content:

                partial_response += content

                history[-1]["content"] = partial_response

                yield history, ""

    except Exception as e:

        history[-1]["content"] = f"오류 발생: {str(e)}"

        yield history, ""
# ==================================================
# 채팅 초기화
# ==================================================

def clear_chat():
    return []

# ==================================================
# Gradio UI
# ==================================================

with gr.Blocks(title="금융 상담 챗봇") as demo:

    gr.Markdown(
        """
        # 💰 금융 상담 챗봇

        OpenAI 또는 Gemini를 선택하여 금융 관련 질문을 할 수 있습니다.
        """
    )

    # ------------------------------------------
    # 상단 설정 영역
    # ------------------------------------------

    with gr.Row():
        model_dropdown = gr.Dropdown(
            choices=list(MODEL_CONFIG.keys()),
            value="GPT-4.1 Mini",
            label="LLM 모델"
        )

    # ------------------------------------------
    # 챗봇
    # ------------------------------------------

    chatbot = gr.Chatbot(
        height=600,
        label="대화"
    )

    # ------------------------------------------
    # 입력 영역
    # ------------------------------------------

    with gr.Row():
        msg = gr.Textbox(
            placeholder="질문을 입력하세요...",
            scale=8
        )

        send_btn = gr.Button(
            "전송",
            scale=1
        )

    # ------------------------------------------
    # 이벤트 연결
    # ------------------------------------------

    send_btn.click(
        fn=chat,
        inputs=[
            msg,
            chatbot,
            model_dropdown
        ],
        outputs=[
            chatbot,
            msg
        ]
    )

    msg.submit(
        fn=chat,
        inputs=[
            msg,
            chatbot,
            model_dropdown
        ],
        outputs=[
            chatbot,
            msg
        ]
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
Linux

export OPENAI_API_KEY="sk-xxxx"
export GOOGLE_API_KEY="xxxx"

Windows

set OPENAI_API_KEY=sk-xxxx
set GOOGLE_API_KEY=xxxx
"""

# 실행
#
# uvicorn step11:app --reload --host 0.0.0.0 --port 8000
#
# 접속
#
# http://localhost:8000
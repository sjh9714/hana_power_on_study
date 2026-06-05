import os
import uuid
from fastapi import FastAPI
import gradio as gr

# LangChain 관련 모듈 임포트
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.chat_history import (
    InMemoryChatMessageHistory
)

# ==================================================
# Prompt Template (프롬프트 템플릿 설정)
# ==================================================
# 챗봇의 페르소나, 답변 규칙 및 대화 기록(History)을 결합하는 프롬프트 구조 정의
prompt = ChatPromptTemplate.from_messages(
    [
        # 1. System Message: 챗봇에게 고유한 역할과 성격, 규칙을 부여
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
            """
        ),
        # 2. MessagesPlaceholder: 이전 대화 기록(chat_history)이 동적으로 삽입될 공간
        MessagesPlaceholder(
            variable_name="chat_history"
        ),
        # 3. Human Message: 사용자가 새로 입력한 질문이 들어갈 공간
        (
            "human",
            "{question}"
        )
    ]
)

# ==================================================
# 모델 설정 (지원하는 LLM 메타데이터)
# ==================================================
# 사용자가 UI에서 선택할 모델의 이름과 실제 연동할 API 공급자/모델 매핑 리스트
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
# Session History 저장소
# ==================================================
# 서버 메모리에 세션 ID별로 대화 기록을 저장할 딕셔너리 변수
store = {}

def get_session_history(session_id):
    """
    세션 ID에 해당하는 대화 기록 객체(InMemoryChatMessageHistory)를 반환하는 함수.
    기존 기록이 없으면 새로 생성하여 스토어에 등록합니다.
    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# ==================================================
# LLM 생성 팩토리 함수
# ==================================================
def get_llm(selected_model):
    """
    Gradio 드롭다운에서 선택된 모델 이름을 바탕으로 
    해당 공급자(OpenAI 또는 Google)의 LangChain LLM 객체를 동적으로 생성하여 반환합니다.
    """
    config = MODEL_CONFIG[selected_model]
    provider = config["provider"]
    model = config["model"]

    # OpenAI 모델 객체 생성
    if provider == "openai":
        return ChatOpenAI(
            model=model,
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7,
            streaming=True # 실시간 스트리밍 답변 활성화
        )

    # Google Gemini 모델 객체 생성
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            streaming=True # 실시간 스트리밍 답변 활성화
        )

    raise ValueError("지원하지 않는 모델")

# ==================================================
# Chat 핵심 비즈니스 로직 함수 (Gradio Event Handler)
# ==================================================
def chat(
    message,         # 사용자가 텍스트박스에 입력한 메시지
    history,         # Gradio Chatbot 컴포넌트가 내부적으로 유지하는 대화 히스토리 (List[Dict])
    selected_model,  # 드롭다운에서 선택된 LLM 모델 이름
    session_id       # 현재 사용자의 고유 세션 ID (gr.State)
):
    # 빈 메시지가 들어오면 아무 작업도 하지 않고 리턴
    if not message:
        yield history, ""
        return

    # 대화 기록 배열이 초기화되어 있지 않다면 빈 배열 생성
    if history is None:
        history = []

    # 선택된 모델에 알맞은 LLM 객체 획득
    llm = get_llm(selected_model)

    # ------------------------------------------
    # Session History 가져오기
    # ------------------------------------------
    # 서버 메모리 저장소(store)에서 해당 세션의 LangChain 대화 객체를 불러옴
    chat_history_obj = get_session_history(session_id)

    # ------------------------------------------
    # Prompt 생성 및 이전 대화 결합
    # ------------------------------------------
    # 프롬프트 템플릿에 [이전 대화 목록]과 [현재 질문]을 주입하여 최종 메시지 번들 생성
    messages = prompt.format_messages(
        chat_history=chat_history_obj.messages,
        question=message
    )

    # ------------------------------------------
    # User Message 저장 (LangChain 대화 기록 관리)
    # ------------------------------------------
    # 다음 턴 대화에서 기억할 수 있도록, 유저의 새 질문을 세션 저장소에 즉시 기록
    chat_history_obj.add_user_message(message)

    # ------------------------------------------
    # Gradio Chatbot UI에 유저 입력 반영 및 AI 답변 영역 준비
    # ------------------------------------------
    # 1. 유저 질문 추가
    history.append(
        {
            "role": "user",
            "content": message
        }
    )
    # 2. AI 답변이 실시간으로 쓰여질 빈 공간 확보
    history.append(
        {
            "role": "assistant",
            "content": ""
        }
    )

    partial_response = ""

    try:
        # --------------------------------------
        # Streaming (실시간 답변 렌더링)
        # --------------------------------------
        # LLM으로부터 글자 조각(chunk)을 하나씩 받아올 때마다 화면을 갱신(yield)
        for chunk in llm.stream(messages):
            if chunk.content:
                partial_response += chunk.content
                history[-1]["content"] = partial_response  # Chatbot의 마지막 메시지 내용 업데이트
                yield history, ""  # 첫 번째 반환값: 갱신된 대화 내역, 두 번째 반환값: 유저 입력창 비우기("")

        # --------------------------------------
        # AI Message 저장 (LangChain 대화 기록 관리)
        # --------------------------------------
        # 스트리밍이 정상적으로 완료되면 완성된 AI 답변 전체를 세션 저장소에 기록
        chat_history_obj.add_ai_message(
            partial_response
        )

    except Exception as e:
        # 에러 발생 시 UI 창에 에러 내용 표시
        history[-1]["content"] = f"오류 발생: {str(e)}"
        yield history, ""

# ==================================================
# 대화 초기화 함수
# ==================================================
def clear_chat(session_id):
    """
    현재 사용자의 세션 ID 데이터를 메모리 저장소에서 완전 삭제하여 대화를 포맷팅합니다.
    """
    if session_id in store:
        del store[session_id]

    # Gradio UI의 chatbot 히스토리를 비우고([]), 입력창도 비웁니다("")
    return [], ""

# ==================================================
# UI 화면 설계 (Gradio Blocks)
# ==================================================
with gr.Blocks(
    title="금융 상담 챗봇"
) as demo:

    gr.Markdown("# 💰 금융 상담 챗봇")

    # ------------------------------------------
    # Session ID (사용자 고유 상태값)
    # ------------------------------------------
    # 웹페이지 접속 시 브라우저 탭마다 유니크한 UUID를 생성하여 세션 식별자로 사용 (화면엔 안 보임)
    session_state = gr.State(str(uuid.uuid4()))

    # ------------------------------------------
    # 모델 선택 컴포넌트
    # ------------------------------------------
    model_dropdown = gr.Dropdown(
        choices=list(MODEL_CONFIG.keys()),
        value="GPT-4.1 Mini",
        label="LLM 모델"
    )

    # ------------------------------------------
    # Chatbot (대화창 컴포넌트)
    # ------------------------------------------
    chatbot = gr.Chatbot(
        height=600,
        label="대화"
    )

    # ------------------------------------------
    # 입력창 및 전송 버튼 배치
    # ------------------------------------------
    with gr.Row():
        msg = gr.Textbox(
            placeholder="질문을 입력하세요...",
            scale=8  # 가로 비율을 버튼보다 넓게 설정
        )

        send_btn = gr.Button(
            "전송",
            scale=1  # 가로 비율 작게 설정
        )

    # ------------------------------------------
    # 초기화 버튼 컴포넌트
    # ------------------------------------------
    clear_btn = gr.Button("대화 초기화")

    # ------------------------------------------
    # 이벤트 리스너 정의 (전송 버튼 클릭 시 동작)
    # ------------------------------------------
    send_btn.click(
        fn=chat,
        inputs=[
            msg,             # chat()의 첫 번째 인자
            chatbot,         # chat()의 두 번째 인자
            model_dropdown,  # chat()의 세 번째 인자
            session_state    # chat()의 네 번째 인자
        ],
        outputs=[
            chatbot,         # 첫 번째 yield 결과가 반영될 UI 컴포넌트
            msg              # 두 번째 yield 결과(입력창 초기화 "")가 반영될 UI 컴포넌트
        ]
    )

    # ------------------------------------------
    # 이벤트 리스너 정의 (텍스트 박스에서 엔터 입력 시 동작)
    # ------------------------------------------
    msg.submit(
        fn=chat,
        inputs=[
            msg, chatbot, model_dropdown, session_state
        ],
        outputs=[
            chatbot, msg
        ]
    )

    # ------------------------------------------
    # 이벤트 리스너 정의 (대화 초기화 버튼 클릭 시 동작)
    # ------------------------------------------
    clear_btn.click(
        fn=clear_chat,
        inputs=[
            session_state
        ],
        outputs=[
            chatbot, msg
        ]
    )

# ==================================================
# FastAPI 웹 백엔드 서버 설정 및 통합
# ==================================================
app = FastAPI()

# FastAPI 애플리케이션의 루트 경로('/')에 Gradio UI(demo)를 탑재(Mount)함
app = gr.mount_gradio_app(
    app,
    demo,
    path="/"
)

# ==================================================
# 실행 방법 가이드 (터미널에서 명령어 입력)
# ==================================================
# 이 스크립트 파일명이 만약 step12.py 라면, 아래 주석 명령어로 실행 가능합니다.
# uvicorn step12:app --reload --host 0.0.0.0 --port 8000


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
from langchain_core.runnables.history import (
    RunnableWithMessageHistory
)

# ==================================================
# Prompt Template (프롬프트 템플릿 설정)
# ==================================================
# 챗봇의 페르소나, 답변 규칙 및 대화 기록(History)을 결합하는 프롬프트 구조 정의
# LangChain은 이 템플릿을 기반으로 시스템 메시지, 이전 대화, 새 질문을 하나의 프롬프트로 조립합니다.
prompt = ChatPromptTemplate.from_messages(
    [
        # 1. System Message: 챗봇에게 고유한 역할(금융 전문가)과 성격, 답변 규칙을 엄격하게 부여
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
        # 2. MessagesPlaceholder: RunnableWithMessageHistory에 의해 
        # 'chat_history' 키로 저장된 이전 대화 목록(List[Message])이 동적으로 삽입되는 공간
        MessagesPlaceholder(
            variable_name="chat_history"
        ),
        # 3. Human Message: 사용자가 UI를 통해 새로 입력한 질문({question})이 주입되는 공간
        (
            "human",
            "{question}"
        )
    ]
)

# ==================================================
# 모델 설정 (지원하는 LLM 메타데이터)
# ==================================================
# 사용자가 UI(Dropdown)에서 선택할 명칭과, 실제 내부 팩토리 함수에서 사용할 공급자/모델명 매핑 리스트
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
# Session History 저장소 (In-Memory DB 역할)
# ==================================================
# 서버 메모리에 세션 ID(Key)별로 대화 기록 객체(Value)를 저장하는 딕셔너리 변수
# 주의: 프로덕션 환경에서는 서버 재시작 시 초기화되므로 Redis나 데이터베이스(DB) 전환이 필요합니다.
store = {}

def get_session_history(session_id: str):
    """
    세션 ID에 해당하는 대화 기록 객체(InMemoryChatMessageHistory)를 조회 및 반환하는 함수.
    RunnableWithMessageHistory가 대화 흐름 중에 내부적으로 호출하여 히스토리를 가져옵니다.
    """
    if session_id not in store:
        # 기존 기록이 없으면 해당 세션 전용 대화 기록 객체를 새로 생성하여 스토어에 등록
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# ==================================================
# LLM 생성 팩토리 함수
# ==================================================
def get_llm(selected_model: str):
    """
    Gradio 드롭다운에서 선택된 모델 이름을 바탕으로 환경변수(API Key)를 참조하여
    해당 공급자(OpenAI 또는 Google)의 LangChain LLM 객체를 동적으로 생성하여 반환합니다.
    """
    config = MODEL_CONFIG[selected_model]
    provider = config["provider"]
    model = config["model"]

    # OpenAI 모델 객체 생성 및 스트리밍 옵션 활성화
    if provider == "openai":
        return ChatOpenAI(
            model=model,
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7,
            streaming=True # 토큰 단위로 실시간 답변을 받아오기 위해 필수 설정
        )

    # Google Gemini 모델 객체 생성 및 스트리밍 옵션 활성화
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            streaming=True # 토큰 단위로 실시간 답변을 받아오기 위해 필수 설정
        )

    raise ValueError("지원하지 않는 모델입니다.")

# ==========================================
# LCEL Chain 생성 함수
# ==========================================
def create_chain(selected_model: str):
    """
    선택된 모델에 맞는 LLM 객체를 생성하고, 프롬프트와 결합한 뒤
    대화 기록 관리 모듈(RunnableWithMessageHistory)을 래핑하여 최종 실행 가능한 체인을 반환합니다.
    """
    # 1. 동적으로 사용할 LLM 객체 획득
    llm = get_llm(selected_model)

    # 2. LCEL(LangChain Expression Language) 파이프라인 구성 (프롬프트 -> 모델)
    chain = (
        prompt
        | llm
    )

    # 3. 대화 기록을 자동으로 추적/삽입해주는 Runnable 생성
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,                       # 세션 ID를 받아 히스토리 객체를 리턴하는 함수 매핑
        input_messages_key="question",             # 사용자 입력이 들어가는 프롬프트 변수명 지정
        history_messages_key="chat_history"        # 대화 기록이 주입될 MessagesPlaceholder 변수명 지정
    )

    return chain_with_history

# ==================================================
# Chat 핵심 비즈니스 로직 함수 (Gradio Event Handler)
# ==================================================
def chat(
    message,         # 사용자가 텍스트박스에 입력한 현재 메시지 (str)
    history,         # Gradio Chatbot 컴포넌트가 유지하는 대화 히스토리 상태 (List[Dict])
    selected_model,  # 드롭다운에서 현재 선택된 LLM 모델 이름 (str)
    session_id       # 현재 사용자의 웹 브라우저 탭 고유 세션 ID (gr.State)
):
    # 사용자가 공백이나 빈 메시지를 전송한 경우 예외 처리
    if not message:
        yield history, ""
        return

    # 대화 기록 배열이 초기화되어 있지 않다면 안전하게 빈 배열([])로 초기화
    if history is None:
        history = []

    # 사용자가 선택한 모델 버전에 맞춰 LangChain 체인을 유연하게 생성
    chain = create_chain(selected_model)

    # ------------------------------------------
    # Gradio Chatbot UI에 유저 입력 반영 및 AI 답변 영역 준비
    # ------------------------------------------
    # 1. 사용자의 질문을 Chatbot UI 포맷에 맞춰 추가
    history.append(
        {
            "role": "user",
            "content": message
        }
    )
    # 2. AI의 답변이 실시간(Streaming)으로 업데이트될 빈 껍데기 메시지 미리 확보
    history.append(
        {
            "role": "assistant",
            "content": ""
        }
    )

    # 스트리밍 텍스트 조각들을 누적해서 저장할 변수
    partial_response = ""

    try:
        # --------------------------------------
        # Streaming (실시간 답변 렌더링 소모 구조)
        # --------------------------------------
        # chain.stream()은 LLM으로부터 글자 조각(chunk)이 완성될 때마다 Generator 형태로 값을 반환합니다.
        for chunk in chain.stream(
            {
                "question": message                # 프롬프트의 {question}에 유저 메시지 주입
            },
            config={
                "configurable": {
                    "session_id": session_id       # 어떤 사용자의 대화 기록을 불러오고 저장할지 세션 식별자 전달
                }
            }
        ):
            # 받아온 chunk의 텍스트 내용을 누적 문자열에 합산
            partial_response += chunk.content
            
            # Chatbot의 맨 마지막 메시지(방금 만든 assistant 공간)의 내용을 실시간 갱신
            history[-1]["content"] = partial_response  
            
            # 제너레이터(yield)를 통해 한 글자씩 늘어나는 대화 내역(history)을 UI에 지속적으로 밀어 넣음
            # 두 번째 반환값 ""은 사용자의 입력 텍스트 박스를 비워주는 효과를 냄
            yield history, ""  

    except Exception as e:
        # 체인 실행 혹은 API 통신 중 에러 발생 시 사용자 UI 창에 직관적으로 에러 내용 표시
        history[-1]["content"] = f"오류 발생: {str(e)}"
        yield history, ""

# ==================================================
# 대화 초기화 함수
# ==================================================
def clear_chat(session_id):
    """
    현재 사용자의 세션 ID 데이터를 서버 메모리(store)에서 완전 삭제하여 
    이전 대화 기억을 완전히 포맷팅(Reset)합니다.
    """
    if session_id in store:
        del store[session_id]

    # Gradio UI 단에서도 chatbot 히스토리를 완전히 비우고([]), 입력창도 초기화("")하도록 반환값 설정
    return [], ""

# ==================================================
# UI 화면 설계 (Gradio Blocks View)
# ==================================================
with gr.Blocks(
    title="금융 상담 챗봇"
) as demo:

    gr.Markdown("# 💰 금융 상담 챗봇")

    # ------------------------------------------
    # Session ID (사용자 고유 상태값 관리)
    # ------------------------------------------
    # 웹페이지 접속 시 브라우저 탭(세션)마다 유니크한 UUID를 생성하여 내부 상태값으로 보관 (UI 레이아웃에는 숨겨짐)
    # 새로고침을 하거나 새 탭으로 열면 완전히 새로운 대화 세션으로 격리됩니다.
    session_state = gr.State(str(uuid.uuid4()))

    # ------------------------------------------
    # 모델 선택 컴포넌트 (Dropdown)
    # ------------------------------------------
    model_dropdown = gr.Dropdown(
        choices=list(MODEL_CONFIG.keys()),
        value="GPT-4.1 Mini",                # 기본 선택값
        label="LLM 모델"
    )

    # ------------------------------------------
    # Chatbot (대화 내역 디스플레이 컴포넌트)
    # ------------------------------------------
    chatbot = gr.Chatbot(
        height=600,                          # 대화창 세로 크기 고정
        label="대화"
    )

    # ------------------------------------------
    # 입력창 및 전송 버튼 배치 (가로 정렬 Layout)
    # ------------------------------------------
    with gr.Row():
        msg = gr.Textbox(
            placeholder="질문을 입력하세요...",
            scale=8                          # 텍스트박스가 가로 공간의 80%를 차지하도록 가중치 설정
        )

        send_btn = gr.Button(
            "전송",
            scale=1                          # 버튼이 가로 공간의 10% 내외를 차지하도록 가중치 설정
        )

    # ------------------------------------------
    # 대화 리셋 버튼 컴포넌트
    # ------------------------------------------
    clear_btn = gr.Button("대화 초기화")

    # ------------------------------------------
    # 이벤트 리스너: [전송] 버튼 클릭 시 동작 정의
    # ------------------------------------------
    send_btn.click(
        fn=chat,                             # 호출할 비즈니스 로직 함수
        inputs=[
            msg,                             # chat()의 첫 번째 인자 (사용자 입력문)
            chatbot,                         # chat()의 두 번째 인자 (기존 대화 리스트 상태)
            model_dropdown,                  # chat()의 세 번째 인자 (선택된 LLM 명칭)
            session_state                    # chat()의 네 번째 인자 (사용자 세션 고유 ID)
        ],
        outputs=[
            chatbot,                         # chat() 함수에서 yield된 첫 번째 결과가 바인딩되어 업데이트될 UI
            msg                              # chat() 함수에서 yield된 두 번째 결과("")가 바인딩되어 초기화될 UI
        ]
    )

    # ------------------------------------------
    # 이벤트 리스너: 텍스트 박스 안에서 [Enter] 입력 시 동작 정의
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
    # 이벤트 리스너: [대화 초기화] 버튼 클릭 시 동작 정의
    # ------------------------------------------
    clear_btn.click(
        fn=clear_chat,                       # 메모리 스토어 및 세션 기록을 지우는 함수 호출
        inputs=[
            session_state                    # 삭제 타겟을 식별하기 위한 현재 세션 ID 입력
        ],
        outputs=[
            chatbot,                         # 반환된 빈 배열([])을 통해 대화창 시각적 초기화
            msg                              # 반환된 공백("")을 통해 입력 폼 비우기
        ]
    )

# ==================================================
# FastAPI 웹 백엔드 서버 설정 및 통합
# ==================================================
app = FastAPI()

# FastAPI 애플리케이션의 루트 경로('/')에 Gradio가 설계한 인터페이스(demo)를 서브 어플리케이션으로 마운트
# 이를 통해 고성능 FastAPI 백엔드 위에서 Gradio 웹 UI가 완벽하게 구동됩니다.
app = gr.mount_gradio_app(
    app,
    demo,
    path="/"
)

# ==================================================
# 실행 방법 가이드 (터미널에서 명령어 입력)
# ==================================================
# 이 스크립트 파일명이 만약 step26.py 라면, 아래 주석 명령어로 인스턴스를 실행할 수 있습니다.
# uvicorn step26:app --reload --host 0.0.0.0 --port 8000
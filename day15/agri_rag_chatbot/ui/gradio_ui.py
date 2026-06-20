import uuid
import gradio as gr

# 설정값과 비즈니스 로직 함수, 메모리 관리 함수를 임포트
from config.settings import (
    CHATBOT_TITLE,
    MODEL_CONFIG
)

# 비즈니스 로직 함수 (사용자 입력 처리 및 모델 응답 생성) 임포트
from services.chat_service import (
    chat
)

# 세션 메모리 초기화 함수 임포트
from memory.session_memory import (
    clear_session
)

# 대화 초기화 함수: 세션 메모리를 지우고 UI를 초기 상태로 리셋
def clear_chat(session_id):

    clear_session(session_id)

    return [], ""

# Gradio UI 생성 함수
# FastAPI 앱에서 이 함수를 호출하여 Gradio 인터페이스를 생성하고 마운트할 예정
# UI 레이아웃과 이벤트 핸들링을 정의하는 핵심 함수입니다.
# UI 구성 요소(모델 선택 드롭다운, 처리 방식 선택 드롭다운, 챗봇 대화창, 입력창, 버튼 등)를 배치하고,
# 사용자 상호작용(버튼 클릭, 입력 제출 등)에 따른 이벤트 리스너를 설정하여 chat() 및 clear_chat() 함수를 호출하도록 연결합니다.
# 이 함수가 반환하는 Gradio Blocks 객체는 FastAPI 앱에 마운트되어 웹 인터페이스로 제공됩니다.
def create_ui():

    # ==================================================
    # UI 화면 설계 (Gradio Blocks View)
    # ==================================================
    with gr.Blocks(
        title=CHATBOT_TITLE
    ) as demo:

        # ------------------------------------------
        # Session ID (사용자 고유 상태값 관리)
        # ------------------------------------------
        # 웹페이지 접속 시 브라우저 탭(세션)마다 유니크한 UUID를 생성하여 내부 상태값으로 보관 (UI 레이아웃에는 숨겨짐)
        # 새로고침을 하거나 새 탭으로 열면 완전히 새로운 대화 세션으로 격리됩니다.
        session_state = gr.State(
            str(uuid.uuid4())
        )

        # ------------------------------------------
        # 챗봇 타이틀 (Markdown)
        # ------------------------------------------
        gr.Markdown(f"# 🌱 {CHATBOT_TITLE}")

        # ------------------------------------------
        # 모델 선택 컴포넌트 (Dropdown)
        # ------------------------------------------
        model_dropdown = gr.Dropdown(
            choices=list(MODEL_CONFIG.keys()),
            value="GPT-4.1 Mini",    # 기본 선택값
            label="LLM 모델"
        )

        # ------------------------------------------
        # 처리 방식 선택
        # ------------------------------------------

        mode_dropdown = gr.Dropdown(
            choices=[
                "AUTO", # 자동으로 RAG 또는 GPT 처리 방식 선택
                "RAG",  # RAG 방식으로 질문 처리 (문서 검색 + LLM 응답 생성)
                "GPT"   # GPT 방식으로 질문 처리 (문서 검색 없이 LLM 응답 생성)
            ],
            value="AUTO", # 기본 선택값
            label="질문 처리 방식"
        )

        # ------------------------------------------
        # Chatbot (대화 내역 디스플레이 컴포넌트)
        # ------------------------------------------
        chatbot = gr.Chatbot(
            height=500,                          # 대화창 세로 크기 고정
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

            # ------------------------------------------
            # 전송 버튼 컴포넌트
            # ------------------------------------------
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
                mode_dropdown,                   # chat()의 네 번째 인자 (선택된 처리 방식)
                session_state                    # chat()의 다섯 번째 인자 (사용자 세션 고유 ID)
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
                msg, chatbot, model_dropdown, mode_dropdown, session_state
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
        
        return demo

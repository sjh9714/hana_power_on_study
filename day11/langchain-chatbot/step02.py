# =========================================
# 라이브러리
# =========================================
import os
import gradio as gr

from fastapi import FastAPI

# LangChain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# =========================================
# LLM 생성
# =========================================

# LangChain 라이브러리에서 제공하는 클래스입니다. OpenAI에서 제공하는 챗봇 형태의 모델(Chat Model)을 생성하고 대화할 준비를 하겠다는 뜻입니다.
llm = ChatOpenAI(
    model="gpt-4.1-mini", # 사용할 AI 모델의 이름을 지정하는 부분입니다. 여기서는 gpt-4.1-mini라는 모델을 사용하겠다고 명시했습니다. 오타가 없다면 해당 버전의 가볍고 빠른(mini) GPT 모델을 호출하게 됩니다.
    api_key=os.getenv("OPENAI_API_KEY"), # OpenAI의 서비스를 이용하기 위한 인증 키(API Key)를 입력하는 부분입니다. 보안을 위해 코드에 키를 직접 적지 않고, 운영체제의 환경 변수(os.getenv)에 저장해둔 "OPENAI_API_KEY"라는 값을 자동으로 가져와 사용하도록 안전하게 작성되었습니다.
    temperature=0.7 # AI의 답변 성향(창의성 및 무작위성)을 조절하는 하이퍼파라미터입니다. 값은 보통 0에서 2 사이로 설정합니다.
)

# =========================================
# 채팅 함수
# =========================================

def chat(message, history):

    # 사용자 질문 생성
    messages = [
        # HumanMessage는 LangChain에서 사용자가 입력한 메시지(User Message) 를 나타내는 객체
        # OpenAI API에서 사용하는 동일한 의미라고 생각하면 됩니다.
        # { 
        #   "role": "user",
        #   "content": "안녕하세요"
        # }
        #
        HumanMessage(content=message)
    ]

    # GPT 호출, 동기화 함수, 응답이 길면 응답이 완료될때 까지 기다립니다. 
    response = llm.invoke(messages)

    return response.content


# =========================================
# Gradio ChatInterface
# =========================================

demo = gr.ChatInterface(
    fn=chat,
    title="LangChain ChatBot"
)

# =========================================
# FastAPI 생성
# =========================================

app = FastAPI()

# =========================================
# Gradio Mount
# =========================================

app = gr.mount_gradio_app(
    app,
    demo,
    path="/"
)

# =========================================
# 실행
# =========================================

# uvicorn step02:app --reload --host 0.0.0.0 --port 8000
from fastapi import FastAPI

# Gradio UI를 임포트하여 FastAPI 앱에 마운트
import gradio as gr

# Gradio UI 생성 함수 임포트
from ui.gradio_ui import (
    create_ui
)

# Gradio UI 객체 생성
demo = create_ui()

# FastAPI 앱 생성
app = FastAPI()

# Gradio UI를 FastAPI 앱에 마운트
app = gr.mount_gradio_app(
    app,
    demo,
    path="/"
)
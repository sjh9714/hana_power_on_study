from fastapi import FastAPI

# Import the Gradio UI and mount it to the FastAPI app
import gradio as gr

# Import the Gradio UI creation function
from day15.agri_rag_chatbot.ui.gradio_ui import (
    create_ui
)

#Gradio U I객체 생성
demo = create_ui()

# FastAPI 앱 생성
app = FastAPI()

# Gradio UI를 FastAPI 앱에 마운트
app = gr.mount_gradio_app(
    app,
    demo,
    path="/"
)
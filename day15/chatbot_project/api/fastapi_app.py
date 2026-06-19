from fastapi import FastAPI

import gradio as gr

from day15.chatbot_project.ui.gradio_ui import (
    create_ui
)

demo = create_ui()

app = FastAPI()

app = gr.mount_gradio_app(
    app,
    demo,
    path="/"
)
import time
import gradio as gr

def chat(message, history):

    text = "안녕하세요. 저는 AI입니다."

    partial = ""

    for c in text:
        partial += c
        time.sleep(0.05)
        yield partial

demo = gr.ChatInterface(chat)

demo.launch()
import gradio as gr

def chat(message, history):
    return f"당신이 입력한 내용: {message}"

demo = gr.ChatInterface(chat)

demo.launch()
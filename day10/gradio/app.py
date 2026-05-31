import gradio as gr

def greeting(name):
    return f"안녕하세요 {name}"

demo = gr.Interface(
    fn=greeting,
    inputs="text",
    outputs="text"
)

demo.launch()
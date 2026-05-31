from openai import OpenAI
import gradio as gr
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def chat(message, history):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"user",
                "content":message
            }
        ]
    )

    return response.choices[0].message.content

demo = gr.ChatInterface(chat)

demo.launch()
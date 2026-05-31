from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.chat.completions.create(
    model="gpt-5",
    temperature=0.7,
    messages=[
        {
            "role": "system",
            "content": "너는 친절한 AI 튜터이다."
        },
        {
            "role": "user",
            "content": "Docker란 무엇인가?"
        }
    ]
)

print(response.choices[0].message.content)
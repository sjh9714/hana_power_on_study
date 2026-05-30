from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

messages = [
    {
        "role": "system",
        "content": """
        너는 시니어 금융 AI 엔지니어이다.

        규칙:
        - Python 코드만 생성
        - XGBoost 사용
        - 실무 기준 적용
        """
    },
    {
        "role": "user",
        "content": """
        신용카드 이상거래 탐지 코드를 작성해줘
        """
    }
]

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages
)

print(response.choices[0].message.content)


# 실행 방법 
# python step6.py
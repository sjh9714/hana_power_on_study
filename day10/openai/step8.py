from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

question = "AI란 무엇인가?"

for temp in [0, 0.3, 0.7, 1.2]:

    response = client.chat.completions.create(
        model="gpt-5",
        temperature=temp,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    print("=" * 50)
    print(f"temperature = {temp}")
    print(response.choices[0].message.content)
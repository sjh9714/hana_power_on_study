import os
from langchain.tools import tool
from langchain.agents import create_agent

from langchain_openai import ChatOpenAI
import json

# ---------------------------------
# Tool
# ---------------------------------

@tool
def add(a: int, b: int) -> int:
    """두 숫자를 더한다."""
    print(f"\n[ADD] {a} + {b}")
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """두 숫자를 곱한다."""
    print(f"\n[MULTIPLY] {a} * {b}")
    return a * b


# ---------------------------------
# LLM
# ---------------------------------

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

# Tool 바인딩
llm_with_tools = llm.bind_tools(
    [add, multiply]
)

# 질문
response = llm_with_tools.invoke(
    "15와 20을 더해줘"
)

# 결과 확인
print(json.dumps(response.model_dump(), indent=4, ensure_ascii=False))
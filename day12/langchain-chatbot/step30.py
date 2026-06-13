from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


# ----------------------------
# Tool
# ----------------------------

@tool
def add(a: int, b: int) -> int:
    """두 숫자를 더한다."""
    print(f"\n[TOOL] add({a}, {b})")
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """두 숫자를 곱한다."""
    print(f"\n[TOOL] multiply({a}, {b})")
    return a * b


# ----------------------------
# LLM
# ----------------------------

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

# ----------------------------
# Agent
# ----------------------------

agent = create_agent(
    model=llm,
    tools=[add, multiply],
    system_prompt="""
    너는 계산 전문가이다.
    반드시 Tool을 사용하여 계산하라.
    """
)

# ----------------------------
# Stream 실행
# ----------------------------

for chunk in agent.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "15와 20을 더한 후 2를 곱해줘"
            }
        ]
    }
):
    print("\n====================")
    print(chunk)
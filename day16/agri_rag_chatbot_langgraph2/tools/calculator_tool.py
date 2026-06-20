from langchain.tools import tool

@tool
def calculator(expression: str):
    """
    수식을 계산
    """

    print("\n[Calculator Tool 실행]")
    print(f"수식: {expression}")

    return str(eval(expression))


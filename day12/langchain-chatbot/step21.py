# pip install langchain_core
from langchain_core.runnables import RunnablePassthrough

# RunnablePassthrough: 입력을 그대로 출력하는 LCEL Runnable
chain = RunnablePassthrough()

# LCEL Runnable 실행
result = chain.invoke(
    "안녕하세요"
)

# 결과 출력
print(result)

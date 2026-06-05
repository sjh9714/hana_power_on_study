from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda
)

# LCEL Runnable 체인 구성
chain = {
    "name": RunnablePassthrough(),

    "message": RunnableLambda(
        lambda x: f"{x}님 반갑습니다."
    )
}

# LCEL Runnable 체인 실행
result = chain.invoke(
    "홍길동"
)

# 결과 출력
print(result)

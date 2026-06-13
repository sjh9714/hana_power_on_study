from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)

# LCEL Runnable 체인 구성
chain = RunnableParallel({
    "context": RunnableLambda(
        lambda x: f"검색 결과: {x}"
    ),

    "question": RunnablePassthrough()
})

# LCEL Runnable 체인 실행
print(
    chain.invoke("RAG란?")
)

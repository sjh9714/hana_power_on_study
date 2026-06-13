from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda

chain = RunnablePassthrough()

print("RunnablePassthrough 결과 : ")
print(
    chain.invoke(10)
)

chain = RunnableLambda(
    lambda x: x * 10
)

print("RunnableLambda 결과 : ")
print(
    chain.invoke(10)
)
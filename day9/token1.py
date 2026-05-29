import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o")

text = "안녕하세요. LLM을 공부하고 있습니다."

tokens = encoding.encode(text)

print("토큰 수:", len(tokens))
print(tokens)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from prompts.loader import promprt_loader


# Load prompt from prompts/rag_prompt.txt and split into system/human parts
raw = promprt_loader("rag_prompt")
parts = raw.split("\n---\n", 1)
if len(parts) == 2:
    system_text, human_text = parts[0].strip(), parts[1].strip()
else:
    system_text = "당신은 스마트농업 전문가입니다.\n반드시 제공된 문서 내용만 사용하세요."
    human_text = "문서:\n{context}\n\n질문:\n{query}\n\n참고 문서:\n{page_text}"


rag_prompt = ChatPromptTemplate.from_messages([
    ("system", system_text),
    MessagesPlaceholder("history"),
    ("human", human_text),
])

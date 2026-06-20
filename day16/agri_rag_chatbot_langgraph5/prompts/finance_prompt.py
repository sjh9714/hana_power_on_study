from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from prompts.loader import promprt_loader


# Load finance prompt and split by '---' into system/human
raw = promprt_loader("finance_prompt")
parts = raw.split("\n---\n", 1)
if len(parts) == 2:
    system_text, human_text = parts[0].strip(), parts[1].strip()
else:
    system_text = "너는 친절한 금융 전문 AI 비서이다."
    human_text = "{question}"


prompt = ChatPromptTemplate.from_messages([
    ("system", system_text),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", human_text),
])
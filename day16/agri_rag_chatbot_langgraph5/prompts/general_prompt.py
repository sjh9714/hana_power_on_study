
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from prompts.loader import promprt_loader


# Load prompt text and split system/human by '---'
raw = promprt_loader("general_prompt")
parts = raw.split("\n---\n", 1)
if len(parts) == 2:
    system_text, human_text = parts[0].strip(), parts[1].strip()
else:
    system_text = "질문에 친절하게 답변하세요."
    human_text = "{query}"


general_prompt = ChatPromptTemplate.from_messages([
    ("system", system_text),
    MessagesPlaceholder("history"),
    ("human", human_text),
])

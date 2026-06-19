
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# general_prompt는 LLM에게 일반적인 질문에 답변하도록 지시하는 프롬프트입니다.
general_prompt = ChatPromptTemplate.from_messages([
    ("system","질문에 친절하게 답변하세요."),   # 시스템 메시지로, LLM에게 질문에 친절하게 답변하도록 지시하는 역할을 합니다. 이렇게 함으로써, 모델이 보다 친절하고 도움이 되는 응답을 생성하도록 유도할 수 있습니다.     
    MessagesPlaceholder("history"),             # MessagesPlaceholder는 대화 히스토리를 프롬프트에 포함시키는 역할을 합니다. "history"라는 변수 이름으로 대화 히스토리를 참조할 수 있도록 설정되어 있습니다. 이렇게 함으로써, 모델이 이전 대화 내용을 참조하여 보다 일관되고 맥락에 맞는 응답을 생성할 수 있도록 합니다.    
    ("human","{query}")                         # 사용자 메시지로, "{query}"라는 플레이스홀더를 사용하여 사용자 질문을 프롬프트에 포함시키는 역할을 합니다. 이렇게 함으로써, 모델이 사용자 질문을 입력으로 받아서 해당 질문에 대한 응답을 생성할 수 있도록 합니다.  
])

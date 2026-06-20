from day15.chatbot_project.prompts.finance_prompt import prompt

from day15.chatbot_project.llms.llm_factory import (
    get_llm
)

from day15.chatbot_project.memory.session_memory import (
    get_session_history
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from langchain_core.runnables.history import (
    RunnableWithMessageHistory
)

def create_chain(selected_model):

    llm = get_llm(selected_model)

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history"
    )
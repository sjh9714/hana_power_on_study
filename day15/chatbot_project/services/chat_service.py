from day15.chatbot_project.chains.chat_chain import (
    create_chain
)

def chat(
    message,
    history,
    selected_model,
    session_id
):

    if history is None:
        history = []

    chain = create_chain(
        selected_model
    )

    history.append(
        {
            "role": "user",
            "content": message
        }
    )

    history.append(
        {
            "role": "assistant",
            "content": ""
        }
    )

    partial = ""

    for chunk in chain.stream(
        {
            "question": message
        },
        config={
            "configurable": {
                "session_id": session_id
            }
        }
    ):

        partial += chunk

        history[-1]["content"] = partial

        yield history, ""
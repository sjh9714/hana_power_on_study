from langchain_openai import ChatOpenAI

import os

from day15.retrievers_refactoring.config.settings import (
    OPENAI_MODEL
)

def get_llm():

    return ChatOpenAI(
        model=OPENAI_MODEL,
        api_key=os.getenv(
            "OPENAI_API_KEY"
        ),
        temperature=0
    )
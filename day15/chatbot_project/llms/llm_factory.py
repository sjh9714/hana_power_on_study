import os

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from day15.chatbot_project.config.settings import (
    MODEL_CONFIG,
    DEFAULT_TEMPERATURE
)

def get_llm(selected_model):

    config = MODEL_CONFIG[selected_model]

    if config["provider"] == "openai":

        return ChatOpenAI(
            model=config["model"],
            api_key=os.getenv(
                "OPENAI_API_KEY"
            ),
            temperature=DEFAULT_TEMPERATURE,
            streaming=True
        )

    return ChatGoogleGenerativeAI(
        model=config["model"],
        google_api_key=os.getenv(
            "GOOGLE_API_KEY"
        ),
        temperature=DEFAULT_TEMPERATURE,
        streaming=True
    )
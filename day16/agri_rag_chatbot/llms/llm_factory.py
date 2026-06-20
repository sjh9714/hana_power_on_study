
import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from day16.agri_rag_chatbot.config.settings import MODEL_CONFIG, DEFAULT_TEMPERATURE

# get_llm() 함수는 선택된 모델 정보를 기반으로 적절한 LLM 객체를 생성하여 반환하는 역할을 합니다.
# MODEL_CONFIG 딕셔너리에서 선택된 모델의 정보를 가져와서, 해당 모델의 제공자(provider)에 따라 ChatOpenAI 또는 ChatGoogleGenerativeAI 객체를 생성하여 반환합니다.
# OpenAI 모델인 경우, OPENAI_API_KEY 환경 변수를 사용하여 API 키를 설정하고, 
# Google Generative AI 모델인 경우 GOOGLE_API_KEY 환경 변수를 사용하여 API 키를 설정합니다. 
# 또한, 생성된 LLM 객체는 DEFAULT_TEMPERATURE 값을 사용하여 응답의 창의성 수준을 조절하도록 설정됩니다.    
# 이 함수는 Gradio UI에서 사용자가 선택한 모델에 따라 적절한 LLM 객체를 생성하여, 이후 체인 생성 시 해당 LLM을 사용하여 응답을 생성할 수 있도록 합니다.
def get_llm(selected_model):
    config = MODEL_CONFIG[selected_model]

    if config["provider"] == "openai":  
        return ChatOpenAI(
            model=config["model"],   # MODEL_CONFIG에서 선택된 모델의 이름을 가져와서 ChatOpenAI 객체를 생성할 때 사용합니다. 예를 들어, "gpt-4.1-mini"와 같은 모델 이름이 될 수 있습니다.
            api_key=os.getenv("OPENAI_API_KEY"), # OPENAI_API_KEY 환경 변수를 사용하여 OpenAI API 키를 설정합니다. 이렇게 함으로써, API 키가 코드에 하드코딩되지 않고, 환경 변수로 관리되어 보안성이 향상됩니다.    
            temperature=DEFAULT_TEMPERATURE,     # 응답의 창의성 수준을 조절하는 temperature 값을 설정합니다. DEFAULT_TEMPERATURE는 config/settings.py 파일에서 정의된 상수로, 일반적으로 0.7과 같은 값이 사용됩니다. 이 값을 높이면 모델의 응답이 더 창의적이고 다양해 지고, 낮추면 더 일관되고 예측 가능한 응답이 생성됩니다.  
            streaming=True                       # streaming=True로 설정하여, 모델의 응답을 스트리밍 방식으로 받아올 수 있도록 합니다. 이렇게 하면, 모델이 응답을 생성하는 동안 실시간으로 청크 단위로 응답을 받아올 수 있어서, UI에 실시간으로 업데이트할 수 있습니다. 
        )

    return ChatGoogleGenerativeAI(
        model=config["model"],       # MODEL_CONFIG에서 선택된 모델의 이름을 가져와서 ChatGoogleGenerativeAI 객체를 생성할 때 사용합니다. 예를 들어, "gemini-2.5-flash"와 같은 모델 이름이 될 수 있습니다.  
        google_api_key=os.getenv("GOOGLE_API_KEY"), # GOOGLE_API_KEY 환경 변수를 사용하여 Google Generative AI API 키를 설정합니다. 이렇게 함으로써, API 키가 코드에 하드코딩되지 않고, 환경 변수로 관리되어 보안성이 향상됩니다.   
        temperature=DEFAULT_TEMPERATURE,            # 응답의 창의성 수준을 조절하는 temperature 값을 설정합니다. DEFAULT_TEMPERATURE는 config/settings.py 파일에서 정의된 상수로, 일반적으로 0.7과 같은 값이 사용됩니다. 이 값을 높이면 모델의 응답이 더 창의적이고 다양해 지고, 낮추면 더 일관되고 예측 가능한 응답이 생성됩니다.
        disable_streaming=False                     # Google Generative AI 모델의 경우, disable_streaming=False로 설정하여 스트리밍 방식으로 응답을 받아올 수 있도록 합니다. 이렇게 하면, 모델이 응답을 생성하는 동안 실시간으로 청크 단위로 응답을 받아올 수 있어서, UI에 실시간으로 업데이트할 수 있습니다.   
    )

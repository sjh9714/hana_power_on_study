
from day15.agri_rag_chatbot.chains.router_chain import create_chain

# 비즈니스 로직 함수 (사용자 입력 처리 및 모델 응답 생성) 임포트
# chat() 함수는 Gradio UI에서 사용자 입력이 제출될 때 호출되는 핵심 함수입니다.
# 이 함수는 사용자 메시지, 대화 히스토리, 선택된 모델과
# 처리 방식을 인자로 받아서, create_chain() 함수를 사용하여 적절한 체인을 생성하고,
# 모델의 응답을 스트리밍 방식으로 받아서 대화 히스토리를 업데이트하면서 실시간으로 UI에 반환하는 역할을 합니다.
def chat(message,           # 사용자 입력 메시지
         history,           # 대화 히스토리 (이전 메시지와 응답을 포함하는 리스트)
         selected_model,    # 사용자가 선택한 모델 (예: "GPT-4.1 Mini", "Gemini 2.5 Flash" 등)
         selected_mode,     # 사용자가 선택한 처리 방식 (예: "AUTO", "RAG", "GPT" 등)
         session_id):       # 세션 ID (사용자 고유 상태값 관리)

    # 대화 히스토리가 None인 경우 빈 리스트로 초기화
    # Gradio는 상태값이 없는 경우 None으로 전달하기 때문에, 이 경우 빈 리스트로 초기화하여 이후 대화 히스토리를 관리할 수 있도록 합니다.
    if history is None:
        history = []

    # create_chain() 함수를 사용하여 적절한 체인을 생성합니다.
    # 선택된 모델과 처리 방식에 따라 내부적으로 RAG 체인, GPT 체인, 또는 라우터 체인이 생성됩니다.
    # 생성된 체인은 이후 모델의 응답을 스트리밍 방식으로 받아서 대화 히스토리를 업데이트하는 데 사용됩니다.
    chain = create_chain(
        selected_model,   # 사용자가 선택한 모델
        selected_mode,    # 사용자가 선택한 처리 방식
        message           # 사용자 입력 메시지 (체인 생성 시 참고용으로 전달, 실제 체인 내부에서 사용 여부는 체인 구현에 따라 다름)
    )

    # 사용자 메시지를 대화 히스토리에 추가 (역할: "user")
    # 사용자가 입력한 메시지를 대화 히스토리에 추가하여, 이후 모델의 응답과 함께 대화 흐름을 관리할 수 있도록 합니다.
    # 모델의 응답이 생성되는 동안, 마지막 메시지의 역할을 "assistant"로 추가하여 모델의 응답이 생성되는 동안 대화 히스토리를 실시간으로 업데이트할 수 있도록 합니다.
    history.append({"role":"user","content":message})
    history.append({"role":"assistant","content":""})

    partial = ""

    # 모델의 응답을 스트리밍 방식으로 받아서 대화 히스토리를 업데이트하면서 실시간으로 UI에 반환합니다.
    # chain.stream() 메서드는 모델의 응답을 스트리밍 방식으로 받아올 수 있도록 하는 제너레이터입니다.
    # 각 응답 청크가 도착할 때마다 partial 변수에 누적하여 저장하고, 대화 히스토리의 마지막 메시지(역할: "assistant")의 content를 업데이트하여 실시간으로 UI에 반환합니다.
    for chunk in chain.stream(
        {"query": message},
        config={ # 모델 체인 실행 시 참고할 수 있는 추가 설정값 (예: session_id 등)을 전달할 수 있는 딕셔너리입니다. 필요에 따라 체인 내부에서 참조하여 세션 관리, 로깅, 디버깅 등에 활용할 수 있습니다.
            "configurable":{ 
                "session_id": session_id
            }
        }
    ):
        # 모델의 응답 청크가 도착할 때마다 partial 변수에 누적하여 저장하고, 대화 히스토리의 마지막 메시지(역할: "assistant")의 content를 업데이트하여 실시간으로 UI에 반환합니다.
        partial += str(chunk)

        # 대화 히스토리의 마지막 메시지(역할: "assistant")의 content를 업데이트하여 실시간으로 UI에 반환합니다.
        history[-1]["content"] = partial

        # 현재까지의 대화 히스토리를 UI에 반환합니다. Gradio는 이 반환값을 받아서 챗봇 인터페이스에 실시간으로 업데이트합니다.
        yield history, ""

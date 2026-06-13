from openai import OpenAI
import os

# 환경 변수에서 OpenAI API 키를 가져옵니다.
api_key = os.getenv('OPENAI_API_KEY')

def summarize_txt(file_path: str): # ① 텍스트 파일을 입력받아 요약하는 함수 정의
    # OpenAI 클라이언트 인스턴스를 생성합니다.
    client = OpenAI(api_key=api_key)

    # ② 지정된 경로의 텍스트 파일을 '읽기(r)' 모드로 열어 내용을 가져옵니다.
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    # ③ LLM(대형 언어 모델)에게 전달할 시스템 프롬프트를 구성합니다.
    # 역할(요약 봇), 수행할 작업(문제 인식 및 주장 파악), 출력 포맷을 명시하고 본문을 삽입합니다.
    system_prompt = f'''
    너는 다음 글을 요약하는 봇이다. 아래 글을 읽고, 저자의 문제 인식과 주장을 파악하고, 주요 내용을 요약하라. 

    작성해야 하는 포맷은 다음과 같다. 
    
    # 제목

    ## 저자의 문제 인식 및 주장 (15문장 이내)
    
    ## 저자 소개

    
    =============== 이하 텍스트 ===============

    { txt }
    '''

    # 프롬프트 구성이 잘 되었는지 콘솔에 출력하여 확인합니다.
    print(system_prompt)
    print('=========================================')

    # ④ OpenAI API의 Chat Completions 엔드포인트를 호출하여 요약을 요청합니다.
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # 사용할 모델을 지정합니다.
        temperature=0.1,       # 답변의 일관성과 정형성을 높이기 위해 낮은 온도로 설정합니다.
        messages=[
            {"role": "system", "content": system_prompt}, # 시스템 역할을 부여하고 프롬프트를 전달합니다.
        ]
    )

    # 생성된 답변 결과 텍스트만 추출하여 반환합니다.
    return response.choices[0].message.content

# 요약할 대상 파일의 경로를 설정합니다.
file_path = 'output/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축_with_preprocessing2.txt'

# 함수를 호출하여 요약 작업을 수행하고 결과를 변수에 저장합니다.
summary = summarize_txt(file_path)
print(summary)

# ⑤ 요약이 완료된 텍스트 내용을 새로운 파일로 저장합니다.
with open('output/crop_model_summary.txt', 'w', encoding='utf-8') as f:
    f.write(summary)
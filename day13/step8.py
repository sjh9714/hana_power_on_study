from openai import OpenAI
import os
# LangChain의 토큰 기반 텍스트 스플리터 임포트
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 환경 변수에서 OpenAI API 키를 가져옵니다.
api_key = os.getenv('OPENAI_API_KEY')

# 1. OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

def read_text_file(file_path: str) -> str:
    """지정된 경로의 텍스트 파일을 읽어 내용을 반환하는 함수"""
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
    return txt

# -------------------------------------------------------------
# [수정] LangChain의 tiktoken 기반 스플리터를 사용하는 함수
# -------------------------------------------------------------
def chunk_text_by_tokens(text: str, max_tokens: int = 3000, overlap_tokens: int = 200):
    """
    tiktoken 인코더를 사용하여 텍스트를 안전하게 토큰 단위로 나누는 함수.
    줄바꿈(\n\n, \n), 공백 등 자연스러운 경계를 우선시하여 분할합니다.
    """
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4o",      # 사용할 모델 계열의 인코더 지정 (gpt-4.1-mini, gpt-4o 등 호환)
        chunk_size=max_tokens,    # 한 청크당 최대 토큰 수
        chunk_overlap=overlap_tokens # 청크 간 겹치는 토큰 수 (문맥 유실 방지)
    )
    
    # split_text는 문자열 리스트를 반환합니다.
    chunks = text_splitter.split_text(text)
    return chunks
# -------------------------------------------------------------

def summarize_chunk(text_chunk):
    """각 텍스트 조각을 요약하는 함수 (Map 단계)"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # 혹은 사용하시는 gpt-4o-mini 등
        messages=[
            {
                "role": "system", 
                "content": "당신은 전문 AI 연구원입니다. 제공된 논문 텍스트 조각의 핵심 연구 내용, 방법론, 수치적 성과를 누락 없이 상세히 요약하세요."
            },
            {"role": "user", "content": f"다음 논문 내용을 요약해 주세요:\n\n{text_chunk}"}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content

def final_comprehensive_summary(summary_list):
    """분할 요약된 결과물들을 하나로 모아 최종 논문 보고서 형태로 정제하는 함수 (Reduce 단계)"""
    combined_summary = "\n\n".join(summary_list)
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system", 
                "content": (
                    "당신은 수석 연구원입니다. 분할 요약된 논문 내용들을 종합하여 "
                    "구조화된 최종 연구 보고서를 작성하세요. "
                    "반드시 다음 구조를 포함해야 합니다:\n"
                    "1. 연구 배경 및 목적 (Introduction)\n"
                    "2. 제안 방법론 및 핵심 알고리즘 (Methodology)\n"
                    "3. 실험 결과 및 주요 성과 (Results)\n"
                    "4. 결론 및 향후 연구 방향 (Conclusion)"
                )
            },
            {"role": "user", "content": f"다음은 논문의 파트별 요약본입니다. 이를 종합하여 최종 보고서를 작성해 주세요:\n\n{combined_summary}"}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def ai_researcher_pipeline(txt_file_path):
    """전체 논문 요약 파이프라인 실행 함수"""
    raw_text = read_text_file(txt_file_path)
    
    print("2. 텍스트 토큰 청킹 진행 중...")
    # [수정] 글자 수 기준(5000자)에서 토큰 수 기준(3000 토큰)으로 변경
    # OpenAI API 입력 제한을 안전하게 맞추기 위해 3000~4000 토큰 수준이 적당합니다.
    chunks = chunk_text_by_tokens(raw_text, max_tokens=3000, overlap_tokens=200)
    print(f"총 {len(chunks)} 개의 텍스트 블록이 생성되었습니다.")
    
    print("3. 파트별 개별 요약 진행 중...")
    partial_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"[{i+1}/{len(chunks)}] 블록 요약 중...")
        summary = summarize_chunk(chunk)
        partial_summaries.append(summary)
        
    print("4. 최종 종합 보고서 생성 중...")
    final_report = final_comprehensive_summary(partial_summaries)
    
    return final_report


# 요약할 대상 파일의 경로를 설정합니다.
file_path = 'output/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축_with_preprocessing2.txt'

# 함수를 호출하여 요약 작업을 수행하고 결과를 변수에 저장합니다.
summary = ai_researcher_pipeline(file_path)
print("\n--- 최종 요약 보고서 결과 ---")
print(summary)

# ⑤ 요약이 완료된 텍스트 내용을 새로운 파일로 저장합니다.
with open('output/crop_model_chunk_summary2.txt', 'w', encoding='utf-8') as f:
    f.write(summary)
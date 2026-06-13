from openai import OpenAI
import os

# 환경 변수에서 OpenAI API 키를 가져옵니다.
api_key = os.getenv('OPENAI_API_KEY')

# 1. OpenAI 클라이언트 초기화
# 환경 변수에 OPENAI_API_KEY가 설정되어 있어야 합니다. (os.environ["OPENAI_API_KEY"])
client = OpenAI(api_key=api_key)

def read_text_file(file_path: str) -> str:
    """지정된 경로의 텍스트 파일을 읽어 내용을 반환하는 함수"""
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
    return txt


def chunk_text(text, max_chars=5000):
    """컨텍스트 한계를 고려하여 텍스트를 일정 글자 수 단위로 나누는 함수"""
    chunks = []
    current_chunk = ""
    
    # 문장이나 줄바꿈 기준으로 분할하여 단락이 깨지는 것을 방지
    for line in text.split('\n'):
        if len(current_chunk) + len(line) < max_chars:
            current_chunk += line + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
            
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def summarize_chunk(text_chunk):
    """각 텍스트 조각을 요약하는 함수 (Map 단계)"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # 또는 gpt-4o
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
    
    print("2. 텍스트 청킹 진행 중...")
    chunks = chunk_text(raw_text, max_chars=5000)
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
print(summary)

# ⑤ 요약이 완료된 텍스트 내용을 새로운 파일로 저장합니다.
with open('output/crop_model_chunk_summary.txt', 'w', encoding='utf-8') as f:
    f.write(summary)
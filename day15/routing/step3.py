################################################
# 예제3 Hybrid Search Routing
# ################################################
# Hybrid Search Routing은 RAG 시스템에서 가장 많이 사용하는 라우팅 방식입니다.
# 핵심 아이디어는 매우 간단합니다.
# 질문을 보고
#   - 외부 지식/문서 검색이 필요한 질문 → RAG 경로로 분기
#   - 검색이 필요 없는 일반적인 질문 → 오직 LLM(GPT) 지식으로만 답변하도록 분기
# 으로 분기하는 것입니다.

# 1. 질문의 키워드를 분석하여 'RAG'로 갈지 'GPT'로 갈지 결정하는 라우터 클래스
class HybridRouter:
    def route(self, question):
        # 외부 문서 참조가 필요함을 암시하는 핵심 키워드 목록 정의
        keywords = [
            "논문",
            "문서",
            "보고서",
            "매뉴얼",
            "PDF"
        ]

        # 질문에 지정된 키워드 중 하나라도 포함되어 있는지 순차적으로 확인
        for keyword in keywords:
            if keyword in question:
                return "rag"  # 키워드가 매칭되면 RAG 파이프라인 문자열 반환

        return "gpt"  # 매칭되는 키워드가 없으면 순수 LLM 파이프라인 문자열 반환
    
# 2. 외부 데이터 검색 없이 오직 내부 파라미터 지식(LLM)으로만 답변을 생성하는 함수
def gpt_chain(question):
    return f"""
GPT 답변 생성
질문:
{question}
"""    

# 3. Vector DB 등에서 관련 문서를 찾은(Retrieval) 뒤 이를 참고하여 답변을 생성하는 함수
def rag_chain(question):
    return f"""
RAG 검색 수행
질문
{question}
유사 문서 검색 완료
답변 생성
"""

# ================================================
# 실행부 (Execution)
# ================================================

# 라우터 객체 인스턴스 생성
router = HybridRouter()

# 사용자 요청 쿼리 정의
question = "이 논문 설명해줘"

# 1. 라우터를 통해 어떤 파이프라인 경로(Path)를 탈지 결정
# 여기서는 질문에 "논문"이 포함되어 있으므로 path에 "rag"가 저장됨
path = router.route(question)
print(path)  # 출력: rag

# 2. 결정된 경로(path)에 따라 적절한 체인(함수)을 호출하여 최종 답변 생성
if path == "rag":
    answer = rag_chain(question)  # 외부 검색 엔진 가동 및 LLM 결합
else:
    answer = gpt_chain(question)  # 순수 LLM 처리

# 3. 최종 결과 출력
print(answer)

# 실행 방법
# python step3.py
#
# 결과
#
#rag
# RAG 검색 수행
# 질문
# 이 논문 설명해줘
# 유사 문서 검색 완료
# 답변 생성
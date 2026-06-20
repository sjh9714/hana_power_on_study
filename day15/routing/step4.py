################################################
# 예제4 Prompt Routing
# ################################################

# 1. 도메인별 프롬프트 템플릿 정의 (시스템 역할 부여)

# 농업 관련 질문일 때 사용할 프롬프트 템플릿
agri_prompt = """
당신은 농업전문가입니다.
질문:
{question}
"""

# 개발/인프라 관련 질문일 때 사용할 프롬프트 템플릿
dev_prompt = """
당신은 DevOps 전문가입니다.
질문:
{question}
"""

# 2. 질문에 따라 적절한 프롬프트 템플릿을 선택하는 라우터 클래스
class PromptRouter:
    def route(self, q):
        # 질문(q)에 "밀"이라는 단어가 포함되어 있으면 농업 프롬프트 템플릿 반환
        if "밀" in q:
            return agri_prompt
        # 포함되어 있지 않으면 기본값으로 DevOps 프롬프트 템플릿 반환
        return dev_prompt
    

# 3. 실제 실행 흐름

# 프롬프트 라우터 객체 생성
router = PromptRouter()

# 테스트용 질문 설정
q = "밀 재배 방법"

# 라우터에게 질문을 전달하여 알맞은 프롬프트 템플릿(문자열)을 받아옴
# (여기서는 "밀"이 포함되어 있으므로 agri_prompt가 선택됨)
prompt = router.route(q)

# 선택된 프롬프트 템플릿의 {question} 자리에 실제 질문(q)을 삽입(Format)하여 최종 프롬프트 완성
prompt_format = prompt.format(question=q)

# 완성된 프롬프트 출력
print(prompt_format)

# 실행 방법
# python step3.py
# 
# 결과 
# 
# 당신은 농업전문가입니다.
# 질문:

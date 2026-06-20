################################################
# 예제8 Agent Routing
# ################################################

# 1. 농업 도메인 지식을 담당하는 전문 에이전트
class AgriAgent:
    def invoke(self, query):
        return "농업 Agent"

# 2. 금융/주식 도메인 지식을 담당하는 전문 에이전트
class FinanceAgent:
    def invoke(self, query):
        return "금융 Agent"

# 3. 개발/IT 관련 질문이나, 다른 에이전트에 해당하지 않는 기본 요청을 처리하는 에이전트
class DevAgent:
    def invoke(self, query):
        return "개발 Agent"
    

# 4. 사용자의 질문 내용에 따라 가장 적절한 전문 에이전트를 매칭해주는 라우터 클래스
class AgentRouter:
    def route(self, query):
        # 질문에 "주식" 또는 "주가"라는 단어가 하나라도 포함되어 있다면 금융 에이전트로 라우팅
        if any(op in query for op in ["주식", "주가"]):
            return FinanceAgent()

        # 질문에 "밀"이라는 단어가 포함되어 있다면 농업 에이전트로 라우팅
        elif "밀" in query:
            return AgriAgent()

        # 위의 어떤 조건에도 해당하지 않는 모든 질문은 기본적으로 개발 에이전트가 처리 (Fallback Agent)
        return DevAgent()    


# ================================================
# 실행부 (Execution)
# ================================================

# 에이전트 라우터 인스턴스 생성
router = AgentRouter()

# 사용자 요청 쿼리 정의
query = "삼성전자 주가"

# 1. 라우터에게 쿼리를 전달하여 적절한 에이전트를 선정받음
# 여기서는 query에 "주가"가 포함되어 있으므로 FinanceAgent 객체가 반환됨
agent = router.route(query)

# 2. 매칭된 에이전트가 존재한다면 해당 에이전트의 invoke 메서드를 실행하여 최종 답변을 얻음
if agent:
    result = agent.invoke(query)  # FinanceAgent.invoke("삼성전자 주가")가 호출됨
    print(result)                 # 결과 출력: "금융 Agent"

# 실행 방법
# python step6.py
#
# 결과
#
# 금융 Agent


## Retriever Router와 Agent Router 핵심 차이점
#
# * **Retriever Router (문서 네비게이터)**
# * **생성자에서 미리 만드는 이유:** Vector DB 연결, 임베딩 모델 로드 등은 비용이 크기 때문에 프로그램이 켜질 때 한 번만 생성(`__init__`)해두고 돌려쓰는 것이 효율적입니다.
# * **본질:** LLM이 답변을 잘할 수 있도록 "올바른 참고서적(데이터)을 찾아서 펼쳐주는 역할"입니다.
#
# * **Agent Router (작업 반장)**
# * **`route`에서 매번 생성하는 이유 (혹은 에이전트 객체를 받는 이유):** 에이전트는 사용자의 질문을 받고 "1단계: 검색, 2단계: 계산, 3단계: 요약"과 같이 여러 단계의 상태(State)를 거치며 실행되므로, 이전 질문의 상태가 꼬이지 않도록 독립적인 객체로 다루는 경우가 많습니다.
# * **본질:** 질문을 해결하기 위해 "스스로 계획을 세우고 도구를 사용해 임무를 완수하는 독립적인 AI를 지정하는 역할"입니다.
#
# 즉, 외관상으로는 똑같이 객체를 전달하는 `if-else` 분기문처럼 보이지만, **Retriever는 '데이터 검색기'를 토스하는 것이고, Agent는 '지능형 해결사'를 토스하는 것**이라는 비즈니스 로직의 스코프 차이가 존재합니다.

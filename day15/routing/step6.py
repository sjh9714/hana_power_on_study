################################################
# 예제6 Tool Routing
# ################################################

# 1. 계산기 기능을 담당하는 도구(Tool) 클래스
class Calculator:
    def invoke(self, query):
        # eval(): 문자열로 된 수식(예: "10*30+20")을 실제로 계산하여 결과를 반환
        return eval(query)

# 2. 날씨 정보를 제공하는 도구(Tool) 클래스
class Weather:
    def invoke(self, query):
        # 날씨 관련 질문이 들어오면 고정된 날씨 정보를 반환 (Mock 데이터)
        return "서울 25도"


# 3. 사용자의 입력(Query)을 분석하여 적절한 도구로 연결해주는 라우터 클래스
class ToolRouter:
    def route(self, query):
        # any()를 활용해 사칙연산 기호(["*", "+", "-", "/"]) 중 하나라도 query에 포함되어 있는지 검사
        if any(op in query for op in ["*", "+", "-", "/"]):
            return Calculator()  # 연산 기호가 있으면 Calculator 객체 반환
        
        # 질문에 "날씨"라는 단어가 포함되어 있는지 검사
        if "날씨" in query:
            return Weather()     # "날씨"가 포함되어 있으면 Weather 객체 반환
            
        return None              # 일치하는 도구가 없으면 None 반환


# ================================================
# 실행부 (Execution)
# ================================================

# 라우터 인스턴스 생성
router = ToolRouter()

# 사용자 요청 쿼리 정의 (수식 입력)
query = "10*30+20"

# 1. 라우터를 통해 쿼리에 맞는 적절한 도구(Tool)를 추천받음
# 여기서는 query에 '*', '+'가 포함되어 있으므로 Calculator 객체가 반환됨
tool = router.route(query)

# 2. 매칭된 도구가 존재한다면 해당 도구의 invoke 메서드를 실행
if tool:
    result = tool.invoke(query)  # Calculator.invoke("10*30+20")가 호출되어 320이 저장됨
    print(result)                # if문 내부에서 결과 출력 (320)


# 실행 방법
# python step5.py
#
# 결과
#
# 320
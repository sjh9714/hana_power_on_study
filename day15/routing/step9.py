################################################
# 예제9  Multi Agent Routing
# ################################################

# 1. 기상 데이터를 전문적으로 수집하는 에이전트
class WeatherAgent:
    def invoke(self, question):
        print("날씨 정보 수집")
        # 기온, 강수량, 일조량 데이터를 딕셔너리 형태로 반환
        return {
            "temperature": 28,
            "rainfall": 120,
            "sunshine": 240
        }

# 2. 기상 데이터를 바탕으로 작물(밀)의 생육 상태를 분석하는 에이전트
class CropAgent:
    def invoke(self, weather):
        print("밀 생육 분석")
        growth = "양호"
        # 자신의 분석 결과(growth)와 전달받은 기상 데이터(weather)를 함께 묶어서 반환
        return {
            "growth": growth,
            "weather": weather
        }
    
# 3. 생육 상태 및 기상 데이터를 기반으로 예상 수확량을 계산하는 에이전트
class AnalysisAgent:
    def invoke(self, data):
        print("수확량 분석")
        yield_estimate = 7200
        # 계산된 수확량(yield)과 이전 단계까지의 모든 데이터(data)를 함께 반환
        return {
            "yield": yield_estimate,
            "data": data
        }

# 4. 최종 분석 결과를 사람이 읽기 좋은 텍스트 형식의 보고서로 작성하는 에이전트
class ReportAgent:
    def invoke(self, data):
        print("보고서 생성")
        # 중첩된 딕셔너리 구조에서 필요한 데이터(['yield'], ['data']['growth'])를 추출하여 문서 작성
        report = f"""
예상 수확량
{data['yield']} kg/ha

생육 상태
{data['data']['growth']}
"""
        return report
    
# 5. 전체 에이전트들의 실행 순서와 데이터 흐름을 총괄하는 관리자(Supervisor) 클래스
class Supervisor:
    def __init__(self):
        # 관리할 하위 전문 에이전트들을 생성자에서 미리 인스턴스화
        self.weather = WeatherAgent()
        self.crop = CropAgent()
        self.analysis = AnalysisAgent()
        self.report = ReportAgent()

    def invoke(self, question):
        # 파이프라인 형태로 데이터가 순차적으로 흐름 (A의 출력이 B의 입력이 됨)
        weather = self.weather.invoke(question)  # 1단계: 날씨 정보 수집
        crop = self.crop.invoke(weather)         # 2단계: 날씨를 기반으로 생육 분석
        analysis = self.analysis.invoke(crop)    # 3단계: 생육 상태를 기반으로 수확량 분석
        report = self.report.invoke(analysis)    # 4단계: 분석 데이터를 기반으로 보고서 생성
        
        return report    


# ================================================
# 실행부 (Execution)
# ================================================

# 슈퍼바이저(관리자) 객체 생성
supervisor = Supervisor()

# 사용자 요청 및 업무 시작
# 슈퍼바이저 내부에서 Weather -> Crop -> Analysis -> Report Agent가 체인처럼 순서대로 실행됨
result = supervisor.invoke("밀 수확량 예측 보고서")

# 최종 완성된 보고서 출력
print(result)

# 실행 방법
# python step9.py
#
# 결과
#
# 날씨 정보 수집
# 밀 생육 분석
# 수확량 분석
# 보고서 생성
# 
# 예상 수확량
# 7200 kg/ha
# 
# 생육 상태
# 양호
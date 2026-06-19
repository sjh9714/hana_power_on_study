################################################
# 예제2 Retriever Routing
# ################################################

# 1. 특정 도메인에 특화된 검색기(Retriever) 클래스 정의

# '밀' 관련 문서를 검색하는 리트리버
class WheatRetriever:
    def invoke(self, q):
        return "밀 문서 검색"

# '토양' 관련 문서를 검색하는 리트리버
class SoilRetriever:
    def invoke(self, q):
        return "토양 문서 검색"

# '병충해' 관련 문서를 검색하는 리트리버
class PestRetriever:
    def invoke(self, q):
        return "병충해 검색"


# 2. 질문을 분석하여 적절한 리트리버를 연결해주는 라우터 클래스
class RetrieverRouter:
    def __init__(self):
        # 라우터 클래스가 생성될 때, 위에서 정의한 3개의 리트리버 객체를 미리 생성하여 저장합니다.
        self.wheat = WheatRetriever()
        self.soil = SoilRetriever()
        self.pest = PestRetriever()

    def route(self, q):
        # 질문(q)에 "토양"이 포함되어 있으면 SoilRetriever 객체를 반환
        if "토양" in q:
            return self.soil

        # 질문(q)에 "병"이 포함되어 있으면 PestRetriever 객체를 반환
        elif "병" in q:
            return self.pest
        
        # 위 조건에 모두 해당하지 않으면 기본값으로 WheatRetriever 객체를 반환
        return self.wheat
    


# 3. 실제 실행 흐름

# 라우터 객체 생성
router = RetrieverRouter()

# 테스트용 질문 설정
query = "토양 산도"

# 라우터에게 질문을 던져 적절한 리트리버 객체를 받아옴 (여기서는 "토양"이 있으므로 SoilRetriever 객체가 반환됨)
retriever = router.route(query)

# 선택된 리트리버의 invoke 메서드를 호출하여 검색 결과(문서)를 가져옴
docs = retriever.invoke(query)

# 최종 검색 결과 출력 ("토양 문서 검색"이 출력됨)
print(docs)

# 실행 방법
# python step2.py
# 토양 문서 검색

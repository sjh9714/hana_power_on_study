################################################
# 예제5 Model Routing
# ################################################

# 1. 사용할 LLM 모델 클래스 정의

# 상대적으로 가볍고 비용이 저렴한 모델
class GPT4mini:
    def invoke(self, q):
        return "gpt4-mini"

# 무겁지만 고성능인 최신 모델
class GPT5:
    def invoke(self, q):
        return "gpt5"


# 2. 질문의 길이에 따라 적절한 모델을 선택하는 라우터 클래스
class Router:
    def route(self, q):
        # 질문(q)의 글자 수가 100자 미만으로 짧다면, 
        # 빠르고 가성비가 좋은 GPT4mini 객체를 생성하여 반환
        if len(q) < 100:
            return GPT4mini()

        # 질문이 100자 이상으로 길고 복잡하다면,
        # 고성능 처리를 위해 GPT5 객체를 생성하여 반환
        return GPT5()


# 3. 실제 실행 흐름

# 라우터 객체 생성
router = Router()

# 라우터에게 짧은 질문("안녕")을 던져 적절한 모델 객체를 받아옴
# (글자 수가 100자 미만이므로 GPT4mini 객체가 반환됨)
model = router.route("안녕")

# 선택된 모델의 invoke 메서드를 호출하여 답변을 생성
# (여기서는 가상의 문자열 "gpt4-mini"가 리턴됨)
print(model.invoke("안녕"))


# 실행 방법
# python step4.py
#
# 결과
#
# gpt4-mini
# transformers 라이브러리에서
# 토크나이저(AutoTokenizer)와 모델(AutoModel)을 가져옴
from transformers import AutoTokenizer, AutoModel

# PyTorch 라이브러리
import torch

# 사용할 사전학습 모델 지정
# KLUE(Korean Language Understanding Evaluation)용 BERT 모델
model_name = "klue/bert-base"

# ==========================================================
# 1. 토크나이저 로드
# ==========================================================
# 텍스트를 모델이 이해할 수 있는 토큰(Token)으로 변환
tokenizer = AutoTokenizer.from_pretrained(model_name)

# ==========================================================
# 2. 모델 로드
# ==========================================================
# 사전학습된 BERT 모델을 메모리에 적재
model = AutoModel.from_pretrained(model_name)

# ==========================================================
# 3. 임베딩할 문장 또는 단어
# ==========================================================
text = "고양이"

# ==========================================================
# 4. 토큰화(Tokenization)
# ==========================================================
# return_tensors="pt"
# → 결과를 PyTorch Tensor 형태로 반환
#
# 예)
# "고양이"
#
# inputs =
# {
#   'input_ids': tensor([[2, 5505, 3]]),
#   'token_type_ids': tensor([[0,0,0]]),
#   'attention_mask': tensor([[1,1,1]])
# }
#
inputs = tokenizer(
    text,
    return_tensors="pt"
)

# 토큰화 결과 확인
print("===== Tokenizer 결과 =====")
print(inputs)

# ==========================================================
# 5. 추론(Inference)
# ==========================================================
# no_grad()
# → 학습이 아닌 추론만 수행
# → 메모리 사용량 감소
# → 속도 향상
#
with torch.no_grad():
    outputs = model(**inputs)

# ==========================================================
# 6. 모델 출력 확인
# ==========================================================
#
# outputs.last_hidden_state
#
# shape:
# (배치크기, 토큰수, hidden_size)
#
# 예)
# torch.Size([1, 3, 768])
#
# 1 : 문장 개수
# 3 : [CLS] 고양이 [SEP]
# 768 : BERT 벡터 크기
#
print("\n===== 모델 출력 =====")
print(outputs.last_hidden_state.shape)

# ==========================================================
# 7. [CLS] 벡터 추출
# ==========================================================
#
# BERT 입력 형태
#
# [CLS] 고양이 [SEP]
#
# index
#   0      1      2
#
# [:,0,:]
# ↓
# 모든 배치에서
# 첫 번째 토큰([CLS])의
# 768차원 벡터 추출
#
vector = outputs.last_hidden_state[:, 0, :]

# ==========================================================
# 8. 결과 출력
# ==========================================================
print("\n===== CLS 벡터 =====")

# 벡터 크기
print("벡터 크기:", vector.shape)

# 벡터 일부 출력
print("벡터 일부:")
print(vector[0][:10])

# ==========================================================
# 9. 전체 벡터 확인
# ==========================================================
#
# tensor → numpy 변환
#
embedding = vector[0].numpy()

print("\n===== 전체 임베딩 정보 =====")
print("차원 수:", len(embedding))
print("최소값:", embedding.min())
print("최대값:", embedding.max())
print("평균값:", embedding.mean())
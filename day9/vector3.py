from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. 한국어/영어 모두 잘 지원하는 멀티링구얼 모델 로드
model = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 2. 문맥(Context)이 포함된 문장으로 정의
sentences = [
    "동물학적으로 분류했을 때 고양잇과에 속하는 고양이",  # 인덱스 0
    "동물학적으로 분류했을 때 고양잇과에 속하는 호랑이",      # 인덱스 1
]

# 3. 문장을 임베딩 벡터로 변환
embeddings = model.encode(sentences)

cat_vector = [embeddings[0]]
dog_vector = [embeddings[1]]
car_vector = [embeddings[2]]

# 4. 코사인 유사도 계산
cat_dog_sim = cosine_similarity(cat_vector, dog_vector)[0][0]
cat_car_sim = cosine_similarity(cat_vector, car_vector)[0][0]

# 5. 결과 출력
print("=== 문맥을 반영한 유사도 결과 ===")
print(f"고양이 ↔ 호랑이 유사도: {cat_dog_sim:.4f}")
print(f"고양이 ↔ 자동차 유사도: {cat_car_sim:.4f}")

#=== 단어 유사도 결과 ===
#고양이 ↔ 강아지 유사도: 0.1260
#=== 문맥을 반영한 유사도 결과 ===
#고양이 ↔ 강아지 유사도: 0.4136
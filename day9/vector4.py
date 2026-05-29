from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. 한국어/영어 모두 잘 지원하는 멀티링구얼 모델 로드
model = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 2. 문맥(Context)이 포함된 문장으로 정의
sentences = [
    "고양이",  # 인덱스 0
    "강아지",      # 인덱스 1
]

# 3. 문장을 임베딩 벡터로 변환
embeddings = model.encode(sentences)

cat_vector = [embeddings[0]]
dog_vector = [embeddings[1]]

# 4. 코사인 유사도 계산
cat_dog_sim = cosine_similarity(cat_vector, dog_vector)[0][0]

# 5. 결과 출력
print("=== 단어 유사도 결과 ===")
print(f"고양이 ↔ 강아지 유사도: {cat_dog_sim:.4f}")
    

# 2. 문맥(Context)이 포함된 문장으로 정의
sentences = [
    "고양이가 생선을 먹었다",  # 인덱스 0
    "강아지가 사료를 먹었다",      # 인덱스 1
]

# 3. 문장을 임베딩 벡터로 변환
embeddings = model.encode(sentences)

cat_vector = [embeddings[0]]
dog_vector = [embeddings[1]]

# 4. 코사인 유사도 계산
cat_dog_sim = cosine_similarity(cat_vector, dog_vector)[0][0]

# 5. 결과 출력
print("=== 문맥을 반영한 유사도 결과 ===")
print(f"고양이 ↔ 강아지 유사도: {cat_dog_sim:.4f}")
        
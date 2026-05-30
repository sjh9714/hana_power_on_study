import numpy as np

# ==========================================
# 단어 정의
# ==========================================

words = ["나는", "피자를", "먹었다"]

# ==========================================
# 임의의 벡터(Embedding)
# 실제로는 학습된 값이지만, 예시에서는 임의로 설정
# ==========================================

embeddings = np.array([
    [1, 0, 1],  # 나는
    [0, 2, 1],  # 피자를
    [1, 1, 2]   # 먹었다
])

print("=== Embedding ===")
for word, emb in zip(words, embeddings):
    print(word, emb)

# ==========================================
# Query = 먹었다
# ==========================================

query = embeddings[2]

print("\nQuery (먹었다):")
print(query)

# ==========================================
# Attention Score 계산
# Dot Product
# ==========================================

scores = []

for emb in embeddings:
    score = np.dot(query, emb)
    scores.append(score)

scores = np.array(scores)

print("\nAttention Scores")
for word, score in zip(words, scores):
    print(word, score)
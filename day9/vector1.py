from sentence_transformers import SentenceTransformer

# 한국어 지원 임베딩 모델
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

word = "고양이"

# 벡터 변환
vector = model.encode(word)

print("단어:", word)
print("벡터 길이:", len(vector))
print("벡터 일부:", vector[:10])
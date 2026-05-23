import pandas as pd
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ==========================================
# 1. seaborn 데이터 로드
# ==========================================

df = sns.load_dataset("iris")

print(df.head())

# ==========================================
# 2. CSV 저장
# ==========================================

df.to_csv(
    "iris.csv",
    index=False,
    encoding="utf-8-sig"
)

print("iris.csv 저장 완료")

# ==========================================
# 3. 입력(X) / 정답(y)
# ==========================================

# 정답 필드 삭제함  
X = df.drop("species", axis=1)

#정답 필드 
y = df["species"]

# ==========================================
# 4. 학습 / 테스트 분리
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# 5. 모델 생성
# ==========================================

model = RandomForestClassifier()

# ==========================================
# 6. 모델 학습
# ==========================================

model.fit(X_train, y_train)

# ==========================================
# 7. 예측
# ==========================================

pred = model.predict(X_test)

# ==========================================
# 8. 정확도 평가
# ==========================================

acc = accuracy_score(y_test, pred)

print("정확도:", acc)

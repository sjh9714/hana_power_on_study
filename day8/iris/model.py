import pandas as pd
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# ==========================================
# 1. seaborn 데이터 로드
# ==========================================

df = sns.load_dataset("iris")

# ==========================================
# 3. 입력(X) / 정답(y)
# ==========================================

# 정답 필드 제거
X = df.drop("species", axis=1)

# 정답(Label)
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

model = RandomForestClassifier(
    random_state=42
)

# ==========================================
# 6. 모델 학습
# ==========================================

model.fit(X_train, y_train)

# ==========================================
# 7. 모델 저장
# ==========================================

joblib.dump(
    model,
    "iris_model.pkl"
)

print("모델 저장 완료 : iris_model.pkl")

import pandas as pd
import seaborn as sns
import joblib

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
# 7. 예측
# ==========================================

pred = model.predict(X_test)

# ==========================================
# 8. 정확도 평가
# ==========================================

acc = accuracy_score(y_test, pred)

print("정확도:", acc)

# ==========================================
# 9. 모델 저장
# ==========================================

joblib.dump(
    model,
    "iris_model.pkl"
)

print("모델 저장 완료 : iris_model.pkl")

# ==========================================
# 10. 저장된 모델 로드
# ==========================================

loaded_model = joblib.load(
    "iris_model.pkl"
)

print("모델 로드 완료")

# ==========================================
# 11. 새로운 데이터 추론(Inference)
# ==========================================

# 새로운 꽃 데이터
new_data = pd.DataFrame(
    [
        [5.1, 3.5, 1.4, 0.2]
    ],
    columns=[
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width"
    ]
)

# 예측
result = loaded_model.predict(new_data)

# 확률 예측
proba = loaded_model.predict_proba(new_data)

print("예측 결과 :", result[0])

print("예측 확률 :", proba)
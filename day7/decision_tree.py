import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

# =========================
# 1. 데이터 로드
# =========================
df = pd.read_csv("data/credit_card_transactions.csv")

# =========================
# 2. 시간 feature 생성
# =========================
df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])
df["hour"] = df["trans_date_trans_time"].dt.hour

# =========================
# 3. 범주형 인코딩
# =========================
le = LabelEncoder()
df["category"] = le.fit_transform(df["category"])

# =========================
# 4. Feature / Label
# =========================
X = df[[
    "amt",
    "category",
    "hour",
    "lat",
    "long",
    "city_pop"
]]

y = df["is_fraud"]

# =========================
# 5. Train / Test split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# 6. Decision Tree 모델
# =========================
model = DecisionTreeClassifier(
    max_depth=6,          # 트리 깊이 제한 (과적합 방지)
    min_samples_split=20, # 분기 최소 샘플
    class_weight="balanced",
    random_state=42
)

# =========================
# 7. 학습
# =========================
model.fit(X_train, y_train)

# =========================
# 8. 예측 (클래스)
# =========================
pred = model.predict(X_test)

# =========================
# 9. 평가
# =========================
print(classification_report(y_test, pred))
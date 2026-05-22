import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

from xgboost import XGBClassifier

# =========================================
# 1. 데이터 로드
# =========================================
df = pd.read_csv("data/credit_card_transactions.csv")

# =========================================
# 2. 날짜/시간 처리
# =========================================
df["trans_date_trans_time"] = pd.to_datetime(
    df["trans_date_trans_time"]
)

# 시간(hour) feature 생성
df["hour"] = df["trans_date_trans_time"].dt.hour

# =========================================
# 3. 범주형 데이터 인코딩
# =========================================
le = LabelEncoder()

df["category"] = le.fit_transform(
    df["category"]
)

# =========================================
# 4. Feature 선택
# =========================================
X = df[[
    "amt",
    "category",
    "hour",
    "lat",
    "long",
    "city_pop"
]]

# 정답(Label)
y = df["is_fraud"]

# =========================================
# 5. Train / Test 분리
# =========================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================================
# 6. imbalance 비율 계산
# =========================================
normal_count = y_train.value_counts()[0]
fraud_count = y_train.value_counts()[1]

scale_pos_weight = normal_count / fraud_count

print("정상 거래 수 :", normal_count)
print("사기 거래 수 :", fraud_count)
print("scale_pos_weight :", scale_pos_weight)

# =========================================
# 7. XGBoost 모델 생성
# =========================================
model = XGBClassifier(
    n_estimators=300,         # 트리 개수
    max_depth=6,              # 트리 깊이
    learning_rate=0.05,       # 학습률
    subsample=0.8,            # 데이터 샘플링
    colsample_bytree=0.8,     # feature 샘플링

    scale_pos_weight=scale_pos_weight,

    eval_metric="logloss",
    random_state=42
)

# =========================================
# 8. 모델 학습
# =========================================
model.fit(X_train, y_train)

# =========================================
# 9. 기본 예측 (threshold = 0.5)
# =========================================
pred_default = model.predict(X_test)

print("\n==============================")
print("Threshold = 0.5")
print("==============================")

print(
    classification_report(
        y_test,
        pred_default
    )
)

# =========================================
# 10. Fraud 확률 추출
# =========================================
probs = model.predict_proba(X_test)[:, 1]

# =========================================
# 11. Threshold 튜닝
# =========================================
thresholds = [0.3, 0.5, 0.7, 0.9]

for threshold in thresholds:

    print("\n==============================")
    print(f"Threshold = {threshold}")
    print("==============================")

    # threshold 기준 fraud 판단
    pred_custom = (probs >= threshold).astype(int)

    # 평가 출력
    print(
        classification_report(
            y_test,
            pred_custom
        )
    )
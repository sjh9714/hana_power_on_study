# Fraud Detection: XGBoost + Threshold Optimization 적용된 코드 
#
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

from xgboost import XGBClassifier

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
# 4. Feature / Label 분리
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
# 6. XGBoost 모델 생성 (핵심)
# =========================
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=(y_train.value_counts()[0] / y_train.value_counts()[1]),
    eval_metric="logloss",
    random_state=42
)

# =========================
# 7. 모델 학습
# =========================
model.fit(X_train, y_train)

# =========================
# 8. 기본 예측 (threshold = 0.5)
# =========================
pred_default = model.predict(X_test)

print("\n===== Threshold = 0.5 결과 =====")
print(classification_report(y_test, pred_default))

# =========================
# 9. 확률 예측 (threshold tuning용)
# =========================
probs_all = model.predict_proba(X_test)
print(probs_all)
print(f"크기 {len(probs_all)}")
probs = model.predict_proba(X_test)[:, 1]

# =========================
# 10. Threshold 최적화
# =========================
threshold = 0.7   # 🔥 Precision 높이려면 0.6~0.8

pred_custom = (probs >= threshold).astype(int)

print(f"\n===== Threshold = {threshold} 결과 =====")
print(classification_report(y_test, pred_custom))

# =========================
# 11. Threshold 여러 개 비교 (옵션)
# =========================
print("\n===== Threshold 비교 =====")

for t in [0.3, 0.5, 0.7, 0.9]:
    pred = (probs >= t).astype(int)
    print(f"\n--- Threshold: {t} ---")
    print(classification_report(y_test, pred))
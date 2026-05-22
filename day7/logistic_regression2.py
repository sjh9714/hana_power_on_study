import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from imblearn.over_sampling import SMOTE

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
# 3. 범주형 처리
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
# 5. Train / Test 분리 (중요)
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# 6. Scaling (매우 중요 ⭐)
# =========================
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =========================
# 7. SMOTE (Train에만 적용)
#    소수 클래스 데이터를 인위적으로 생성
# =========================
smote = SMOTE(random_state=42)

X_train_resampled, y_train_resampled = smote.fit_resample(
    X_train_scaled,
    y_train
)

# =========================
# 8. 모델 (튜닝 개선)
# =========================
model = LogisticRegression(
    max_iter=1000,   #최대 반복 학습 횟수 
    solver="lbfgs",  # 최적의 가중치를 찾는 최적화 알고리즘
                     # L-BFGS (Limited-memory Broyden–Fletcher–Goldfarb–Shanno)
                     # 빠르고 안정적으로 최적값 찾기
    class_weight=None   # SMOTE 사용 시 보통 제거
)

#
#| solver    | 특징           |
#| --------- | ---------      |
#| lbfgs     | 기본 추천      |
#| liblinear | 작은 데이터    |
#| sag       | 매우 큰 데이터 |
#| saga      | 희소행렬 + L1  |
#| newton-cg | 고정밀         |


# =========================
# 9. 학습 (중요: resampled 데이터 사용)
# =========================
model.fit(X_train_resampled, y_train_resampled)

# =========================
# 10. 예측
# =========================
pred = model.predict(X_test_scaled)

# =========================
# 11. 평가
# =========================
print(classification_report(y_test, pred))
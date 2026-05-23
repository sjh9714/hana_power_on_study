import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 데이터 로드
df = pd.read_csv("data/credit_card_transactions.csv")

# 범주형 인코딩
le = LabelEncoder()
df["category"] = le.fit_transform(df["category"])

# 사용할 컬럼
X = df[["amt", "category"]]

# 정답
y = df["is_fraud"]

# 학습/테스트 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# 모델 생성
model = LogisticRegression()

# 학습
model.fit(X_train, y_train)

# 예측
pred = model.predict(X_test)

# 평가
print(classification_report(y_test, pred))
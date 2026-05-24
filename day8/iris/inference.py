import pandas as pd
import joblib

# ==========================================
# 1. 저장된 모델 로드
# ==========================================

loaded_model = joblib.load(
    "iris_model.pkl"
)

print("모델 로드 완료")

# ==========================================
# 2. 새로운 데이터 추론(Inference)
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

print("예측 결과 :", result[0])

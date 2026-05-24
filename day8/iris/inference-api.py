from fastapi import FastAPI
from pydantic import BaseModel 
import pandas as pd
import joblib

app = FastAPI()

# ==========================================
# 1. 저장된 모델 로드
# ==========================================

loaded_model = joblib.load(
    "iris_model.pkl"
)

print("모델 로드 완료")


class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float 
    petal_width: float 


@app.post("/predict")
def predict(data: IrisData):
# ==========================================
# 2. 새로운 데이터 추론(Inference)
# ==========================================

# 새로운 꽃 데이터
    new_data = pd.DataFrame(
        [
            [
                #5.1, 3.5, 1.4, 0.2
                data.sepal_length, #5.1
                data.sepal_width,  #3.5
                data.petal_length, #1.4
                data.petal_width   #0.2
            ]
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
    # 결과 반환 
    return {
        "prediction" : result[0]
    }


#실행 방법 
#uvicorn inference-api:app 
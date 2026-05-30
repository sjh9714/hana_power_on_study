# ============================================================
# FastAPI
# ============================================================

from fastapi import FastAPI

# ============================================================
# 기본 라이브러리
# ============================================================

import joblib
import pandas as pd
import numpy as np

# ============================================================
# TensorFlow AutoEncoder 로드
# ============================================================

from tensorflow.keras.models import load_model

# ============================================================
# Request Schema
# ============================================================

from schemas.transaction import Transaction

# ============================================================
# Redis 서비스
# ============================================================

from services.redis_service import (
    get_customer_state,
    save_customer_state
)

# ============================================================
# Feature 생성
# ============================================================

from services.feature_engineering import (
    create_features
)

# ============================================================
# Risk 계산
# ============================================================

from services.risk_scoring import (
    calculate_risk
)

# ============================================================
# FastAPI 객체
# ============================================================

app = FastAPI()

# ============================================================
# 모델 로드
# ============================================================

# ============================================================
# XGBoost
# ============================================================

model = joblib.load(
    "app/model/xgb_model.pkl"
)

# ============================================================
# KMeans
# ============================================================

kmeans = joblib.load(
    "app/model/kmeans.pkl"
)

# ============================================================
# Isolation Forest
# ============================================================

iso_model = joblib.load(
    "app/model/isolation_forest.pkl"
)

# ============================================================
# Scaler
# ============================================================

scaler = joblib.load(
    "app/model/scaler.pkl"
)

# ============================================================
# AutoEncoder
# ============================================================

autoencoder = load_model(
    "app/model/autoencoder.h5"
)

# ============================================================
# 실시간 Fraud Detection API
# ============================================================

@app.post("/predict")

def predict(tx: Transaction):

    # ========================================================
    # 1. 고객 이전 상태 조회
    # ========================================================

    state = get_customer_state(
        tx.cc_num
    )

    # ========================================================
    # 2. Feature 생성
    # ========================================================

    features, updated_state = (
        create_features(
            tx,
            state
        )
    )

    # ========================================================
    # 3. KMeans 입력 생성
    # ========================================================

    segment_features = pd.DataFrame([{

        "amt":
            features["amt"],

        "hour":
            features["hour"],

        "dayofweek":
            features["dayofweek"],

        "month":
            features["month"],

        "night_transaction":
            features["night_transaction"],

        "distance":
            features["distance"],

        "amount_ratio":
            features["amount_ratio"],

        "customer_tx_count":
            features["customer_tx_count"],

        "time_diff":
            features["time_diff"],

        "velocity_flag":
            features["velocity_flag"]

    }])

    # ========================================================
    # 4. 정규화
    # ========================================================

    X_scaled = scaler.transform(
        segment_features
    )

    # ========================================================
    # 5. 고객 세그먼트 생성
    # ========================================================

    segment = kmeans.predict(
        X_scaled
    )[0]

    # ========================================================
    # 6. Isolation Forest 이상 점수
    # ========================================================

    iso_score = (
        iso_model.decision_function(
            X_scaled
        )[0]
    )

    # ========================================================
    # 7. AutoEncoder Reconstruction Error
    # ========================================================

    reconstructed = autoencoder.predict(
        X_scaled,
        verbose=0
    )

    reconstruction_error = np.mean(

        np.power(
            X_scaled - reconstructed,
            2
        ),

        axis=1

    )[0]

    # ========================================================
    # 8. 최종 Feature 구성
    # ========================================================

    features["segment"] = segment

    features["iso_score"] = iso_score

    features[
        "reconstruction_error"
    ] = reconstruction_error

    # ========================================================
    # 9. 최종 XGBoost 입력
    # ========================================================

    final_features = [

        "amt",
        "hour",
        "dayofweek",
        "month",
        "night_transaction",
        "distance",
        "amount_ratio",
        "customer_tx_count",
        "time_diff",
        "velocity_flag",
        "segment",
        "iso_score",
        "reconstruction_error"

    ]

    X = pd.DataFrame([
        {
            key: features[key]
            for key in final_features
        }
    ])

    # ========================================================
    # 10. Fraud 확률 계산
    # ========================================================

    probability = (
        model.predict_proba(X)[0][1]
    )

    # ========================================================
    # 11. Rule Engine
    # ========================================================

    rule_score = 0

    # ========================================================
    # 고액 거래
    # ========================================================

    if features["amt"] > 3000:
        rule_score += 1

    # ========================================================
    # 야간 거래
    # ========================================================

    if features["night_transaction"] == 1:
        rule_score += 1

    # ========================================================
    # 매우 빠른 거래
    # ========================================================

    if features["time_diff"] < 30:
        rule_score += 1

    # ========================================================
    # 이동 거리 큼
    # ========================================================

    if features["distance"] > 5:
        rule_score += 1

    # ========================================================
    # 최종 위험 점수
    # ========================================================

    final_score = (

        probability * 0.7 +

        (rule_score / 4) * 0.3

    )

    # ========================================================
    # 승인 정책
    # ========================================================

    risk_score, action = (
        calculate_risk(
            final_score
        )
    )

    # ========================================================
    # 12. Redis 상태 저장
    # ========================================================

    save_customer_state(
        tx.cc_num,
        updated_state
    )

    # ========================================================
    # 13. API 응답
    # ========================================================

    return {

        # Fraud 확률
        "fraud_probability":
            float(probability),

        # Isolation Forest 점수
        "iso_score":
            float(iso_score),

        # AutoEncoder 오차
        "reconstruction_error":
            float(reconstruction_error),

        # Rule 점수
        "rule_score":
            int(rule_score),

        # 최종 위험 점수
        "risk_score":
            float(risk_score),

        # 업무 처리
        #
        # APPROVE
        # MFA
        # BLOCK
        "action":
            action,

        # 고객 세그먼트
        "segment":
            int(segment)

    }
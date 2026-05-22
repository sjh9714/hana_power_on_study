# ============================================================
# 라이브러리
# ============================================================

import numpy as np
import pandas as pd


# ============================================================
# Feature 생성
# ============================================================

def create_features(tx, state):

    # ========================================================
    # 거래 시간
    # ========================================================

    dt = pd.to_datetime(
        tx.trans_date_trans_time
    )

    hour = dt.hour

    dayofweek = dt.dayofweek

    month = dt.month

    # ========================================================
    # 야간 거래 여부
    # ========================================================

    night_transaction = int(
        (hour >= 22) or
        (hour <= 5)
    )

    # ========================================================
    # 거리 계산
    # ========================================================

    distance = np.sqrt(

        (tx.lat - tx.merch_lat) ** 2 +

        (tx.long - tx.merch_long) ** 2
    )

    # ========================================================
    # 이전 상태가 없으면 초기값 생성
    # ========================================================

    if state is None:

        state = {

            "transaction_count": 0,

            "total_amount": 0,

            "night_count": 0,

            "total_distance": 0,

            "last_transaction_time": None
        }

    # ========================================================
    # 거래 횟수 증가
    # ========================================================

    transaction_count = (
        state["transaction_count"] + 1
    )

    # ========================================================
    # 총 거래 금액
    # ========================================================

    total_amount = (
        state["total_amount"] + tx.amt
    )

    # ========================================================
    # 평균 거래 금액
    # ========================================================

    avg_amount = (
        total_amount /
        transaction_count
    )

    # ========================================================
    # amount_ratio
    # ========================================================

    amount_ratio = (
        tx.amt /
        (avg_amount + 1)
    )

    # ========================================================
    # 야간 거래 횟수
    # ========================================================

    night_count = (
        state["night_count"] +
        night_transaction
    )

    # ========================================================
    # 야간 거래 비율
    # ========================================================

    night_ratio = (
        night_count /
        transaction_count
    )

    # ========================================================
    # 총 이동 거리
    # ========================================================

    total_distance = (
        state["total_distance"] +
        distance
    )

    # ========================================================
    # 평균 이동 거리
    # ========================================================

    avg_distance = (
        total_distance /
        transaction_count
    )

    # ========================================================
    # 이전 거래 시간 차이
    # ========================================================

    if state["last_transaction_time"]:

        prev_time = pd.to_datetime(
            state["last_transaction_time"]
        )

        time_diff = (
            dt - prev_time
        ).total_seconds()

    else:

        time_diff = 999999

    # ========================================================
    # Velocity Feature
    # ========================================================

    velocity_flag = int(
        time_diff < 60
    )

    # ========================================================
    # 최종 Feature
    # ========================================================

    features = {

        "amt":
            tx.amt,

        "hour":
            hour,

        "dayofweek":
            dayofweek,

        "month":
            month,

        "night_transaction":
            night_transaction,

        "distance":
            distance,

        "amount_ratio":
            amount_ratio,

        "customer_tx_count":
            transaction_count,

        "time_diff":
            time_diff,

        "velocity_flag":
            velocity_flag

    }

    # ========================================================
    # 업데이트 상태
    # ========================================================

    updated_state = {

        "transaction_count":
            transaction_count,

        "total_amount":
            total_amount,

        "night_count":
            night_count,

        "total_distance":
            total_distance,

        "last_transaction_time":
            str(dt)
    }

    return features, updated_state
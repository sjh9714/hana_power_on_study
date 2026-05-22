import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 데이터 정규화
from sklearn.preprocessing import StandardScaler

# 군집화 알고리즘
from sklearn.cluster import KMeans

# 차원 축소
from sklearn.decomposition import PCA

# 이상 탐지 모델
from sklearn.ensemble import IsolationForest


# =========================================
# 1. 데이터 로드
# =========================================

# CSV 파일 읽기
df = pd.read_csv("data/credit_card_transactions.csv")

# 상위 5개 데이터 출력
print(df.head())

# 데이터 구조 및 타입 확인
print(df.info())


# =========================================
# 2. 날짜 변환
# =========================================

# 문자열 형태의 날짜 데이터를 datetime 타입으로 변환
df["trans_date_trans_time"] = pd.to_datetime(
    df["trans_date_trans_time"]
)

# 거래 시간(hour) 추출
df["hour"] = df["trans_date_trans_time"].dt.hour

# 요일 추출
# 월요일=0 ~ 일요일=6
df["dayofweek"] = df["trans_date_trans_time"].dt.dayofweek


# =========================================
# 3. Feature Engineering
# =========================================

# 야간 거래 여부 생성
# 22시~05시는 1
# 나머지는 0
df["night_transaction"] = df["hour"].apply(
    lambda x: 1 if (x >= 22 or x <= 5) else 0
)

# 주말 거래 여부 생성
# 토요일(5), 일요일(6)은 1
df["weekend"] = df["dayofweek"].apply(
    lambda x: 1 if x >= 5 else 0
)


# =========================================
# 4. 고객별 행동 패턴 생성
# =========================================

# 고객 카드 번호(cc_num) 기준으로 그룹화
customer_behavior = df.groupby("cc_num").agg({

    # 거래 금액 통계 생성
    "amt": [

        # 총 거래 건수
        "count",

        # 평균 거래 금액
        "mean",

        # 거래 금액 표준편차
        # 값이 크면 소비 패턴 변화가 큼
        "std",

        # 최대 거래 금액
        "max",

        # 최소 거래 금액
        "min"
    ],

    # 야간 거래 비율
    # 0~1 사이 값
    "night_transaction": "mean",

    # 주말 거래 비율
    "weekend": "mean",

    # 도시 인구 평균
    # 고객이 주로 거래한 지역 규모 분석 가능
    "city_pop": "mean"

})

# MultiIndex 컬럼명을 단순화
customer_behavior.columns = [

    "transaction_count",  # 거래 건수
    "avg_amount",         # 평균 거래 금액
    "std_amount",         # 거래 금액 표준편차
    "max_amount",         # 최대 거래 금액
    "min_amount",         # 최소 거래 금액
    "night_ratio",        # 야간 거래 비율
    "weekend_ratio",      # 주말 거래 비율
    "avg_city_pop"        # 평균 도시 인구

]

# 결측치(NaN) 제거
# std는 거래가 1건이면 NaN 발생 가능
customer_behavior = customer_behavior.fillna(0)

# 생성된 고객 행동 데이터 확인
print(customer_behavior.head())


# =========================================
# 5. 정규화
# =========================================

# 평균=0, 표준편차=1 형태로 변환
# 거리 기반 알고리즘(KMeans)에 중요
# 각 컬럼의 평균 계산
# 각 컬럼의 표준편차 계산
# 이후 데이터를 변환할 준비를 수행하는 객체입니다.
scaler = StandardScaler()

# 데이터 정규화 수행
# 먼저 데이터의 통계를 계산합니다.
# | feature | 평균 | 표준편차 |
# | ------- | ---: | -------: |
# | 나이    |   35 |       10 |
# | 급여    | 5000 |     2000 |

# 표준화 공식 : z = (x-u)/σ 
# x = 원래 값
# μ = 평균
# σ = 표준편차

# 원본 데이터:
# | 나이 | 급여 |
# | --- | ------ |
# | 20  | 3000   |
# | 30  | 5000   |
# | 40  | 7000   |

# 표준화 후:
# | 나이_scaled | 급여_scaled |
# | ---------- | ------------- |
# | -1.22      | -1.22         |
# | 0          | 0             |
# | 1.22       | 1.22          |

# 스케일링 후 모든 컬럼이 비슷한 범위가 됩니다. 
# | feature      | 범위   |
# | ------------ | ------ |
# | 나이_scaled  | -2 ~ 2 |
# | 급여_scaled  | -2 ~ 2 |

X_scaled = scaler.fit_transform(customer_behavior)
print(X_scaled)

# =========================================
# 6. K-Means 군집화
# =========================================

# 고객을 4개 그룹으로 분류
kmeans = KMeans(
    n_clusters=4,
    random_state=42
)

# 군집 예측 수행
customer_behavior["cluster"] = kmeans.fit_predict(X_scaled)
# 군집별 고객 수 출력
print(customer_behavior["cluster"].value_counts())


# =========================================
# 7. PCA 차원 축소
# =========================================

# 고차원 데이터를 2차원으로 축소
# 시각화 목적
pca = PCA(n_components=2)

# PCA 적용
X_pca = pca.fit_transform(X_scaled)

# PCA 결과 저장
customer_behavior["pca1"] = X_pca[:, 0]
customer_behavior["pca2"] = X_pca[:, 1]


# =========================================
# 8. 군집 시각화
# =========================================

plt.figure(figsize=(10, 6))

# PCA 결과를 scatter plot으로 시각화
# 색상은 cluster 값 사용
scatter = plt.scatter(
    customer_behavior["pca1"],
    customer_behavior["pca2"],
    c=customer_behavior["cluster"]
)

plt.title("Customer Clustering")

plt.xlabel("PCA1")
plt.ylabel("PCA2")

# 색상 범례 표시
plt.colorbar(scatter)

plt.show()


# =========================================
# 9. Isolation Forest 이상 탐지
# =========================================

# contamination=0.02
# 전체 데이터 중 2%를 이상치로 간주
iso = IsolationForest(
    contamination=0.02,
    random_state=42
)

# 이상 탐지 수행
# 결과:
#  1  = 정상
# -1 = 이상
customer_behavior["anomaly"] = iso.fit_predict(
    X_scaled
)

# 사람이 읽기 쉬운 라벨 생성
customer_behavior["anomaly_label"] = customer_behavior[
    "anomaly"
].apply(
    lambda x: "Fraud" if x == -1 else "Normal"
)

# 이상 점수 계산
# 값이 낮을수록 이상 가능성이 높음
customer_behavior["anomaly_score"] = iso.decision_function(
    X_scaled
)


# =========================================
# 10. 이상 고객 확인
# =========================================

# anomaly=-1 인 고객만 추출
fraud_customers = customer_behavior[
    customer_behavior["anomaly"] == -1
]

print("\n===== 이상 고객 =====")

# 상위 5개 출력
print(fraud_customers.head())

print("\n이상 고객 수:")

# 이상 고객 수 출력
print(len(fraud_customers))


# =========================================
# 11. 이상 고객 시각화
# =========================================

plt.figure(figsize=(10, 6))

# 정상/이상 색상 매핑
# 정상=0
# 이상=1
colors = customer_behavior["anomaly"].map({
    1: 0,
    -1: 1
})

# 이상 탐지 결과 시각화
scatter = plt.scatter(
    customer_behavior["pca1"],
    customer_behavior["pca2"],
    c=colors
)

plt.title("이상 탐지 결과")

plt.xlabel("PCA1")
plt.ylabel("PCA2")

plt.colorbar(scatter)

plt.show()


# =========================================
# 12. 클러스터별 특징 분석
# =========================================

# 분석할 feature 목록
feature_cols = [

    "transaction_count",
    "avg_amount",
    "std_amount",
    "max_amount",
    "min_amount",
    "night_ratio",
    "weekend_ratio",
    "avg_city_pop"

]

# 클러스터별 평균 계산
cluster_summary = customer_behavior.groupby(
    "cluster"
)[feature_cols].mean()

print("\n===== 클러스터별 평균 =====")

print(cluster_summary)


# =========================================
# 13. 이상 고객 저장
# =========================================

# 이상 고객 데이터를 CSV 파일로 저장
fraud_customers.to_csv(
    "fraud_customers.csv",
    index=True
)

print("\nfraud_customers.csv 저장 완료")
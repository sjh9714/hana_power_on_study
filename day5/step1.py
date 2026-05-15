# =========================================================
# credit_card_transactions.csv 파일 읽기 및 CSV 로딩
# =========================================================

# 필요한 라이브러리 설치
# !pip install pandas

import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# 1. CSV 파일 로딩
# ---------------------------------------------------------

csv_path = f"data/credit_card_transactions.csv"

df = pd.read_csv(csv_path)

print("CSV 로딩 완료")

# ---------------------------------------------------------
# 2. 기본 데이터 확인
# ---------------------------------------------------------

print("\n===== 데이터 상위 5개 =====")
print(df.head())

print("\n===== 데이터 정보 =====")
print(df.info())

print("\n===== 결측치 확인 =====")
print(df.isnull().sum())

print("\n===== 기술 통계 =====")
print(df.describe())

# ---------------------------------------------------------
# 3. 날짜 컬럼 변환
# ---------------------------------------------------------

df["trans_date_trans_time"] = pd.to_datetime(
    df["trans_date_trans_time"]
)

print("\n날짜 변환 완료")

# ---------------------------------------------------------
# 4. 분석용 컬럼 추가
# ---------------------------------------------------------

df["year"] = df["trans_date_trans_time"].dt.year
df["month"] = df["trans_date_trans_time"].dt.month
df["day"] = df["trans_date_trans_time"].dt.day
df["hour"] = df["trans_date_trans_time"].dt.hour
df["weekday"] = df["trans_date_trans_time"].dt.day_name()

print("\n분석 컬럼 생성 완료")

# ---------------------------------------------------------
# 5. 기본 거래 분석
# ---------------------------------------------------------

print("\n===== 총 거래 건수 =====")
print(len(df))

print("\n===== 총 거래 금액 =====")
print(df["amt"].sum())

print("\n===== 평균 거래 금액 =====")
print(df["amt"].mean())

print("\n===== 최대 거래 금액 =====")
print(df["amt"].max())

print("\n===== 최소 거래 금액 =====")
print(df["amt"].min())


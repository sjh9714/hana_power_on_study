import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 1. 데이터 로드
# ==============================

df = pd.read_csv("data/credit_card_transactions.csv")

print("데이터 크기:", df.shape)
print(df.head())

# ==============================
# 2. 날짜 변환
# ==============================

# trans_date 컬럼명을 실제 데이터에 맞게 수정 가능
df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])

# 년 / 월 / 일 / 시간 생성
df['year'] = df['trans_date_trans_time'].dt.year
df['month'] = df['trans_date_trans_time'].dt.month
df['day'] = df['trans_date_trans_time'].dt.day
df['hour'] = df['trans_date_trans_time'].dt.hour

# ==============================
# 3. 지역 컬럼 확인
# ==============================

# 보통 state 또는 city 컬럼 사용
# 실제 CSV에 맞게 수정 가능

print("\n컬럼 목록:")
print(df.columns)

# 예시:
# state 컬럼 사용
REGION_COL = "state"

# ==============================
# 4. 기본 데이터 확인
# ==============================

print("\n결측치 확인")
print(df.isnull().sum())

print("\n지역 개수")
print(df[REGION_COL].nunique())

print("\n월 개수")
print(df['month'].nunique())

# ==============================
# 5. 지역 + 월별 거래 금액 분석
# ==============================

region_month_amt = (
    df.groupby([REGION_COL, 'month'])['amt']
    .agg([
        'count',
        'sum',
        'mean',
        'max'
    ])
    .reset_index()
)

region_month_amt.columns = [
    REGION_COL,
    'month',
    'tx_count',
    'total_amt',
    'avg_amt',
    'max_amt'
]

print("\n지역 + 월별 거래 분석")
print(region_month_amt.head(20))

# ==============================
# 6. 지역 + 월별 Fraud 분석
# ==============================

if 'is_fraud' in df.columns:

    fraud_analysis = (
        df.groupby([REGION_COL, 'month'])['is_fraud']
        .agg([
            'sum',
            'count',
            'mean'
        ])
        .reset_index()
    )

    fraud_analysis.columns = [
        REGION_COL,
        'month',
        'fraud_count',
        'total_tx',
        'fraud_ratio'
    ]

    # 퍼센트 변환
    fraud_analysis['fraud_ratio'] *= 100

    print("\n지역 + 월별 Fraud 분석")
    print(fraud_analysis.head(20))

# ==============================
# 7. Pivot Table 생성
# ==============================

pivot_total = pd.pivot_table(
    region_month_amt,
    index=REGION_COL,
    columns='month',
    values='total_amt',
    fill_value=0
)

print("\n지역별 월 거래금액 Pivot")
print(pivot_total)

# ==============================
# 8. 상위 지역 분석
# ==============================

top_regions = (
    df.groupby(REGION_COL)['amt']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n상위 10개 지역")
print(top_regions)

# ==============================
# 9. 월별 전체 거래 분석
# ==============================

monthly_total = (
    df.groupby('month')['amt']
    .sum()
)

print("\n월별 총 거래액")
print(monthly_total)

# ==============================
# 10. 시각화 - 월별 총 거래액
# ==============================

plt.figure(figsize=(10, 5))

monthly_total.plot(
    kind='line',
    marker='o'
)

plt.title("Monthly Total Transaction Amount")
plt.xlabel("Month")
plt.ylabel("Total Amount")

plt.grid(True)

plt.show()

# ==============================
# 11. 시각화 - 상위 지역 거래액
# ==============================

plt.figure(figsize=(12, 6))

top_regions.plot(kind='bar')

plt.title("Top 10 Regions by Transaction Amount")
plt.xlabel("Region")
plt.ylabel("Total Amount")

plt.xticks(rotation=45)

plt.show()

# ==============================
# 12. 지역 + 월 Heatmap용 데이터 생성
# ==============================

heatmap_data = pd.pivot_table(
    region_month_amt,
    index=REGION_COL,
    columns='month',
    values='avg_amt',
    fill_value=0
)

print("\nHeatmap 데이터")
print(heatmap_data)

# ==============================
# 13. VIP 고객 분석
# ==============================

vip_customer = (
    df.groupby('cc_num')['amt']
    .agg([
        'sum',
        'mean',
        'count'
    ])
    .reset_index()
)

vip_customer.columns = [
    'cc_num',
    'total_amt',
    'avg_amt',
    'tx_count'
]

# VIP 점수 계산
vip_customer['vip_score'] = (
    vip_customer['total_amt'] * 0.5 +
    vip_customer['avg_amt'] * 0.3 +
    vip_customer['tx_count'] * 0.2
)

# 상위 1% VIP
vip_threshold = vip_customer['vip_score'].quantile(0.99)

vip_customer['grade'] = np.where(
    vip_customer['vip_score'] >= vip_threshold,
    'VIP',
    'NORMAL'
)

print("\nVIP 고객")
print(
    vip_customer
    .sort_values(by='vip_score', ascending=False)
    .head(20)
)

# ==============================
# 14. 지역별 VIP 고객 수
# ==============================

# 원본 데이터와 VIP 정보 병합
vip_merge = df.merge(
    vip_customer[['cc_num', 'grade']],
    on='cc_num',
    how='left'
)

region_vip = (
    vip_merge[vip_merge['grade'] == 'VIP']
    .groupby(REGION_COL)['cc_num']
    .nunique()
    .sort_values(ascending=False)
)

print("\n지역별 VIP 고객 수")
print(region_vip)

# ==============================
# 15. CSV 저장
# ==============================

region_month_amt.to_csv(
    "region_month_analysis.csv",
    index=False
)

vip_customer.to_csv(
    "vip_customer_analysis.csv",
    index=False
)

print("\n분석 완료")
print("저장 파일:")
print("- region_month_analysis.csv")
print("- vip_customer_analysis.csv")
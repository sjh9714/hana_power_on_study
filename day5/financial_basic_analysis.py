import pandas as pd

# 1. CSV 파일 로드
df = pd.read_csv("data/credit_card_transactions.csv")

# 2. 데이터 기본 확인 (선택)
print("=== 데이터 미리보기 ===")
print(df.head())

# 3. 핵심 분석 대상 컬럼 확인
# amt 컬럼이 거래 금액
if "amt" not in df.columns:
    raise ValueError("데이터에 'amt' 컬럼이 없습니다. 거래 금액 컬럼명을 확인하세요.")

# 4. 총 거래 건수
total_count = len(df)

# 5. 총 거래 금액
total_amount = df["amt"].sum()

# 6. 평균 거래 금액
avg_amount = df["amt"].mean()

# 7. 최대 / 최소 거래 금액
max_amount = df["amt"].max()
min_amount = df["amt"].min()

# 8. 결과 출력
print("\n===== 금융 데이터 기본 분석 결과 =====")
print(f"총 거래 건수     : {total_count}")
print(f"총 거래 금액     : {total_amount:,.2f}")
print(f"평균 거래 금액   : {avg_amount:,.2f}")
print(f"최대 거래 금액   : {max_amount:,.2f}")
print(f"최소 거래 금액   : {min_amount:,.2f}")


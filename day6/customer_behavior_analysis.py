import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 한글 폰트 설정 (중요)
# =========================
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows 기준
plt.rcParams["axes.unicode_minus"] = False     # 마이너스 깨짐 방지

# =========================
# 1. 데이터 로드
# =========================
df = pd.read_csv("data/credit_card_transactions.csv")

df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])

df["hour"] = df["trans_date_trans_time"].dt.hour
df["day"] = df["trans_date_trans_time"].dt.day_name()

# =========================
# 2. 고객 단위 행동 분석
# =========================
customer_group = df.groupby("cc_num")


customer_behavior = customer_group.agg(
    총소비금액=("amt", "sum"),
    평균소비금액=("amt", "mean"),
    거래횟수=("amt", "count"),
    사기거래횟수=("is_fraud", "sum"),
)

customer_behavior["사기비율"] = (
    customer_behavior["사기거래횟수"] / customer_behavior["거래횟수"]
)

# =========================
# 3. 상위 소비 고객 TOP 10
# =========================
top_spenders = customer_behavior.sort_values("총소비금액", ascending=False).head(10)

print("\n[TOP 10 고액 소비 고객]")
print(top_spenders)

# =========================
# 4. 시각화 1 - 고객별 총 소비
# =========================

#새로운 그래프 영역(캔버스)을 생성
plt.figure()
top_spenders["총소비금액"].plot(kind="bar")
plt.title("상위 10 고객 - 총 소비금액")
plt.xlabel("고객 (cc_num)")
plt.ylabel("총 소비금액")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =========================
# 5. 시각화 2 - 거래 횟수 vs 평균 금액
# =========================

#새로운 그래프 영역(캔버스)을 생성
plt.figure()
plt.scatter(
    customer_behavior["거래횟수"],
    customer_behavior["평균소비금액"]
)
plt.title("거래 횟수 vs 평균 소비금액")
plt.xlabel("거래 횟수")
plt.ylabel("평균 소비금액")
plt.tight_layout()
plt.show()

# =========================
# 6. 시간대별 소비 패턴
# =========================
hourly_spend = df.groupby("hour")["amt"].mean()

#새로운 그래프 영역(캔버스)을 생성
plt.figure()
hourly_spend.plot(kind="line")
plt.title("시간대별 평균 소비금액")
plt.xlabel("시간 (Hour)")
plt.ylabel("평균 금액")
plt.tight_layout()
plt.show()

# =========================
# 7. 사기 vs 정상 거래 비교
# =========================
fraud_group = df.groupby("is_fraud")["amt"].mean()

#새로운 그래프 영역(캔버스)을 생성
plt.figure()
fraud_group.plot(kind="bar")
plt.title("사기 vs 정상 거래 - 평균 거래 금액")
plt.xlabel("사기 여부 (0=정상, 1=사기)")
plt.ylabel("평균 거래 금액")
plt.tight_layout()
plt.show()
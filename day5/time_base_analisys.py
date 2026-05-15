import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 한글 폰트 설정
# -----------------------------
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 1. 데이터 로드
df = pd.read_csv("data/credit_card_transactions.csv")

# 2. 시간 파생 변수 생성
df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])

df["hour"] = df["trans_date_trans_time"].dt.hour
df["day"] = df["trans_date_trans_time"].dt.day_name()
df["month"] = df["trans_date_trans_time"].dt.month

# -----------------------------
# 3. 시간대별 거래량
# -----------------------------
hourly = df.groupby("hour")["amt"].count()

plt.figure()
plt.plot(hourly.index, hourly.values)
plt.title("시간대별 거래량")
plt.xlabel("시간 (Hour)")
plt.ylabel("거래 건수")
plt.grid()
plt.show()

# -----------------------------
# 4. 나이 / 연령대 생성
# -----------------------------
df["dob"] = pd.to_datetime(df["dob"])

current_year = pd.to_datetime("today").year
df["age"] = current_year - df["dob"].dt.year

# 연령대 구간 생성
bins = [0, 20, 30, 40, 50, 60, 100]
labels = ["10대", "20대", "30대", "40대", "50대", "60대+"]
df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)

# -----------------------------
# 연령대별 시간 소비 패턴
# -----------------------------
age_group = df.groupby("age_group")
age_group_count = age_group["amt"].count()
age_group_mean = age_group["amt"].mean()
print(age_group_count)
print(age_group_mean)

#hour = df.groupby("hour")
#hour_count = age_group["amt"].count()
#print(hour_count)

age_hour = df.groupby(["age_group", "hour"])["amt"].count().unstack()

plt.figure()
plt.imshow(age_hour.fillna(0), aspect="auto")
plt.title("연령대별 시간 소비 패턴")
plt.xlabel("시간 (Hour)")
plt.ylabel("연령대")
plt.yticks(range(len(age_hour.index)), age_hour.index)
plt.colorbar(label="거래 건수")
plt.show()


# -----------------------------
# 5. 시간대별 Fraud 비율
# -----------------------------
fraud_rate = df.groupby("hour")["is_fraud"].mean()

plt.figure()
plt.plot(fraud_rate.index, fraud_rate.values)
plt.title("시간대별 사기 거래 비율")
plt.xlabel("시간 (Hour)")
plt.ylabel("사기 확률")
plt.grid()
plt.show()

# -----------------------------
# 6. 요일별 분석
# -----------------------------
weekday = df.groupby("day")["amt"].count()

weekday = weekday.reindex([
    "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"
])

plt.figure()
plt.bar(weekday.index, weekday.values)
plt.title("요일별 거래 패턴")
plt.xlabel("요일")
plt.ylabel("거래 건수")
plt.xticks(rotation=45)
plt.show()


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반지름 (km)

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c

## 거리 계산 적용
df["distance_km"] = haversine(
    df["lat"],
    df["long"],
    df["merch_lat"],
    df["merch_long"]
)

# 시간 차이 계산
df = df.sort_values(by=["cc_num", "trans_date_trans_time"])
df["time_diff"] = df.groupby("cc_num")["trans_date_trans_time"].diff().dt.total_seconds() / 60

# 속도 계산
df["speed_kmh"] = df["distance_km"] / (df["time_diff"] / 60)

## 이상 탐지 조건
df["velocity_fraud"] = (
    (df["distance_km"] > 100) & (df["time_diff"] < 10)
)

# 📈 5. 시각화 코드
## 📌 거리 vs 시간 scatter plot
plt.figure()
plt.scatter(df["time_diff"], df["distance_km"], alpha=0.3)

plt.title("시간 vs 이동거리 기반 이상 탐지")
plt.xlabel("시간 차이 (분)")
plt.ylabel("이동 거리 (km)")
plt.grid()
plt.show()
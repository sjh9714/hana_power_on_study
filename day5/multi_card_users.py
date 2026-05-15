import pandas as pd

# 1. 데이터 로드
df = pd.read_csv("data/credit_card_transactions.csv")

# 2. 사람 기준 생성 (동일 인물 식별 키)
df["person_id"] = df["first"].astype(str) + "_" + df["last"].astype(str)# + "_" + df["dob"].astype(str)

# 3. 사람별 카드 개수 계산
card_count = df.groupby("person_id")["cc_num"].nunique().reset_index()

# 4. 2개 이상 카드 사용하는 사람 필터링
multi_card_users = card_count[card_count["cc_num"] >= 2]

# 5. 결과 정렬
multi_card_users = multi_card_users.sort_values(by="cc_num", ascending=False)

# 6. 저장
print("===== 2개 이상 카드 사용하는 사용자 저장 =====")
multi_card_users.to_csv("data/multi_card_users.csv")


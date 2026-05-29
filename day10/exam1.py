import pandas as pd

# ==========================================
# 1. 데이터 로드
# ==========================================

df = pd.read_csv("data/credit_card_transactions.csv")

# ==========================================
# 2. 날짜 변환
# ==========================================

# trans_date 컬럼을 datetime으로 변환
df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])

# 년도 / 월 추출
df['year'] = df['trans_date_trans_time'].dt.year
df['month'] = df['trans_date_trans_time'].dt.month

# ==========================================
# 3. 2019년 데이터 특정 지역만 선택
# TX, NY, PA, CA
# ==========================================

# 2019년
target_year = 2019

# 2019년도에 거래가 발생한 것만 선택함 
df_2019 = df[df['year'] == target_year]

# 거래가 많이 발생한 지역 대상으로 구성함  
df_state_trans = df_2019.groupby("state").size().sort_values(ascending=False)

# 거래가 많이 발생한 지역 4개만 선택 했습니다 
df_state_trans_top4 = df_state_trans.head(4)

# 위 3줄과 동일한 코드로 거래가 많이 발생한 지역 4개를 선택합니다
df_state_trans_top4 = df[df['year'] == target_year].groupby("state")["amt"].count().sort_values(ascending=False).head(4)

print(df_state_trans_top4)
# df_state_trans_top4는 시리얼 객체입니다 
# state 목록을 얻는방법은 아래와 같이합니다 
print(df_state_trans_top4.index)

# 2019년도에 대한 조건 
condition_year = df['year'] == target_year
# 거래가 많은 4개의 지역 조건 설정 
condition_state = df['state'].isin(df_state_trans_top4.index)

#조건에 맞는 대상 목록을 선택합니다 
df_region = df[condition_year & condition_state]

# 
print("선택 지역 데이터 수:", len(df_region))
# 
# ==========================================
# 5. state 기준 그룹 처리
# ==========================================
# 
result_list = []

# 지역별로 그룹을 지워 처리를 하기 위해 지역별로 묶습니다  
state_group = df_region.groupby('state')
# 
for state, state_data in state_group:

    print("=" * 60)
    print("STATE:", state)

    # ======================================
    # 6. 월별 전체 거래건수 계산
    # ======================================
    monthly_total = (
        state_data.groupby('month')
        .size()
        .reset_index(name='total_tx')
    )

    print("\n월별 전체 거래건수")
    print(monthly_total)
    
    # ======================================
    # 7. 고객별 월간 거래건수 계산
    # ======================================
    customer_month = (
        state_data.groupby(['month', 'cc_num'])
        .size()
        .reset_index(name='customer_tx')
    )
 
    # ======================================
    # 8. 월별 전체 거래건수 병합
    # ======================================
    customer_month = customer_month.merge(
        monthly_total,
        on='month',
        how='left'
    )
 
    # ======================================
    # 9. 거래 비율 계산
    # ======================================
    customer_month['tx_ratio'] = (customer_month['customer_tx'] / customer_month['total_tx']) * 100
 
    # ======================================
    # 10. 월간 거래건수 5% 이상 고객 선택
    # ======================================
    top_customer = customer_month[customer_month['tx_ratio'] >= 5]

    # state 컬럼 추가
    top_customer['state'] = state
 
    # 결과 저장
    result_list.append(top_customer)
 
    print("\n5% 이상 고객")
    print(
        top_customer[
            [
                'state',
                'month',
                'cc_num',
                'customer_tx',
                'total_tx',
                'tx_ratio'
            ]
        ]
    )
# 
# ==========================================
# 11. 최종 결과 합치기
# ==========================================
# 
final_result = pd.concat(
    result_list,
    ignore_index=True
)
# 
# ==========================================
# 12. 거래 비율 기준 정렬
# ==========================================
# 
final_result = final_result.sort_values(
    by='tx_ratio',
    ascending=False
)
# 
# ==========================================
# 13. 출력
# ==========================================
# 
print("\n최종 결과")
print(final_result)
# 
# ==========================================
# 14. CSV 저장
# ==========================================
# 
final_result.to_csv(
    "top_5percent_customers_1999.csv",
    index=False
)
# 
print("\n저장 완료")
print("파일명: top_5percent_customers_1999.csv")
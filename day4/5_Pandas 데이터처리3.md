# Pandas 데이터처리

## 데이터 처리 기본 절차

Pandas는 데이터 분석과 전처리에서 가장 많이 사용하는 Python 라이브러리입니다.
실무에서는 보통 아래와 같은 순서로 데이터를 처리합니다.

```python
## STEP 1: 데이터 로드
## STEP 2: 구조 확인
## STEP 3: 결측치 처리
## STEP 4: 필요 데이터 선택
## STEP 5: 변환/가공
## STEP 6: 분석 or ML 입력
```

---

# 1. 간단한 예제

아래 예제는 학생 성적 데이터를 사용하는 가장 기본적인 Pandas 흐름입니다.

---

## 예제 데이터

```python
import pandas as pd
import numpy as np

# 샘플 데이터 생성
data = {
    "이름": ["홍길동", "김철수", "이영희", "박민수"],
    "나이": [20, 21, np.nan, 23],
    "점수": [85, 90, 78, np.nan],
    "학과": ["컴퓨터", "전자", "컴퓨터", "기계"]
}

df = pd.DataFrame(data)

print(df)

# student.csv 로 저장합니다
df.to_csv("student.csv")
```

---

# STEP 1: 데이터 로드

실무에서는 CSV, Excel, DB에서 데이터를 불러옵니다.

```python
import pandas as pd

# CSV 파일 읽기
df = pd.read_csv("student_100.csv")

# Excel 파일 읽기
# df = pd.read_excel("student.xlsx")
```

설명:

* `read_csv()` : CSV 파일 로드
* `read_excel()` : Excel 파일 로드

---

# STEP 2: 구조 확인

데이터 상태를 먼저 확인합니다.

```python
# 상위 5개 출력
print(df.head())

# 데이터 구조 확인
print(df.info())

# 통계 정보 확인
print(df.describe())

# 컬럼명 확인
print(df.columns)
```

설명:

* `head()` : 데이터 일부 확인
* `info()` : 데이터 타입 및 결측치 확인
* `describe()` : 평균, 최대값 등 통계 정보 출력

---

# STEP 3: 결측치 처리

실무에서 매우 중요합니다.

```python
# 결측치 개수 확인
print(df.isnull().sum())

# 평균값으로 결측치 채우기
df["나이"] = df["나이"].fillna(df["나이"].mean())

# 점수 결측치는 0으로 처리
df["점수"] = df["점수"].fillna(0)

print(df)
```

설명:

* `isnull()` : 결측치 확인
* `fillna()` : 결측치 채우기

---

# STEP 4: 필요 데이터 선택

분석에 필요한 컬럼만 선택합니다.

```python
# 특정 컬럼 선택
result = df[["이름", "점수"]]

print(result)

# 조건 검색
high_score = df[df["점수"] >= 80]

print(high_score)
```

설명:

* 컬럼 선택 가능
* 조건 필터링 가능

---

# STEP 5: 변환/가공

새로운 컬럼 생성 및 데이터 변환을 수행합니다.

```python
# 점수 등급 생성
df["등급"] = df["점수"].apply(
    lambda x: "A" if x >= 90 else "B"
)

print(df)
```

설명:

* `apply()` : 데이터 변환
* lambda 함수로 조건 처리 가능

---

# STEP 6: 분석 or ML 입력

분석 또는 머신러닝 모델에 사용합니다.

```python
# 학과별 평균 점수
group_result = df.groupby("학과")["점수"].mean()

print(group_result)
```

설명:

* `groupby()` : 그룹 분석
* 평균, 합계, 개수 등 계산 가능

---

# 전체 예제 

```python
import pandas as pd
import numpy as np

# STEP 1: 데이터 로딩
df = pd.read_csv("student_100.csv")

# STEP 2: 구조 확인
print(df.info())

# STEP 3: 결측치 처리
df["나이"] = df["나이"].fillna(df["나이"].mean())
df["점수"] = df["점수"].fillna(0)

# STEP 4: 데이터 선택
df = df[["이름", "점수", "학과"]]

# STEP 5: 데이터 가공
df["등급"] = df["점수"].apply(
    lambda x: "A" if x >= 90 else "B"
)

# STEP 6: 분석
result = df.groupby("학과")["점수"].mean()

print(result)
```

---

# 2. 실전 활용 예제 (금융 소비 데이터 분석)

실무에서는 고객 소비 데이터를 많이 분석합니다.

---

# 실전 시나리오

목표:

* 고객 소비 패턴 분석
* VIP 고객 분류
* 머신러닝 입력 데이터 생성

---

# 예제 데이터

```python
import pandas as pd
import numpy as np

data = {
    "고객ID": [101, 102, 103, 104, 105],
    "나이": [25, 32, np.nan, 45, 28],
    "지역": ["서울", "부산", "서울", "대구", None],
    "월소비금액": [320000, 540000, 120000, 830000, 250000],
    "구매횟수": [5, 8, 2, 12, 4]
}

df = pd.DataFrame(data)

print(df)

df.to_csv("customer.csv")
```

---

# STEP 1: 데이터 로드

```python
# CSV 파일 로드
df = pd.read_csv("customer.csv")
```

---

# STEP 2: 데이터 구조 확인

```python
print(df.head())

print(df.info())

print(df.describe())
```

확인 내용:

* 숫자형 데이터인지
* 결측치 존재 여부
* 이상치 여부

---

# STEP 3: 결측치 처리

```python
# 나이는 평균으로 채움
df["나이"] = df["나이"].fillna(df["나이"].mean())

# 지역 결측치는 '미상'
df["지역"] = df["지역"].fillna("미상")
```

실무 포인트:

* 숫자형 → 평균/중앙값
* 문자열 → 기본값 사용

---

# STEP 4: 필요한 데이터 선택

```python
# 서울 고객만 선택
seoul_customer = df[df["지역"] == "서울"]

print(seoul_customer)
```

---

# STEP 5: 데이터 가공

## 1) 고객 등급 생성

```python
# VIP 여부 생성
df["VIP"] = df["월소비금액"].apply(
    lambda x: 1 if x >= 500000 else 0
)

print(df)
```

---

## 2) 고객 평균 구매 금액 계산

```python
# 1회 평균 구매 금액
df["평균구매금액"] = (
    df["월소비금액"] / df["구매횟수"]
)

print(df)
```

---

## 3) 머신러닝용 숫자 변환

머신러닝은 문자열을 사용할 수 없기 때문에 숫자로 변환합니다.

```python
# 지역 One-Hot Encoding
encoded_df = pd.get_dummies(df, columns=["지역"])

print(encoded_df)
```

설명:

* 서울 → 지역_서울
* 부산 → 지역_부산
* 머신러닝 입력 가능 형태로 변경됨

---

# STEP 6: 분석 및 머신러닝 입력

## 소비 평균 분석

```python
# 지역별 평균 소비 금액
result = df.groupby("지역")["월소비금액"].mean()

print(result)
```

---

## 머신러닝 입력 데이터 생성

```python
# 입력(X)
X = encoded_df[[
    "나이",
    "월소비금액",
    "구매횟수"
]]

# 정답(Y)
y = encoded_df["VIP"]

print(X)
print(y)
```

설명:

* `X` : 입력 데이터
* `y` : 예측 대상

---

# 실무 핵심 정리

| 단계          | 목적                  |
| ------------- | --------------------  |
| 데이터 로드   | CSV/DB/Excel 읽기     |
| 구조 확인     | 데이터 상태 파악      |
| 결측치 처리   | 데이터 품질 향상      |
| 데이터 선택   | 필요한 정보만 사용    |
| 변환/가공     | 분석 가능한 형태 생성 |
| 분석/ML 입력  | 통계 분석 및 AI 학습  |

---

# 실무에서 가장 많이 사용하는 Pandas 함수

| 함수            | 설명             |
| --------------- | ---------------- |
| `head()`        | 상위 데이터 확인 |
| `info()`        | 구조 확인        |
| `describe()`    | 통계 확인        |
| `isnull()`      | 결측치 확인      |
| `fillna()`      | 결측치 처리      |
| `groupby()`     | 그룹 분석        |
| `apply()`       | 데이터 가공      |
| `sort_values()` | 정렬             |
| `merge()`       | 데이터 병합      |
| `pivot_table()` | 피벗 분석        |

---

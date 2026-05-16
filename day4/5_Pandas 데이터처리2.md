# Pandas의 핵심 구조: Series / DataFrame

Pandas를 제대로 사용하려면 반드시 아래 2가지를 완전히 이해해야 합니다.

---

# 1. Pandas 핵심 구조

Pandas는 내부적으로 아래 2개의 자료구조를 사용합니다.

| 구조        | 설명          |
| --------- | ----------- |
| Series    | 1차원 데이터     |
| DataFrame | 2차원 테이블 데이터 |

---

# 2. Series란 무엇인가?

## 2-1. 정의

> Series = 하나의 컬럼(열)

즉:

* 리스트 + 인덱스(index)
* 1차원 배열
* NumPy 기반

---

# 3. Series 구조

```python id="7xjlwm"
import pandas as pd

s = pd.Series([10, 20, 30, 40])

print(s)
```

---

## 결과

```python id="1a3u75"
0    10
1    20
2    30
3    40
dtype: int64
```

---

# 4. Series 내부 구성

Series는 아래 구조를 가진다.

```python id="drvc5s"
index -> 0,1,2,3
value -> 10,20,30,40
dtype -> int64
```

---

# 5. Series 기본 예제

---

## 5-1. 문자열 Series

```python id="n7r4e7"
name = pd.Series(["Kim", "Lee", "Park"])

print(name)
```

---

## 5-2. index 지정 별도 지정 

```python id="u4kjgc"
score = pd.Series(
    [90, 80, 70],
    index=["Kim", "Lee", "Park"]
)

print(score)
```

---

## 결과

```python id="pkb2f8"
Kim     90
Lee     80
Park    70
```

---

# 6. Series 데이터 접근

---

## 6-1. index 접근

```python id="1c1of1"
print(score["Kim"])
```

---

## 6-2. 위치 접근

```python id="vc2uxg"
print(score.iloc[0])
```

---

# 7. Series 주요 함수

---

## 7-1. 평균

```python id="0g8q5g"
print(score.mean())
```

---

## 7-2. 최대값

```python id="r3zj7v"
print(score.max())
```

---

## 7-3. 합계

```python id="n65f4z"
print(score.sum())
```

---

# 8. Series 조건 필터링

```python id="pz0b0r"
print(score[score >= 80])
```

---

# 9. Series 활용 예제 (금융 데이터)

---

## 주식 가격 분석

```python id="0k3nvf"
stock = pd.Series(
    [50000, 51000, 49000, 53000],
    index=["Mon", "Tue", "Wed", "Thu"]
)

print(stock)

# 평균 주가
print("평균:", stock.mean())

# 최고가
print("최고:", stock.max())

# 상승한 날짜
print(stock[stock > 50000])
```

---

# 10. DataFrame이란?

## 정의

> DataFrame = 여러 개의 Series를 묶은 테이블 구조

즉:

* 행(row)
* 열(column)
* index

를 가진다.

---

# 11. DataFrame 구조

```python id="zry6e1"
# Pandas 라이브러리를 pd라는 이름으로 불러옵니다.
import pandas as pd

# 딕셔너리 형태로 데이터를 생성합니다.
# 각 key는 컬럼명(name, age, score)이 되고,
# 리스트 값은 각 행(row)의 데이터가 됩니다.
data = {
    "name": ["Kim", "Lee", "Park"],   # 이름 데이터
    "age": [20, 25, 30],              # 나이 데이터
    "score": [90, 80, 70]             # 점수 데이터
}

# 딕셔너리 데이터를 DataFrame 형태로 변환합니다.
# DataFrame은 표(Table) 형태의 데이터 구조입니다.
df = pd.DataFrame(data)

# 생성된 DataFrame 내용을 출력합니다.
print(df)
```

---

## 결과

```python id="xq0ncr"
   name  age  score
0   Kim   20     90
1   Lee   25     80
2  Park   30     70
```

---

# 12. DataFrame 내부 구조

```python id="98b1vq"
DataFrame
│
├── Index
│     [0,1,2]
│
├── Columns
│     ["name","age","score"]
│
└── Data
      ├── "name"
      │      ndarray(["Kim","Lee","Park"])
      │
      ├── "age"
      │      ndarray([20,25,30])
      │
      └── "score"
             ndarray([90,80,70])
```

---

# 13. DataFrame 기본 사용법

---

## 13-1. 컬럼 선택


```python id="kpsls8"
print(df[0])
```

👉 결과는 Series

```
0    Kim
1     20
2     90
Name: name, dtype: object
```

---

## 13-2. 여러 컬럼 선택

```python id="0ll4fa"
print(df[["name", "score"]])
```

## 결과
```
   name  score
0   Kim     90
1   Lee     80
2  Park     70
```
---

# 14. 행 선택(Row Selection)

Pandas에서 **행 선택**은 데이터 분석에서 가장 많이 사용하는 기능 중 하나입니다.
특정 행만 조회하거나, 조건에 맞는 데이터만 추출할 때 사용합니다.

주로 사용하는 방법은 다음과 같습니다.

1. `loc[]` → 이름(Index) 기반 선택
2. `iloc[]` → 숫자 위치(Index Number) 기반 선택
3. 조건식(Boolean Indexing) → 특정 조건의 행 선택
4. 슬라이싱(Slicing) → 여러 행 범위 선택

---

## 14-1. 실습용 데이터 생성

```python
import pandas as pd

# 학생 데이터 생성
data = {
    "name": ["Kim", "Lee", "Park", "Choi"],
    "age": [20, 25, 30, 22],
    "score": [90, 80, 70, 95]
}

# DataFrame 생성
df = pd.DataFrame(data)

print(df)
```

실행 결과

```python
   name  age  score
0   Kim   20     90
1   Lee   25     80
2  Park   30     70
3  Choi   22     95
```

---

## 14-2. loc[] : 이름(Index) 기반 행 선택

`loc[]`는 **행 이름(index label)** 을 기준으로 데이터를 선택합니다.
결과는 Series 자료 구조입니다. 즉 1차원 데이터 입니다  

기본 index는 `0,1,2,3` 입니다.

---

### 14-2-1. 한 개 행 선택

```python
print(df.loc[0])
```

설명

* index가 `0`인 행을 선택합니다.
* 첫 번째 행 데이터를 가져옵니다.

결과

```python
name     Kim
age        20
score      90
Name: 0, dtype: object
```

---

### 14-2-2. 여러 행 선택

```python
print(df.loc[[0, 2]])
```

설명

* index가 `0`, `2`인 행을 선택합니다.
* 리스트 형태로 여러 개 지정합니다.
* 결과는 DataFrame 입니다.
* 즉 2차원 배열 구조입니다 

결과

```python
   name  age  score
0   Kim   20     90
2  Park   30     70
```

---

### 14-2-3. 범위 선택

```python
print(df.loc[0:2])
```

설명

* index `0`부터 `2`까지 선택합니다.
* `loc`는 끝 번호 포함입니다.

결과

```python
   name  age  score
0   Kim   20     90
1   Lee   25     80
2  Park   30     70
```

---

## 14-3. iloc[] : 숫자 위치 기반 행 선택

`iloc[]`는 **행의 위치 번호(position)** 로 선택합니다.
현재는 index와 행의 위치 번호 동일하기 때문에 결과는 동일합니다.

Python 리스트처럼 동작합니다.

---

### 14-3-1. 한 개 행 선택

```python
print(df.iloc[1])
```

설명

* 위치 번호 `1`
* 두 번째 행 선택

결과

```python
name     Lee
age        25
score      80
Name: 1, dtype: object
```

---

### 14-3-2. 여러 행 선택

```python
print(df.iloc[[1, 3]])
```

설명

* 두 번째, 네 번째 행 선택

결과

```python
   name  age  score
1   Lee   25     80
3  Choi   22     95
```

---

### 14-3-3. 범위 선택

```python
print(df.iloc[0:2])
```

설명

* 위치 `0`부터 `2` 이전까지 선택
* Python 슬라이싱 규칙 적용
* 끝 번호 제외

결과

```python
   name  age  score
0   Kim   20     90
1   Lee   25     80
```

---

## 14-4. 조건으로 행 선택 (가장 중요)

데이터 분석에서 가장 많이 사용하는 방식입니다.
결과는 항상 DataFrame, 2차원 구조입니다.
결과가 1건이어도 DataFrame, 2차원 구조입니다

---

### 14-4-1. 점수가 80 이상인 학생 선택

```python
print(df[df["score"] >= 80])
```

설명

* `score` 값이 80 이상인 행만 선택합니다.

결과

```python
   name  age  score
0   Kim   20     90
1   Lee   25     80
3  Choi   22     95
```

---

### 14-4-2. 나이가 25 이상인 학생 선택

```python
print(df[df["age"] >= 25])
```

결과

```python
   name  age  score
1   Lee   25     80
2  Park   30     70
```

---

### 14-5. 여러 조건 사용

---

### 14-5-1. AND 조건

```python
print(df[(df["age"] >= 25) & (df["score"] >= 80)])
```

설명

* 나이 25 이상
* 점수 80 이상

두 조건을 모두 만족하는 행 선택

결과

```python
  name  age  score
1  Lee   25     80
```

---

### 14-5-2. OR 조건

```python
print(df[(df["score"] >= 90) | (df["age"] >= 30)])
```

설명

* 점수 90 이상
  또는
* 나이 30 이상

결과

```python
   name  age  score
0   Kim   20     90
2  Park   30     70
3  Choi   22     95
```

---

## 14-6. 특정 컬럼과 함께 행 선택

---

### 14-6-1. 특정 행 + 특정 컬럼

```python
print(df.loc[0, "name"])
```

설명

* index 0의
* name 컬럼 값 선택

결과

```python
Kim
```

---

### 14-6-2. 여러 행 + 여러 컬럼

```python
print(df.loc[[0, 1], ["name", "score"]])
```

결과

```python
  name  score
0  Kim     90
1  Lee     80
```

---

## 14-7. index 변경 후 loc 사용

index를 이름으로 변경할 수도 있습니다.

```python
df2 = df.set_index("name")

print(df2)
```

결과

```python
      age  score
name
Kim    20     90
Lee    25     80
Park   30     70
Choi   22     95
```

---

## 이름으로 행 선택

```python
print(df2.loc["Kim"])
```

결과

```python
age      20
score    90
Name: Kim, dtype: int64
```

---

## 14-8. loc 와 iloc 차이점 정리

| 구분              | loc                 | iloc           |
| ----------------- | ------------------- | -------------  |
| 기준              | 이름(index label)   | 숫자 위치      |
| 사용 방식         | df.loc[0]           | df.iloc[0]     |
| 범위 끝 포함 여부 | 포함                | 제외           |
| 실제 사용         | 조건 검색 많이 사용 | 위치 기반 처리 |

---

## 14-9. 가장 많이 사용하는 패턴

## 조건 검색

```python
df[df["score"] >= 90]
```

---

## 특정 컬럼만 보기

```python
df.loc[:, ["name", "score"]]
```

---

## 조건 + 컬럼 선택

```python
df.loc[df["score"] >= 80, ["name", "score"]]
```

---

## 14-10. 핵심 정리

| 기능           | 예제                    |
| -------------- | ----------------------- |
| 한 행 선택     | `df.loc[0]`             |
| 위치 기반 선택 | `df.iloc[1]`            |
| 여러 행 선택   | `df.loc[[0,2]]`         |
| 범위 선택      | `df.loc[0:2]`           |
| 조건 선택      | `df[df["score"] >= 80]` |
| AND 조건       | `(조건1) & (조건2)`     |
| OR 조건        | `(조건1) \| (조건2)`    |

행 선택은 Pandas 데이터 분석의 핵심 기능이며,
특히 조건 기반 행 선택(Boolean Indexing)은 매우 자주 사용합니다.

---

# 15. DataFrame 정보 확인

Pandas에서 `DataFrame`을 생성한 후 가장 먼저 해야 하는 작업은 데이터의 구조와 상태를 확인하는 것입니다.

이를 통해 다음 내용을 파악할 수 있습니다.

* 데이터 개수
* 컬럼 이름
* 데이터 타입(dtype)
* 결측치 여부
* 통계 정보
* 데이터 크기(shape)
* 일부 데이터 미리 보기

이 과정을 **EDA(탐색적 데이터 분석, Exploratory Data Analysis)** 의 시작 단계라고 합니다.

---

## 15-1. 실습용 데이터 생성

```python id="rt5qne"
# Pandas 라이브러리 불러오기
import pandas as pd

# 예제 데이터 생성
data = {
    "name": ["Kim", "Lee", "Park", "Choi", "Jung"],
    "age": [20, 25, 30, 22, 28],
    "score": [90, 80, 70, 95, 88],
    "city": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon"]
}

# DataFrame 생성
df = pd.DataFrame(data)

# 전체 데이터 출력
print(df)
```

---

## 15-2. head() : 상위 데이터 확인

데이터가 많을 경우 일부만 확인합니다.

```python id="mboq7y"
# 상위 5개 행 출력
print(df.head())
```

설명

* 기본값은 5개 행입니다.
* 데이터 구조를 빠르게 확인할 때 사용합니다.

---

## 원하는 개수만 보기

```python id="ktc8lt"
# 상위 3개 행 출력
print(df.head(3))
```

---

## 15-3. tail() : 하위 데이터 확인

마지막 데이터를 확인합니다.

```python id="c7r7l5"
# 마지막 5개 행 출력
print(df.tail())
```

---

## 원하는 개수 지정

```python id="7z0kct"
# 마지막 2개 행 출력
print(df.tail(2))
```

---

## 15-4. shape : 데이터 크기 확인

행(row)과 열(column) 개수를 확인합니다.

```python id="x8g3m0"
# DataFrame 크기 확인
print(df.shape)
```

결과

```python id="a8lvn2"
(5, 4)
```

설명

* 5개의 행(row)
* 4개의 컬럼(column)

---

## 15-5. columns : 컬럼 이름 확인

```python id="8lhws9"
# 컬럼 이름 확인
print(df.columns)
```

결과

```python id="0p1wri"
Index(['name', 'age', 'score', 'city'], dtype='object')
```

---

## 15-6. index : 인덱스 확인

```python id="42aqxy"
# index 정보 확인
print(df.index)
```

결과

```python id="s8l9ks"
RangeIndex(start=0, stop=5, step=1)
```

---

## 15-7. dtypes : 데이터 타입 확인

각 컬럼의 데이터 타입을 확인합니다.

```python id="0eu5qb"
# 컬럼별 데이터 타입 확인
print(df.dtypes)
```

결과

```python id="44qsgw"
name     object
age       int64
score     int64
city     object
dtype: object
```

---

# 데이터 타입 설명

| 타입       | 의미           |
| ---------- | -------------- |
| object     | 문자열(String) |
| int64      | 정수(Integer)  |
| float64    | 실수(Float)    |
| bool       | True/False     |
| datetime64 | 날짜/시간      |

---

## 15-8. info() : DataFrame 전체 정보 확인

가장 많이 사용하는 정보 확인 함수입니다.

```python id="ylv8qk"
# DataFrame 전체 정보 출력
print(df.info())
```

결과 예시

```python id="1cn3h4"
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5 entries, 0 to 4
Data columns (total 4 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   name    5 non-null      object
 1   age     5 non-null      int64
 2   score   5 non-null      int64
 3   city    5 non-null      object
```

---

## info()에서 확인 가능한 내용

| 항목           | 설명          |
| -------------- | -------       |
| RangeIndex     | 행 개수       |
| Column         | 컬럼 이름     |
| Non-Null Count | 결측치 여부   |
| Dtype          | 데이터 타입   |
| memory usage   | 메모리 사용량 |

---

## 15-9. describe() : 통계 정보 확인

숫자 데이터의 통계 정보를 자동 계산합니다.

```python id="w9pn2o"
# 숫자 데이터 통계 정보 확인
print(df.describe())
```

결과 예시

```python id="8j07xk"
             age      score
count   5.000000   5.000000
mean   25.000000  84.600000
std     4.123106   9.607289
min    20.000000  70.000000
max    30.000000  95.000000
```

---

### describe() 주요 항목 설명

| 항목  | 의미        |
| ----- | ----------- |
| count | 데이터 개수 |
| mean  | 평균        |
| std   | 표준편차    |
| min   | 최소값      |
| 25%   | 1사분위수   |
| 50%   | 중앙값      |
| 75%   | 3사분위수   |
| max   | 최대값      |

---

## 15-10. value_counts() : 값 개수 확인

범주형 데이터 분석 시 매우 중요합니다.

```python id="f0zvsz"
# city 값 개수 확인
print(df["city"].value_counts())
```

결과 : 
```
city
Seoul      1
Busan      1
Incheon    1
Daegu      1
Daejeon    1
Name: count, dtype: int64
```
---

## 15-11. unique() : 고유값 확인

```python id="e5r2s8"
# city 컬럼의 고유값 확인
print(df["city"].unique())


```

결과 : 
```
<StringArray>
['Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon']
Length: 5, dtype: str
```

---

## 15-12. nunique() : 고유값 개수 확인

```python id="jckn0m"
# city 컬럼의 고유값 개수
print(df["city"].nunique())
```

결과 :
```
5
```

---

## 15-13. isnull() : 결측치 확인

데이터 분석에서 매우 중요합니다.

---

### 결측치 여부 확인

```python id="4u0wzh"
# 결측치 여부 확인
print(df.isnull())
```

결과 : 
```
    name    age  score   city
0  False  False  False  False
1  False  False  False  False
2  False  False  False  False
3  False  False  False  False
4  False  False  False  False
```
---

### 컬럼별 결측치 개수 확인

```python id="7mbb9j"
# 컬럼별 결측치 개수 확인
print(df.isnull().sum())
```

결과 : 
```
name     0
age      0
score    0
city     0
dtype: int64
```
---

## 15-14. sample() : 랜덤 데이터 확인

```python id="8tsw8v"
# 랜덤으로 2개 행 출력
print(df.sample(2))
```

---

## 15-15. 전체 정보 확인 실무 패턴

실무에서는 아래 순서로 가장 많이 확인합니다.

```python id="7mpv6v"
# 1. 상위 데이터 확인
print(df.head())

# 2. 데이터 구조 확인
print(df.shape)

# 3. 컬럼 정보 확인
print(df.info())

# 4. 통계 정보 확인
print(df.describe())

# 5. 결측치 확인
print(df.isnull().sum())
```

---

## 15-16. 금융 데이터 분석 예제

```python id="8u3s2k"
import pandas as pd

# 금융 거래 데이터 생성
data = {
    "customer": ["Kim", "Lee", "Park", "Kim", "Lee"],
    "amount": [50000, 70000, 30000, 100000, 20000],
    "category": ["Food", "Shopping", "Transport", "Food", "Cafe"]
}

df = pd.DataFrame(data)

# 데이터 구조 확인
print(df.info())

# 통계 정보 확인
print(df.describe())

# category별 개수 확인
print(df["category"].value_counts())
```

---

## 15-17. 핵심 정리

| 함수           | 설명             |
| -------------- | ---------------- |
| head()         | 상위 데이터 확인 |
| tail()         | 하위 데이터 확인 |
| shape          | 행/열 개수       |
| columns        | 컬럼 이름        |
| dtypes         | 데이터 타입      |
| info()         | 전체 구조 확인   |
| describe()     | 통계 정보        |
| isnull()       | 결측치 확인      |
| value_counts() | 값 개수 확인     |
| unique()       | 고유값 확인      |

---

# 가장 중요한 함수 TOP 5

가장 많이 사용하는 함수는 다음과 같습니다.

```python id="9t4a9y"
df.head()
df.info()
df.describe()
df.shape
df.isnull().sum()
```

이 5개만 잘 사용해도 대부분의 데이터 구조를 빠르게 파악할 수 있습니다.

---

# 16. Pandas DataFrame 컬럼(Column) 관리

DataFrame에서 컬럼(Column)은 데이터를 구성하는 가장 중요한 요소입니다.
실무에서는 다음 작업을 매우 자주 수행합니다.

* 컬럼 조회
* 컬럼 추가
* 컬럼 수정
* 컬럼 삭제
* 컬럼 이름 변경
* 컬럼 순서 변경
* 새로운 계산 컬럼 생성
* 조건 기반 컬럼 생성

이번에는 위 기능들을 하나씩 자세하게 설명합니다.

---

## 16-1. 실습용 데이터 생성

```python id="5xpf3y"
# Pandas 라이브러리 불러오기
import pandas as pd

# 학생 데이터 생성
data = {
    "name": ["Kim", "Lee", "Park", "Choi", "Jung"],
    "age": [20, 25, 30, 22, 28],
    "score": [90, 80, 70, 95, 88],
    "city": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon"]
}

# DataFrame 생성
df = pd.DataFrame(data)

# 전체 데이터 출력
print(df)
```

실행 결과

```python id="b7i6vt"
    name  age  score      city
0    Kim   20     90     Seoul
1    Lee   25     80     Busan
2   Park   30     70   Incheon
3  Choi   22     95     Daegu
4   Jung   28     88   Daejeon
```

---

## 16-2. 컬럼(Column) 확인

---

## 16-2-1. 전체 컬럼 이름 확인

```python id="xj4kdy"
# 전체 컬럼 이름 확인
print(df.columns)
```

결과

```python id="x9h0eh"
Index(['name', 'age', 'score', 'city'], dtype='object')
```

---

### 16-2-2. 컬럼을 리스트 형태로 변환

```python id="5v4ckw"
# 컬럼명을 리스트로 변환
print(list(df.columns))
```

결과

```python id="fkkk6y"
['name', 'age', 'score', 'city']
```

---

## 16-3. 특정 컬럼 선택

---

### 16-3-1. 한 개 컬럼 선택

```python id="2jlwm0"
# name 컬럼 선택
print(df["name"])
```

설명

* Series 형태로 반환됩니다.

---

### 16-3-2. 여러 컬럼 선택

```python id="8t5uxu"
# name, score 컬럼 선택
print(df[["name", "score"]])
```

설명

* DataFrame 형태로 반환됩니다.
* 리스트 형태로 컬럼명을 전달합니다.

---

## 16-4. 새로운 컬럼 추가

---

### 16-4-1. 고정값 컬럼 추가

```python id="e57h9m"
# gender 컬럼 추가
df["gender"] = "M"

# 결과 출력
print(df)
```

설명

* 모든 행에 동일한 값이 들어갑니다.

---

### 16-4-2. 리스트 데이터로 컬럼 추가

```python id="0xw6nv"
# grade 컬럼 추가
df["grade"] = ["A", "B", "C", "A", "B"]

# 결과 출력
print(df)
```

---

## 16-5. 계산된 컬럼 추가

실무에서 가장 많이 사용하는 방식입니다.

---

### 16-5-1. 점수 보너스 컬럼 생성

```python id="8vtksw"
# score 컬럼에 5점 추가한 bonus_score 컬럼 생성
df["bonus_score"] = df["score"] + 5

# 결과 출력
print(df)
```

설명

* 기존 컬럼을 이용하여 새로운 컬럼 생성

---

### 16-5-2. 나이 10년 후 컬럼 생성

```python id="6jnd6x"
# 10년 후 나이 계산
df["future_age"] = df["age"] + 10

# 결과 출력
print(df)
```

---

## 16-6. 조건 기반 컬럼 생성

---

# 16-6-1. 합격 여부 컬럼 생성

```python id="39hxvw"
# score가 80 이상이면 Pass, 아니면 Fail
# lambda 구문으로 표현하는 방법 
df["result"] = df["score"].apply(
    lambda x: "Pass" if x >= 80 else "Fail"
)

# where() 함수 사용하는 방법 
df["result"] = np.where(df["score"] >= 80, "Pass", "Fail")


# ().map() 함수를 사용하는 방법 
df["result"] = (df["score"] >= 80).map({
    True: "Pass",
    False: "Fail"
})

# 결과 출력
print(df)
```

설명

* `apply()` 함수 사용
* `lambda`를 이용한 조건 처리
* () 표기법은 Pandas 스타일로 간단하게 true/false로 함. 
* ().map() 함수를 사용하여 원하는 결과로 변경함  

---

# 16-7. 컬럼 수정

---

### 16-7-1. 기존 컬럼 값 수정

```python id="lrmjtx"
# score 컬럼에 10점 추가
df["score"] = df["score"] + 10

# 결과 출력
print(df)
```

---

### 16-7-2. 문자열 수정

```python id="xv7fqe"
# city 컬럼 값을 모두 대문자로 변경
df["city"] = df["city"].str.upper()

# 결과 출력
print(df)
```

결과 예시

```python id="5q7nmy"
SEOUL
BUSAN
INCHEON
```

---

## 16-8. 컬럼 이름 변경

---

### 16-8-1. rename() 사용

```python id="1hh8pc"
# 컬럼 이름 변경
df.rename(
    columns={
        "name": "student_name",
        "score": "exam_score"
    },
    inplace=True
)

# 결과 출력
print(df)
```

설명

* `columns={기존:새이름}`
* `inplace=True` → 원본 데이터 직접 수정

---

## 16-9. 전체 컬럼명 변경

```python id="ww1sfe"
# 전체 컬럼명 변경
df.columns = [
    "NAME",
    "AGE",
    "SCORE",
    "CITY"
]

# 결과 출력
print(df)
```

주의

* 컬럼 개수가 정확히 일치해야 합니다.

---

## 16-10. 컬럼 삭제

---

### 16-10-1. 한 개 컬럼 삭제

```python id="m5j4a7"
# city 컬럼 삭제
df = df.drop("city", axis=1)

# 결과 출력
print(df)
```

설명

* `axis=1` → 컬럼 삭제
* `axis=0` → 행 삭제

---

### 16-10-2. 여러 컬럼 삭제

```python id="d3d65t"
# age, city 컬럼 삭제
df = df.drop(["age", "city"], axis=1)

# 결과 출력
print(df)
```

---

## 16-11. 컬럼 순서 변경

```python id="2w6vhj"
# 컬럼 순서 재배치
df = df[["city", "name", "score", "age"]]

# 결과 출력
print(df)
```

설명

* 원하는 순서대로 리스트 작성

---

## 16-12. 컬럼 존재 여부 확인

```python id="s0y9yf"
# score 컬럼 존재 여부 확인
print("score" in df.columns)
```

결과

```python id="gspmvk"
True
```

---

## 16-13. 데이터 타입 변경

---

## age를 문자열로 변경

```python id="v4kpnm"
# age 컬럼 타입 변경
df["age"] = df["age"].astype(str)

# 데이터 타입 확인
print(df.dtypes)
```

---

## 16-14. 실습 예제

```python id="jlwmye"
import pandas as pd

# 데이터 생성
data = {
    "name": ["Kim", "Lee", "Park", "Choi", "Jung"],
    "age": [20, 25, 30, 22, 28],
    "score": [90, 80, 70, 95, 88],
    "city": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon"]
}

# DataFrame 생성
df = pd.DataFrame(data)

# -----------------------------
# 새로운 컬럼 추가
# -----------------------------

# bonus 컬럼 생성
df["bonus"] = df["score"] + 5

# 합격 여부 컬럼 생성
df["result"] = df["score"].apply(
    lambda x: "Pass" if x >= 80 else "Fail"
)

# -----------------------------
# 컬럼 이름 변경
# -----------------------------

df.rename(
    columns={
        "name": "student_name",
        "score": "exam_score"
    },
    inplace=True
)

# -----------------------------
# 컬럼 삭제
# -----------------------------

df = df.drop("city", axis=1)

# -----------------------------
# 결과 출력
# -----------------------------

print(df)
```

---

# 17. Pandas DataFrame 결측치(Missing Value) 처리

## 17-1. 결측치란?

결측치(Missing Value)란 데이터가 비어있는 값을 의미합니다.
Pandas에서는 보통 아래와 같이 표현됩니다.

* `NaN` : 숫자형 데이터 결측치
* `None` : 객체(Object) 타입 결측치
* `pd.NA` : Pandas 최신 결측 표현

실무에서는 다음과 같은 이유로 자주 발생합니다.

* 센서 오류
* 사용자 입력 누락
* 데이터 수집 실패
* CSV 파일 오류
* DB 저장 실패

---

## 17-2. 예제 데이터 생성

```python
import pandas as pd
import numpy as np

# 학생 성적 데이터 생성
df = pd.DataFrame({
    '이름': ['김철수', '이영희', '박민수', '최지은', '한지민'],
    '수학': [90, 85, np.nan, 70, 100],
    '영어': [88, np.nan, 75, 95, 92],
    '과학': [np.nan, 80, 85, 90, 95]
})

print(df)
```

---

### 실행 결과

```python
     이름     수학    영어    과학
0  김철수   90.0  88.0   NaN
1  이영희   85.0   NaN  80.0
2  박민수    NaN  75.0  85.0
3  최지은   70.0  95.0  90.0
4  한지민  100.0  92.0  95.0
```

---

## 17-3. 결측치 확인 방법

### (1) isnull()

결측치 여부를 True/False로 확인합니다.

```python
print(df.isnull())
```

---

### 실행 결과

```python
      이름     수학     영어     과학
0  False  False  False   True
1  False  False   True  False
2  False   True  False  False
3  False  False  False  False
4  False  False  False  False
```

---

## 17-4. 결측치 개수 확인

## (1) 컬럼별 결측치 개수

```python
print(df.isnull().sum())
```

---

## 실행 결과

```python
이름    0
수학    1
영어    1
과학    1
dtype: int64
```

---

## 17-5. 결측치가 있는 행 조회

```python
print(df[df.isnull().any(axis=1)])
```

---

## 설명

* `axis=1`

  * 행(Row) 기준 검사


* `any()`

  * 하나라도 결측치가 있으면 True

---

## 17-6. 결측치 제거

### (1) 결측치가 있는 행 제거

```python
df_drop = df.dropna()

print(df_drop)
```

---

### 실행 결과

```python
     이름     수학    영어    과학
3  최지은   70.0  95.0  90.0
4  한지민  100.0  92.0  95.0
```

---

## 17-7. 특정 컬럼 결측치 제거

## 영어 점수가 없는 학생 제거

```python
df_drop_eng = df.dropna(subset=['영어'])

print(df_drop_eng)
```

---

## 17-8. 결측치 채우기(fillna)

---

### (1) 고정값으로 채우기

```python
df_fill = df.fillna(0)

print(df_fill)
```

---

### 실행 결과

```python
     이름     수학    영어    과학
0  김철수   90.0  88.0   0.0
1  이영희   85.0   0.0  80.0
2  박민수    0.0  75.0  85.0
3  최지은   70.0  95.0  90.0
4  한지민  100.0  92.0  95.0
```

---

## 17-9. 평균값으로 결측치 채우기

실무에서 가장 많이 사용하는 방법 중 하나입니다.

```python
# 수학 평균 계산
math_mean = df['수학'].mean()

# 결측치 평균값으로 대체
df['수학'] = df['수학'].fillna(math_mean)

print(df)
```

---

### 설명

* `mean()` : 평균 계산
* `fillna()` : 결측치 채우기

---

## 17-10. 여러 컬럼 평균값으로 채우기

```python
df_fill_mean = df.fillna(df.mean(numeric_only=True))

print(df_fill_mean)
```

---

## 17-11. 이전 값으로 채우기 (Forward Fill)

## ffill()

위의 데이터를 아래로 복사합니다.

```python
df_ffill = df.ffill()

print(df_ffill)
```

---

### 예시 설명

```python
NaN → 바로 위 값 사용
```

---

## 17-12. 다음 값으로 채우기 (Backward Fill)


## bfill()

아래 데이터를 위로 복사합니다.

```python
df_bfill = df.bfill()

print(df_bfill)
```

---

## 17-13. 특정 값만 결측치 처리

예를 들어 `-1` 을 결측치로 변경할 수 있습니다.

```python
df2 = pd.DataFrame({
    '점수': [90, -1, 85, -1, 100]
})

# -1을 NaN으로 변경
df2['점수'] = df2['점수'].replace(-1, np.nan)

print(df2)
```

---

## 17-14. interpolate() 선형 보간

시계열 데이터 분석에서 매우 많이 사용됩니다.

```python
df3 = pd.DataFrame({
    '온도': [20, np.nan, np.nan, 26, 28]
})

# 선형 보간
df3['온도'] = df3['온도'].interpolate()

print(df3)
```

---

### 실행 결과

```python
    온도
0  20.0
1  22.0
2  24.0
3  26.0
4  28.0
```

---

## 17-15. 예제

## 쇼핑몰 주문 데이터 결측치 처리

```python
import pandas as pd
import numpy as np

# 주문 데이터
orders = pd.DataFrame({
    '주문번호': [101, 102, 103, 104, 105],
    '고객명': ['김철수', '이영희', None, '박민수', '최지은'],
    '결제금액': [50000, np.nan, 70000, 65000, np.nan],
    '배송지역': ['서울', '부산', '서울', None, '대전']
})

print("===== 원본 데이터 =====")
print(orders)

# --------------------------------------------------
# 1. 고객명이 없는 데이터 확인
# --------------------------------------------------

print("\n===== 고객명 결측치 확인 =====")
print(orders['고객명'].isnull())

# --------------------------------------------------
# 2. 결제금액 평균 계산
# --------------------------------------------------

avg_price = orders['결제금액'].mean()

print("\n결제금액 평균:", avg_price)

# --------------------------------------------------
# 3. 결제금액 결측치 평균값으로 채우기
# --------------------------------------------------

orders['결제금액'] = orders['결제금액'].fillna(avg_price)

# --------------------------------------------------
# 4. 배송지역 결측치 '미확인'으로 처리
# --------------------------------------------------

orders['배송지역'] = orders['배송지역'].fillna('미확인')

# --------------------------------------------------
# 5. 고객명이 없는 행 제거
# --------------------------------------------------

orders = orders.dropna(subset=['고객명'])

# --------------------------------------------------
# 최종 결과 출력
# --------------------------------------------------

print("\n===== 결측치 처리 완료 =====")
print(orders)
```

---

## 17-16. 실무에서 자주 사용하는 결측치 처리 전략

| 상황             | 처리 방법           |
| ---------------- | ------------------- |
| 데이터 일부 누락 | 평균값 대체         |
| 시계열 데이터    | ffill / bfill       |
| 중요 데이터 없음 | 행 제거             |
| 범주형 데이터    | "Unknown", "미확인" |
| 센서 데이터      | interpolate()       |
| AI 학습 데이터   | 중앙값(median) 사용 |

---

## 17-17. 결측치 처리 시 주의사항

### 평균값 대체 문제점

이상치(Outlier)가 있으면 평균이 왜곡될 수 있습니다.

```python
df['컬럼'].median()
```

중앙값 사용이 더 안전한 경우가 많습니다.

---

# 18. 결측치 처리 핵심 함수 정리

| 함수          | 설명             |
| ------------- | ---------------- |
| isnull()      | 결측치 확인      |
| notnull()     | 결측치 아님 확인 |
| dropna()      | 결측치 제거      |
| fillna()      | 결측치 채우기    |
| ffill()       | 이전 값 채우기   |
| bfill()       | 다음 값 채우기   |
| interpolate() | 선형 보간        |
| replace()     | 특정값 변경      |

---

## 17-19. 머신러닝에서 매우 중요한 이유

결측치가 존재하면 다음 문제가 발생합니다.

* 머신러닝 모델 오류 발생
* 통계 분석 왜곡
* 시각화 오류
* 데이터 품질 저하

따라서 데이터 전처리 단계에서 반드시 처리해야 합니다.

---


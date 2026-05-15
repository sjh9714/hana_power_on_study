# Pandas 데이터처리

## Pandas 여러가지 함수

Pandas는 데이터 분석에서 매우 강력한 기능을 제공합니다.
그 중에서도 실무에서 가장 많이 사용하는 핵심 기능은 다음과 같습니다.

| 기능            | 설명                               |
| --------------- | ---------------------------------- |
| `pivot_table()` | 데이터를 요약하여 피벗 테이블 생성 |
| `merge()`       | 여러 데이터프레임 결합             |
| `concat()`      | 데이터프레임 연결                  |
| `apply()`       | 사용자 정의 함수 적용              |
| `transform()`   | 그룹별 계산 후 원래 형태 유지      |
| `query()`       | SQL 스타일 데이터 조회             |

---

# 1. pivot_table()

## 개념

`pivot_table()`은 데이터를 그룹화하고 요약하여 엑셀의 피벗 테이블처럼 분석할 수 있게 해주는 기능입니다.

주로 아래 작업에 사용합니다.

* 부서별 평균 급여
* 월별 매출 합계
* 지역별 판매량 집계
* 카테고리별 통계 분석

---

# 기본 예제

## 직원 데이터 생성

```python
import pandas as pd

# 직원 데이터 생성
df = pd.DataFrame({
    '부서': ['IT', 'IT', 'HR', 'HR', '영업'],
    '직급': ['대리', '과장', '대리', '과장', '대리'],
    '급여': [300, 500, 280, 450, 350]
})

print(df)
```

## 실행 결과

```python
   부서 직급   급여
0  IT 대리  300
1  IT 과장  500
2  HR 대리  280
3  HR 과장  450
4  영업 대리  350
```

---

## 피벗 테이블 생성

```python
# 부서별 평균 급여 계산
pivot = df.pivot_table(
    index='부서',     # 행 기준
    values='급여',    # 계산할 값
    aggfunc='mean'    # 평균 계산
)

print(pivot)
```

---

## 실행 결과

```python
       급여
부서
HR   365
IT   400
영업  350
```

---

# 활용 예제

## 부서 + 직급별 평균 급여

```python
pivot = df.pivot_table(
    index='부서',
    columns='직급',
    values='급여',
    aggfunc='mean',
    fill_value=0
)

print(pivot)
```

---

## 실행 결과

|부서\직급   |  과장  |   대리 |
|----|---|---|
|HR   |   450.0 | 280.0 | 
|IT   |   500.0 | 300.0 |
|영업 |     0.0 | 350.0 |

---

## 설명

| 옵션         | 의미        |
| ------------ | ----------  |
| `index`      | 행 기준     |
| `columns`    | 열 기준     |
| `values`     | 계산 대상   |
| `aggfunc`    | 집계 함수   |
| `fill_value` | NaN 대체값  |

---

# 2. merge()

# 개념

`merge()`는 SQL의 JOIN과 동일한 기능입니다.

두 개 이상의 데이터프레임을 공통 컬럼 기준으로 합칩니다.

---

# 기본 예제

## 고객 정보

```python
customer = pd.DataFrame({
    '고객ID': [1, 2, 3],
    '이름': ['김철수', '이영희', '박민수']
})
```

## 주문 정보

```python
order = pd.DataFrame({
    '고객ID': [1, 1, 2],
    '주문금액': [10000, 20000, 15000]
})
```

---

## 데이터 결합

```python
# 고객ID 기준으로 INNER JOIN 수행
result = pd.merge(
    customer,
    order,
    on='고객ID',
    how='inner'
)

print(result)
```

## 실행 결과

```python
   고객ID   이름  주문금액
0      1  김철수  10000
1      1  김철수  20000
2      2  이영희  15000
```

## 컬럼명이 다른 경우 

```python
customer = pd.DataFrame({
    '고객ID': [1, 2, 3],
    '이름': ['김철수', '이영희', '박민수']
})

order = pd.DataFrame({
    '고객아이디': [1, 1, 2],
    '주문금액': [10000, 20000, 15000]
})

# 고객ID 기준으로 INNER JOIN 수행
result = pd.merge(
    customer,
    order,
    left_on='고객ID',
    right_on='고객아이디',
    how='inner'
)

print(result)

#두개중 한개의 컬럼을 삭제함 
result = result.drop(columns=['고객아이디'])

print(result)

```

결과 : 

```

   고객ID   이름  고객아이디   주문금액
0     1  김철수      1  10000
1     1  김철수      1  20000
2     2  이영희      2  15000

   고객ID   이름    주문금액
0     1  김철수      10000
1     1  김철수      20000
2     2  이영희      15000
```

---

# 활용 예제

## LEFT JOIN

```python
result = pd.merge(
    customer,
    order,
    on='고객ID',
    how='left'
)

print(result)
```

---

## JOIN 종류

| 옵션    | 설명        |
| ----- | --------- |
| inner | 공통 데이터만   |
| left  | 왼쪽 기준 전체  |
| right | 오른쪽 기준 전체 |
| outer | 전체 데이터    |

---

# 3. concat()

# 개념

`concat()`은 데이터프레임을 위아래 또는 좌우로 연결합니다.

주로 아래 상황에서 사용합니다.

* 월별 데이터 합치기
* 여러 CSV 통합
* 컬럼 추가 연결

---

# 기본 예제

## 데이터 생성

```python
df1 = pd.DataFrame({
    '이름': ['김철수', '이영희']
})

df2 = pd.DataFrame({
    '이름': ['박민수', '최수진']
})
```

---

## 위아래 연결

```python
result = pd.concat([df1, df2])

print(result)
```

---

## 실행 결과

```python
     이름
0  김철수
1  이영희
0  박민수
1  최수진
```

---

# 인덱스 재정렬

```python
result = pd.concat(
    [df1, df2],
    ignore_index=True
)

print(result)
```

출력결과 :

```phthon
    이름
0  김철수
1  이영희
2  박민수
3  최수진
```

---

# 활용 예제

## 좌우 연결

```python
name_df = pd.DataFrame({
    '이름': ['김철수', '이영희']
})

score_df = pd.DataFrame({
    '점수': [90, 80]
})

result = pd.concat(
    [name_df, score_df],
    axis=1
)

print(result)
```

## 결과 : 

```python
     이름  점수
0  김철수  90
1  이영희  80
```

---


# 설명

| 옵션         | 설명            |
| ------------ | -----------     |
| axis=0       | 세로 연결(기본) |
| axis=1       | 가로 연결       |
| ignore_index | 인덱스 재정렬   |

---

# 4. apply()

# 개념

`apply()`는 각 행 또는 열에 사용자 정의 함수를 적용합니다.

실무에서 매우 많이 사용됩니다.

---

# 기본 예제

## 점수 데이터

```python
df = pd.DataFrame({
    '점수': [70, 85, 90]
})
```

---

## 함수 생성

```python
# 합격 여부 판단 함수
def pass_check(score):

    # 80점 이상이면 합격
    if score >= 80:
        return '합격'
    else:
        return '불합격'
```

---

## 함수 적용

```python
# apply()로 함수 적용
df['결과'] = df['점수'].apply(pass_check)

print(df)
```

---

## 실행 결과

```python
   점수    결과
0  70  불합격
1  85   합격
2  90   합격
```

---

# 활용 예제 (람다 함수 사용)

```python
# 점수를 등급으로 변환
df['등급'] = df['점수'].apply(
    lambda x: 'A' if x >= 90 else 'B'
)

print(df)
```

---

## 실행 결과

```python
   점수    결과
0  70  불합격
1  85   합격
2  90   합격
```

---

# 행 단위 처리

```python
df = pd.DataFrame({
    '국어': [90, 80],
    '영어': [85, 95]
})

# 평균 계산
df['평균'] = df.apply(
    lambda row: (row['국어'] + row['영어']) / 2,
    axis=1
)

print(df)
```

## 실행 결과 :

```python
   국어  영어  평균
0  90  85  87.5
1  80  95  87.5 
```

---

# 설명

| 옵션     | 설명   |
| ------ | ---- |
| axis=0 | 열 기준 |
| axis=1 | 행 기준 |

---

# 5. transform()

# 개념

`transform()`은 그룹별 계산 결과를
원래 데이터 개수 그대로 유지하면서 반환합니다.

`groupby()`와 함께 많이 사용합니다.

---

# 기본 예제

```python
df = pd.DataFrame({
    '부서': ['IT', 'IT', 'HR', 'HR'],
    '급여': [300, 500, 280, 450]
})
```

---

## 부서 평균 급여 계산

```python
# transform() 사용
df['부서평균급여'] = df.groupby('부서')['급여'].transform('mean')

print(df)
```

---

## 실행 결과

```python
   부서   급여  부서평균급여
0  IT  300    400
1  IT  500    400
2  HR  280    365
3  HR  450    365
```

---

# 활용 예제

## 부서 평균 대비 차이 계산

```python
# 부서 평균 계산
df['부서평균'] = df.groupby('부서')['급여'].transform('mean')

# 평균 대비 차이 계산
df['평균차이'] = df['급여'] - df['부서평균']

print(df)
```

---

# transform() 특징

| 기능                    | 설명       |
| --------------------- | -------- |
| groupby().agg()       | 그룹 결과 축소 |
| groupby().transform() | 원본 크기 유지 |

---

# 6. query()

# 개념

`query()`는 SQL WHERE 문처럼 데이터를 조회합니다.

가독성이 매우 좋습니다.

---

# 기본 예제

```python
df = pd.DataFrame({
    '이름': ['김철수', '이영희', '박민수'],
    '나이': [25, 32, 28]
})
```

---

## 조건 조회

```python
# 나이가 30 이상인 데이터 조회
result = df.query('나이 >= 30')

print(result)
```

---

## 실행 결과

```python
    이름  나이
1  이영희   32
```

---

# 활용 예제

## AND 조건

```python
df = pd.DataFrame({
    '이름': ['김철수', '이영희', '박민수'],
    '나이': [25, 32, 28],
    '부서': ['IT', 'HR', 'IT']
})

# 조건 조회
result = df.query(
    '나이 >= 25 and 부서 == "IT"'
)

print(result)
```

---

# 변수 사용

```python
age = 30

# @ 사용
result = df.query('나이 >= @age')

print(result)
```

---

# query() 장점

| 장점           | 설명              |
| -------------- | ----------------- |
| 가독성 우수    | SQL과 유사        |
| 코드 간결      | 조건식 단순       |
| 복합 조건 편리 | and/or 사용 가능  |

---

# 실무 종합 예제

```python
import pandas as pd

# 판매 데이터 생성
df = pd.DataFrame({
    '지역': ['서울', '서울', '부산', '부산'],
    '상품': ['노트북', '마우스', '노트북', '마우스'],
    '판매액': [100, 20, 120, 30]
})

# 1. 피벗 테이블 생성
pivot = df.pivot_table(
    index='지역',
    columns='상품',
    values='판매액',
    aggfunc='sum'
)

print("피벗 테이블")
print(pivot)

# 2. query로 조건 조회
result = df.query('판매액 >= 50')

print("\n고액 판매")
print(result)

# 3. transform으로 지역 평균 계산
df['지역평균'] = df.groupby('지역')['판매액'].transform('mean')

print("\n지역 평균 추가")
print(df)
```

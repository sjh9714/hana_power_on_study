# Pandas 데이터처리

## 데이터 그룹(GroupBy) / 정렬(Sort)

데이터 분석에서 가장 많이 사용하는 기능 중 하나가 바로 **그룹(GroupBy)** 과 **정렬(Sort)** 입니다.
특히 금융 데이터, 로그 데이터, 쇼핑몰 데이터, IoT 데이터 분석에서 매우 중요합니다.

---

# 1. Pandas 그룹(GroupBy)이란?

`groupby()` 는 특정 기준으로 데이터를 묶어서 통계 계산을 수행하는 기능입니다.

예를 들어:
 
| 부서 | 급여  |
| ---- | ----: |
| 개발 | 300   |
| 개발 | 400   |
| 인사 | 250   |

위 데이터를 부서별로 묶으면:

* 개발 → 300, 400
* 인사 → 250

이렇게 그룹화 후:

* 평균
* 합계
* 최대값
* 최소값
* 개수

등을 계산할 수 있습니다.

---

# 2. 기본 데이터 생성

```python
import pandas as pd

# 샘플 데이터 생성
data = {
    '이름': ['김철수', '이영희', '박민수', '최지은', '홍길동'],
    '부서': ['개발', '개발', '인사', '인사', '개발'],
    '급여': [300, 450, 250, 280, 500],
    '나이': [29, 31, 35, 28, 40]
}

# DataFrame 생성
df = pd.DataFrame(data)

# 출력
print(df)
```

---

# 실행 결과

```python
    이름   부서   급여  나이
0  김철수  개발  300  29
1  이영희  개발  450  31
2  박민수  인사  250  35
3  최지은  인사  280  28
4  홍길동  개발  500  40
```

---

# 3. 그룹(GroupBy) 기본 사용법

## (1) 부서별 급여 평균

```python
import pandas as pd

# 데이터 생성
data = {
    '부서': ['개발', '개발', '인사', '인사', '개발'],
    '급여': [300, 450, 250, 280, 500]
}

df = pd.DataFrame(data)

# 부서별 그룹화 후 평균 계산
result = df.groupby('부서')['급여'].mean()

# 결과 출력
print(result)
```

---

# 결과

```python
부서
개발    416.666667
인사    265.000000
```

---

# 설명

```python
df.groupby('부서')
```

의미:

* 부서 기준으로 데이터를 묶습니다.

```python
['급여']
```

의미:

* 급여 컬럼만 선택합니다.

```python
.mean()
```

의미:

* 평균을 계산합니다.

---

# 4. 그룹 통계 함수

| 함수    | 설명     |
| ------- | ------   |
| mean()  | 평균     |
| sum()   | 합계     |
| max()   | 최대값   |
| min()   | 최소값   |
| count() | 개수     |
| std()   | 표준편차 |

---

# 5. 여러 통계 한번에 계산하기

```python
import pandas as pd

# 데이터 생성
data = {
    '부서': ['개발', '개발', '인사', '인사', '개발'],
    '급여': [300, 450, 250, 280, 500]
}

df = pd.DataFrame(data)

# 여러 통계를 한번에 계산
result = df.groupby('부서')['급여'].agg(['mean', 'sum', 'max', 'min'])

print(result)
```

---

# 결과

```python
           mean   sum  max  min
부서
개발  416.666667  1250  500  300
인사  265.000000   530  280  250
```

---

# 6. 여러 컬럼 기준 그룹화

## 부서 + 나이 기준 그룹화

```python
import pandas as pd

# 데이터 생성
data = {
    '부서': ['개발', '개발', '인사', '인사', '개발'],
    '나이': [29, 31, 35, 28, 29],
    '급여': [300, 450, 250, 280, 500]
}

df = pd.DataFrame(data)

# 여러 컬럼 기준 그룹화
result = df.groupby(['부서', '나이'])['급여'].mean()

print(result)
```

---

# 결과

```python
부서  나이
개발  29    400.0
     31    450.0
인사  28    280.0
     35    250.0
```

---

# 7. 정렬(Sort)이란?

정렬은 데이터를:

* 오름차순
* 내림차순

으로 정리하는 기능입니다.

---

# 8. sort_values() 기본 사용법

## 급여 기준 오름차순 정렬

```python
import pandas as pd

# 데이터 생성
data = {
    '이름': ['김철수', '이영희', '박민수'],
    '급여': [300, 500, 250]
}

df = pd.DataFrame(data)

# 급여 기준 오름차순 정렬
result = df.sort_values(by='급여')

print(result)
```

---

# 결과

```python
    이름   급여
2  박민수  250
0  김철수  300
1  이영희  500
```

---

# 9. 내림차순 정렬

```python
import pandas as pd

# 데이터 생성
data = {
    '이름': ['김철수', '이영희', '박민수'],
    '급여': [300, 500, 250]
}

df = pd.DataFrame(data)

# 급여 기준 내림차순 정렬
result = df.sort_values(by='급여', ascending=False)

print(result)
```

---

# 결과

```python
    이름   급여
1  이영희  500
0  김철수  300
2  박민수  250
```

---

# 설명

```python
ascending=False
```

의미:

* 내림차순 정렬을 수행합니다.

---

# 10. 여러 컬럼 기준 정렬

```python
import pandas as pd

# 데이터 생성
data = {
    '부서': ['개발', '개발', '인사', '인사'],
    '급여': [300, 500, 250, 500],
    '나이': [29, 25, 35, 28]
}

df = pd.DataFrame(data)

# 여러 컬럼 기준 정렬
result = df.sort_values(
    by=['급여', '나이'],
    ascending=[False, True]
)

print(result)
```

---

# 설명

```python
by=['급여', '나이']
```

의미:

1차 기준:

* 급여

2차 기준:

* 나이

---

```python
ascending=[False, True]
```

의미:

* 급여 → 내림차순
* 나이 → 오름차순

---

# 11. 그룹 + 정렬 함께 사용하기

실무에서 가장 많이 사용하는 형태입니다.

---

# 부서별 평균 급여 계산 후 정렬

```python
import pandas as pd

# 데이터 생성
data = {
    '부서': ['개발', '개발', '인사', '인사', '영업'],
    '급여': [300, 450, 250, 280, 600]
}

df = pd.DataFrame(data)

# 부서별 평균 급여 계산
result = (
    df.groupby('부서')['급여']
      .mean()
      .sort_values(ascending=False)
)

print(result)
```

---

# 결과

```python
부서
영업    600.0
개발    375.0
인사    265.0
```

---

# 12. reset_index()

groupby 결과는 인덱스 구조가 변경됩니다.

이를 일반 DataFrame 형태로 되돌릴 때 사용합니다.

```python
import pandas as pd

# 데이터 생성
data = {
    '부서': ['개발', '개발', '인사'],
    '급여': [300, 500, 250]
}

df = pd.DataFrame(data)

# 그룹화 후 평균 계산
result = (
    df.groupby('부서')['급여']
      .mean()
)

print(result)


# 그룹화 후 평균 계산, 재색인
result = (
    df.groupby('부서')['급여']
      .mean()
      .reset_index()
)

print(result)
```

---

# 결과

```python
# 그룹화 후 평균 계산
부서
개발    400.0
인사    250.0
Name: 급여, dtype: float64

# 그룹화 후 평균 계산, 재색인
   부서     급여
0  개발  400.0
1  인사  250.0
```

---

# 13. 실무 활용 예제 (금융 데이터 분석)

# 고객별 총 결제 금액 계산

```python
import pandas as pd

# 거래 데이터 생성
data = {
    '고객': ['김철수', '김철수', '이영희', '박민수', '이영희'],
    '카테고리': ['식비', '쇼핑', '식비', '교통', '쇼핑'],
    '금액': [12000, 50000, 15000, 7000, 30000]
}

df = pd.DataFrame(data)

# 고객별 총 소비 금액 계산
result = (
    df.groupby('고객')['금액']
      .sum()
      .sort_values(ascending=False)
      .reset_index()
)

print(result)
```

---

# 결과

```python
     고객     금액
0  김철수  62000
1  이영희  45000
2  박민수   7000
```

---

# 14. 카테고리별 소비 분석

```python
import pandas as pd

# 거래 데이터 생성
data = {
    '카테고리': ['식비', '쇼핑', '식비', '교통', '쇼핑', '교통'],
    '금액': [12000, 50000, 15000, 7000, 30000, 9000]
}

df = pd.DataFrame(data)

# 카테고리별 통계 계산
result = (
    df.groupby('카테고리')['금액']
      .agg(['sum', 'mean', 'max'])
      .sort_values(by='sum', ascending=False)
)

print(result)
```

---

# 결과

```python
           sum    mean    max
카테고리
쇼핑      80000  40000  50000
식비      27000  13500  15000
교통      16000   8000   9000
```

---

# 15. 자주 사용하는 실무 패턴

---

# TOP N 데이터 추출

```python
# 급여 상위 3명
top3 = df.sort_values(by='급여', ascending=False).head(3)

print(top3)
```

---

# 그룹별 최대값 찾기

```python
# 부서별 최고 급여
result = df.groupby('부서')['급여'].max()

print(result)
```

---

# 그룹별 데이터 개수

```python
# 부서별 인원 수
result = df.groupby('부서').size()

print(result)
```

---

# 16. 매우 중요한 핵심 정리

| 기능            | 설명             |
| --------------- | ---------------  |
| groupby()       | 그룹화           |
| agg()           | 여러 통계 계산   |
| sort_values()   | 값 정렬          |
| ascending=False | 내림차순         |
| reset_index()   | 인덱스 초기화    |
| head()          | 상위 데이터 조회 |

---

# 17. 실무에서 가장 많이 사용하는 형태

```python
result = (
    df.groupby('부서')['급여']
      .mean()
      .sort_values(ascending=False)
      .reset_index()
)

print(result)
```

이 패턴은:

* 데이터 분석
* 머신러닝 전처리
* 금융 데이터 분석
* 로그 분석
* 매출 분석

에서 매우 자주 사용됩니다.


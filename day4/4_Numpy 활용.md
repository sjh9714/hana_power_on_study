# NumPy란?

NumPy 는 Python에서 **수치 계산(Numerical Computing)** 을 빠르게 수행하기 위한 핵심 라이브러리입니다.

AI, 머신러닝(ML), 딥러닝(DL), 데이터 분석 분야에서 사실상 기본이 되는 라이브러리이며, 대부분의 AI 프레임워크가 NumPy 개념 위에서 동작합니다.

대표적으로:

* Pandas → 내부적으로 NumPy 사용
* Scikit-Learn → NumPy 기반
* TensorFlow / PyTorch → NumPy와 매우 유사한 배열 개념 사용
* OpenCV → 이미지 배열 처리

즉, **NumPy를 제대로 이해하면 AI/ML 데이터 처리의 기초 체력을 갖추게 됩니다.**

---

# NumPy의 핵심 특징

1. ndarray (다차원 배열)
2. 벡터 연산 지원
3. 매우 빠른 속도
4. Broadcasting 지원

## 1. ndarray (다차원 배열)

NumPy의 핵심 객체는:

```python
ndarray
```

입니다.

Python 리스트보다:

* 훨씬 빠름
* 메모리 효율적
* 벡터 연산 가능
* 대용량 데이터 처리 가능

예시:

```python
import numpy as np

a = np.array([1, 2, 3])
print(a)
```

---

## 2. 벡터 연산 지원

Python 리스트:

```python
import numpy as np

a = np.array([1,2,3])
b = np.array([4,5,6])

a = [1,2,3]
b = [4,5,6]

# 오류 또는 반복문 필요
#print(a + b)
```

NumPy:

```python
import numpy as np

a = np.array([1,2,3])
b = np.array([4,5,6])

print(a + b)
```

결과:

```python
[5 7 9]
```

---

## 3. 매우 빠른 속도

NumPy는 내부적으로 C언어 기반으로 구현되어 있어 Python 반복문보다 매우 빠릅니다.

예시:

```python
# Python loop
import random
import time

# 1. 100만 개 난수 생성
start = time.time()

arr = [random.randint(1, 100) for _ in range(1_000_000)]

# 2. 각 값을 * 2
result = [x * 2 for x in arr]

end = time.time()

print(f"원본 데이터 개수: {len(arr)}")
print(f"결과 데이터 개수: {len(result)}")

# 앞부분 일부 출력
print("원본 데이터 샘플:", arr[:10])
print("변환 데이터 샘플:", result[:10])

print(f"실행 시간: {end - start:.4f} 초")
```

vs

```python
# NumPy vectorized operation
import numpy as np
import time

start = time.time()

# 100만 개 난수 배열 생성
np.random.seed(0)  # 재현성을 위해 시드 설정
arr = np.random.randint(1, 100, size=1_000_000)

# 벡터 연산
# NumPy vectorized operation
result = arr * 2

end = time.time()

print("샘플:", result[:10])
print(f"실행 시간: {end - start:.6f} 초")

```

AI 데이터 처리에서는 속도 차이가 매우 큽니다.

---

## 4. Broadcasting 지원

차원이 다른 배열끼리 자동 연산 가능

예시:

```python
arr = np.array([1,2,3])

print(arr + 10)
```

결과:

```python
[11 12 13]
```

---

# NumPy에서 반드시 이해해야 하는 핵심 개념

## 배열 차원(Dimension)

```python
1차원: [1,2,3]
2차원: [[1,2],[3,4]]
3차원: 이미지/영상 데이터
```

AI에서는:

* 벡터
* 행렬
* 텐서

개념이 매우 중요합니다.

---

# ndarray 기본 속성

```python
arr.shape     # 형태
arr.ndim      # 차원 수
arr.dtype     # 데이터 타입
arr.size      # 전체 원소 수
```

예시:

```python
import numpy as np  # NumPy 라이브러리 불러오기

# 2행 3열 형태의 2차원 ndarray 생성
arr = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

# 배열의 형태(shape) 출력
# (행 개수, 열 개수) 형태로 반환됨
print(arr.shape)   # 결과: (2, 3)

# 배열의 차원 수(ndim) 출력
# 현재는 2차원 배열이므로 결과는 2
print(arr.ndim)    # 결과: 2

# 배열 전체 원소 개수(size) 출력
# 2행 × 3열 = 총 6개 원소
print(arr.size)    # 결과: 6
```

---

# NumPy 함수 종류별 정리

1. 배열 생성 함수
2. 데이터 형태 변환 함수
3. 인덱싱 / 슬라이싱
4. 수학 연산 함수
5. 통계 함수
6. 조건 처리 함수
7. 행렬 연산 함수

---

# 1. 배열 생성 함수

AI/ML에서 매우 중요

| 함수                | 설명         |
| ------------------- | -------      |
| np.array()          | 배열 생성    |
| np.zeros()          | 0으로 초기화 |
| np.ones()           | 1로 초기화   |
| np.empty()          | 빈 배열      |
| np.arange()         | 범위 생성    |
| np.linspace()       | 구간 분할    |
| np.eye()            | 단위 행렬    |
| np.random.rand()    | 랜덤 실수    |
| np.random.randint() | 랜덤 정수    |

---

## 예제

```python
import numpy as np

a = np.zeros((2,3))
b = np.ones((3,3))
c = np.eye(3)

print(a)
print(b)
print(c)
```

---

# 2. 데이터 형태 변환 함수

ML에서 매우 중요

| 함수        | 설명       |
| ----------- | ---------  |
| reshape()   | 형태 변경  |
| flatten()   | 1차원 변환 |
| transpose() | 행렬 전치  |
| astype()    | 타입 변환  |

---

## 데이터 형태 변환 함수 예제

```python
import numpy as np

# 0부터 11까지의 정수를 생성
# 결과: [0 1 2 3 4 5 6 7 8 9 10 11]
arr = np.arange(12)

# 1차원 배열을 3행 4열 형태로 변환
# 결과:
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]
arr2 = arr.reshape(3, 4)

# transpose()
# 행(row)과 열(column)을 서로 바꾸는 함수
# 3x4 -> 4x3 형태로 변경됨
arr_transpose = arr2.transpose()

# astype()
# 배열의 데이터 타입(dtype)을 변경하는 함수
# int -> float 형태로 변경
arr_float = arr2.astype(float)

# 원본 배열 출력
print("=== arr2 원본 배열 ===")
print(arr2)

# transpose 결과 출력
print("\n=== transpose() 결과 ===")
print(arr_transpose)

# astype 결과 출력
print("\n=== astype(float) 결과 ===")
print(arr_float)

# 데이터 타입 확인
print("\n=== 데이터 타입 확인 ===")
print(arr2.dtype)        # 원본 타입
print(arr_float.dtype)   # 변경된 타입
```

실행 결과 예시:

```python
=== arr2 원본 배열 ===
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]

=== transpose() 결과 ===
[[ 0  4  8]
 [ 1  5  9]
 [ 2  6 10]
 [ 3  7 11]]

=== astype(float) 결과 ===
[[ 0.  1.  2.  3.]
 [ 4.  5.  6.  7.]
 [ 8.  9. 10. 11.]]

=== 데이터 타입 확인 ===
int64
float64
```

추가로 꼭 알아야 하는 핵심 개념:

* `reshape()`
  → 배열의 구조(행/열)를 변경

* `transpose()`
  → 행과 열을 교환
  → 머신러닝에서 데이터 축(axis) 변경 시 매우 자주 사용

* `astype()`
  → 데이터 타입 변경
  → AI/ML에서는 `float32`, `int32` 변환을 자주 사용

AI 학습에서는 메모리 절약과 GPU 연산 최적화를 위해 `float32`를 많이 사용합니다.

---

# 3. 인덱싱 / 슬라이싱

딥러닝 데이터 전처리 핵심

```python
arr[0]      # 0번째 행(row) 전체 선택
arr[1:5]    # 1번째 행부터 4번째 행까지 선택 (5는 포함되지 않음)
arr[:,0]    # 모든 행(:)의 0번째 열(column) 선택
arr[0,:]    # 0번째 행의 모든 열(:) 선택
```

예를 들어 `arr`가 아래와 같다면:

```python
import numpy as np

arr = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
```

각 결과는 다음과 같습니다.

```python
arr[0]
# [1 2 3]

arr[:,0]
# [1 4 7]

arr[0,:]
# [1 2 3]
```

NumPy 배열에서:

* `:` → 전체 선택
* `행, 열` 형태로 접근
* `슬라이싱 start:end` → end는 포함되지 않음

---

## 예제

```python
# 2차원 배열 생성
arr = np.array([
    [1,2,3],
    [4,5,6]
])

# 0번째 행의 모든 원소
print(arr[:,1])
```

결과:

```python
[2 5]
```

---

# 4. 수학 연산 함수

| 함수      | 설명     |
| --------- | ----     |
| np.sum()  | 합계     |
| np.mean() | 평균     |
| np.max()  | 최대값   |
| np.min()  | 최소값   |
| np.std()  | 표준편차 |
| np.var()  | 분산     |
| np.sqrt() | 제곱근   |
| np.exp()  | 지수     |
| np.log()  | 로그     |

---

## AI/ML 핵심 예제

```python
scores = np.array([80,90,100])

# 평균 구하기 
print(np.mean(scores))
# 표준 편차 계산
print(np.std(scores))
```

머신러닝에서는 평균/분산/표준편차를 매우 많이 사용합니다.

---

# 5. 통계 함수

데이터 분석 필수

```python
np.median()
np.percentile()
np.unique()
np.argmax()
np.argmin()
```

## 통계 함수 예제

```python
import numpy as np

# =========================
# np.median()
# =========================

# 중앙값(Median)을 구하는 함수
# 데이터를 정렬했을 때 가운데 위치한 값을 반환
# 이상치(outlier)의 영향을 평균보다 덜 받음

arr = np.array([10, 20, 30, 40, 100])

median_value = np.median(arr)

print(median_value)  # 30.0



# =========================
# np.percentile()
# =========================

# 백분위수(Percentile)를 구하는 함수
# 데이터에서 특정 퍼센트 위치의 값을 반환
# 예:
# 25 -> 하위 25%
# 50 -> 중앙값(median)
# 75 -> 상위 75% 위치 값

arr = np.array([10, 20, 30, 40, 50])

p25 = np.percentile(arr, 25)  # 25% 위치 값
p50 = np.percentile(arr, 50)  # 중앙값
p75 = np.percentile(arr, 75)  # 75% 위치 값

print(p25)  # 20.0
print(p50)  # 30.0
print(p75)  # 40.0



# =========================
# np.unique()
# =========================

# 중복된 값을 제거하고
# 유일한(unique) 값만 반환하는 함수

arr = np.array([1, 2, 2, 3, 3, 3, 4])

unique_values = np.unique(arr)

print(unique_values)  # [1 2 3 4]



# =========================
# np.argmax()
# =========================

# 가장 큰 값(max)의 인덱스(index)를 반환
# 실제 값이 아니라 위치를 반환함

arr = np.array([5, 10, 99, 30])

max_index = np.argmax(arr)

print(max_index)  # 2
print(arr[max_index])  # 99



# =========================
# np.argmin()
# =========================

# 가장 작은 값(min)의 인덱스(index)를 반환
# 실제 값이 아니라 위치를 반환함

arr = np.array([5, 10, -3, 30])

min_index = np.argmin(arr)

print(min_index)  # 2
print(arr[min_index])  # -3
```

---

# 6. 조건 처리 함수

AI 데이터 필터링 핵심

| 함수       | 설명          |
| ---------- | ---------     |
| np.where() | 조건 분기     |
| np.any()   | 하나라도 True |
| np.all()   | 모두 True     |

---

## 예제

```python
import numpy as np

# ================================
# np.where()
# ================================
# 조건에 따라 값을 선택하거나 위치를 찾는 함수

# 예제 배열 생성
arr = np.array([10, 20, 30, 40, 50])

# 조건:
# 30보다 크면 1
# 그렇지 않으면 0
result = np.where(arr > 30, 1, 0)

print("원본 배열:", arr)
print("30보다 크면 1, 아니면 0:", result)

# 결과:
# [0 0 0 1 1]

# --------------------------------
# 위치(index) 찾기 예제
# --------------------------------

# 조건을 만족하는 인덱스 반환
index_result = np.where(arr >= 30)

print("30 이상인 값의 위치:", index_result)

# 실제 값 출력
print("30 이상인 값:", arr[index_result])

# ================================
# np.any()
# ================================
# 배열 안에 하나라도 True가 있으면 True 반환

# 조건 검사
condition_any = arr > 45

print("\n45보다 큰 값 존재 여부:", condition_any)

# 하나라도 True인지 확인
any_result = np.any(condition_any)

print("하나라도 True 인가?:", any_result)

# 결과:
# True



# --------------------------------
# 모든 값이 False 인 경우
# --------------------------------

condition_any2 = arr > 100

print("\n100보다 큰 값 존재 여부:", condition_any2)

any_result2 = np.any(condition_any2)

print("하나라도 True 인가?:", any_result2)

# 결과:
# False



# ================================
# np.all()
# ================================
# 배열 안의 모든 값이 True일 때만 True 반환

# 모든 값이 5보다 큰지 검사
condition_all = arr > 5

print("\n모든 값이 5보다 큰가?:", condition_all)

all_result = np.all(condition_all)

print("모두 True 인가?:", all_result)

# 결과:
# True



# --------------------------------
# 하나라도 False가 있는 경우
# --------------------------------

condition_all2 = arr > 25

print("\n모든 값이 25보다 큰가?:", condition_all2)

all_result2 = np.all(condition_all2)

print("모두 True 인가?:", all_result2)

# 결과:
# False
```

추가로 AI/ML에서 자주 사용하는 방식으로:

* `np.where()` → 데이터 전처리(Label 변경)
* `np.any()` → 이상치 존재 여부 검사
* `np.all()` → 데이터 검증(validation)

---

# 7. 행렬 연산 함수 (매우 중요)

AI/딥러닝 핵심

| 함수            | 설명    |
| --------------- | ----    |
| np.dot()        | 행렬 곱 |
| np.matmul()     | 행렬 곱 |
| np.linalg.inv() | 역행렬  |
| np.linalg.det() | 행렬식  |
| np.linalg.eig() | 고유값  |

---

#  행렬 연산 함수 예제 

```python
import numpy as np

# =========================================================
# 1. np.dot()
# =========================================================
# dot() 함수는 벡터 내적 또는 행렬 곱셈을 수행한다.
# 2차원 배열에서는 일반적인 행렬 곱(Matrix Multiplication)으로 동작한다.

A = np.array([
    [1, 2],
    [3, 4]
])

B = np.array([
    [5, 6],
    [7, 8]
])

# 행렬 곱 수행
dot_result = np.dot(A, B)

print("=== np.dot() 결과 ===")
print(dot_result)

# 계산 과정
# [ [1*5 + 2*7, 1*6 + 2*8],
#   [3*5 + 4*7, 3*6 + 4*8] ]
#
# 결과:
# [[19 22]
#  [43 50]]



# =========================================================
# 2. np.matmul()
# =========================================================
# matmul() 함수도 행렬 곱셈을 수행한다.
# Python의 @ 연산자와 동일한 기능이다.

matmul_result = np.matmul(A, B)

print("\n=== np.matmul() 결과 ===")
print(matmul_result)

# np.dot()과 동일한 결과가 출력된다.
#
# 결과:
# [[19 22]
#  [43 50]]



# =========================================================
# 3. np.linalg.inv()
# =========================================================
# inv() 함수는 역행렬(Inverse Matrix)을 구한다.
#
# 역행렬은 다음 조건을 만족한다.
# A × A^-1 = I (단위행렬)

C = np.array([
    [1, 2],
    [3, 4]
])

# 역행렬 계산
inverse_C = np.linalg.inv(C)

print("\n=== np.linalg.inv() 결과 ===")
print(inverse_C)

# 결과 예시:
# [[-2.   1. ]
#  [ 1.5 -0.5]]

# 역행렬 검증
# 원본 행렬 × 역행렬 = 단위행렬(I)
identity = np.matmul(C, inverse_C)

print("\n=== 역행렬 검증 ===")
print(identity)

# 결과:
# [[1. 0.]
#  [0. 1.]]



# =========================================================
# 4. np.linalg.det()
# =========================================================
# det() 함수는 행렬식(Determinant)을 계산한다.
#
# 행렬식이 0이면 역행렬이 존재하지 않는다.

det_C = np.linalg.det(C)

print("\n=== np.linalg.det() 결과 ===")
print(det_C)

# 계산:
# (1*4) - (2*3)
# = 4 - 6
# = -2

# 결과:
# -2.0000000000000004



# =========================================================
# 5. np.linalg.eig()
# =========================================================
# eig() 함수는 고유값(Eigenvalue)과
# 고유벡터(Eigenvector)를 계산한다.
#
# 선형대수, 머신러닝, PCA 등에 매우 중요하게 사용된다.

D = np.array([
    [4, 2],
    [1, 3]
])

# 고유값과 고유벡터 계산
eigen_values, eigen_vectors = np.linalg.eig(D)

print("\n=== np.linalg.eig() 결과 ===")

print("\n고유값(Eigenvalues)")
print(eigen_values)

print("\n고유벡터(Eigenvectors)")
print(eigen_vectors)

# 의미:
# D × v = λ × v
#
# λ (lambda) : 고유값
# v           : 고유벡터

# =========================================================
# 추가: @ 연산자
# =========================================================
# Python에서는 @ 연산자를 이용해
# 행렬 곱을 더 직관적으로 수행할 수 있다.

result_operator = A @ B

print("\n=== @ 연산자 결과 ===")
print(result_operator)

# 결과:
# [[19 22]
#  [43 50]]
```

추가로 AI/ML 학습 관점에서 매우 중요한 내용은 다음과 같습니다.

* `dot()` → 신경망 연산
* `matmul()` → 딥러닝 텐서 계산
* `inv()` → 선형회귀 수식
* `det()` → 역행렬 가능 여부 판단
* `eig()` → PCA(차원 축소), 추천 시스템, 이미지 처리

특히 PCA는 다음 수식 기반으로 동작합니다.

𝐴𝑣 = 𝜆𝑣

여기서:

* `A` → 데이터 행렬
* `v` → 고유벡터
* `λ` → 고유값

AI/ML에서는 가장 큰 고유값 방향으로 데이터를 압축합니다.

---

# 8. 난수(Random) 함수

머신러닝 핵심

| 함수                | 설명      |
| ------------------- | -----     |
| np.random.rand()    | 균등분포  |
| np.random.randn()   | 정규분포  |
| np.random.randint() | 랜덤 정수 |
| np.random.seed()    | 시드 고정 |
| np.random.shuffle() | 섞기      |

---

## ML 필수 예제

```python
import numpy as np

# =========================================================
# 1. np.random.rand()
# =========================================================
# 0 ~ 1 사이의 균등분포(Uniform Distribution) 난수를 생성
# shape(행, 열)을 지정 가능

print("1. np.random.rand()")
arr_rand = np.random.rand(3, 4)   # 3행 4열 배열 생성
print(arr_rand)
print()


# =========================================================
# 2. np.random.randn()
# =========================================================
# 평균 0, 표준편차 1인 정규분포(Normal Distribution) 난수 생성
# 음수와 양수가 모두 나올 수 있음

print("2. np.random.randn()")
arr_randn = np.random.randn(3, 4)  # 3행 4열 배열 생성
print(arr_randn)
print()


# =========================================================
# 3. np.random.randint()
# =========================================================
# 지정한 범위의 랜덤 정수 생성
# randint(시작값, 종료값, 개수)
# 종료값은 포함되지 않음

print("3. np.random.randint()")
arr_int = np.random.randint(1, 100, 10)  # 1 ~ 99 사이 정수 10개 생성
print(arr_int)
print()


# =========================================================
# 4. np.random.seed()
# =========================================================
# 난수 생성 기준(seed)을 고정
# 항상 동일한 난수가 생성됨
# 실험 재현(Reproducibility)에 매우 중요

print("4. np.random.seed()")

np.random.seed(100)   # 시드값 고정

a = np.random.rand(5)
print("첫 번째 실행 결과:")
print(a)

# 다시 같은 seed 설정
np.random.seed(100)

b = np.random.rand(5)
print("두 번째 실행 결과:")
print(b)

# 결과 비교
print("두 결과가 같은가?")
print(np.array_equal(a, b))
print()


# =========================================================
# 5. np.random.shuffle()
# =========================================================
# 배열의 요소 순서를 랜덤하게 섞음
# 원본 배열 자체가 변경됨 (in-place)

print("5. np.random.shuffle()")

data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

print("섞기 전:")
print(data)

np.random.shuffle(data)

print("섞은 후:")
print(data)
print()


# =========================================================
# 추가 예제 : shuffle과 permutation 차이
# =========================================================
# shuffle()     -> 원본 변경
# permutation() -> 원본 유지 후 새로운 배열 반환

print("추가 예제 : permutation")

data2 = np.array([10, 20, 30, 40, 50])

print("원본 배열:")
print(data2)

new_data = np.random.permutation(data2)

print("permutation 결과:")
print(new_data)

print("원본 유지 여부:")
print(data2)
```

### 실행 결과 예시

```python
1. np.random.rand()
[[0.23 0.45 0.11 0.92]
 [0.67 0.31 0.55 0.77]
 [0.14 0.88 0.42 0.69]]

2. np.random.randn()
[[-0.52  1.32 -0.44  0.88]
 [ 0.13 -1.42  0.71 -0.08]
 [ 1.01  0.45 -0.91  0.33]]

3. np.random.randint()
[12 55 89 33 71 28 64 91 45 10]
```

재현 가능한 실험(Reproducibility)에 매우 중요

---

# 예제 1: 데이터 정규화

```python
import numpy as np  # NumPy 라이브러리를 np라는 이름으로 불러옴 (수치 계산용)

# 1차원 배열 생성
data = np.array([10, 20, 30, 40, 50])  # 데이터 배열 생성

# 평균 계산
mean = np.mean(data)  # data의 평균값 계산

# 표준편차 계산
std = np.std(data)  # data의 표준편차 계산 (데이터가 평균에서 얼마나 퍼져있는지)

# 정규화 (Standardization)
normalized = (data - mean) / std  
# 각 데이터에서 평균을 빼고, 표준편차로 나눔
# → 평균 0, 표준편차 1인 형태로 변환 (Z-score normalization)

# 결과 출력
print(normalized)  # 정규화된 값 출력
```

---

# 예제 2: 이미지 데이터 처리

이미지는 NumPy 배열입니다.

```python
import numpy as np  # NumPy 라이브러리 import (수치 계산 및 배열 처리용)
from PIL import Image           # 이미지 저장을 위한 PIL 라이브러리

# 0~255 사이의 랜덤 정수로 구성된 224x224 크기의 RGB 이미지 생성
image = np.random.randint(
    0,      # 최소값 (포함)
    255,    # 최대값 (미포함 → 실제로는 0~254)
    (224,224,3),  # 이미지 shape: 224x224 픽셀, 3채널(RGB)
    dtype=np.uint8
)

# 생성된 이미지 배열의 형태 출력 (높이, 너비, 채널)
print(image.shape)

# numpy 배열을 PIL 이미지로 변환
img = Image.fromarray(image)

# 이미지 파일로 저장 (현재 디렉토리에 random_image.png 생성)
img.save("random_image.png")
```

결과:

```python
(224, 224, 3)
```

---

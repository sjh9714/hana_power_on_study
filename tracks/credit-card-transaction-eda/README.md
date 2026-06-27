# Credit Card Transaction EDA

## 문제 정의

신용카드 거래 데이터는 고객, 시간, 금액, 지역, 가맹점 유형이 함께 움직이는 이벤트 데이터입니다. 이 트랙은 Pandas로 거래 데이터를 읽고, 시간대와 거래 금액을 기준으로 금융 데이터의 기본 구조를 이해하는 데 초점을 둡니다.

## 사용 기술

- Python
- Pandas
- Jupyter Notebook
- CSV/JSON 파일 처리
- 기초 시계열 분석

## 실행 및 재현 방법

공개 저장소에서는 실제 교육 제공 데이터 대신 synthetic 샘플 데이터를 사용합니다.

```bash
python3 scripts/create_sample_credit_data.py
```

생성된 파일은 `sample_data/credit-card-transactions-sample.csv`에서 확인할 수 있습니다.

## 핵심 결과

- 거래 데이터를 행 단위 이벤트로 바라보는 관점을 정리했습니다.
- 시간, 금액, 고객, 카테고리별로 데이터를 나누어 보는 EDA 흐름을 학습했습니다.
- 원본 대형 데이터는 공개 저장소에서 제거하고, 샘플 데이터로 재현 가능한 구조만 남겼습니다.

## GitHub Evidence

- [`step1`](../../step1)
- [`step1/notebooks/step_pandas.ipynb`](../../step1/notebooks/step_pandas.ipynb)
- [`step1/notebooks/step_time_series.ipynb`](../../step1/notebooks/step_time_series.ipynb)
- [`step1/notebooks/step_credit.ipynb`](../../step1/notebooks/step_credit.ipynb)
- [`day8/fraud_detection_system`](../../day8/fraud_detection_system)
- [`sample_data`](../../sample_data)

## 관련 Velog

- [Pandas로 신용카드 거래 데이터 EDA 구조 잡기](https://velog.io/@sjh9714/hana-credit-card-eda)

## 한계와 다음 단계

- 샘플 데이터는 구조 재현용이므로 실제 거래 분포를 설명하지 않습니다.
- 이후에는 feature, label, event 단위를 분리해 FDS 관점의 분석 흐름으로 확장할 수 있습니다.

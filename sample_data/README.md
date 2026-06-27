# Sample Data

이 폴더의 데이터는 공개 포트폴리오 재현을 위해 만든 synthetic 샘플입니다.

## 포함 파일

- `credit-card-transactions-sample.csv`: 신용카드 거래 EDA 구조를 설명하기 위한 작은 예시 데이터

## 공개 기준

- 실제 고객, 실제 카드번호, 실제 거래 내역을 포함하지 않습니다.
- 교육 과정에서 제공된 원본 데이터가 아닙니다.
- 컬럼 구조와 분석 흐름을 보여주기 위한 재현용 데이터입니다.

## 재생성

샘플 데이터는 아래 명령으로 다시 만들 수 있습니다.

```bash
python3 scripts/create_sample_credit_data.py
```

다른 경로에 생성하려면 `--output` 옵션을 사용합니다.

```bash
python3 scripts/create_sample_credit_data.py --output /tmp/credit-card-sample.csv
```

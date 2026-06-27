# Scripts

공개 저장소에는 실제 교육 제공 데이터나 대형 산출물을 포함하지 않습니다. 이 폴더는 공개 가능한 샘플 데이터와 재현 절차를 관리합니다.

## Synthetic Sample 생성

```bash
python3 scripts/create_sample_credit_data.py
```

기본 출력 경로는 `sample_data/credit-card-transactions-sample.csv`입니다.

```bash
python3 scripts/create_sample_credit_data.py --output /tmp/credit-card-sample.csv
```

## 운영 기준

- 실제 고객 데이터, 실제 거래 내역, 카드번호는 생성하지 않습니다.
- 교육 자료 원문과 내부 제공 데이터는 스크립트 입력으로 요구하지 않습니다.
- 분석 노트북을 공개할 때는 이 샘플 데이터를 기준으로 실행 예시를 구성합니다.

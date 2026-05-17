# Step 1 Study Workspace

`step1`은 Python 기초, 파일 입출력, Pandas, 시계열, 신용카드 거래 데이터 실습을 모아둔 학습 공간입니다.

## 폴더 구조

```text
step1/
├── data/          # 실습용 작은 CSV/JSON/TXT 데이터
├── notebooks/     # 주피터 노트북 실습
├── outputs/       # 노트북 실행으로 생성된 결과 파일
├── scripts/       # 간단한 Python 실행 예제
├── requirements.txt
└── README.md
```

## 노트북

| 파일 | 내용 |
| --- | --- |
| `notebooks/step.ipynb` | Python 기초 문법, 파일 입출력, JSON, 이미지 생성 |
| `notebooks/step_pandas.ipynb` | Pandas DataFrame, CSV 저장/읽기, 기본 데이터 처리 |
| `notebooks/step_time_series.ipynb` | 날짜/시간 데이터와 시계열 기초 |
| `notebooks/step_credit.ipynb` | 신용카드 거래 데이터 확인 및 기초 분석 |

## 스크립트

| 파일 | 내용 |
| --- | --- |
| `scripts/main.py` | Python 실행, 디버깅, 함수 호출 기초 |
| `scripts/info.py` | PyTorch, Pandas 버전과 GPU 사용 가능 여부 확인 |

## 데이터 관리

작은 실습 데이터는 `data/`에 함께 보관합니다.

대형 데이터인 `data/credit_card_transactions.csv`는 GitHub에 올리지 않습니다. 파일 크기가 크기 때문에 `.gitignore`에서 제외했습니다. 신용카드 노트북을 실행하려면 로컬에 아래 경로로 파일을 두면 됩니다.

```text
step1/data/credit_card_transactions.csv
```

## 실행 방법

필요한 패키지를 설치합니다.

```bash
pip install -r step1/requirements.txt
```

Python 스크립트 실행 예시:

```bash
python step1/scripts/main.py
python step1/scripts/info.py
```

노트북은 `step1/notebooks/` 폴더에서 열어 실행하면 됩니다. 노트북 안에서는 `STEP1_ROOT`, `DATA_DIR`, `OUTPUT_DIR`를 사용하도록 정리해 두었기 때문에 프로젝트 루트나 `step1` 안에서 실행해도 데이터 경로를 찾을 수 있습니다.

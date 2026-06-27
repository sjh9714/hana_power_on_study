# Finance Prompt Engineering Lab

## 문제 정의

금융 안내 챗봇은 답변의 정확도뿐 아니라 말할 수 있는 범위, 말하면 안 되는 범위, 출력 형식이 중요합니다. 이 트랙은 프롬프트를 단순 질문이 아니라 AI가 지켜야 할 요구사항 명세로 바라본 실습입니다.

## 사용 기술

- Python
- OpenAI API 실습 코드
- 프롬프트 엔지니어링
- 역할/제약/출력 형식 설계
- Gradio 기반 빠른 검증

## 실행 및 재현 방법

API key는 저장소에 포함하지 않습니다. 로컬에서 실행할 때는 환경 변수로 주입합니다.

```bash
export OPENAI_API_KEY="..."
python3 day10/openai/step1.py
```

실행 전에는 각 하위 폴더의 `requirements.txt`를 확인하세요.

## 핵심 결과

- 역할 부여, 금지 조건, 출력 포맷이 답변 품질에 미치는 영향을 비교했습니다.
- 금융 안내 문맥에서는 확정적 조언보다 정보 제공과 한계 고지가 중요하다는 점을 정리했습니다.
- 프롬프트를 요구사항 명세처럼 다루는 관점을 얻었습니다.

## GitHub Evidence

- [`day10/1.1.md`](../../day10/1.1.md)
- [`day10/openai`](../../day10/openai)
- [`day10/analysis.py`](../../day10/analysis.py)
- [`day10/gradio`](../../day10/gradio)

## 관련 Velog

- [프롬프트는 요구사항 명세에 가깝다](https://velog.io/@sjh9714/hana-finance-prompt-engineering)

## 한계와 다음 단계

- 실습 코드는 운영용 금융 상담 서비스가 아닙니다.
- 이후에는 답변 평가 기준, 근거 문서 연결, 금칙어/위험 표현 검사를 추가할 수 있습니다.

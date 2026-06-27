# FastAPI + Gradio AI Chat Demo

## 문제 정의

AI 기능은 모델 호출 코드만으로는 사용자 흐름을 검증하기 어렵습니다. 이 트랙은 Gradio UI와 FastAPI API 레이어를 통해 질문 입력, 응답 확인, 대화 흐름을 빠르게 실험하는 데 초점을 둡니다.

## 사용 기술

- Python
- Gradio
- FastAPI
- LangChain
- 대화 히스토리 관리
- 스트리밍 응답 구조

## 실행 및 재현 방법

각 실습 폴더의 의존성을 설치한 뒤 로컬에서 실행합니다.

```bash
pip install -r day10/gradio/requirements.txt
python3 day10/gradio/app.py
```

LangChain 챗봇 실습은 `day11/langchain-chatbot`, `day12/langchain-chatbot` 폴더를 기준으로 확인합니다.

## 핵심 결과

- Gradio를 통해 AI 응답을 빠르게 확인하는 인터페이스를 만들었습니다.
- FastAPI와 UI 레이어를 분리해 데모에서 API 구조로 넘어가는 흐름을 학습했습니다.
- 대화 히스토리와 스트리밍 응답처럼 실제 챗봇에서 필요한 주변 구조를 확인했습니다.

## GitHub Evidence

- [`day10/gradio`](../../day10/gradio)
- [`day11/langchain-chatbot`](../../day11/langchain-chatbot)
- [`day12/langchain-chatbot`](../../day12/langchain-chatbot)

## 관련 Velog

- [학습 기록을 포트폴리오로 재구성한 이유](https://velog.io/@sjh9714/hana-finance-ai-portfolio-reorganization)
- [Blog Roadmap](../../docs/blog-roadmap.md)

## 한계와 다음 단계

- 데모 목적의 코드이므로 인증, 로깅, 비용 관리, 배포 설정은 제한적입니다.
- 이후에는 API 요청/응답 스키마, 예외 처리, 테스트 코드를 보강할 수 있습니다.

# Hana Power On Study

`hana_power_on_study`는 하나 청년 금융인재 양성 프로젝트에서 학습한 Python, 금융 데이터 분석, AI 서비스 구현, RAG/Agent 실습을 정리한 저장소입니다.

기존 날짜별 학습 로그는 그대로 보존하고, 채용자나 동료 개발자가 빠르게 볼 수 있도록 대표 실습을 포트폴리오 관점으로 재구성했습니다.

## Portfolio Positioning

> 금융 서비스 문제를 데이터 분석, AI 인터페이스, 백엔드 구조로 풀어내기 위한 학습 기록

이 저장소는 단순 강의 필기가 아니라 다음 역량을 보여주는 증거로 관리합니다.

- 금융 거래 데이터 구조 이해
- Python/Pandas 기반 데이터 전처리와 EDA
- FastAPI, Gradio 기반 AI 데모 구현
- LangChain, RAG, Chroma, LangGraph 기반 문서 질의 흐름 실습
- 학습 내용을 GitHub 문서와 Velog 회고로 재구성하는 습관

## Recommended Reading Order

1. [Portfolio Index](docs/portfolio-index.md)에서 대표 프로젝트 4개를 먼저 확인합니다.
2. [Learning Log](docs/learning-log.md)에서 날짜별 학습 흐름을 확인합니다.
3. [Blog Roadmap](docs/blog-roadmap.md)에서 Velog 글로 확장할 주제를 확인합니다.
4. 원본 실습 폴더(`day*`, `step1`)에서 코드와 노트북을 확인합니다.
5. [Public Data Policy](docs/public-data-policy.md)에서 공개 범위와 데이터 관리 기준을 확인합니다.

## Highlighted Portfolio Tracks

| Track | Summary | Evidence |
| --- | --- | --- |
| Credit Card Transaction EDA | 신용카드 거래 데이터를 Pandas와 시계열 관점으로 분석하는 기초 실습 | [`step1`](step1), [`day5`](day5), [`day6`](day6) |
| Finance Prompt Engineering Lab | 금융 안내 챗봇을 위한 역할, 제약 조건, 출력 형식 중심 프롬프트 설계 | [`day10`](day10) |
| FastAPI + Gradio AI Chat Demo | Gradio UI와 FastAPI 구조로 빠르게 검증 가능한 AI 챗봇 데모 실습 | [`day10/gradio`](day10/gradio), [`day11/langchain-chatbot`](day11/langchain-chatbot), [`day12/langchain-chatbot`](day12/langchain-chatbot) |
| RAG + LangGraph Agent Chatbot | PDF 문서 처리, Chroma 검색, Tool Router, LangGraph Agent 흐름 실습 | [`day13`](day13), [`day14`](day14), [`day15`](day15), [`day16`](day16) |

## Repository Structure

```text
.
├── step1/      # Python, Pandas, 시계열, 신용카드 거래 데이터 기초 실습
├── day3~day9/ # Python, 데이터 처리, 금융 데이터 구조, FDS 기초
├── day10~12/  # 프롬프트 엔지니어링, Gradio, OpenAI, LangChain 챗봇 실습
├── day13~16/  # PDF 처리, RAG, Chroma, Router, LangGraph Agent 실습
├── data/      # 로컬 재현용 대형 데이터 압축 파일
└── docs/      # 포트폴리오 인덱스와 공개 정책 문서
```

## What This Repository Is

- 교육 과정에서 직접 작성한 학습 코드와 실습 기록입니다.
- 금융 데이터와 AI 서비스 구현을 연결해 보기 위한 개인 학습 저장소입니다.
- Velog 글과 GitHub 프로필에서 보여줄 포트폴리오 증거 자료입니다.

## What This Repository Is Not

- 실제 금융 상품 추천 서비스가 아닙니다.
- 운영 가능한 금융 시스템 구현체가 아닙니다.
- 교육 자료 원문이나 내부 데이터를 배포하기 위한 저장소가 아닙니다.

## Data And Disclosure Notes

이 저장소에는 실습 재현을 위한 데이터 압축 파일, 벡터 DB 산출물, PDF 처리 결과물이 포함되어 있습니다. 이번 정리에서는 기존 파일을 삭제하지 않고, 공개 범위와 주의사항을 문서화하는 방식으로 관리합니다.

자세한 기준은 [Public Data Policy](docs/public-data-policy.md)를 참고하세요.

## Related Blog Plan

Velog에는 강의 내용을 그대로 요약하기보다, 다음 흐름으로 정리할 예정입니다.

```text
문제 정의 -> 실습 코드 -> 헷갈린 점 -> 금융 서비스와 연결 -> 한계와 개선점
```

자세한 글 목록은 [Blog Roadmap](docs/blog-roadmap.md)에 정리했습니다.

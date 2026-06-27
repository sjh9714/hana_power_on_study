# Portfolio Index

이 문서는 `hana_power_on_study`의 날짜별 학습 기록을 포트폴리오 관점으로 다시 묶은 인덱스입니다.

GitHub는 코드와 학습 흔적을 보여주는 증거로, Velog는 문제를 이해하고 정리한 사고 과정을 보여주는 설명서로 사용합니다.

## 1. Credit Card Transaction EDA

### 문제 정의

신용카드 거래 데이터는 단순한 표 데이터가 아니라 고객, 시간, 거래 금액, 위치, 위험 신호가 함께 얽힌 이벤트 데이터입니다. 이 트랙은 거래 데이터를 Pandas로 다루면서 금융 데이터 분석의 기본 단위를 이해하는 데 초점을 둡니다.

### 핵심 학습

- CSV/JSON 파일 입출력
- Pandas DataFrame 처리
- 날짜/시간 컬럼과 시계열 기초
- 거래 금액, 고객, 시간대 중심의 EDA
- 대형 데이터 파일을 GitHub에 직접 올릴 때의 관리 이슈

### Evidence

- Track README: [`tracks/credit-card-transaction-eda`](../tracks/credit-card-transaction-eda)
- [`step1`](../step1)
- [`day5`](../day5)
- [`day6`](../day6)
- [`day8/fraud_detection_system`](../day8/fraud_detection_system)
- [`sample_data`](../sample_data)

### 포트폴리오 메시지

> 금융 데이터는 평균과 합계만 보는 것이 아니라, 거래가 발생한 시간과 주체, 이벤트 맥락을 함께 봐야 한다.

## 2. Finance Prompt Engineering Lab

### 문제 정의

금융 안내 챗봇은 일반적인 대화형 챗봇보다 답변의 범위, 톤, 제약 조건이 중요합니다. 이 트랙은 프롬프트를 단순 질문이 아니라 요구사항 명세처럼 설계하는 관점으로 정리합니다.

### 핵심 학습

- 역할 부여
- 출력 형식 지정
- 제약 조건 추가
- Few-shot 예시
- 금융 안내에서 단정적 표현을 피하는 방식

### Evidence

- Track README: [`tracks/finance-prompt-engineering-lab`](../tracks/finance-prompt-engineering-lab)
- [`day10/1.1.md`](../day10/1.1.md)
- [`day10/openai`](../day10/openai)
- [`day10/analysis.py`](../day10/analysis.py)
- [`day10/gradio`](../day10/gradio)

### 포트폴리오 메시지

> 프롬프트는 짧은 문장이 아니라, AI가 지켜야 할 역할과 출력 규칙을 담은 인터페이스에 가깝다.

## 3. FastAPI + Gradio AI Chat Demo

### 문제 정의

AI 기능은 빠르게 검증 가능한 UI와 API 구조가 있어야 사용자 흐름을 테스트할 수 있습니다. 이 트랙은 Gradio와 FastAPI를 활용해 챗봇 데모를 빠르게 구성하는 과정을 보여줍니다.

### 핵심 학습

- Gradio 기반 챗봇 UI
- FastAPI API 레이어
- LangChain chain 구조
- 모델 선택과 대화 히스토리 관리
- 스트리밍 응답 흐름

### Evidence

- Track README: [`tracks/fastapi-gradio-ai-chat-demo`](../tracks/fastapi-gradio-ai-chat-demo)
- [`day10/gradio`](../day10/gradio)
- [`day11/langchain-chatbot`](../day11/langchain-chatbot)
- [`day12/langchain-chatbot`](../day12/langchain-chatbot)

### 포트폴리오 메시지

> AI 기능은 모델 호출만으로 끝나지 않고, 사용자가 질문하고 답변을 확인하는 인터페이스까지 함께 설계해야 한다.

## 4. RAG + LangGraph Agent Chatbot

### 문제 정의

문서 기반 질의응답은 LLM이 모든 지식을 알고 있다고 가정하는 방식보다, 필요한 문서를 검색하고 그 근거를 바탕으로 답변하는 구조가 필요합니다. 이 트랙은 PDF 처리, Chroma 기반 검색, Router Chain, LangGraph Agent를 연결한 실습입니다.

### 핵심 학습

- PDF 텍스트 추출과 전처리
- 문서 chunking
- Chroma 벡터 저장소
- RAG chain
- Router chain
- LangGraph ReAct Agent
- Tool 호출과 후처리 노드 분리

### Evidence

- Track README: [`tracks/rag-langgraph-agent-chatbot`](../tracks/rag-langgraph-agent-chatbot)
- [`day13`](../day13)
- [`day14`](../day14)
- [`day15/agri_rag_chatbot`](../day15/agri_rag_chatbot)
- [`day16/agri_rag_chatbot_langgraph2`](../day16/agri_rag_chatbot_langgraph2)

### 포트폴리오 메시지

> 문서 기반 AI 서비스는 답변 생성보다 먼저 검색, 근거, 도구 호출, 후처리의 경계를 나누는 설계가 중요하다.

## Portfolio Next Steps

- 대표 트랙별 README를 추가해 실행 방법과 결과 화면을 분리했습니다.
- 대형 데이터, PDF 원본, 벡터 DB 산출물은 공개 저장소의 현재 트래킹과 Git 히스토리에서 제거했습니다.
- 공개 재현은 [`sample_data`](../sample_data)와 [`scripts`](../scripts)를 기준으로 진행합니다.
- Velog 글에서는 강의 요약보다 설계 판단, 실패 지점, 금융 도메인 연결을 중심으로 정리합니다.

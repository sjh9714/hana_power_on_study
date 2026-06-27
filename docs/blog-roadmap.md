# Blog Roadmap

Velog 시리즈는 `하나 청년 금융인재 프로젝트`로 운영합니다.

강의 내용을 그대로 요약하기보다, 각 글은 다음 구조를 따릅니다.

```text
문제 정의 -> 실습 코드와 구조 -> 헷갈린 점 -> 금융 서비스와 연결 -> 한계와 개선점 -> GitHub 근거 링크
```

## Priority Posts

| Order | Title | Purpose | GitHub Evidence | Velog |
| --- | --- | --- | --- | --- |
| 1 | `[하나 금융인재 프로젝트] 학습 기록을 포트폴리오로 재구성한 이유` | 저장소 전체 방향과 GitHub/Velog 역할 분리 설명 | [`README.md`](../README.md), [`docs/portfolio-index.md`](portfolio-index.md) | [보기](https://velog.io/@sjh9714/hana-finance-ai-portfolio-reorganization) |
| 2 | `[금융 데이터 분석] Pandas로 신용카드 거래 데이터 EDA 구조 잡기` | 거래 데이터 구조와 EDA 관점 정리 | [`step1`](../step1), [`day5`](../day5), [`day6`](../day6) | [보기](https://velog.io/@sjh9714/hana-credit-card-eda) |
| 3 | `[금융 AI] 프롬프트는 요구사항 명세에 가깝다` | 금융 안내 챗봇에서 역할, 제약, 출력 형식이 필요한 이유 | [`day10`](../day10) | [보기](https://velog.io/@sjh9714/hana-finance-prompt-engineering) |
| 4 | `[RAG 챗봇] PDF 문서를 검색 가능한 지식베이스로 바꾸기` | PDF 처리, chunking, embedding, vector store 흐름 정리 | [`day13`](../day13), [`day14`](../day14) | [보기](https://velog.io/@sjh9714/hana-pdf-rag-knowledge-base) |
| 5 | `[LangGraph] 금융/문서 챗봇에 Tool Router를 붙이며 배운 점` | ReAct Agent, ToolNode, 전처리/후처리 경계 설명 | [`day16/agri_rag_chatbot_langgraph2`](../day16/agri_rag_chatbot_langgraph2) | [보기](https://velog.io/@sjh9714/hana-langgraph-tool-router) |

## Post Template

```markdown
# 제목

## 한 줄 요약

## 문제 정의

## 실습 코드와 구조

## 헷갈린 점

## 금융 서비스와 연결

## GitHub 근거 링크

## 한계와 개선점

## 마무리
```

## Writing Rules

- 강의 자료 원문을 옮겨 적지 않습니다.
- 직접 작성한 코드, 직접 겪은 시행착오, 직접 이해한 구조를 중심으로 씁니다.
- 금융 상품 추천이나 확정적 금융 조언처럼 보이는 표현은 피합니다.
- 데이터 출처와 공개 가능 여부가 불명확한 경우, 결과 화면이나 샘플 구조 위주로 설명합니다.
- GitHub 링크는 증거로, Velog 본문은 설계 판단과 회고로 사용합니다.

## Later Posts

- `[금융 데이터 구조] Entity, Event, Feature, Label로 거래 데이터를 나눠보기`
- `[FDS 기초] 이상 거래 탐지를 데이터 구조 관점에서 이해하기`
- `[Gradio] AI 데모를 빠르게 검증하는 UI 만들기`
- `[LangChain] Chain을 나누면 챗봇 구조가 읽히기 시작한다`
- `[RAG 한계] 벡터 DB를 붙여도 답변 품질이 자동으로 좋아지지는 않는다`

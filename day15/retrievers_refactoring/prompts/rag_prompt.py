from langchain_core.prompts import (
    PromptTemplate
)

rag_prompt = (PromptTemplate.from_template(
"""
당신은 스마트농업 전문가입니다.

반드시 제공된 문서 내용만 사용하세요.

문서:
{context}

질문:
{query}

답변 규칙

1. 문서 내용만 사용
2. 추측 금지
3. 문서에 없으면
   "문서에서 찾을 수 없습니다."
4. 참고 페이지 표시

참고 페이지:
{page_text}

답변:
"""
))

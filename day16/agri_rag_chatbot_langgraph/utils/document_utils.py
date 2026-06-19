
# 문서 관련 유틸리티 함수를 정의하는 모듈입니다. 이 모듈에서는 검색된 문서들을 적절한 형식으로 변환하여 LLM이 이해할 수 있도록 하는 역할을 합니다.
# format_docs_with_pages() 함수는 검색된 문서들의 리스트를 입력으로 받아서,
# 각 문서의 내용을 하나의 문자열로 결합하여 "context"라는 키로 반환하는 역할을 합니다. 
# 또한, 각 문서의 출처와 페이지 정보를 기반으로 참조 문서 목록을 생성하여 "page_text"라는 키로 반환하는 역할을 합니다.
# 이렇게 반환된 "context"와 "page_text"는 이후 rag_prompt에 입력으로 전달되어, LLM이 제공된 문서 내용을 기반으로 질문에 답변할 수 있도록 하는 데 사용됩니다.
def format_docs_with_pages(docs):

    # 각 문서의 내용을 하나의 문자열로 결합하여 "context"라는 키로 반환합니다.
    context = "\n\n".join(doc.page_content for doc in docs)

    # 각 문서의 출처와 페이지 정보를 기반으로 참조 문서 목록을 생성합니다.
    references = []

    # 각 문서에 대해, 문서의 메타데이터에서 "source"와 "page" 정보를 추출하여 참조 문서 목록에 추가합니다.
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "?")

        references.append(
            f"{source} (page {page})"
        )

    # 참조 문서 목록을 하나의 문자열로 결합하여 "page_text"라는 키로 반환합니다. 
    # 이렇게 반환된 "page_text"는 이후 rag_prompt에 입력으로 전달되어, 
    # LLM이 제공된 문서의 출처와 페이지 정보를 기반으로 질문에 답변할 수 있도록 하는 데 사용됩니다. 
    page_text = "\n".join(sorted(set(references)))

    # "context"와 "page_text"를 딕셔너리 형태로 반환합니다. 
    # 이렇게 반환된 딕셔너리는 이후 rag_prompt에 입력으로 전달되어, 
    # LLM이 제공된 문서 내용을 기반으로 질문에 답변할 수 있도록 하는 데 사용됩니다.
    return {
        "context": context,
        "page_text": page_text
    }

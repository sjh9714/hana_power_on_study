def format_docs_with_pages(docs):

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    pages = sorted(
        set(
            doc.metadata.get("page")
            for doc in docs
            if doc.metadata.get("page")
            is not None
        )
    )

    page_text = ", ".join(
        map(str, pages)
    )

    return {
        "context": context,
        "page_text": page_text
    }
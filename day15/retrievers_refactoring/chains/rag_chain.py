from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough
)

from day15.retrievers_refactoring.retrievers.retriever import (
    get_retriever
)

from day15.retrievers_refactoring.prompts.rag_prompt import (
    rag_prompt
)

from day15.retrievers_refactoring.llms.llm import get_llm

from day15.retrievers_refactoring.utils.document_utils import (
    format_docs_with_pages
)

from langchain_core.output_parsers import (
    StrOutputParser
)

retriever = get_retriever()

llm = get_llm()

parser = StrOutputParser()

rag_chain = (
    {
        "docs": retriever,
        "query": RunnablePassthrough()
    }
    | RunnableLambda(
        lambda x: {
            **format_docs_with_pages(
                x["docs"]
            ),
            "query": x["query"]
        }
    )
    | rag_prompt
    | llm
    | parser
)
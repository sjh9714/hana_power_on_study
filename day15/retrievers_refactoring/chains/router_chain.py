from day15.retrievers_refactoring.prompts.router_prompt import (
    router_prompt
)

from day15.retrievers_refactoring.chains.rag_chain import (
    rag_chain
)

from day15.retrievers_refactoring.chains.general_chain import (
    general_chain
)

from day15.retrievers_refactoring.llms.llm import get_llm

from langchain_core.output_parsers import (
    StrOutputParser
)

llm = get_llm()

parser = StrOutputParser()

router_llm_chain = (
    router_prompt
    | llm
    | parser
)

def ask(query):

    category = (
        router_llm_chain.invoke(
            {"query": query}
        )
        .strip()
        .lower()
    )

    if category == "rag":

        return rag_chain.invoke(
            query
        )

    return general_chain.invoke(
        query
    )
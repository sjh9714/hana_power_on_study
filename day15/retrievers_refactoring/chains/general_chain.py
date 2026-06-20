from day15.retrievers_refactoring.prompts.general_prompt import (
    general_prompt
)

from day15.retrievers_refactoring.llms.llm import get_llm

from langchain_core.output_parsers import (
    StrOutputParser
)

from langchain_core.runnables import (
    RunnablePassthrough
)

llm = get_llm()

parser = StrOutputParser()

general_chain = (
    {
        "query": RunnablePassthrough()
    }
    | general_prompt
    | llm
    | parser
)

from langchain_core.prompts import (
    PromptTemplate
)

##############################################################################
# GPT Prompt
##############################################################################

general_prompt = (PromptTemplate.from_template(
"""
질문에 친절하게 답변하세요.

질문:
{query}

답변:
"""
))
from opengraphrag.llm.base import LLMBase
from opengraphrag.prompt.expert import GENERATE_EXPERT_PROMPT


def generate_expert(llm: LLMBase, chunk:str) -> str:
    """Generate an LLM persona to use for GraphRAG prompts.

    Parameters
    ----------
    - llm (CompletionLLM): The LLM to use for generation
    - domain (str): The domain to generate a persona for
    - task (str): The task to generate a persona for. Default is DEFAULT_TASK
    """
    expert_prompt = GENERATE_EXPERT_PROMPT.format(input_text=chunk)
    return llm.invoke(expert_prompt)
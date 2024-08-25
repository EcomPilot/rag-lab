from typing import List, Union
from graphrag.llm.base import LLMBase
from graphrag.prompt.expert import GENERATE_EXPERT_PROMPT
import random


def generate_expert(llm: LLMBase, chunk: Union[str, List[str]], chunk_select_num: int=3) -> str:
    """Generate an LLM persona to use for GraphRAG prompts.

    Parameters
    ----------
    - llm (CompletionLLM): The LLM to use for generation
    - domain (str): The domain to generate a persona for
    - task (str): The task to generate a persona for. Default is DEFAULT_TASK
    """
    if isinstance(chunk, list): chunk = ". ".join(random.choices(chunk, k=chunk_select_num))
    expert_prompt = GENERATE_EXPERT_PROMPT.format(input_text=chunk)
    return llm.invoke(expert_prompt)
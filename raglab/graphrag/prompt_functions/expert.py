from typing import List, Union
from raglab.llm.base import LLMBase
from ..prompt.expert import GENERATE_EXPERT_PROMPT
import random


def generate_expert(llm: LLMBase, chunk: Union[str, List[str]], chunk_select_num: int=3) -> str:
    """The `generate_expert` function is designed to generate expert-level content based on the given text chunks.

    #### Parameters
    - `llm: LLMBase`: An instance of a language model used for generating expert content.
    - `chunk: Union[str, List[str]]`: The text chunk(s) to be analyzed, which can be a string or a list of strings.
    - `chunk_select_num: int` (default is 3): The number of text chunks to randomly select if `chunk` is a list.

    #### Returns
    - `str`: The generated expert content.
    """
    if isinstance(chunk, list): chunk = ". ".join(random.choices(chunk, k=chunk_select_num))
    expert_prompt = GENERATE_EXPERT_PROMPT.format(input_text=chunk)
    return llm.invoke(expert_prompt)
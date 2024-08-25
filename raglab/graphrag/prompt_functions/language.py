import random
from typing import List, Union
from raglab.llms.base import LLMBase
from ..prompt.language import DETECT_LANGUAGE_PROMPT


def detect_text_language(llm: LLMBase, chunk: Union[str, List[str]], chunk_select_num: int=3) -> str:
    """### 
    The `detect_text_language` function is designed to detect the language of given text chunks.

    #### Parameters
    - `llm: LLMBase`: An instance of a language model used for language detection tasks.
    - `chunk: Union[str, List[str]]`: The text chunk(s) to be analyzed, which can be a string or a list of strings.
    - `chunk_select_num: int` (default is 3): The number of text chunks to randomly select if `chunk` is a list.

    #### Returns
    - `str`: The detected language.
    """
    if isinstance(chunk, list): chunk = ". ".join(random.choices(chunk, k=chunk_select_num))
    expert_prompt = DETECT_LANGUAGE_PROMPT.format(input_text=chunk)
    return llm.invoke(expert_prompt)
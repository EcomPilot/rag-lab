import random
from typing import List, Union
from graphrag.llm.base import LLMBase
from graphrag.prompt.language import DETECT_LANGUAGE_PROMPT


def detect_text_language(llm: LLMBase, chunk: Union[str, List[str]], chunk_select_num: int=3) -> str:
    """Detect the current chunks' language.
    """
    if isinstance(chunk, list): chunk = ". ".join(random.choices(chunk, k=chunk_select_num))
    expert_prompt = DETECT_LANGUAGE_PROMPT.format(input_text=chunk)
    return llm.invoke(expert_prompt)
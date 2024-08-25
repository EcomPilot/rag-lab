from typing import List
from raglab.llms.base import LLMBase
from ..prompt.chunk_graph_extraction import ENTITY_RELATIONSHIPS_GENERATION_PROMPT
from ..utils.json_paser import list_loads_from_text


def generate_entity_relationship_examples(llm: LLMBase, chunk:str, language:str, expert:str='') -> List:
    """Generate a list of entity/relationships examples for use in generating an entity configuration.
    Will return entity/relationships examples as either JSON or in tuple_delimiter format depending
    """
    return list_loads_from_text(llm.invoke(ENTITY_RELATIONSHIPS_GENERATION_PROMPT.format(input_text=chunk, language=language, expert=expert)))
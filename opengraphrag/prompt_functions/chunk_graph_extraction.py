from typing import List
from opengraphrag.llm.base import LLMBase
from opengraphrag.prompt.chunk_graph_extraction import ENTITY_RELATIONSHIPS_GENERATION_PROMPT
from opengraphrag.utils.json_paser import list_loads_from_text


def generate_entity_relationship_examples(llm: LLMBase, chunk:str, language:str) -> List:
    """Generate a list of entity/relationships examples for use in generating an entity configuration.
    Will return entity/relationships examples as either JSON or in tuple_delimiter format depending
    """
    return list_loads_from_text(llm.invoke(ENTITY_RELATIONSHIPS_GENERATION_PROMPT.format(input_text=chunk, language=language)))
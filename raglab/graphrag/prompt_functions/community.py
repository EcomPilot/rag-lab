from dataclasses import asdict
from typing import Any, Dict, List
from ..data_contracts.graph import Relationship, Entity
from raglab.llms.base import LLMBase
from ..prompt.community import COMMUNITY_REPORT_SUMMARIZATION_PROMPT
import pandas as pd
from ...utils import json_loads_from_text
from ..utils.graph_utils import convert_to_dataframe


def generate_community_report(llm: LLMBase, entities: List[Entity], relationships: List[Relationship], language:str, expert:str='') -> Dict[str, Any]:
    '''
    The `generate_community_report` function is designed to generate a community report from a list of entities and relationships.

    #### Parameters
    - `llm: LLMBase`: An instance of a language model used for generating the community report.
    - `entities: List[Entity]`: A list of entities to be included in the report.
    - `relationships: List[Relationship]`: A list of relationships to be included in the report.
    - `language: str`: The language in which the report should be generated.
    - `expert: str` (default is an empty string): An optional expert input for generating the community report.

    #### Returns
    - `Dict[str, Any]`: A dictionary containing the generated community report.
    '''
    entity_df = convert_to_dataframe(entities)[['readable_id', 'entity_name', 'entity_description']]
    entity_df = entity_df.rename(columns={"readable_id": "id", "entity_name": "name", "entity_description": "description"})
    relationship_df = convert_to_dataframe(relationships)[['readable_id', 'source_entity', 'target_entity', 'relationship_description']]
    relationship_df = relationship_df.rename(columns={"readable_id": "id", "relationship_description": "description"})
    entity_table = entity_df.to_csv(index=False)
    relationship_table = relationship_df.to_csv(index=False)
    prompt = COMMUNITY_REPORT_SUMMARIZATION_PROMPT.format(expert=expert, entity_table=entity_table, relationship_table=relationship_table, language=language)
    output = llm.invoke(prompt=prompt)
    return json_loads_from_text(output)

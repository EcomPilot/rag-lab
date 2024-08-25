from dataclasses import asdict
from typing import Any, Dict, List
from graphrag.data_contracts.graph import Relationship, Entity
from graphrag.llm.base import LLMBase
from graphrag.prompt.community import COMMUNITY_REPORT_SUMMARIZATION_PROMPT
import pandas as pd
from graphrag.utils.json_paser import json_loads_from_text


def generate_community_report(llm: LLMBase, entities: List[Entity], relationships: List[Relationship], language:str, expert:str='') -> Dict[str, Any]:
    entity_df = pd.DataFrame([asdict(entity) for entity in entities])[['readable_id', 'entity_name', 'entity_description']]
    entity_df = entity_df.rename(columns={"readable_id": "id", "entity_name": "name", "entity_description": "description"})
    relationship_df = pd.DataFrame([asdict(rel) for rel in relationships])[['readable_id', 'source_entity', 'target_entity', 'relationship_description']]
    relationship_df = relationship_df.rename(columns={"readable_id": "id", "relationship_description": "description"})
    entity_table = entity_df.to_csv(index=False)
    relationship_table = relationship_df.to_csv(index=False)
    prompt = COMMUNITY_REPORT_SUMMARIZATION_PROMPT.format(expert=expert, entity_table=entity_table, relationship_table=relationship_table, language=language)
    output = llm.invoke(prompt=prompt)
    return json_loads_from_text(output)

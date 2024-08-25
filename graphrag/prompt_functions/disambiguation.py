from typing import Dict, List
from graphrag.data_contracts.graph import Entity, Relationship
from graphrag.data_contracts.type import Strategy
from graphrag.llm.base import LLMBase
from graphrag.prompt.disambiguation import DISAMBIGUATION_ENTITY_PROMPT, SUMMARY_ENTITY_DISCRIPTIONS_PROMPT, SUMMARY_ENTITY_TYPE_PROMPT, SUMMARY_RELATIONSHIP_DISCRIPTIONS_PROMPT
from graphrag.utils.json_paser import list_loads_from_text
from collections import defaultdict
import json


def disambigute_entity(llm: LLMBase, entities:List[Entity], expert: str='') -> List[List[int]]:
    '''
    The `disambigute_entity` function is designed to disambiguate entities by generating a list of entity IDs that are considered to be the same entity.

    #### Parameters
    - `llm: LLMBase`: An instance of a language model used for disambiguating entities.
    - `entities: List[Entity]`: A list of entities to be disambiguated.
    - `expert: str` (default is an empty string): An optional expert input for disambiguating entities.

    #### Returns
    - `List[List[int]]`: A list of lists, where each inner list contains the IDs of entities that are considered to be the same.
    '''
    entities_with_id = [{
        "node_id": i + 1,
        "entity_name": entity.entity_name,
        "entity_description": entity.entity_description} for i, entity in enumerate(entities)]
    return list_loads_from_text(llm.invoke(DISAMBIGUATION_ENTITY_PROMPT.format(entities=json.dumps(entities_with_id), expert=expert)))


def merge_summary_entity(llm: LLMBase, entities:List[Entity], expert: str='', strategy:Strategy = Strategy.accuracy) -> List[Entity]:
    '''
    The `merge_summary_entity` function is designed to merge and summarize entities based on their names, descriptions, and types.

    #### Parameters
    - `llm: LLMBase`: An instance of a language model used for summarizing entity descriptions and types.
    - `entities: List[Entity]`: A list of entities to be merged and summarized.
    - `expert: str` (default is an empty string): An optional expert input for summarizing entities.
    - `strategy: Strategy` (default is `Strategy.accuracy`): The strategy to be used for summarizing entities.

    #### Returns
    - `List[Entity]`: A list of merged and summarized entities.
    '''
    entity_name_description_list_mapping = defaultdict(list)
    entity_name_type_list_mapping = defaultdict(set)
    entity_name_chunk_ids_mapping = defaultdict(list)

    for entity in entities:
        entity_name_description_list_mapping[entity.entity_name].append(entity.entity_description)
        entity_name_type_list_mapping[entity.entity_name].add(entity.entity_type)
        entity_name_chunk_ids_mapping[entity.entity_name].extend(entity.source_chunk_ids)
    entity_name_description_list_mapping = dict(entity_name_description_list_mapping)
    entity_name_chunk_ids_mapping = dict(entity_name_chunk_ids_mapping)
    entity_name_type_list_mapping = dict(entity_name_type_list_mapping)

    entities.clear()
    for entity_name in entity_name_description_list_mapping:
        discription_list = entity_name_description_list_mapping[entity_name]
        type_list = entity_name_type_list_mapping[entity_name]
        source_chunk_ids = entity_name_chunk_ids_mapping[entity_name]
        discription_summary = '.'.join(discription_list)
        entity_type = ','.join(type_list)
        if strategy == Strategy.accuracy:
            if len(discription_list) > 1: discription_summary = llm.invoke(SUMMARY_ENTITY_DISCRIPTIONS_PROMPT.format(discriptions=json.dumps(discription_list), expert=expert))
            if len(type_list) > 1: entity_type = llm.invoke(SUMMARY_ENTITY_TYPE_PROMPT.format(expert=expert, entity_types=entity_type, discriptions=discription_summary, entity_name=entity_name))
        entities.append(Entity(entity_name=entity_name, entity_type=entity_type, entity_description=discription_summary, source_chunk_ids=source_chunk_ids))

    return entities


def merge_summary_relationship(llm: LLMBase, origin_relationships:List[Relationship], expert: str='', strategy:Strategy = Strategy.accuracy) -> List[Relationship]:
    '''
    The `merge_summary_relationship` function is designed to merge and summarize relationships based on their descriptions and strengths.

    #### Parameters
    - `llm: LLMBase`: An instance of a language model used for summarizing relationship descriptions.
    - `origin_relationships: List[Relationship]`: A list of original relationships to be merged and summarized.
    - `expert: str` (default is an empty string): An optional expert input for summarizing relationships.
    - `strategy: Strategy` (default is `Strategy.accuracy`): The strategy to be used for summarizing relationships.

    #### Returns
    - `List[Relationship]`: A list of merged and summarized relationships.
    '''
    relationship_description_dict,  relationship_strength_dict, relationship_source_chunk_ids = defaultdict(list), defaultdict(list), defaultdict(list)
    result = []

    for relationship in origin_relationships:
        key = (relationship.source_entity, relationship.target_entity)
        relationship_description_dict[key].append(relationship.relationship_description)
        relationship_strength_dict[key].append(relationship.relationship_strength)
        relationship_source_chunk_ids[key].extend(relationship.source_chunk_ids)

    relationship_description_dict, relationship_strength_dict, relationship_source_chunk_ids = dict(relationship_description_dict), dict(relationship_strength_dict), dict(relationship_source_chunk_ids)
    for key in relationship_description_dict:
        strength = sum(relationship_strength_dict[key]) / len(relationship_strength_dict[key])
        source_chunk_ids = relationship_source_chunk_ids[key]
        description = '.'.join(relationship_description_dict[key])
        if strategy == Strategy.accuracy and  len(relationship_description_dict[key]) > 1:
            description = llm.invoke(SUMMARY_RELATIONSHIP_DISCRIPTIONS_PROMPT.format(source_entity=key[0], target_entity=key[1], descriptions=json.dumps(relationship_description_dict[key]), expert=expert))
        result.append(Relationship(source_entity=key[0], target_entity=key[1], relationship_description=description, relationship_strength=strength, source_chunk_ids=source_chunk_ids))

    return result
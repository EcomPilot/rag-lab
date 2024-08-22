from typing import Dict, List
from opengraphrag.data_contracts.graph import Entity, Relationship
from opengraphrag.data_contracts.type import Strategy
from opengraphrag.llm.base import LLMBase
from opengraphrag.prompt.disambiguation import DISAMBIGUATION_ENTITY_PROMPT, SUMMARY_ENTITY_DISCRIPTIONS_PROMPT, SUMMARY_ENTITY_TYPE_PROMPT, SUMMARY_RELATIONSHIP_DISCRIPTIONS_PROMPT
from opengraphrag.utils.json_paser import list_loads_from_text
from collections import defaultdict
import json


def disambigute_entity(llm: LLMBase, entities:List[Entity], expert: str='') -> List[List[int]]:
    entities_with_id = [{
        "node_id": i + 1,
        "entity_name": entity.entity_name,
        "entity_description": entity.entity_description} for i, entity in enumerate(entities)]
    return list_loads_from_text(llm.invoke(DISAMBIGUATION_ENTITY_PROMPT.format(entities=json.dumps(entities_with_id), expert=expert)))


def merge_summary_entity(llm: LLMBase, entities:List[Entity], expert: str='', strategy:Strategy = Strategy.accuracy) -> List[Entity]:
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
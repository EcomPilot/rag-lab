from opengraphrag.data_contracts.graph import Entity, Relationship
from typing import List, Dict, Union
from collections import defaultdict


def get_entity_types_mapping(entities: List[Entity]) -> Dict[str, Entity]:
    entity_dict = defaultdict(list)
    for entity in entities: entity_dict[entity.entity_type].append(entity)
    return dict(entity_dict)


def merge_entity_types(entity_dict: Dict[str, Entity], merged_entity_type_list: List[List[str]]) -> Dict[str, Entity]:
    merged_entity_type_list = __validate_entity_type(entity_dict, merged_entity_type_list)

    merged_entity_dict = defaultdict(list)
    for type_list in merged_entity_type_list:
        new_type = type_list[0]
        for old_type in type_list:
            current_entity_list = entity_dict[old_type]
            current_entity_list = __reset_entity_type(current_entity_list, new_type)
            merged_entity_dict[new_type].extend(current_entity_list)
    
    return dict(merged_entity_dict)


def flatten_dict_list(dict_list:Dict[str, List[Union[Entity, Relationship]]]) -> List[Union[Entity, Relationship]]:
    return [item for key in dict_list for item in dict_list[key]]


def __validate_entity_type(entity_dict: Dict[str, Entity], merged_entity_type_list: List[List[str]]) -> List[List[str]]:
    entity_types = set(entity_dict.keys())
    flattern_types = set([item for sublist in merged_entity_type_list for item in sublist])
    external_types = entity_types - flattern_types
    for entity_type in external_types: merged_entity_type_list.append([entity_type])
    return merged_entity_type_list


def __reset_entity_type(entities:List[Entity], new_type:str):
    for entity in entities: entity.entity_type = new_type
    return entities
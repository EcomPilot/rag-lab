from dataclasses import asdict
from typing import List, Tuple
from ..data_contracts import Entity, Relationship, Community
from loguru import logger
import pandas as pd


def covert_virtual_relationship_to_enetity(entities: List[Entity], relationships: List[Relationship]) -> Tuple[List[Entity], List[Relationship]]:
    '''
    The `covert_virtual_relationship_to_enetity` function is designed to convert virtual relationships into entities if they do not have both source and target entities in the existing entities list.

    #### Parameters
    - `entities: List[Entity]`: A list of entities to be processed.
    - `relationships: List[Relationship]`: A list of relationships to be processed.

    #### Returns
    - `Tuple[List[Entity], List[Relationship]]`: A tuple containing the updated list of entities and the filtered list of relationships.
    '''
    entities_set = {entity.entity_name for entity in entities}
    new_relations = []
    for rel in relationships:
        if (rel.source_entity in entities_set) and (rel.target_entity in entities_set):
            new_relations.append(rel)
        else:
            if rel.source_entity in entities_set: entities.append(Entity(entity_name=rel.source_entity, entity_type=rel.target_entity, entity_description=rel.relationship_description, source_chunk_ids=rel.source_chunk_ids))
            elif rel.target_entity in entities_set: entities.append(Entity(entity_name=rel.target_entity, entity_type=rel.source_entity, entity_description=rel.relationship_description, source_chunk_ids=rel.source_chunk_ids))
            logger.info(f"Convert Relationship to Entity: {rel}")
    return entities, new_relations


def update_readable_id(items:List[Entity | Relationship | Community]) -> List[Entity | Relationship | Community]:
    '''
    The `update_readable_id` function is designed to update the `readable_id` attribute of a list of items, which can be entities, relationships, or communities.

    #### Parameters
    - `items: List[Entity | Relationship | Community]`: A list of items whose `readable_id` attributes need to be updated.

    #### Returns
    - `List[Entity | Relationship | Community]`: The list of items with updated `readable_id` attributes.
    '''
    for i in range(len(items)):
        items[i].readable_id = (i+1)

    return items


def convert_to_dataframe(items:List[Entity | Relationship | Community]) -> pd.DataFrame:
    '''
    The `convert_to_dataframe` function is designed to convert a list of items (which can be entities, relationships, or communities) into a Pandas DataFrame.

    #### Parameters
    - `items: List[Entity | Relationship | Community]`: A list of items to be converted into a DataFrame.

    #### Returns
    - `pd.DataFrame`: A DataFrame containing the data from the list of items.
    '''
    return pd.DataFrame([asdict(item) for item in items])
from typing import List, Tuple
from graphrag.data_contracts.graph import Entity, Relationship, Community
from loguru import logger


def covert_virtual_relationship_to_enetity(entities: List[Entity], relationships: List[Relationship]) -> Tuple[List[Entity], List[Relationship]]:
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
    for i in range(len(items)):
        items[i].readable_id = (i+1)

    return items
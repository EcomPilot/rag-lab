from dataclasses import dataclass, field
import uuid


@dataclass
class Entity:
    entity_name:str
    entity_type:str
    entity_description:str
    entity_id:str = field(default_factory=lambda: str(uuid.uuid4()))
    source_chunk_ids:list = field(default_factory=list)


@dataclass
class Relationship:
    source_entity:str
    target_entity:str
    relationship_description:str
    relationship_strength:str = 1
    relationship_id:str = field(default_factory=lambda: str(uuid.uuid4()))
    source_chunk_ids:list = field(default_factory=list)


if __name__ == "__main__":
    entity = Entity(1,2,3,4,5)
    print(entity, type(entity))
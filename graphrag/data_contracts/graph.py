from dataclasses import dataclass, field
from typing import Dict, List
import uuid


@dataclass
class Entity:
    entity_name:str
    entity_type:str
    entity_description:str
    readable_id:int = 0
    entity_id:str = field(default_factory=lambda: str(uuid.uuid4()))
    source_chunk_ids:list = field(default_factory=list)


@dataclass
class Relationship:
    source_entity:str
    target_entity:str
    relationship_description:str
    relationship_strength:str = 1
    readable_id:int = 0
    relationship_id:str = field(default_factory=lambda: str(uuid.uuid4()))
    source_chunk_ids:list = field(default_factory=list)


@dataclass
class Community:
    title:str
    summary:str
    rating:float
    rating_explanation:str
    findings: List[Dict[str,str]]
    readable_id:int = 0
    community_id:str = field(default_factory=lambda: str(uuid.uuid4()))
    source_entity_ids:list = field(default_factory=list)
    source_relationship_ids:list = field(default_factory=list)


if __name__ == "__main__":
    entity = Entity(1,2,3,4,5)
    print(entity, type(entity))
from dataclasses import dataclass, field
import uuid


@dataclass
class Entity:
    entity_name:str
    entity_type:str
    entity_description:str
    entity_id:uuid.UUID = field(default_factory=uuid.uuid4)
    source_chunk_ids:list = field(default_factory=list)


@dataclass
class Relationship:
    source_entity:str
    target_entity:str
    relationship_description:str
    relationship_strength:str
    relationship_id:uuid.UUID = field(default_factory=uuid.uuid4)
    source_chunk_ids:list = field(default_factory=list)
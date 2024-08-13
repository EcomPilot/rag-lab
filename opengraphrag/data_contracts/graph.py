from dataclasses import dataclass


@dataclass
class Entity:
    entity_name:str
    entity_type:str
    entity_description:str


@dataclass
class Relationship:
    source_entity:str
    target_entity:str
    relationship_description:str
    relationship_strength:str
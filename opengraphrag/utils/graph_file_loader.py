from dataclasses import asdict
from typing import List, Tuple
from opengraphrag.data_contracts.graph import Entity, Relationship
import json
from loguru import logger
import os


def graph_save(entities: List[Entity], relationships: List[Relationship], filepath: str):
    logger.info(f"Saveing graph to [{filepath}]...")
    output = {
        "entities": [asdict(entity) for entity in entities],
        "relationships": [asdict(rel) for rel in relationships]
    }
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(file=filepath, mode="w", encoding="utf-8") as fp:
        json.dump(output, fp, indent=4)
    logger.info(f"Saved graph!")


def graph_load(filepath: str) -> Tuple[List[Entity], List[Relationship]]:
    logger.info(f"Loading entities, relationship...")
    output = {}
    with open(file=filepath, mode="r", encoding="utf-8") as fp:
        output = json.load(fp=fp)

    entities = output.get("entities")
    relationships = output.get("relationships")
    assert isinstance(entities, list) or isinstance(relationships, list), f"please check your file path {filepath}, we cannot load graph file from it."
    entities = [Entity(**entity) for entity in entities]
    relationships = [Relationship(**rel) for rel in relationships]
    logger.info(f"Loading entities, relationship succeed.")
    return entities, relationships

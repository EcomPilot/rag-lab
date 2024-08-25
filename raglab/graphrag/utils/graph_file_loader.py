from dataclasses import asdict
from typing import List, Tuple
from ..data_contracts.graph import Community, Entity, Relationship
import json
from loguru import logger
import os


def graph_save_json(entities: List[Entity], relationships: List[Relationship], communities:List[Community], filepath: str):
    '''
    The `graph_save_json` function is designed to save entities, relationships, and communities to a JSON file.

    #### Parameters
    - `entities: List[Entity]`: A list of entities to be saved.
    - `relationships: List[Relationship]`: A list of relationships to be saved.
    - `communities: List[Community]`: A list of communities to be saved.
    - `filepath: str`: The path where the JSON file will be saved.

    #### Returns
    - None: This function saves the graph data to a specified JSON file.
    '''
    logger.info(f"Saveing graph to [{filepath}]...")
    output = {
        "entities": [asdict(entity) for entity in entities],
        "relationships": [asdict(rel) for rel in relationships],
        "communities": [asdict(com) for com in communities]
    }
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(file=filepath, mode="w", encoding="utf-8") as fp:
        json.dump(output, fp, indent=4)
    logger.info(f"Saved graph!")


def graph_load_json(filepath: str) -> Tuple[List[Entity], List[Relationship], List[Community]]:
    '''
    #### Purpose
    The `graph_load_json` function is designed to load entities, relationships, and communities from a JSON file.

    #### Parameters
    - `filepath: str`: The path to the JSON file to be loaded.

    #### Returns
    - `Tuple[List[Entity], List[Relationship], List[Community]]`: A tuple containing lists of entities, relationships, and communities.
    '''
    logger.info(f"Loading entities, relationships, communities...")
    output = {}
    with open(file=filepath, mode="r", encoding="utf-8") as fp:
        output = json.load(fp=fp)

    entities = output.get("entities")
    relationships = output.get("relationships")
    communities = output.get("communities")
    assert isinstance(entities, list) or isinstance(relationships, list) or isinstance(communities, list), f"please check your file path {filepath}, we cannot load graph file from it."

    entities = [Entity(**entity) for entity in entities]
    relationships = [Relationship(**rel) for rel in relationships]
    communities = [Community(**com) for com in communities]
    logger.info(f"Loading entities, relationships, communities succeed.")
    return entities, relationships, communities

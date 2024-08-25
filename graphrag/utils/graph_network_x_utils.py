from typing import List
from networkx import Graph
import numpy as np
import networkx as nx
from graphrag.data_contracts.graph import Entity, Relationship
from loguru import logger


def convert_to_network_x_graph(entities: List[Entity], relationships: List[Relationship]) -> Graph:
    G = nx.Graph()

    for entity in entities:
        G.add_node(entity.entity_name, type=entity.entity_type, description=entity.entity_description)

    for relationship in relationships:
        if relationship.source_entity in G.nodes and relationship.target_entity in G.nodes:
            G.add_edge(relationship.source_entity, relationship.target_entity, 
                    description=relationship.relationship_description, 
                    weight=relationship.relationship_strength)
        else:
            logger.warning(f"Warning: Relationship {relationship} contains nodes not in entities list.")
        
    return G
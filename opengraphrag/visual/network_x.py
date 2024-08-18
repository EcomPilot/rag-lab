import networkx as nx
import matplotlib.pyplot as plt
from typing import List
from opengraphrag.data_contracts.graph import Entity, Relationship


def visualize_knowledge_graph_network_x(entities: List[Entity], relationships: List[Relationship]):
    G = nx.DiGraph()

    for entity in entities:
        G.add_node(entity.entity_name, type=entity.entity_type, description=entity.entity_description)

    for relationship in relationships:
        G.add_edge(relationship.source_entity, relationship.target_entity, 
                   description=relationship.relationship_description, 
                   strength=relationship.relationship_strength)

    pos = nx.spring_layout(G)
    node_labels = {node: f"{node}\n({G.nodes[node].get('type', 'N/A')})" for node in G.nodes}
    edge_labels = nx.get_edge_attributes(G, 'description')
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=700, node_color='lightblue', edge_color='gray', font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title('Knowledge Graph')
    plt.show()
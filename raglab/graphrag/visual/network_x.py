import networkx as nx
import matplotlib.pyplot as plt
from typing import List
from ..data_contracts.graph import Entity, Relationship
from ..utils.graph_network_x_utils import convert_to_network_x_graph


def visualize_knowledge_graph_network_x(entities: List[Entity], relationships: List[Relationship]):
    '''
    The `visualize_knowledge_graph_network_x` function is designed to visualize a knowledge graph using the NetworkX library.

    #### Parameters
    - `entities: List[Entity]`: A list of entities to be visualized.
    - `relationships: List[Relationship]`: A list of relationships to be visualized.

    #### Returns
    - None: This function generates a visualization of the knowledge graph and displays it using Matplotlib.
    '''
    G = convert_to_network_x_graph(entities, relationships)

    pos = nx.spring_layout(G)
    node_labels = {node: f"{node}\n({G.nodes[node].get('type', 'N/A')})" for node in G.nodes}
    edge_labels = nx.get_edge_attributes(G, 'description')
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=700, node_color='lightblue', edge_color='gray', font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title('Knowledge Graph')
    plt.show()
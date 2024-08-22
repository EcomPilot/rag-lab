import numpy as np
from opengraphrag.utils.graph_file_loader import graph_load
from opengraphrag.utils.graph_network_x_utils import convert_to_network_x_graph
from opengraphrag.visual.network_x import visualize_knowledge_graph_network_x
from communities.algorithms import louvain_method
import networkx as nx
import matplotlib.pyplot as plt


if __name__ == "__main__":
    graph_filepath = "./examples/graphfiles/Gullivers-travels-A-Voyage-to-Lilliput.json"
    entities, relationships = graph_load(graph_filepath)

    # visualize_knowledge_graph_network_x(entities, relationships)
    G = convert_to_network_x_graph(entities, relationships)
    adj_matrix = nx.to_numpy_array(G)
    communities, _ = louvain_method(adj_matrix)
    pos = nx.spring_layout(G)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(communities)))

    for community, color in zip(communities, colors):
        node_names = [entities[node].entity_name for node in community]
        nx.draw_networkx_nodes(G, pos, nodelist=node_names, node_color=[color])
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, nx.get_node_attributes(G, 'label'))
    plt.show()
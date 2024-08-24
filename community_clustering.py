import os
import numpy as np
from opengraphrag.llm.azure_openai import AzureOpenAILLM
from opengraphrag.prompt_functions.community import generate_community_report
from opengraphrag.utils.graph_file_loader import graph_load
from opengraphrag.utils.graph_network_x_utils import convert_to_network_x_graph
from opengraphrag.visual.network_x import visualize_knowledge_graph_network_x
from communities.algorithms import louvain_method
import networkx as nx
import matplotlib.pyplot as plt


if __name__ == "__main__":
    graph_filepath = "./examples/graphfiles/Gullivers-travels-A-Voyage-to-Lilliput.json"
    entities, relationships = graph_load(graph_filepath)
    min_entities_in_cummunity = 5

    AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
    AZURE_OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]
    AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]

    muti_thread = 20
    aoai_llm = AzureOpenAILLM(
        model_id=AZURE_OPENAI_DEPLOYMENT,
        access_token= AZURE_OPENAI_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT
    )

    # visualize_knowledge_graph_network_x(entities, relationships)
    G = convert_to_network_x_graph(entities, relationships)
    adj_matrix = nx.to_numpy_array(G)
    communities, _ = louvain_method(adj_matrix)
    communities = [com for com in communities if len(com) >= min_entities_in_cummunity]

    for com in communities:
        com_entities = [entities[i] for i in com]
        com_entity_set = {entity.entity_name for entity in com_entities}
        com_rels = [rel for rel in relationships if (rel.target_entity in com_entity_set) or (rel.source_entity in com_entity_set)]
        reprot = generate_community_report(aoai_llm, com_entities, com_rels, 'English')

    pos = nx.spring_layout(G)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(communities)))

    count = 0
    for com in communities:
        if len(com) > 6:
            count += 1
            print(com)

    for community, color in zip(communities, colors):
        node_names = [entities[node].entity_name for node in community]
        nx.draw_networkx_nodes(G, pos, nodelist=node_names, node_color=[color])
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, nx.get_node_attributes(G, 'label'))
    plt.show()
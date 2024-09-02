from typing import List
import networkx as nx
import networkx.algorithms.community as nx_comm

def detect_communities_louvain(G: nx.Graph, min_entities_in_community: int) -> List[List[int]]:
    """
    Detect communities in a graph using the Louvain algorithm.

    **Parameters:**
    - G (nx.Graph): The input graph.
    - min_entities_in_community (int): The minimum number of entities required in a community.

    **Returns:**
    - List[List[int]]: A list of communities, where each community is represented
                       as a list of node indices.
    """
    partition = nx_comm.louvain_communities(G, seed=42)
    node_list = list(G.nodes)
    communities = [
        [node_list.index(node) for node in community]
        for community in partition if len(community) >= min_entities_in_community
    ]
    return communities

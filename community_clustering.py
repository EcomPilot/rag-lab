import os
from typing import List
import numpy as np
from graphrag.data_contracts.graph import Community, Entity, Relationship
from graphrag.data_contracts.type import Strategy
from graphrag.llm.azure_openai import AzureOpenAILLM
from graphrag.llm.base import LLMBase
from graphrag.prompt_functions.community import generate_community_report
from graphrag.utils.dataclass_utils import dict2object, dict_matches_dataclass
from graphrag.utils.graph_file_loader import graph_save_json, graph_load_json
from graphrag.utils.graph_network_x_utils import convert_to_network_x_graph
from graphrag.utils.parallel_utils import parallel_for
from graphrag.visual.network_x import visualize_knowledge_graph_network_x
from loguru import logger
from communities.algorithms import louvain_method
import networkx as nx
import matplotlib.pyplot as plt


if __name__ == "__main__":
    graph_filepath = "./examples/graphfiles/Gullivers-travels-A-Voyage-to-Lilliput.json"
    entities, relationships, communities = graph_load_json(graph_filepath)
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
    community_reports = generate_community_reports_executor(aoai_llm, entities, relationships, num_threads=3)
    graph_save_json(entities, relationships, community_reports, graph_filepath)

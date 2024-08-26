import os
from raglab.embeddings import AzureOpenAIEmbedding
from raglab.graphrag import (
    disambiguate_entity_executor, 
    disambiguate_relationship_executor, 
    generate_community_reports_executor, 
    generate_entire_chunk_graph_executor,
    update_graph_embeddings_executor,
    detect_text_language,
    generate_expert,
    graph_load_json,
    graph_save_json,
    convert_to_dataframe,
)
import numpy as np
import pandas as pd
from loguru import logger
from raglab.graphrag.prompt.search import SIMPLE_SEARCH_PROMPT
from raglab.llms import AzureOpenAILLM


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


if __name__ == "__main__":
    AZURE_OPENAI_LLM_DEPLOYMENT = os.environ["AZURE_OPENAI_LLM_DEPLOYMENT"]
    AZURE_OPENAI_EMBED_DEPLOYMENT = os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"]
    AZURE_OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]
    AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]

    aoai_llm = AzureOpenAILLM(
        model_id=AZURE_OPENAI_LLM_DEPLOYMENT,
        access_token= AZURE_OPENAI_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT
    )

    aoai_embed = AzureOpenAIEmbedding(
        model_id=AZURE_OPENAI_EMBED_DEPLOYMENT,
        access_token= AZURE_OPENAI_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT
    )

    # load graph objects and convert them to DataFrame
    graph_filepath = "./examples/graphfiles/Gullivers-travels.json"
    entities, relations, communities = graph_load_json(graph_filepath)
    entity_select_num = 5
    # entities_df, relations_df, communities_df = convert_to_dataframe(entities), convert_to_dataframe(relations), convert_to_dataframe(communities)

    ## 1. embedding query and selecting the most similar search entities
    query = "Who is the king of Lilliput?"
    query_embed = aoai_embed.embed_query(query)

    entities_cosine_similarity = [cosine_similarity(entity.embedding, query_embed) for entity in entities]
    selected_entity_indexes = np.argsort(entities_cosine_similarity)[-entity_select_num:]
    selected_entity = [entities[i] for i in selected_entity_indexes]

    ## 2. selecting all relationships from selected entities
    selected_entity_set = {entity.entity_name for entity in selected_entity}
    selected_relations = [rel for rel in relations if (rel.source_entity in selected_entity_set) or (rel.target_entity in selected_entity_set)]

    ## 3. selecting all communities from selected entities
    selected_entity_id_set = {entity.entity_id for entity in selected_entity}
    selected_communities = [com for com in communities if any(id in selected_entity_id_set for id in com.source_entity_ids)]
    if len(selected_communities) > 1:
        communities_cosine_similarity = [cosine_similarity(com.embedding, query_embed) for com in selected_communities]
        selected_commnity = selected_communities[np.argsort(communities_cosine_similarity)[-1]]
    elif selected_communities == 1:
        selected_commnity = selected_communities[0]
    else:
        selected_commnity = None

    ## 4. generate the final answer
    entity_df = convert_to_dataframe(selected_entity)[['readable_id', 'entity_name', 'entity_description']]
    entity_df = entity_df.rename(columns={"readable_id": "id", "entity_name": "name", "entity_description": "description"})
    relationship_df = convert_to_dataframe(selected_relations)[['readable_id', 'source_entity', 'target_entity', 'relationship_description']]
    relationship_df = relationship_df.rename(columns={"readable_id": "id", "relationship_description": "description"})
    entity_table = entity_df.to_csv(index=False)
    relationship_table = relationship_df.to_csv(index=False)

    prompt = SIMPLE_SEARCH_PROMPT.format(
        query=query,
        entity_table=entity_table,
        relationship_table=relationship_table,
        communtiy_report=selected_commnity.summary
        )
    logger.info(f"final answer: {aoai_llm.invoke(prompt)}")
    # final answer: The king of Lilliput is Golbasto Momarem Evlame Gurdilo Shefin Mully Ully Gue. He is the ruler of the kingdom of Lilliput. Lilliput is a unique country with its own inhabitants, laws, and customs. It is currently being threatened by the empire of Blefuscu, with whom they are engaged in a war. The country practices a maxim of rewarding and punishing its citizens based on their adherence to the laws. The Court of Lilliput is the court of the emperor in Lilliput. The Lilliputians are a small people with sharp eyesight who inhabit the fictional island nation of Lilliput. They have different beliefs about the duties of parents and children, with some believing it is unjust to rely on the public for support.
    
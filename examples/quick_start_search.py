import os
from typing import List
from raglab.embeddings import AzureOpenAIEmbedding
from raglab.graphrag import (
    graph_load_json
)
from loguru import logger
from raglab.graphrag.prompt.search import SIMPLE_SEARCH_PROMPT
from raglab.graphrag.search_functions import generate_final_answer_prompt, select_community, select_entities, select_relations
from raglab.llms import AzureOpenAILLM


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

    ## 2. selecting the most similar search entities
    selected_entity = select_entities(query_embed, entities)

    ## 3. selecting all relationships from selected entities
    selected_relations = select_relations(selected_entity, relations)

    ## 4. selecting all communities from selected entities
    selected_commnity = select_community(query_embed, selected_entity, communities)

    ## 5. generate the final answer
    prompt = generate_final_answer_prompt(query, selected_entity, selected_relations, selected_commnity)
    logger.info(f"final answer: {aoai_llm.invoke(prompt)}")
    # final answer: The king of Lilliput is Golbasto Momarem Evlame Gurdilo Shefin Mully Ully Gue. He is the ruler of the kingdom of Lilliput. Lilliput is a unique country with its own inhabitants, laws, and customs. It is currently being threatened by the empire of Blefuscu, with whom they are engaged in a war. The country practices a maxim of rewarding and punishing its citizens based on their adherence to the laws. The Court of Lilliput is the court of the emperor in Lilliput. The Lilliputians are a small people with sharp eyesight who inhabit the fictional island nation of Lilliput. They have different beliefs about the duties of parents and children, with some believing it is unjust to rely on the public for support.
    
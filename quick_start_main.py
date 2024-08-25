from typing import List
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
from raglab.graphrag.visual import (
    visualize_knowledge_graph_echart,
    visualize_knowledge_graph_network_x
)
from raglab.llms import AzureOpenAILLM
from raglab.embeddings import AzureOpenAIEmbedding
from unstructured.partition.text import partition_text
from unstructured.chunking.basic import chunk_elements
from unstructured.cleaners.core import clean_non_ascii_chars, clean_extra_whitespace
from loguru import logger
import os
import uuid


def chuncking_executor(filename:str, chunk_size=1000, overlap=100) -> List[str]:
    elements = partition_text(filename=filename)
    for elem in elements:
        elem.text = clean_extra_whitespace(clean_non_ascii_chars(elem.text))
    chunks = chunk_elements(elements, max_characters=chunk_size, overlap=overlap)
    return [chunk.text for chunk in chunks]


if __name__ == "__main__":
    filename = "./examples/documents/Gullivers-travels-A-Voyage-to-Lilliput.txt"
    graph_filepath = "./examples/graphfiles/"
    
    AZURE_OPENAI_LLM_DEPLOYMENT = os.environ["AZURE_OPENAI_LLM_DEPLOYMENT"]
    AZURE_OPENAI_EMBED_DEPLOYMENT = os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"]
    AZURE_OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]
    AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]

    strategy = "accuracy"
    muti_thread = 2
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

    chunks = chuncking_executor(filename)
    chunk_ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
    logger.info("Generating expert descripiton...")
    expert = generate_expert(aoai_llm, chunks)
    logger.info(f"Generated expert descripiton: {expert}")

    logger.info("Detect language...")
    language = detect_text_language(aoai_llm, chunks)
    logger.info(f"Detected language: {language}")
    
    entities, relations = generate_entire_chunk_graph_executor(aoai_llm, chunks, chunk_ids, expert, language, strategy, muti_thread)
    entities, relations = disambiguate_entity_executor(aoai_llm, entities, relations, expert, language, strategy)
    relations = disambiguate_relationship_executor(aoai_llm, relations, expert, language, strategy)
    community_reports = generate_community_reports_executor(aoai_llm, entities, relations, expert, language, strategy, 5, muti_thread)

    entities = update_graph_embeddings_executor(aoai_embed, entities, num_threads=muti_thread)
    community_reports = update_graph_embeddings_executor(aoai_embed, community_reports, num_threads=muti_thread)

    # save graph
    ## save graph to local as json file
    graph_save_json(entities, relations, community_reports, os.path.join(graph_filepath, "Gullivers-travels.json"))
    ## or you can convert them to DataFrame, and save them as any table format, like csv, excel and so on.
    entities_df, relations_df, community_reports_df = convert_to_dataframe(entities), convert_to_dataframe(relations), convert_to_dataframe(community_reports)
    entities_df.to_csv(os.path.join(graph_filepath, "Gullivers-travels-entities.csv"), index=False)
    relations_df.to_csv(os.path.join(graph_filepath, "Gullivers-travels-relationships.csv"), index=False)
    community_reports_df.to_csv(os.path.join(graph_filepath, "Gullivers-travels-communities.csv"), index=False)


    # for graph visual
    visualize_knowledge_graph_echart(entities, relations)
    visualize_knowledge_graph_network_x(entities, relations)
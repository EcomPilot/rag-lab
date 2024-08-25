from graphrag import disambiguate_entity_executor, disambiguate_relationship_executor, generate_chunk_graph_executor, generate_community_reports_executor
from graphrag.data_contracts.type import Strategy
from graphrag.llm.azure_openai import AzureOpenAILLM
from graphrag.llm.base import LLMBase
from graphrag.prompt_functions.chunk_graph_extraction import generate_entity_relationship_examples
from unstructured.partition.text import partition_text
from unstructured.chunking.basic import chunk_elements
from unstructured.cleaners.core import clean_non_ascii_chars, clean_extra_whitespace
from loguru import logger
from typing import List, Tuple
from graphrag.data_contracts.graph import Entity, Relationship
from graphrag.prompt_functions.disambiguation import merge_summary_entity, merge_summary_relationship
from graphrag.prompt_functions.expert import generate_expert
from graphrag.utils.dataclass_utils import dict2object, dict_matches_dataclass
import os
import uuid
from graphrag.utils.graph_file_loader import graph_save_json
from graphrag.utils.graph_utils import covert_virtual_relationship_to_enetity, update_readable_id
from graphrag.utils.parallel_utils import parallel_for
from graphrag.visual import visualize_knowledge_graph_echart, visualize_knowledge_graph_network_x


def chuncking_executor(filename:str, chunk_size=1000, overlap=100) -> List[str]:
    elements = partition_text(filename=filename)
    for elem in elements:
        elem.text = clean_extra_whitespace(clean_non_ascii_chars(elem.text))
    chunks = chunk_elements(elements, max_characters=chunk_size, overlap=overlap)
    return [chunk.text for chunk in chunks]


if __name__ == "__main__":
    filename = "./examples/documents/Gullivers-travels-A-Voyage-to-Lilliput.txt"
    graph_filepath = "./examples/graphfiles/Gullivers-travels-A-Voyage-to-Lilliput.json"
    AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
    AZURE_OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]
    AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]

    strategy = Strategy.accuracy
    muti_thread = 20
    aoai_llm = AzureOpenAILLM(
        model_id=AZURE_OPENAI_DEPLOYMENT,
        access_token= AZURE_OPENAI_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT
    )

    chunks = chuncking_executor(filename)
    chunk_ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
    logger.info("Generating expert descripiton...")
    expert = generate_expert(aoai_llm, chunks)
    logger.info(f"Generated expert descripiton: {expert}")
    
    relations, entities = [], []
    if muti_thread is None:
        # single thread
        for i in range(0, len(chunks)):
            current_relations, current_entities = generate_chunk_graph_executor(aoai_llm, chunks[i], chunk_ids[i], expert, strategy)
            entities.extend(current_entities)
            relations.extend(current_relations)
    else:
        # multi thread
        parallel_chunks_args_list = [(aoai_llm, chunks[i], chunk_ids[i], expert, strategy) for i in range(0, len(chunks))]
        paralled_chunks_graph_result_list = parallel_for(generate_chunk_graph_executor, parallel_chunks_args_list, num_threads=muti_thread)
        for current_entities, current_relations in paralled_chunks_graph_result_list:
            entities.extend(current_entities)
            relations.extend(current_relations)

    entities, relations = disambiguate_entity_executor(aoai_llm, entities, relations, expert, strategy)
    relations = disambiguate_relationship_executor(aoai_llm, relations, expert, strategy)
    community_reports = generate_community_reports_executor(aoai_llm, entities, relations, num_threads=3)

    # save graph to local file
    graph_save_json(entities, relations, {}, graph_filepath)

    # for graph visual
    visualize_knowledge_graph_echart(entities, relations)
    visualize_knowledge_graph_network_x(entities, relations)
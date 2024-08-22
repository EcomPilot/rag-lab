from opengraphrag.data_contracts.type import Strategy
from opengraphrag.llm.azure_openai import AzureOpenAILLM
from opengraphrag.llm.base import LLMBase
from opengraphrag.prompt_functions.chunk_graph_extraction import generate_entity_relationship_examples
from unstructured.partition.text import partition_text
from unstructured.chunking.basic import chunk_elements
from unstructured.cleaners.core import clean_non_ascii_chars, clean_extra_whitespace
from loguru import logger
from typing import List, Tuple
from opengraphrag.data_contracts.graph import Entity, Relationship
from opengraphrag.prompt_functions.disambiguation import merge_summary_entity, merge_summary_relationship
from opengraphrag.prompt_functions.expert import generate_expert
from opengraphrag.utils.dataclass_utils import dict2object, dict_matches_dataclass
import os
import uuid
from opengraphrag.utils.graph_file_loader import graph_save
from opengraphrag.utils.parallel_utils import parallel_for
from opengraphrag.visual import visualize_knowledge_graph_echart, visualize_knowledge_graph_network_x


def chuncking_executor(filename:str, chunk_size=1000, overlap=100) -> List[str]:
    elements = partition_text(filename=filename)
    for elem in elements:
        elem.text = clean_extra_whitespace(clean_non_ascii_chars(elem.text))
    chunks = chunk_elements(elements, max_characters=chunk_size, overlap=overlap)
    return [chunk.text for chunk in chunks]


def generate_chunk_graph_executor(llm: LLMBase, chunk:str, chunk_id:str="", expert:str="", strategy:Strategy = Strategy.accuracy) -> Tuple[List[Relationship], List[Entity]]:
    logger.info(f"Current chunk: {chunk}.")

    logger.info("Detecting language...")
    language = "English"
    logger.info(f"Detected language: {language}")

    logger.info("Generating entity relationship examples...")
    chunk_entity_relation = generate_entity_relationship_examples(llm, chunk, language, expert)
    logger.info("Done generating entity relationship examples")
    logger.info(f"Generating entity relationship examples: {chunk_entity_relation}")

    logger.info("Generating entity relationship classes...")
    relations, entities = [], []
    for item in chunk_entity_relation:
        if "entity_name" in item:
            entities.append(item)
        else:
            relations.append(item)
    
    relations = [dict2object(Relationship, relation) for relation in relations if dict_matches_dataclass(Relationship, relation)]
    entities = [dict2object(Entity, entity) for entity in entities if dict_matches_dataclass(Entity, entity)]
    if len(chunk_id) > 0: 
        for rel in relations: rel.source_chunk_ids.append(chunk_id)
        for en in entities: en.source_chunk_ids.append(chunk_id)
    logger.info(f"Generating entity relationship classes, entities: {entities}, relations: {relations}")
    return relations, entities


def disambiguate_entity_executor(llm: LLMBase, entities: List[Entity], expert: str='', strategy:Strategy = Strategy.accuracy) -> List[Entity]:
    logger.info(f"Current executor strategy: {strategy}")
    logger.info("Merging entity...")
    
    entities = merge_summary_entity(llm, entities, expert, strategy)
    logger.info(f"Merging the same entity name with descriptions: {entities}")
    return entities


def disambiguate_relationship_executor(llm: LLMBase, relationships: List[Relationship], expert: str='', strategy:Strategy = Strategy.accuracy) -> List[Relationship]:
    logger.info("Merging relationships...")
    relationships = merge_summary_relationship(llm, relationships, expert, strategy)
    logger.info(f"Merging relationships: {relationships}")
    return relationships


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
            relations.extend(current_relations)
            entities.extend(current_entities)
    else:
        # multi thread
        parallel_chunks_args_list = [(aoai_llm, chunks[i], chunk_ids[i], expert, strategy) for i in range(0, len(chunks))]
        paralled_chunks_graph_result_list = parallel_for(generate_chunk_graph_executor, parallel_chunks_args_list, num_threads=muti_thread)
        for current_relations, current_entities in paralled_chunks_graph_result_list:
            relations.extend(current_relations)
            entities.extend(current_entities)

    entities = disambiguate_entity_executor(aoai_llm, entities, expert, strategy)
    relations = disambiguate_relationship_executor(aoai_llm, relations, expert, strategy)

    # save graph to local file
    graph_save(entities, relations, graph_filepath)

    # for graph visual
    visualize_knowledge_graph_echart(entities, relations)
    visualize_knowledge_graph_network_x(entities, relations)
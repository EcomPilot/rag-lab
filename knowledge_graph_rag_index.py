from opengraphrag.llm.azure_openai import AzureOpenAILLM
from opengraphrag.llm.base import LLMBase
from opengraphrag.prompt_functions.chunk_graph_extraction import generate_entity_relationship_examples
from unstructured.partition.text import partition_text
from unstructured.chunking.basic import chunk_elements
from unstructured.cleaners.core import clean_non_ascii_chars, clean_extra_whitespace
from loguru import logger
from typing import List, Tuple
from opengraphrag.data_contracts.graph import Entity, Relationship
from opengraphrag.prompt_functions.disambiguation import disambiguate_entity_type, merge_summary_entity, merge_summary_relationship
from opengraphrag.utils.chunk_executer import flatten_dict_list, get_entity_types_mapping, merge_entity_types
from opengraphrag.utils.dataclass_utils import dict_matches_dataclass
import os
from opengraphrag.visual import visualize_knowledge_graph_echart, visualize_knowledge_graph_network_x


def chuncking_executor(filename:str, chunk_size=1000, overlap=100) -> List[str]:
    elements = partition_text(filename=filename)
    for elem in elements:
        elem.text = clean_extra_whitespace(clean_non_ascii_chars(elem.text))
    chunks = chunk_elements(elements, max_characters=chunk_size, overlap=overlap)
    return [chunk.text for chunk in chunks]


def chunk_graph_executor(llm: LLMBase, chunk:str) -> Tuple[List[Relationship], List[Entity]]:
    logger.info(f"Current chunk: {chunk}.")
    
    # logger.info("Generating expert descripiton...")
    # expert = generate_expert(llm, chunk)
    # logger.info(f"Generated expert descripiton: {expert}")

    logger.info("Detecting language...")
    language = "English"
    logger.info(f"Detected language: {language}")

    logger.info("Generating entity relationship examples...")
    chunk_entity_relation = generate_entity_relationship_examples(llm, chunk, language)
    logger.info("Done generating entity relationship examples")
    logger.info(f"Generating entity relationship examples: {chunk_entity_relation}")

    logger.info("Generating entity relationship classes...")
    relations, entities = [], []
    for item in chunk_entity_relation:
        if "entity_name" in item:
            entities.append(item)
        else:
            relations.append(item)
    
    relations = [Relationship(**relation) for relation in relations if dict_matches_dataclass(Relationship, relation)]
    entities = [Entity(**entity) for entity in entities if dict_matches_dataclass(Entity, entity)]
    logger.info(f"Generating entity relationship classes, entities: {entities}, relations: {relations}")
    return relations, entities


def disambiguation_entity(llm: LLMBase, entities: List[Entity]) -> List[Entity]:
    logger.info("Merging entity types...")
    entity_type_dict = get_entity_types_mapping(entities)
    merged_entity_types = disambiguate_entity_type(llm, list(entity_type_dict.keys()))
    logger.info(f"Merging entity types: {merged_entity_types}")

    entity_type_dict = merge_entity_types(entity_type_dict, merged_entity_types)
    logger.info(f"Merging entity mapping: {entity_type_dict}")

    entity_type_dict = merge_summary_entity(llm, entity_type_dict)
    logger.info(f"Merging the same entity name with descriptions: {entity_type_dict}")
    return flatten_dict_list(entity_type_dict)


def disambiguation_relationship(llm: LLMBase, relationships: List[Relationship]) -> List[Relationship]:
    logger.info("Merging relationships...")
    relationships = merge_summary_relationship(llm, relationships)
    logger.info(f"Merging relationships: {relationships}")
    return relationships


if __name__ == "__main__":
    filename = "./examples/documents/Gullivers-travels-A-Voyage-to-Lilliput.txt"
    AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
    AZURE_OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]
    AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]

    aoai_llm = AzureOpenAILLM(
        model_id=AZURE_OPENAI_DEPLOYMENT,
        access_token= AZURE_OPENAI_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT
    )
    chunks = chuncking_executor(filename)
    relations, entities = [], []
    for chunk in chunks[0:7]:
        current_relations, current_entities = chunk_graph_executor(aoai_llm, chunk)
        relations.extend(current_relations)
        entities.extend(current_entities)

    entities = disambiguation_entity(aoai_llm, entities)
    relations = disambiguation_relationship(aoai_llm, relations)
    # visualize_knowledge_graph_network_x(entities, relations)
    visualize_knowledge_graph_echart(entities, relations)

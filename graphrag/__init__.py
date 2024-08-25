from typing import List, Tuple
from communities.algorithms import louvain_method
import networkx as nx
from loguru import logger
from graphrag.data_contracts.graph import Community, Entity, Relationship
from graphrag.data_contracts.type import Strategy
from graphrag.llm.base import LLMBase
from graphrag.prompt_functions.chunk_graph_extraction import generate_entity_relationship_examples
from graphrag.prompt_functions.community import generate_community_report
from graphrag.prompt_functions.disambiguation import merge_summary_entity, merge_summary_relationship
from graphrag.utils.dataclass_utils import dict2object, dict_matches_dataclass
from graphrag.utils.graph_network_x_utils import convert_to_network_x_graph
from graphrag.utils.graph_utils import covert_virtual_relationship_to_enetity, update_readable_id
from graphrag.utils.parallel_utils import parallel_for


def generate_chunk_graph_executor(llm: LLMBase, chunk:str, chunk_id:str="", expert:str="", strategy:Strategy = Strategy.accuracy) -> Tuple[List[Entity], List[Relationship]]:
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
    return entities, relations


def disambiguate_entity_executor(llm: LLMBase, entities: List[Entity], relationships: List[Relationship], expert: str='', strategy:Strategy = Strategy.accuracy) -> Tuple[List[Entity], List[Relationship]]:
    logger.info(f"Current executor strategy: {strategy}")
    logger.info("Merge Relationship that do not have correct target or source entity to Entity...")
    entities, relationships = covert_virtual_relationship_to_enetity(entities, relationships)
    logger.info(f"Merging the same entity name with descriptions...")
    entities = merge_summary_entity(llm, entities, expert, strategy)
    logger.info(f"Merging the same entity name with descriptions: {entities}")

    logger.info("Update readable Id in Entities and Relationships...")
    entities, relationships = update_readable_id(entities), update_readable_id(relationships)
    logger.info("Update readable Id in relationships")
    return entities, relationships


def disambiguate_relationship_executor(llm: LLMBase, relationships: List[Relationship], expert: str='', strategy:Strategy = Strategy.accuracy) -> List[Relationship]:
    logger.info("Merging relationships...")
    relationships = merge_summary_relationship(llm, relationships, expert, strategy)
    logger.info(f"Merging relationships: {relationships}")

    logger.info("Update readable Id in relationships...")
    relationships = update_readable_id(relationships)
    logger.info("Update readable Id in relationships")
    return relationships


def generate_community_reports_executor(llm: LLMBase, entities: List[Entity], relationships: List[Relationship], expert: str='', strategy:Strategy = Strategy.accuracy, min_entities_in_cummunity:int=5, num_threads:int = 1) -> List[Community]:
    def __multi_thread_loop_generate_community_report(llm: LLMBase, entities: List[Entity], relationships: List[Relationship], community_idx:List[int], expert: str=''):
        logger.info(f"Creating community report...")
        com_entities = [entities[i] for i in community_idx]
        com_entity_set = {entity.entity_name for entity in com_entities}
        com_rels = [rel for rel in relationships if (rel.target_entity in com_entity_set) or (rel.source_entity in com_entity_set)]
        report = generate_community_report(llm, com_entities, com_rels, 'English', expert=expert)
        logger.info(f"Created community report: {report}")
        report = dict2object(Community, report) if dict_matches_dataclass(Community, report) else None
        logger.info(f"Convert community report: {report}")
        return report
    
    logger.info("Creating communities...")
    G = convert_to_network_x_graph(entities, relationships)
    adj_matrix = nx.to_numpy_array(G)
    communities, _ = louvain_method(adj_matrix)
    logger.info("Created communities")

    logger.info(f"Selecting communities which large than {min_entities_in_cummunity}...")
    community_function_args_list = [(llm, entities, relationships, com, expert) for com in communities if len(com) >= min_entities_in_cummunity]
    logger.info(f"Selected communities which large than {min_entities_in_cummunity}")

    logger.info(f"Creating community report with threads {num_threads}")
    community_reports = parallel_for(__multi_thread_loop_generate_community_report, community_function_args_list, num_threads=num_threads)
    return [report for report in community_reports if report is not None]
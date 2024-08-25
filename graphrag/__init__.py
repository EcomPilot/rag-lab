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
from graphrag.prompt_functions.expert import generate_expert
from graphrag.prompt_functions.language import detect_text_language


def generate_single_chunk_graph_executor(llm: LLMBase, chunk:str, chunk_id:str="", expert:str="", language:str="English", strategy:Strategy = "accuracy") -> Tuple[List[Entity], List[Relationship]]:
        '''
        The `generate_single_chunk_graph_executor` function is designed to generate entity and relationship classes from a given text chunk.

        #### Parameters
        - `llm: LLMBase`: An instance of a language model used for generating entity and relationship examples.
        - `chunk: str`: The text chunk to be analyzed.
        - `chunk_id: str` (default is an empty string): An optional identifier for the text chunk.
        - `expert: str` (default is an empty string): An optional expert input for generating entity and relationship examples.
        - `language: str` (default is "English"): The language of the text chunk.
        - `strategy: Strategy` (default is "accuracy"): The strategy to be used for generating entity and relationship examples.

        #### Returns
        - `Tuple[List[Entity], List[Relationship]]`: A tuple containing a list of entities and a list of relationships.
        '''
        strategy = Strategy(strategy)
        logger.info(f"Current chunk: {chunk}.")
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


def generate_entire_chunk_graph_executor(llm: LLMBase, chunks:List[str], chunk_ids:List[str], expert:str="", language:str="English", strategy:Strategy = "accuracy", num_threads:int=1) -> Tuple[List[Entity], List[Relationship]]:
    '''
    The `generate_entire_chunk_graph_executor` function is designed to generate entity and relationship classes from multiple text chunks, utilizing either single-threaded or multi-threaded execution.

    #### Parameters
    - `llm: LLMBase`: An instance of a language model used for generating entity and relationship examples.
    - `chunks: List[str]`: A list of text chunks to be analyzed.
    - `chunk_ids: List[str]`: A list of identifiers corresponding to each text chunk.
    - `expert: str` (default is an empty string): An optional expert input for generating entity and relationship examples.
    - `language: str` (default is "English"): The language of the text chunks.
    - `strategy: Strategy` (default is "accuracy"): The strategy to be used for generating entity and relationship examples.
    - `num_threads: int` (default is 1): The number of threads to use for processing the text chunks.

    #### Returns
    - `Tuple[List[Entity], List[Relationship]]`: A tuple containing a list of entities and a list of relationships.
    '''
    strategy = Strategy(strategy)
    logger.info(f"Creating Graphs from chunks with thread {num_threads}...")
    entities, relations = [], []
    if num_threads == 1:
        # single thread
        for i in range(0, len(chunks)):
            current_entities, current_relations = generate_single_chunk_graph_executor(llm, chunks[i], chunk_ids[i], expert, language, strategy)
            entities.extend(current_entities)
            relations.extend(current_relations)
    else:
        # multi thread
        parallel_chunks_args_list = [(llm, chunks[i], chunk_ids[i], expert, language, strategy) for i in range(0, len(chunks))]
        paralled_chunks_graph_result_list = parallel_for(generate_single_chunk_graph_executor, parallel_chunks_args_list, num_threads=num_threads)
        for current_entities, current_relations in paralled_chunks_graph_result_list:
            entities.extend(current_entities)
            relations.extend(current_relations)
    logger.info("Created Graphs from chunks...")
    return entities, relations


def disambiguate_entity_executor(llm: LLMBase, entities: List[Entity], relationships: List[Relationship], expert: str='', language:str="English", strategy:Strategy = "accuracy") -> Tuple[List[Entity], List[Relationship]]:
    '''
    The `disambiguate_entity_executor` function is designed to merge and disambiguate entities and relationships, ensuring they have readable IDs.

    #### Parameters
    - `llm: LLMBase`: An instance of a language model used for merging and disambiguating entities and relationships.
    - `entities: List[Entity]`: A list of entities to be processed.
    - `relationships: List[Relationship]`: A list of relationships to be processed.
    - `expert: str` (default is an empty string): An optional expert input for merging entities and relationships.
    - `language: str` (default is "English"): The language of the entities and relationships.
    - `strategy: Strategy` (default is "accuracy"): The strategy to be used for merging and disambiguating entities and relationships.

    #### Returns
    - `Tuple[List[Entity], List[Relationship]]`: A tuple containing a list of disambiguated entities and a list of disambiguated relationships.
    '''
    strategy = Strategy(strategy)
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


def disambiguate_relationship_executor(llm: LLMBase, relationships: List[Relationship], expert: str='', language:str="English", strategy:Strategy = "accuracy") -> List[Relationship]:
    '''
    The `disambiguate_relationship_executor` function is designed to merge and disambiguate relationships, ensuring they have readable IDs.

    #### Parameters
    - `llm: LLMBase`: An instance of a language model used for merging and disambiguating relationships.
    - `relationships: List[Relationship]`: A list of relationships to be processed.
    - `expert: str` (default is an empty string): An optional expert input for merging relationships.
    - `language: str` (default is "English"): The language of the relationships.
    - `strategy: Strategy` (default is "accuracy"): The strategy to be used for merging and disambiguating relationships.

    #### Returns
    - `List[Relationship]`: A list of disambiguated relationships with updated readable IDs.
    '''
    strategy = Strategy(strategy)
    logger.info("Merging relationships...")
    relationships = merge_summary_relationship(llm, relationships, expert, strategy)
    logger.info(f"Merging relationships: {relationships}")

    logger.info("Update readable Id in relationships...")
    relationships = update_readable_id(relationships)
    logger.info("Update readable Id in relationships")
    return relationships


def generate_community_reports_executor(llm: LLMBase, entities: List[Entity], relationships: List[Relationship], expert: str='', language:str="English", strategy:Strategy = "accuracy", min_entities_in_cummunity:int=5, num_threads:int = 1) -> List[Community]:
    '''
    The `generate_community_reports_executor` function is designed to generate community reports from a list of entities and relationships, utilizing either single-threaded or multi-threaded execution.

    #### Parameters
    - `llm: LLMBase`: An instance of a language model used for generating community reports.
    - `entities: List[Entity]`: A list of entities to be analyzed.
    - `relationships: List[Relationship]`: A list of relationships to be analyzed.
    - `expert: str` (default is an empty string): An optional expert input for generating community reports.
    - `language: str` (default is "English"): The language of the entities and relationships.
    - `strategy: Strategy` (default is "accuracy"): The strategy to be used for generating community reports.
    - `min_entities_in_cummunity: int` (default is 5): The minimum number of entities required in a community.
    - `num_threads: int` (default is 1): The number of threads to use for processing the communities.

    #### Returns
    - `List[Community]`: A list of generated community reports.
    '''
    def __multi_thread_loop_generate_community_report(llm: LLMBase, entities: List[Entity], relationships: List[Relationship], community_idx:List[int], expert: str=''):
        logger.info(f"Creating community report...")
        com_entities = [entities[i] for i in community_idx]
        com_entity_set = {entity.entity_name for entity in com_entities}
        com_rels = [rel for rel in relationships if (rel.target_entity in com_entity_set) or (rel.source_entity in com_entity_set)]
        report = generate_community_report(llm, com_entities, com_rels, language, expert=expert)
        logger.info(f"Created community report: {report}")
        if dict_matches_dataclass(Community, report):
            report = dict2object(Community, report)
            report.source_entity_ids = [en.entity_id for en in com_entities]
            report.source_relationship_ids = [rel.relationship_id for rel in com_rels]
        else:
            report = None
        logger.info(f"Convert community report: {report}")
        return report
    
    strategy = Strategy(strategy)
    logger.info("Creating communities...")
    G = convert_to_network_x_graph(entities, relationships)
    adj_matrix = nx.to_numpy_array(G)
    communities, _ = louvain_method(adj_matrix)
    logger.info("Created communities")

    logger.info(f"Selecting communities which large than {min_entities_in_cummunity}...")
    communities = [com for com in communities if len(com) >= min_entities_in_cummunity]
    logger.info(f"Selected communities which large than {min_entities_in_cummunity}")

    logger.info(f"Creating community report with threads {num_threads}")
    if num_threads == 1:
        community_reports = [__multi_thread_loop_generate_community_report(llm, entities, relationships, com, expert) for com in communities]
    else:
        community_function_args_list = [(llm, entities, relationships, com, expert) for com in communities]
        community_reports = parallel_for(__multi_thread_loop_generate_community_report, community_function_args_list, num_threads=num_threads)
    return [report for report in community_reports if report is not None]


__all__ = [
    "generate_community_reports_executor",
    "disambiguate_relationship_executor",
    "disambiguate_entity_executor",
    "disambiguate_relationship_executor",
    "generate_entire_chunk_graph_executor",
    "generate_single_chunk_graph_executor",
    "detect_text_language",
    "generate_expert",
]

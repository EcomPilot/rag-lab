from typing import List
from raglab.graphrag import convert_to_dataframe
import numpy as np
import pandas as pd
from loguru import logger
from raglab.graphrag.data_contracts import Entity, Relationship, Community
from raglab.graphrag.prompt.search import SIMPLE_SEARCH_PROMPT


def cosine_similarity(a: List[float], b: List[float]) -> float:
    '''
    This function calculates the cosine similarity between two vectors.

    ### Parameters

    - `a` (`List[float]`): The first vector.
    - `b` (`List[float]`): The second vector.

    ### Returns

    - `float`: The cosine similarity between the two vectors.
    '''
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def select_entities(query_embed:List[float], entities: List[Entity], num_select=5) -> List[Entity]:
    '''
    This function selects a specified number of entities based on their cosine similarity to a given query embedding.

    ### Parameters

    - `query_embed` (`List[float]`): The embedding of the query.
    - `entities` (`List[Entity]`): A list of entities to be evaluated.
    - `num_select` (`int`, optional): The number of entities to select. Default is 5.

    ### Returns

    - `List[Entity]`: A list of the selected entities with the highest cosine similarity to the query embedding.
    '''
    entities_cosine_similarity = [cosine_similarity(entity.embedding, query_embed) for entity in entities]
    selected_entity_indexes = np.argsort(entities_cosine_similarity)[-num_select:]
    selected_entity = [entities[i] for i in selected_entity_indexes]
    return selected_entity

def select_relations(selected_entity: List[Entity], relations: List[Relationship]) -> List[Relationship]:
    '''
    ## `select_relations`

    This function selects relationships that involve any of the specified entities.

    ### Parameters

    - `selected_entity` (`List[Entity]`): A list of entities to be considered.
    - `relations` (`List[Relationship]`): A list of relationships to be evaluated.

    ### Returns

    - `List[Relationship]`: A list of relationships where either the source entity or the target entity is in the list of selected entities.
    '''
    selected_entity_set = {entity.entity_name for entity in selected_entity}
    selected_relations = [rel for rel in relations if (rel.source_entity in selected_entity_set) or (rel.target_entity in selected_entity_set)]
    return selected_relations

def select_community(query_embed:List[float], selected_entity: List[Entity], communities: List[Community]) -> Community | None:
    '''
    This function selects a community based on the cosine similarity of its embedding to a given query embedding and the involvement of selected entities.

    ### Parameters

    - `query_embed` (`List[float]`): The embedding of the query.
    - `selected_entity` (`List[Entity]`): A list of selected entities.
    - `communities` (`List[Community]`): A list of communities to be evaluated.

    ### Returns

    - `Community | None`: The community with the highest cosine similarity to the query embedding if multiple communities are found, the single matching community if only one is found, or `None` if no matching community is found.
    '''
    selected_entity_id_set = {entity.entity_id for entity in selected_entity}
    selected_communities = [com for com in communities if any(id in selected_entity_id_set for id in com.source_entity_ids)]
    if len(selected_communities) > 1:
        communities_cosine_similarity = [cosine_similarity(com.embedding, query_embed) for com in selected_communities]
        selected_commnity = selected_communities[np.argsort(communities_cosine_similarity)[-1]]
    elif len(selected_communities) == 1:
        selected_commnity = selected_communities
    else:
        selected_commnity = None
    return selected_commnity

def generate_final_answer_prompt(query:str, selected_entity:List[Entity], selected_relations:List[Relationship], selected_commnity:Community) -> str:
    '''
    This function generates a final answer prompt based on the query, selected entities, selected relationships, and a selected community.

    ### Parameters

    - `query` (`str`): The search query.
    - `selected_entity` (`List[Entity]`): A list of selected entities.
    - `selected_relations` (`List[Relationship]`): A list of selected relationships.
    - `selected_commnity` (`Community`): The selected community.

    ### Returns

    - `str`: The generated prompt containing the query, entity table, relationship table, and community report.
    '''
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
        communtiy_report=selected_commnity.summary if selected_commnity else "The current query has no related report."
    )
    return prompt
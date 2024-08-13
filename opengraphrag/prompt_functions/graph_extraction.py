from typing import List
import random
from opengraphrag.llm.base import LLMBase
from opengraphrag.prompt.graph_extraction import ENTITY_RELATIONSHIPS_GENERATION_PROMPT, ENTITY_TYPE_GENERATION_PROMPT
from opengraphrag.prompt.topic import GENERATE_TOPIC_PROMPT
from opengraphrag.prompt.expert import GENERATE_EXPERT_PROMPT


def generate_topic(llm: LLMBase, docs: str | List[str], k=1) -> str:
    """Generate an LLM persona to use for GraphRAG prompts.

    Parameters
    ----------
    - llm (CompletionLLM): The LLM to use for generation
    - docs (str | list[str]): The domain to generate a persona for

    Returns
    -------
    - str: The generated domain prompt response.
    """
    docs_str = "\n".join(random.choices(docs, k=k)) if isinstance(docs, list) else docs
    domain_prompt = GENERATE_TOPIC_PROMPT.format(input_text=docs_str)
    response = llm.invoke(domain_prompt)
    return response


def generate_expert(llm: LLMBase, topic:str):
    """Generate an LLM persona to use for GraphRAG prompts.

    Parameters
    ----------
    - llm (CompletionLLM): The LLM to use for generation
    - domain (str): The domain to generate a persona for
    - task (str): The task to generate a persona for. Default is DEFAULT_TASK
    """
    expert_prompt = GENERATE_EXPERT_PROMPT.format(topic=topic)
    return llm.invoke(expert_prompt)


def generate_entity_types(llm: LLMBase, topic: str, expert: str, chunk: str) -> str:
    """
    Generate entity type categories from a given set of (small) documents.

    Example Output:
    ['military unit', 'organization', 'person', 'location', 'event', 'date', 'equipment']
    """
    return llm.invoke(ENTITY_TYPE_GENERATION_PROMPT.format(input_text=chunk, topic=topic, expert=expert))


def generate_entity_relationship_examples(llm: LLMBase, entity_types: str, chunk:str, language:str) -> List[str]:
    """Generate a list of entity/relationships examples for use in generating an entity configuration.
    Will return entity/relationships examples as either JSON or in tuple_delimiter format depending
    """
    return llm.invoke(ENTITY_RELATIONSHIPS_GENERATION_PROMPT.format(entity_types=entity_types, input_text=chunk, language=language))
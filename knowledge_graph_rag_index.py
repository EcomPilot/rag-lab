from opengraphrag.llm.azure_openai import AzureOpenAILLM
from opengraphrag.llm.base import LLMBase
from opengraphrag.prompt_functions.graph_extraction import (
    generate_entity_relationship_examples, 
    generate_topic, generate_expert, 
    generate_entity_types
)
from unstructured.partition.text import partition_text
from unstructured.chunking.basic import chunk_elements
from unstructured.cleaners.core import clean_non_ascii_chars, clean_extra_whitespace
from loguru import logger
from typing import List
import os


def chuncking_executor(filename:str, chunk_size=800, overlap=100) -> List[str]:
    elements = partition_text(filename=filename)
    for elem in elements:
        elem.text = clean_extra_whitespace(clean_non_ascii_chars(elem.text))
    chunks = chunk_elements(elements, max_characters=chunk_size, overlap=overlap)
    return [chunk.text for chunk in chunks]


def indexing_executor(llm: LLMBase, chunk:str):
    logger.info(f"Current chunk: {chunk}.")

    logger.info("Generating topic...")
    topic = generate_topic(llm, chunk)
    logger.info(f"Generated topic: {topic}")

    logger.info("Generating expert descripiton...")
    expert = generate_expert(llm, topic)
    logger.info(f"Generated expert descripiton: {expert}")

    logger.info("Detecting language...")
    language = "English"
    logger.info(f"Detected language: {language}")

    logger.info("Generating entity types")
    entity_types = generate_entity_types(llm, topic, expert, chunk)
    logger.info(f"Generated entity types: {entity_types}")

    logger.info("Generating entity relationship examples...")
    example = generate_entity_relationship_examples(llm, entity_types, chunk, language)
    logger.info("Done generating entity relationship examples")
    logger.info(f"Generating entity relationship examples: {example}")

    # logger.info("Generating entity extraction prompt...")
    # output = create_entity_extraction_prompt(llm, entity_types, chunk, example, language)
    # logger.info(f"Generated entity extraction prompt, stored in folder {output}")


if __name__ == "__main__":
    filename = "./examples/documents/Gullivers-travels-A-Voyage-to-Lilliput.txt"
    AZURE_OPENAI_DEPLOYMENT = os.environ["gpt-35-turbo-16k"]
    AZURE_OPENAI_KEY = os.environ["AZURE_OPENAI_KEY"]
    AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]

    aoai_llm = AzureOpenAILLM(
        model_id=AZURE_OPENAI_DEPLOYMENT,
        access_token= AZURE_OPENAI_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT
    )
    chunks = chuncking_executor(filename)
    indexing_executor(aoai_llm, chunks[-1])
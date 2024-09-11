# RAG-LAB

<div align="left">
  <a href="https://pypi.org/project/raglab2/">
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/raglab2">
  </a>
  <a href="https://pypi.org/project/raglab2/">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/raglab2">
  </a>
  <a href="https://github.com/EcomPilot/rag-lab/issues">
    <img alt="GitHub Issues" src="https://img.shields.io/github/issues/EcomPilot/rag-lab">
  </a>
  <a href="https://github.com/EcomPilot/rag-lab/discussions">
    <img alt="GitHub Discussions" src="https://img.shields.io/github/discussions/EcomPilot/rag-lab">
  </a>
  <a href="https://github.com/EcomPilot/rag-lab/graphs/contributors">
    <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/EcomPilot/rag-lab">
  </a>
</div>

RAG-LAB is an open-source lighter, faster and cheaper RAG toolkit supported by [**TargetPilot**](https://admin.targetpilot.ai/login), designed to transform the latest RAG concepts into stable and practical engineering tools. The project currently supports **GraphRAG** and **HybridRAG**. **[Welcome to star our RAG-Lab!](https://github.com/EcomPilot/rag-lab)** 

**To install: `pip install raglab2`**

## About TargetPilot

[TargetPilot](https://admin.targetpilot.ai/login) is a company focused on empowering the e-commerce sector with artificial intelligence. TargetPilot OnlineAssistant has an industry leading RAG technology solution, feel free to click on the link.

## Goals

The primary goal of RAG-LAB is to explore the latest RAG technologies and convert them into the most stable engineering tools. We aim to:

- **Lighter**: Use **pure Python** to design tools specifically for RAG functionality without integrating unnecessary third-party packages (text chunker, LLM integration, etc. can be done using Unstructured, Langchain, LlamaIndex, etc., or **the simplified text chunker functions we provide**).
- **Faster**: Multiple threads can be selected for acceleration.
- **Cheaper**: Focus on **low-cost development** and achieve the **best functionality** with minimal LLM token consumption.
- **Innovate**: Continuously integrate the latest research and advancements in RAG.

## Features

### GraphRAG (Welcome to try!)

Proposed by Microsoft, GraphRAG integrates graph-based approaches into RAG, offering several key advantages:

- **Enhanced Data Relationships**: By leveraging graph structures, GraphRAG can better capture and utilize the relationships between different data points, leading to more accurate and insightful results.
- **Scalability**: GraphRAG is designed to handle large-scale data efficiently, making it suitable for applications with extensive datasets.
- **Flexibility**: The graph-based approach allows for more flexible data modeling, accommodating complex and dynamic data structures.
- **Improved Query Performance**: GraphRAG can optimize query performance by efficiently navigating through the graph, reducing the time required to retrieve relevant information.

### HybridRAG (In Progress)

Proposed by Intel, HybridRAG combines different RAG methodologies to enhance performance and flexibility. Its advantages include:

- **Versatility**: HybridRAG integrates multiple RAG techniques, allowing it to adapt to various types of data and use cases.
- **Performance Optimization**: By combining the strengths of different RAG methods, HybridRAG can achieve higher performance and accuracy in data retrieval and analysis.
- **Robustness**: The hybrid approach ensures that the system remains robust and reliable, even when dealing with diverse and complex datasets.
- **Customizability**: Users can customize HybridRAG to fit specific requirements, making it a versatile tool for a wide range of applications.

## Quick Start Guide

This quick start guide walks you through the process of chunking text, generating expert descriptions, detecting language, creating and disambiguating entity and relationship graphs, generating community reports, saving the graph to a file, and visualizing the knowledge graph. Follow these steps to efficiently process and visualize your data.

For your reference, you can find the code example in:
- Graph indexing: [quick_start_index.py](./examples/quick_start_index.py).
- Searh: [quick_start_search.py](./examples/quick_start_search.py). **In fact, you can implement the SEARCH part of the code according to the [searching function example](./raglab/graphrag/search_functions/example.py), following the examples we have given and the instructions for each step. This will allow you to use the graph to accommodate more databases and to achieve higher performance searches.**

### Step-by-Step Instructions (Indexing)
0. **Import tools from `raglab`**
    ```python
    from raglab.graphrag import (
        disambiguate_entity_executor, 
        disambiguate_relationship_executor, 
        generate_community_reports_executor, 
        generate_entire_chunk_graph_executor,
        detect_text_language,
        generate_expert,
        graph_save_json,
    )
    from raglab.graphrag.visual import (
        visualize_knowledge_graph_echart,
        visualize_knowledge_graph_network_x
    )

    # the fast and light text spilter with regex, which is powered by JinaAI. You can explore it in https://jina.ai/segmenter/
    # Also you can use Unstructured, Langchain, LlamaIndex to replace it.
    from raglab.chunk import (
        chuncking_executor, # for English
        character_chunking_executor # for languages exclude English
    )

    # import llm from `raglab.llms` or `langchain.llms`.
    # Or You can implement the `llm.invoke` method yourself by inheriting the `LLMBase` class.
    from raglab.llms import (
        AzureOpenAILLM,
        LLMBase
    )

    # Also, you can implement the `embed.embed_query` method yourself by inheriting the `EmbeddingBase` class. Or just import it from `raglab.embeddings` or `langchain.embeddings`
    from raglab.embeddings import (
        AzureOpenAIEmbedding, 
        EmbeddingBase
    )
    ```


1. **Chunking the Text**

    the fast and light text spilter with regex, which is powered by JinaAI. You can explore it in https://jina.ai/segmenter/
    ```python
    # for English, you can use the function `chuncking_executor`
    chunks = chuncking_executor(text=entire_document, max_chunk_size=1000, remove_line_breaks=True)
    chunk_ids = [str(uuid.uuid4()) for _ in range(len(chunks))]

    # for Chinese, you can use the function `chuncking_executor`
    chunks = character_chunking_executor(text=entire_document, max_chunk_size=500, remove_line_breaks=True)
    ```

2. **[Options] Generating Expert Description**
    ```python
    expert = generate_expert(aoai_llm, chunks)
    ```

3. **[Options] Detecting Language**
    ```python
    language = detect_text_language(aoai_llm, chunks)
    ```

4. **Generating Entity and Relationship Graph**
    ```python
    entities, relations = generate_entire_chunk_graph_executor(aoai_llm, chunks, chunk_ids, expert, language, strategy, muti_thread)
    ```

5. **Disambiguating Entities and Relationships**
    ```python
    entities, relations = disambiguate_entity_executor(aoai_llm, entities, relations, expert, language, strategy)
    relations = disambiguate_relationship_executor(aoai_llm, relations, expert, language, strategy)
    ```

6. **Generating Community Reports**
    ```python
    community_reports = generate_community_reports_executor(aoai_llm, entities, relations, expert, language, strategy, 5, muti_thread)
    ```

7. **Generating Embeddings for Entities and Communities**
    ```python
    entities = update_graph_embeddings_executor(aoai_embed, entities, num_threads=muti_thread)
    community_reports = update_graph_embeddings_executor(aoai_embed, community_reports, num_threads=muti_thread)
    ```

8. **Saving the Graph to a Local File**
    ```python
    ## save graph to local as json file
    graph_save_json(entities, relations, community_reports, os.path.join(graph_filepath, "Gullivers-travels.json"))
    ## or you can convert them to DataFrame, and save them as any table format, like csv, excel and so on.
    entities_df, relations_df, community_reports_df = convert_to_dataframe(entities), convert_to_dataframe(relations), convert_to_dataframe(community_reports)
    entities_df.to_csv(os.path.join(graph_filepath, "Gullivers-travels-entities.csv"), index=False)
    relations_df.to_csv(os.path.join(graph_filepath, "Gullivers-travels-relationships.csv"), index=False)
    community_reports_df.to_csv(os.path.join(graph_filepath, "Gullivers-travels-communities.csv"), index=False)
    ```

9. **[Options] Visualizing the Knowledge Graph**
    ```python
    visualize_knowledge_graph_echart(entities, relations)
    visualize_knowledge_graph_network_x(entities, relations)
    ```

### Step-by-Step Instructions (Search)

0. **Import search tools from `raglab`**
    ```python
    from raglab.graphrag import (
        graph_load_json
    )
    from raglab.graphrag.search_functions import (
        generate_final_answer_prompt,
        select_community,
        select_entities,
        select_relations
    )

    # import llm from `raglab.llms` or `langchain.llms`.
    # Or You can implement the `llm.invoke` method yourself by inheriting the `LLMBase` class.
    from raglab.llms import AzureOpenAILLM

    # Also, you can implement the `embed.embed_query` method yourself by inheriting the `EmbeddingBase` class. Or just import it from `raglab.embeddings` or `langchain.embeddings`
    from raglab.embeddings import AzureOpenAIEmbedding
    ```

1. **Load graph objects**
    ```python
    graph_filepath = "./examples/graphfiles/Gullivers-travels.json"
    entities, relations, communities = graph_load_json(graph_filepath)
    entity_select_num = 5
    ```

2. **Embed the query and select the most similar search entities**
    ```python
    query = "Who is the king of Lilliput?"
    query_embed = aoai_embed.embed_query(query)
    selected_entity = select_entities(query_embed, entities)
    ```

3. **Select all relationships from selected entities**
    ```python
    selected_relations = select_relations(selected_entity, relations)
    ```

4. **Select correct community from selected entities**
    ```python
    selected_commnity = select_community(query_embed, selected_entity, communities)
    ```

5. **Generate the final answer**
    ```python
    prompt = generate_final_answer_prompt(query, selected_entity, selected_relations, selected_commnity)
    final_answer = aoai_llm.invoke(prompt)
    print(f"Final answer: {final_answer}")
    ```

## Contributing

We welcome contributions from the community. 

## License

This project is licensed under the [Apache 2.0 License](./LICENSE).

## Contact

For more information, please contact us at pxgong@targetpilot.ai, vincentpo@targetpilot.ai.


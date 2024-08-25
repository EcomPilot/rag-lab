# RAG-LAB

RAG-LAB is an open-source RAG toolkit supported by [**Target Pilot**](https://www.targetpilot.ai/en), designed to transform the latest RAG concepts into stable and practical engineering tools. The project currently supports **GraphRAG** and **HybridRAG**.

## About Target Pilot

[Target Pilot](https://www.targetpilot.ai/en) is a company focused on empowering the e-commerce sector with artificial intelligence.

## Goals

The primary goal of RAG-LAB is to explore the latest RAG technologies and convert them into the most stable engineering tools. We aim to:

- **Innovate**: Continuously integrate the latest research and advancements in RAG.
- **Stabilize**: Ensure that the tools are reliable and robust for real-world applications.

## Features

### GraphRAG

Proposed by Microsoft, GraphRAG integrates graph-based approaches into RAG, offering several key advantages:

- **Enhanced Data Relationships**: By leveraging graph structures, GraphRAG can better capture and utilize the relationships between different data points, leading to more accurate and insightful results.
- **Scalability**: GraphRAG is designed to handle large-scale data efficiently, making it suitable for applications with extensive datasets.
- **Flexibility**: The graph-based approach allows for more flexible data modeling, accommodating complex and dynamic data structures.
- **Improved Query Performance**: GraphRAG can optimize query performance by efficiently navigating through the graph, reducing the time required to retrieve relevant information.

### HybridRAG

Proposed by Intel, HybridRAG combines different RAG methodologies to enhance performance and flexibility. Its advantages include:

- **Versatility**: HybridRAG integrates multiple RAG techniques, allowing it to adapt to various types of data and use cases.
- **Performance Optimization**: By combining the strengths of different RAG methods, HybridRAG can achieve higher performance and accuracy in data retrieval and analysis.
- **Robustness**: The hybrid approach ensures that the system remains robust and reliable, even when dealing with diverse and complex datasets.
- **Customizability**: Users can customize HybridRAG to fit specific requirements, making it a versatile tool for a wide range of applications.

## Quick Start Guide

This quick start guide walks you through the process of chunking text, generating expert descriptions, detecting language, creating and disambiguating entity and relationship graphs, generating community reports, saving the graph to a file, and visualizing the knowledge graph. Follow these steps to efficiently process and visualize your data.

For your reference, you can find the code example in [quick_start_main.py](./examples/quick_start_main.py)

### Step-by-Step Instructions
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
    ```python
    chunks = chuncking_executor(filename)
    chunk_ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
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
    graph_save_json(entities, relations, community_reports, graph_filepath)
    ```

9. **Visualizing the Knowledge Graph**
    ```python
    visualize_knowledge_graph_echart(entities, relations)
    visualize_knowledge_graph_network_x(entities, relations)
    ```

## Contributing

We welcome contributions from the community. Please read our contributing guidelines for more details.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For more information, please contact us at contact@targetpilot.com.


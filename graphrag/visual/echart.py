from typing import List
from graphrag.data_contracts.graph import Entity, Relationship
import pyecharts.options as opts
from pyecharts.charts import Graph
from pyecharts.globals import ThemeType


def visualize_knowledge_graph_echart(entities: List[Entity], relationships: List[Relationship], chart_name: str="knowledge_graph"):
    '''
    The `visualize_knowledge_graph_echart` function is designed to visualize a knowledge graph using the ECharts library.

    #### Parameters
    - `entities: List[Entity]`: A list of entities to be visualized.
    - `relationships: List[Relationship]`: A list of relationships to be visualized.
    - `chart_name: str` (default is "knowledge_graph"): The name of the output HTML file for the chart.

    #### Returns
    - None: This function generates an HTML file with the visualization of the knowledge graph.
    '''
    nodes = [{"name": entity.entity_name, "symbolSize": 10, "value": entity.entity_description, "category": entity.entity_type} for entity in entities]
    links = [{"source": rel.source_entity, "target": rel.target_entity, "value": rel.relationship_description} for rel in relationships]
    categories = [{"name":type} for type in set([entity.entity_type for entity in entities])]

    graph = (
        Graph(init_opts=opts.InitOpts(theme=ThemeType.DARK, width="100%", height="1000%"))
        .add("", nodes, links, categories=categories)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Knowledge Graph"), 
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="left")
            )
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, position="right")
        )
    )
    
    graph.render(f"{chart_name}.html")
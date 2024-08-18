from typing import List
from opengraphrag.data_contracts.graph import Entity, Relationship
import pyecharts.options as opts
from pyecharts.charts import Graph
from pyecharts.globals import ThemeType


def visualize_knowledge_graph_echart(entities: List[Entity], relationships: List[Relationship]):
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
    
    graph.render("knowledge_graph.html")
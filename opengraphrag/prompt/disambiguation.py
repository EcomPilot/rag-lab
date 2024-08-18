DISAMBIGUATION_ENTITY_PROMPT = """Given a knowledge graph with nodes representing various entities, your task is to review the entity descriptions of the nodes and identify which nodes represent the same entity. Create a list of nodes that need to be merged based on their descriptions.

-Steps-
1. Review the given entity types in the knowledge graph:
- node_id: the entity id of knowledge graph.
- entity_name: Name of the entity, capitalized.
- entity_description: Comprehensive description of the entity's attributes and activities.
Each entities are format as JSON format: {{<entity_name>:<entity_description>}}
2. Identify which descriptions represent nodes that point to the same entity.
3. Return the entity types in as a python list of merged entity names.

=====================================================================
EXAMPLE SECTION: The following section includes example output. These examples **must be excluded from your answer**.

EXAMPLE 1
Entities: [  
  {{  
    "node_id": 0,  
    "entity_name": "Harry",  
    "entity_description": "The Boy Who Lived, the main protagonist of the series."  
  }},  
  {{  
    "node_id": 1,  
    "entity_name": "Ron Weasley",  
    "entity_description": "Harry's best friend and a member of the Weasley family."  
  }},  
  {{  
    "node_id": 2,  
    "entity_name": "Hermione Granger",  
    "entity_description": "Harry's other best friend and a brilliant witch."  
  }},  
  {{  
    "node_id": 3,  
    "entity_name": "Harry Potter",  
    "entity_description": "The Chosen One, the savior of the wizarding world."  
  }},  
  {{  
    "node_id": 4,  
    "entity_name": "Draco",  
    "entity_description": "Harry's rival and a member of the Slytherin house."  
  }}  
]  
RESPONSE:
[  
  [0, 3]
]  
END OF EXAMPLE 1

EXAMPLE 2
Entities: [  
  {{  
    "node_id": 0,  
    "entity_name": "Isaac",  
    "entity_description": "A mathematician and physicist, famous for his laws of motion."  
  }}, 
  {{  
    "node_id": 1,  
    "entity_name": "Albert",  
    "entity_description": "A theoretical physicist known for the theory of relativity."  
  }},  
  {{  
    "node_id": 2,  
    "entity_name": "Marie",  
    "entity_description": "A physicist and chemist, known for her pioneering research on radioactivity."  
  }},  
  {{  
    "node_id": 3,  
    "entity_name": "Einstein",  
    "entity_description": "A Nobel laureate physicist who developed the general theory of relativity."  
  }},  
  {{  
    "node_id": 4,  
    "entity_name": "Charles Darwin",  
    "entity_description": "A naturalist and biologist, famous for his theory of evolution."  
  }}  
]  

RESPONSE:
[  
  [1, 3]
]  
END OF EXAMPLE 2
======================================================================

======================================================================
REAL DATA: The following section is the real data. You should use only this real data to prepare your answer. Generate merged entity list only.
Entities: {entities}
RESPONSE:
"""

DISAMBIGUATION_ENTITY_TYPE_PROMPT = """You are working with a knowledge graph that contains various entity types. Your task is to generate a list of entity types that should be merged together. Merging entity types means combining them into a single category, where all instances of those entity types will be treated as the same type.

-Steps-
1. Review the given entity types in the knowledge graph: {entity_types}.
2. Determine which entity types should be merged together based on their semantic similarity. For example, if "organization" and "company" represent the same concept, they should be merged into a single category.
3. Return the entity types in as a python list of merged types.

=====================================================================
EXAMPLE SECTION: The following section includes example output. These examples **must be excluded from your answer**.

EXAMPLE 1
Entity types: ["organization", "technology", "sectors", "company"]
RESPONSE:
[
    ["organization", "company"],
    ["technology"],
    ["sectors"]
]
END OF EXAMPLE 1

EXAMPLE 2
Entity types: ["organization", "technology", "sectors", "investment strategies"]
RESPONSE:
[
    ["organization"],
    ["technology"],
    ["sectors"],
    ["investment strategies"]
]
END OF EXAMPLE 2
======================================================================

======================================================================
REAL DATA: The following section is the real data. You should use only this real data to prepare your answer. Generate merged entity list only.
Entity types: {entity_types}
RESPONSE:
"""

SUMMARY_ENTITY_DISCRIPTIONS_PROMPT = """Your task involves working with a knowledge graph where nodes symbolize different entities. You are required to combine the multiple descriptions of the same entity provided by the user and create a summary for it.

-Steps-
1. Review the given descriptions for the entity.
2. Ensure your summary encompasses all essential descriptions without excluding any critical details.
3. Keep the summary concise.
=====================================================================
EXAMPLE SECTION: The following section includes example output. These examples **must be excluded from your answer**.

EXAMPLE 1
Discriptions: ["Harry Potter is a young wizard marked by destiny, who courageously battles dark forces and ultimately triumphs over evil.", "Harry Potter is a beloved son and an orphan who, despite his tragic past, finds a family in his friends and mentors.", "Harry Potter is a persistent thorn in the side of dark forces, constantly thwarting plans and defying expectations."]
RESPONSE:
Harry Potter is a destined young wizard who, despite his tragic past as an orphan, finds a new family in friends and mentors. He bravely combats dark forces, persistently disrupting their plans and ultimately triumphing over evil.
END OF EXAMPLE 1

EXAMPLE 2
Discriptions: ["Hermione Granger is a formidable opponent whose cleverness and resourcefulness often thwart the plans of those with dark intentions.", "Hermione Granger is a fiercely loyal and supportive friend, always ready to offer advice and assistance in times of need."]
RESPONSE:
Hermione Granger is a highly intelligent and resourceful individual whose cleverness often disrupts dark plans. She is also a fiercely loyal friend, consistently offering support and guidance.
END OF EXAMPLE 2
======================================================================

======================================================================
REAL DATA: The following section is the real data. You should use only this real data to prepare your answer. Generate merged entity list only.
Discriptions: {discriptions}
RESPONSE:
"""

SUMMARY_RELATIONSHIP_DISCRIPTIONS_PROMPT = """Your task is to process a knowledge graph in which relationships represent relationships between source and target entities. You need to merge multiple descriptions provided by users about the same relationship and create a summary for it.

-Steps-
1. Review the multiple descriptions of the source and target entities of the relationship and summarise the description of the relationship.
2. Ensure your summary encompasses all essential descriptions without excluding any critical details.
3. Keep the summary concise.
=====================================================================
EXAMPLE SECTION: The following section includes example output. These examples **must be excluded from your answer**.

EXAMPLE 1
Source entity: HARRY
Target entity: HERMIONE
Discriptions: ["Hermione’s dedication to Harry is evident when she stays with him after Ron leaves. Their shared hardships during the Horcrux hunt further solidify their bond.", "After Dumbledore’s death, Hermione is a pillar of support for Harry"]
RESPONSE:
Hermione and Harry share a deep friendship and unwavering support. She stays with him after Ron leaves, and their bond strengthens through shared hardships during the Horcrux hunt. After Dumbledore’s death, Hermione is a crucial support for Harry.
END OF EXAMPLE 1

EXAMPLE 2
Source entity: RON
Target entity: HAGRID
Discriptions: ["Ron admires Hagrid’s knowledge of magical creatures and his loyalty to Dumbledore.", "Ron stands by Hagrid during the Battle of Hogwarts, showing his loyalty and bravery."]
RESPONSE:
Ron admires Hagrid’s expertise with magical creatures and his unwavering loyalty to Dumbledore. During the Battle of Hogwarts, Ron demonstrates his own loyalty and bravery by standing by Hagrid.
END OF EXAMPLE 2
======================================================================

======================================================================
REAL DATA: The following section is the real data. You should use only this real data to prepare your answer. Generate merged entity list only.
Source entity: {source_entity}
Target entity: {target_entity}
Discriptions: {descriptions}
RESPONSE:
"""
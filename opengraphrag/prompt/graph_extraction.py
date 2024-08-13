ENTITY_RELATIONSHIPS_GENERATION_PROMPT = """
-Goal-
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, capitalized
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as JSON: {{"entity_name":<entity_name>, "entity_type":<entity_type>, "entity_description":<entity_description>}}

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: an integer score between 1 to 10, indicating strength of the relationship between the source entity and target entity
Format each relationship as JSON: {{"source_entity":<source_entity>, "target_entity":<target_entity>, "relationship_description":<relationship_description>, "relationship_strength":<relationship_strength>}}

3. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. 

4. If you have to translate into {language}, just translate the descriptions, nothing else!

######################
-Examples-
######################
Example 1:
Entity_types: ORGANIZATION,PERSON
Text:
The Verdantis's Central Institution is scheduled to meet on Monday and Thursday, with the institution planning to release its latest policy decision on Thursday at 1:30 p.m. PDT, followed by a press conference where Central Institution Chair Martin Smith will take questions. Investors expect the Market Strategy Committee to hold its benchmark interest rate steady in a range of 3.5%-3.75%.
######################
Output:
[
    {{"entity_name": "CENTRAL INSTITUTION", "entity_type": "ORGANIZATION", "entity_description":"The Central Institution is the Federal Reserve of Verdantis, which is setting interest rates on Monday and Thursday"}},
    {{"entity_name":"MARTIN SMITH", "entity_type":"PERSON", "entity_description":"Martin Smith is the chair of the Central Institution"}},
    {{"source_entity":"MARTIN SMITH", "target_entity":"CENTRAL INSTITUTION", "relationship_description":"Martin Smith is the Chair of the Central Institution and will answer questions at a press conference."}}
]
######################
Example 2:
Text:
Five Aurelians jailed for 8 years in Firuzabad and widely regarded as hostages are on their way home to Aurelia.

The swap orchestrated by Quintara was finalized when $8bn of Firuzi funds were transferred to financial institutions in Krohaara, the capital of Quintara.

The exchange initiated in Firuzabad's capital, Tiruzia, led to the four men and one woman, who are also Firuzi nationals, boarding a chartered flight to Krohaara.

They were welcomed by senior Aurelian officials and are now on their way to Aurelia's capital, Cashion.

The Aurelians include 39-year-old businessman Samuel Namara, who has been held in Tiruzia's Alhamia Prison, as well as journalist Durke Bataglani, 59, and environmentalist Meggie Tazbah, 53, who also holds Bratinas nationality.
######################
Output:
[  
    {{ "entity_name": "FIRUZABAD", "entity_type": "GEO", "entity_description": "Firuzabad held Aurelians as hostages"}},  
    {{ "entity_name": "AURELIA", "entity_type": "GEO", "entity_description": "Country seeking to release hostages" }},  
    {{ "entity_name": "QUINTARA", "entity_type": "GEO", "entity_description": "Country that negotiated a swap of money in exchange for hostages" }},  
    {{ "entity_name": "TIRUZIA", "entity_type": "GEO", "entity_description": "Capital of Firuzabad where the Aurelians were being held" }},  
    {{ "entity_name": "KROHAARA", "entity_type": "GEO", "entity_description": "Capital city in Quintara" }},  
    {{ "entity_name": "CASHION", "entity_type": "GEO", "entity_description": "Capital city in Aurelia" }},  
    {{ "entity_name": "SAMUEL NAMARA", "entity_type": "PERSON", "entity_description": "Aurelian who spent time in Tiruzia's Alhamia Prison" }},  
    {{ "entity_name": "ALHAMIA PRISON", "entity_type": "GEO", "entity_description": "Prison in Tiruzia" }},  
    {{ "entity_name": "DURKE BATAGLANI", "entity_type": "PERSON", "entity_description": "Aurelian journalist who was held hostage" }},  
    {{ "entity_name": "MEGGIE TAZBAH", "entity_type": "PERSON",  "entity_description": "Bratinas national and environmentalist who was held hostage"  }},  
    {{ "source_entity": "FIRUZABAD", "target_entity": "AURELIA", "relationship_description": "Firuzabad negotiated a hostage exchange with Aurelia"  }},  
    {{ "source_entity": "QUINTARA", "target_entity": "AURELIA", "relationship_description": "Quintara brokered the hostage exchange between Firuzabad and Aurelia" }},  
    {{ "source_entity": "QUINTARA", "target_entity": "FIRUZABAD", "relationship_description": "Quintara brokered the hostage exchange between Firuzabad and Aurelia" }},  
    {{ "source_entity": "SAMUEL NAMARA", "target_entity": "ALHAMIA PRISON", "relationship_description": "Samuel Namara was a prisoner at Alhamia prison" }},  
    {{ "source_entity": "SAMUEL NAMARA", "target_entity": "MEGGIE TAZBAH", "relationship_description": "Samuel Namara and Meggie Tazbah were exchanged in the same hostage release" }},  
    {{ "source_entity": "SAMUEL NAMARA", "target_entity": "DURKE BATAGLANI", "relationship_description": "Samuel Namara and Durke Bataglani were exchanged in the same hostage release" }},  
    {{ "source_entity": "MEGGIE TAZBAH", "target_entity": "DURKE BATAGLANI", "relationship_description": "Meggie Tazbah and Durke Bataglani were exchanged in the same hostage release" }},  
    {{ "source_entity": "SAMUEL NAMARA", "target_entity": "FIRUZABAD", "relationship_description": "Samuel Namara was a hostage in Firuzabad" }},  
    {{ "source_entity": "MEGGIE TAZBAH", "target_entity": "FIRUZABAD", "relationship_description": "Meggie Tazbah was a hostage in Firuzabad" }},  
    {{ "source_entity": "DURKE BATAGLANI", "target_entity": "FIRUZABAD", "relationship_description": "Durke Bataglani was a hostage in Firuzabad" }}
]

######################

-Real Data-
######################
entity_types: {entity_types}
text: {input_text}
######################
output:
"""


ENTITY_TYPE_GENERATION_PROMPT = """
{expert}
The goal is to study the connections and relations between the entity types and their features in order to understand all available information from the text.
The user's task is to identify the relations and structure of the community of interest, specifically within the {topic} domain..
As part of the analysis, you want to identify the entity types present in the following text.
The entity types must be relevant to the user task.
Avoid general entity types such as "other" or "unknown".
This is VERY IMPORTANT: Do not generate redundant or overlapping entity types. For example, if the text contains "company" and "organization" entity types, you should return only one of them.
Don't worry about quantity, always choose quality over quantity. And make sure EVERYTHING in your answer is relevant to the context of entity extraction.
And remember, it is ENTITY TYPES what we need.
Return the entity types in as a list of comma sepparated of strings.
=====================================================================
EXAMPLE SECTION: The following section includes example output. These examples **must be excluded from your answer**.

EXAMPLE 1
Task: Determine the connections and organizational hierarchy within the specified community.
Text: Example_Org_A is a company in Sweden. Example_Org_A's director is Example_Individual_B.
RESPONSE:
organization, person
END OF EXAMPLE 1

EXAMPLE 2
Task: Identify the key concepts, principles, and arguments shared among different philosophical schools of thought, and trace the historical or ideological influences they have on each other.
Text: Rationalism, epitomized by thinkers such as René Descartes, holds that reason is the primary source of knowledge. Key concepts within this school include the emphasis on the deductive method of reasoning.
RESPONSE:
concept, person, school of thought
END OF EXAMPLE 2

EXAMPLE 3
Task: Identify the full range of basic forces, factors, and trends that would indirectly shape an issue.
Text: Industry leaders such as Panasonic are vying for supremacy in the battery production sector. They are investing heavily in research and development and are exploring new technologies to gain a competitive edge.
RESPONSE:
organization, technology, sectors, investment strategies
END OF EXAMPLE 3
======================================================================

======================================================================
REAL DATA: The following section is the real data. You should use only this real data to prepare your answer. Generate Entity Types only.
Task: Identify the relations and structure of the community of interest, specifically within the {topic} domain.
Text: {input_text}
RESPONSE:
{{<entity_types>}}
"""

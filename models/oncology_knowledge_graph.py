"""
PharmaTab Oncology Knowledge Graph
"""

class OncologyKnowledgeGraph:

    def __init__(self):

        self.graph = {}


    def add_entity(self, entity):

        if entity not in self.graph:
            self.graph[entity] = []


    def add_relation(self, entity1, relation, entity2):

        self.add_entity(entity1)
        self.add_entity(entity2)

        self.graph[entity1].append({
            "relation": relation,
            "target": entity2
        })


    def get_relations(self, entity):

        return self.graph.get(entity, [])


    def find_drugs_for_gene(self, gene):

        drugs = []

        for entity in self.graph:

            for rel in self.graph[entity]:

                if rel["relation"] == "targets" and rel["target"] == gene:

                    drugs.append(entity)

        return drugs
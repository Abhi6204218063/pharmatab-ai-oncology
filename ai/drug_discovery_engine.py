"""
PharmaTab AI Drug Discovery Engine
Suggests drug candidates for mutated genes
"""

import numpy as np


class DrugDiscoveryEngine:

    def __init__(self):

        self.drug_library = {
            "DrugA": ["EGFR", "HER2"],
            "DrugB": ["KRAS", "BRAF"],
            "DrugC": ["PI3K", "AKT"],
            "DrugD": ["MEK", "ERK"]
        }


    def find_targets(self, mutation_list):

        possible_drugs = []

        for drug in self.drug_library:

            targets = self.drug_library[drug]

            for gene in mutation_list:

                if gene in targets:

                    possible_drugs.append(drug)

        return list(set(possible_drugs))


    def score_drugs(self, drugs):

        scores = {}

        for drug in drugs:

            scores[drug] = np.random.uniform(0.5, 1.0)

        return scores


    def suggest_drugs(self, mutations):

        drugs = self.find_targets(mutations)

        scores = self.score_drugs(drugs)

        ranked = sorted(scores.items(),
                        key=lambda x: x[1],
                        reverse=True)

        return ranked
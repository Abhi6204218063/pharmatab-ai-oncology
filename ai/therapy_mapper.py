import pandas as pd


class MutationTherapyMapper:

    def __init__(self):

        self.therapy_db = {
            "EGFR": ["Erlotinib", "Gefitinib", "Osimertinib"],
            "BRAF": ["Vemurafenib", "Dabrafenib"],
            "KRAS": ["Sotorasib"],
            "PIK3CA": ["Alpelisib"],
            "ALK": ["Crizotinib", "Ceritinib"]
        }

    def map_therapies(self, mutations):

        genes = mutations["Hugo_Symbol"].unique()

        therapy_map = []

        for gene in genes:

            if gene in self.therapy_db:

                for drug in self.therapy_db[gene]:

                    therapy_map.append({
                        "gene": gene,
                        "drug": drug
                    })

        return pd.DataFrame(therapy_map)
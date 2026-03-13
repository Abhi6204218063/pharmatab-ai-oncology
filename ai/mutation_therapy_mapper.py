class MutationTherapyMapper:

    def __init__(self):

        self.therapy_database = {

            "BRAF": ["Dabrafenib", "Trametinib"],
            "NRAS": ["MEK inhibitors"],
            "HRAS": ["Tipifarnib"],

            "PIK3CA": ["Alpelisib"],
            "EGFR": ["Osimertinib"],
            "ALK": ["Alectinib"],
            "KRAS": ["Sotorasib"]

        }


    def map_therapies(self, mutations):

        therapies = []

        for gene in mutations:

            if gene in self.therapy_database:

                therapies.extend(self.therapy_database[gene])

        return therapies
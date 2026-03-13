class MutationTherapyMapper:

    def __init__(self):

        # Oncology drug-target knowledge base
        self.therapy_db = {

            "BRAF": [
                ("Dabrafenib", "BRAF inhibitor"),
                ("Vemurafenib", "BRAF inhibitor"),
                ("Trametinib", "MEK inhibitor")
            ],

            "NRAS": [
                ("Trametinib", "MEK inhibitor"),
                ("Cobimetinib", "MEK inhibitor")
            ],

            "HRAS": [
                ("Tipifarnib", "Farnesyltransferase inhibitor")
            ],

            "EGFR": [
                ("Gefitinib", "EGFR inhibitor"),
                ("Erlotinib", "EGFR inhibitor")
            ],

            "ALK": [
                ("Crizotinib", "ALK inhibitor"),
                ("Alectinib", "ALK inhibitor")
            ],

            "KRAS": [
                ("Sotorasib", "KRAS G12C inhibitor")
            ],

            "PIK3CA": [
                ("Alpelisib", "PI3K inhibitor")
            ],

            "TP53": [
                ("APR-246", "p53 reactivator")
            ]

        }


    def map_therapies(self, mutations):

        """
        Map detected mutations to therapies
        """

        therapies = []

        for gene in mutations:

            if gene in self.therapy_db:

                for drug, mechanism in self.therapy_db[gene]:

                    therapies.append({

                        "gene": gene,
                        "drug": drug,
                        "mechanism": mechanism

                    })

        return therapies


    def unique_drugs(self, therapies):

        """
        Extract unique drugs from therapy list
        """

        drugs = []

        for t in therapies:

            if t["drug"] not in drugs:

                drugs.append(t["drug"])

        return drugs


    def therapy_summary(self, therapies):

        """
        Create summary for clinical report
        """

        summary = []

        for t in therapies:

            line = f"{t['drug']} targeting {t['gene']} ({t['mechanism']})"

            summary.append(line)

        return summary
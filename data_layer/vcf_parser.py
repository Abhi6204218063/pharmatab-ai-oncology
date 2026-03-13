"""
PharmaTab VCF Parser
Extract gene mutations from VCF files
"""

class VCFParser:

    def __init__(self, filepath):

        self.filepath = filepath


    def parse(self):

        mutations = []

        with open(self.filepath, "r") as f:

            for line in f:

                if line.startswith("#"):
                    continue

                parts = line.strip().split("\t")

                chromosome = parts[0]
                position = parts[1]
                gene = parts[3]

                mutations.append({
                    "chromosome": chromosome,
                    "position": position,
                    "gene": gene
                })

        return mutations
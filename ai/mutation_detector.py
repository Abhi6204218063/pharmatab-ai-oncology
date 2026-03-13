import pandas as pd


class MutationDetector:

    def __init__(self):

        # Known cancer driver genes
        self.driver_genes = [
            "BRAF",
            "NRAS",
            "HRAS",
            "TP53",
            "PIK3CA",
            "EGFR",
            "KRAS",
            "ALK",
            "PTEN"
        ]


    def load_dataset(self, file_path):

        """
        Load mutation dataset (CSV or TSV)
        """

        if file_path.endswith(".tsv"):
            df = pd.read_csv(file_path, sep="\t")
        else:
            df = pd.read_csv(file_path)

        return df


    def detect_mutations(self, df):

        """
        Extract mutated genes from dataset
        """

        if "gene" in df.columns:

            genes = df["gene"].dropna().unique().tolist()

        elif "Hugo_Symbol" in df.columns:

            genes = df["Hugo_Symbol"].dropna().unique().tolist()

        else:

            raise ValueError(
                "Dataset must contain 'gene' or 'Hugo_Symbol' column"
            )

        return genes


    def detect_driver_mutations(self, genes):

        """
        Identify known cancer driver mutations
        """

        drivers = []

        for g in genes:

            if g in self.driver_genes:
                drivers.append(g)

        return drivers


    def mutation_frequency(self, df):

        """
        Calculate mutation frequency
        """

        if "gene" in df.columns:

            freq = df["gene"].value_counts()

        elif "Hugo_Symbol" in df.columns:

            freq = df["Hugo_Symbol"].value_counts()

        else:

            raise ValueError("No gene column found")

        return freq


    def analyze(self, file_path):

        """
        Full mutation analysis pipeline
        """

        df = self.load_dataset(file_path)

        genes = self.detect_mutations(df)

        drivers = self.detect_driver_mutations(genes)

        freq = self.mutation_frequency(df)

        return {

            "genes": genes,
            "driver_mutations": drivers,
            "mutation_frequency": freq

        }
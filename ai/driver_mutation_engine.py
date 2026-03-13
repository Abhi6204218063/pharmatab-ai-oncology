import pandas as pd


class DriverMutationEngine:

    def detect(self, dataset):

        gene_counts = dataset["Hugo_Symbol"].value_counts()

        top_genes = gene_counts.head(20)

        return top_genes
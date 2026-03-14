import pandas as pd

class GeneExplorer:

    def top_genes(self, df):

        if "Hugo_Symbol" not in df.columns:
            return None

        genes = df["Hugo_Symbol"].value_counts().head(20)

        result = pd.DataFrame({
            "Gene":genes.index,
            "Mutation Count":genes.values
        })

        return result
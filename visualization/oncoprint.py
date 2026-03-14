import pandas as pd
import matplotlib.pyplot as plt


class OncoPrint:

    def plot(self, mutations_df):

        if mutations_df is None:
            return None

        if not isinstance(mutations_df, pd.DataFrame):
            return None

        if "Hugo_Symbol" not in mutations_df.columns:
            return None

        # count gene mutations
        gene_counts = mutations_df["Hugo_Symbol"].value_counts().head(20)

        if gene_counts.empty:
            return None

        fig, ax = plt.subplots(figsize=(8,6))

        gene_counts.sort_values().plot(
            kind="barh",
            ax=ax,
            color="#5DADE2"
        )

        ax.set_title("Top Mutated Genes")
        ax.set_xlabel("Mutation Count")
        ax.set_ylabel("Gene")

        plt.tight_layout()

        return fig
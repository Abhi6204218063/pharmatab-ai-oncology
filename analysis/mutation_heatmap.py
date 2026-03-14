import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class MutationHeatmap:

    def plot(self, df):

        if df is None:
            return None

        if "geneSymbol" not in df.columns:
            return None

        gene_counts = df["geneSymbol"].value_counts().head(20)

        data = gene_counts.values.reshape(1, -1)

        fig, ax = plt.subplots(figsize=(10, 3))

        sns.heatmap(
            data,
            annot=True,
            cmap="Reds",
            xticklabels=gene_counts.index,
            yticklabels=["Mutation Frequency"],
            ax=ax
        )

        ax.set_title("Top Mutated Genes Heatmap")

        return fig
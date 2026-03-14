import seaborn as sns
import matplotlib.pyplot as plt

class MutationHeatmap:

    def plot(self, mutations):

        if mutations is None:
            return None

        gene_counts = mutations["Hugo_Symbol"].value_counts().head(15)

        data = gene_counts.values.reshape(1,-1)

        fig, ax = plt.subplots(figsize=(10,2))

        sns.heatmap(
            data,
            annot=True,
            cmap="Reds",
            xticklabels=gene_counts.index,
            yticklabels=["Mutations"],
            ax=ax
        )

        ax.set_title("Mutation Heatmap")

        return fig
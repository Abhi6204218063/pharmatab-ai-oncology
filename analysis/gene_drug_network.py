import networkx as nx
import matplotlib.pyplot as plt


class GeneDrugNetwork:

    def build(self):

        interactions = {

            "TP53": ["APR-246"],
            "PIK3CA": ["Alpelisib"],
            "BRCA1": ["Olaparib"],
            "BRCA2": ["Olaparib"],
            "EGFR": ["Gefitinib"],
            "KRAS": ["Sotorasib"]

        }

        G = nx.Graph()

        for gene, drugs in interactions.items():

            for drug in drugs:

                G.add_edge(gene, drug)

        pos = nx.spring_layout(G)

        fig, ax = plt.subplots(figsize=(6,6))

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=2000,
            font_size=10,
            ax=ax
        )

        ax.set_title("Gene–Drug Interaction Network")

        return fig
import pandas as pd
from clinical.therapy_db import THERAPY_DB


class TherapyEngine:

    def recommend(self, df):

        recommendations = []

        if df is None:
            return None

        for gene in df["geneSymbol"].unique():

            if gene in THERAPY_DB:

                therapy = THERAPY_DB[gene]["therapy"]
                therapy_type = THERAPY_DB[gene]["type"]

                recommendations.append({

                    "Gene": gene,
                    "Recommended Therapy": therapy,
                    "Therapy Type": therapy_type

                })

        if len(recommendations) == 0:
            return None

        return pd.DataFrame(recommendations)
class TherapyOptimizer:

    def optimize(self, therapy_df):

        scores = {}

        for drug in therapy_df["drug"]:

            scores[drug] = scores.get(drug, 0) + 1

        best_drug = max(scores, key=scores.get)

        return {
            "recommended_therapy": best_drug,
            "score": scores[best_drug]
        }
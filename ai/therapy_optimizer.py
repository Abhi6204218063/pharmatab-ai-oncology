import itertools


class TherapyOptimizer:

    def __init__(self):

        # drug effectiveness scores (literature-inspired heuristic model)

        self.drug_scores = {

            "Dabrafenib": 0.75,
            "Vemurafenib": 0.72,
            "Trametinib": 0.70,
            "Cobimetinib": 0.68,
            "Gefitinib": 0.65,
            "Erlotinib": 0.64,
            "Crizotinib": 0.69,
            "Alectinib": 0.73,
            "Sotorasib": 0.66,
            "Alpelisib": 0.63,
            "Tipifarnib": 0.60,
            "APR-246": 0.58

        }

        # resistance risk

        self.resistance = {

            "Dabrafenib": 0.25,
            "Vemurafenib": 0.28,
            "Trametinib": 0.20,
            "Cobimetinib": 0.22,
            "Gefitinib": 0.30,
            "Erlotinib": 0.32,
            "Crizotinib": 0.26,
            "Alectinib": 0.21,
            "Sotorasib": 0.27,
            "Alpelisib": 0.29,
            "Tipifarnib": 0.33,
            "APR-246": 0.35

        }


    def evaluate_combination(self, drugs):

        """
        Score therapy combination
        """

        effectiveness = 0
        resistance_risk = 0

        for d in drugs:

            if d in self.drug_scores:

                effectiveness += self.drug_scores[d]

                resistance_risk += self.resistance[d]

        effectiveness = effectiveness / len(drugs)

        resistance_risk = resistance_risk / len(drugs)

        # final score

        score = effectiveness - resistance_risk

        return score, effectiveness, resistance_risk


    def optimize(self, therapies):

        """
        Find best therapy combination
        """

        # extract drug names

        drugs = []

        for t in therapies:

            if isinstance(t, dict):

                drugs.append(t["drug"])

            else:

                drugs.append(t)

        drugs = list(set(drugs))


        best_strategy = None

        best_score = -999

        best_effect = 0

        best_resistance = 0


        # try single and pair combinations

        for r in range(1, 3):

            for combo in itertools.combinations(drugs, r):

                score, eff, res = self.evaluate_combination(combo)

                if score > best_score:

                    best_score = score

                    best_strategy = combo

                    best_effect = eff

                    best_resistance = res


        return best_strategy, best_effect, best_resistance
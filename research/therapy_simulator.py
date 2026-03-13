"""
PharmaTab Research Module
Therapy Strategy Simulator
"""

import numpy as np

from research.digital_twin import DigitalTumorTwin


class TherapySimulator:

    def __init__(self,
                 growth_rate=0.03,
                 mutation_rate=1e-7):

        self.growth_rate = growth_rate
        self.mutation_rate = mutation_rate


    def simulate_single_drug(self,
                             drug_dose,
                             steps=50):

        twin = DigitalTumorTwin(
            growth_rate=self.growth_rate,
            mutation_rate=self.mutation_rate,
            drug_sensitivity=0.3
        )

        result = twin.simulate_therapy(
            initial_size=1e6,
            drug_dose=drug_dose,
            steps=steps
        )

        return result


    def simulate_combination_therapy(self,
                                     drug_a,
                                     drug_b,
                                     steps=50):

        twin = DigitalTumorTwin(
            growth_rate=self.growth_rate,
            mutation_rate=self.mutation_rate,
            drug_sensitivity=0.3
        )

        tumor = 1e6

        history = []

        for t in range(steps):

            effect = (drug_a + drug_b) * 0.5

            tumor = tumor * (1 - effect)

            tumor = tumor + self.growth_rate * tumor

            history.append(tumor)

        return history


    def compare_therapies(self,
                          drug_a,
                          drug_b):

        result_a = self.simulate_single_drug(drug_a)

        result_b = self.simulate_single_drug(drug_b)

        result_combo = self.simulate_combination_therapy(
            drug_a,
            drug_b
        )

        final_a = result_a[-1]
        final_b = result_b[-1]
        final_combo = result_combo[-1]

        best = min(final_a, final_b, final_combo)

        if best == final_a:
            strategy = "Drug A"

        elif best == final_b:
            strategy = "Drug B"

        else:
            strategy = "Combination"

        return {
            "drug_a_final": final_a,
            "drug_b_final": final_b,
            "combo_final": final_combo,
            "best_strategy": strategy
        }
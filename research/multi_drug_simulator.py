"""
PharmaTab Multi Drug Therapy Simulator
Simulates combination cancer therapies
"""

import numpy as np


class MultiDrugTherapySimulator:

    def __init__(self,
                 tumor_size,
                 growth_rate,
                 mutation_rate):

        self.tumor_size = tumor_size
        self.growth_rate = growth_rate
        self.mutation_rate = mutation_rate

        self.history = []


    def apply_drugs(self,
                    drug_a_dose,
                    drug_b_dose,
                    sensitivity_a=0.4,
                    sensitivity_b=0.3):

        """
        Apply drug combination effect
        """

        growth = self.tumor_size * self.growth_rate

        mutation_effect = self.tumor_size * self.mutation_rate

        drug_a_effect = self.tumor_size * drug_a_dose * sensitivity_a

        drug_b_effect = self.tumor_size * drug_b_dose * sensitivity_b

        total_drug_effect = drug_a_effect + drug_b_effect

        self.tumor_size = self.tumor_size + growth + mutation_effect - total_drug_effect

        if self.tumor_size < 0:
            self.tumor_size = 0

        self.history.append(self.tumor_size)

        return self.tumor_size


    def run_simulation(self,
                       drug_a_dose,
                       drug_b_dose,
                       steps=50):

        """
        Simulate therapy over time
        """

        for _ in range(steps):

            self.apply_drugs(drug_a_dose,
                             drug_b_dose)

        return self.history


    def compare_therapies(self):

        """
        Compare mono vs combination therapies
        """

        results = {}

        # Drug A only
        self.reset()
        results["drug_A"] = self.run_simulation(0.4, 0)

        # Drug B only
        self.reset()
        results["drug_B"] = self.run_simulation(0, 0.4)

        # Combination therapy
        self.reset()
        results["combo"] = self.run_simulation(0.3, 0.3)

        return results


    def reset(self):

        """
        Reset tumor state
        """

        self.tumor_size = 1e7

        self.history = []
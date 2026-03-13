"""
PharmaTab Evolutionary Cancer Model
Simulates tumor clone evolution and resistance
"""

import numpy as np


class EvolutionaryCancerModel:

    def __init__(self,
                 sensitive_cells,
                 resistant_cells,
                 growth_sensitive=0.03,
                 growth_resistant=0.025,
                 mutation_rate=0.00001):

        self.sensitive = sensitive_cells
        self.resistant = resistant_cells

        self.growth_sensitive = growth_sensitive
        self.growth_resistant = growth_resistant

        self.mutation_rate = mutation_rate

        self.history_sensitive = []
        self.history_resistant = []


    def step(self,
             drug_dose):

        """
        Simulate one evolutionary step
        """

        growth_s = self.sensitive * self.growth_sensitive
        growth_r = self.resistant * self.growth_resistant

        mutation = self.sensitive * self.mutation_rate

        drug_kill = self.sensitive * drug_dose * 0.5

        self.sensitive = self.sensitive + growth_s - drug_kill - mutation

        self.resistant = self.resistant + growth_r + mutation

        if self.sensitive < 0:
            self.sensitive = 0

        if self.resistant < 0:
            self.resistant = 0

        self.history_sensitive.append(self.sensitive)
        self.history_resistant.append(self.resistant)


    def run_simulation(self,
                       drug_dose,
                       steps=50):

        for _ in range(steps):

            self.step(drug_dose)

        return {
            "sensitive": self.history_sensitive,
            "resistant": self.history_resistant
        }
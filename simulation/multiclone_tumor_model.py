"""
PharmaTab Multi-Clone Tumor Evolution Model
"""

import numpy as np


class MultiCloneTumorModel:

    def __init__(self, total_cells=1e7):

        # three clones
        self.clones = {
            "sensitive": total_cells * 0.6,
            "moderate": total_cells * 0.3,
            "resistant": total_cells * 0.1
        }

        self.history = {
            "sensitive": [],
            "moderate": [],
            "resistant": [],
            "total": []
        }


    def growth(self):

        growth_rates = {
            "sensitive": 0.03,
            "moderate": 0.035,
            "resistant": 0.04
        }

        for clone in self.clones:
            self.clones[clone] += self.clones[clone] * growth_rates[clone]


    def drug_effect(self, drug_dose):

        kill_rates = {
            "sensitive": 0.08,
            "moderate": 0.03,
            "resistant": 0.005
        }

        for clone in self.clones:

            kill = drug_dose * self.clones[clone] * kill_rates[clone]

            self.clones[clone] -= kill

            if self.clones[clone] < 0:
                self.clones[clone] = 0


    def step(self, drug_dose):

        self.growth()

        self.drug_effect(drug_dose)

        total = sum(self.clones.values())

        for clone in self.clones:
            self.history[clone].append(self.clones[clone])

        self.history["total"].append(total)


    def run(self, drug_dose=0.4, steps=60):

        for _ in range(steps):

            self.step(drug_dose)

        return self.history
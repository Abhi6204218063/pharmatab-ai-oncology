"""
PharmaTab Research Module
Digital Tumor Twin Engine
"""

import numpy as np


class DigitalTumorTwin:

    def __init__(self,
                 growth_rate,
                 mutation_rate,
                 drug_sensitivity):

        self.growth_rate = growth_rate
        self.mutation_rate = mutation_rate
        self.drug_sensitivity = drug_sensitivity


    def simulate_growth(self, tumor_size, steps):

        history = []

        for t in range(steps):

            growth = self.growth_rate * tumor_size

            tumor_size = tumor_size + growth

            history.append(tumor_size)

        return history


    def apply_drug(self, tumor_size, drug_dose):

        effect = drug_dose * self.drug_sensitivity

        tumor_size = tumor_size * (1 - effect)

        if tumor_size < 0:
            tumor_size = 0

        return tumor_size


    def simulate_therapy(self,
                         initial_size,
                         drug_dose,
                         steps):

        tumor = initial_size

        history = []

        for t in range(steps):

            tumor = self.apply_drug(tumor, drug_dose)

            tumor = tumor + self.growth_rate * tumor

            history.append(tumor)

        return history
"""
PharmaTab Tumor Microenvironment Model
Simulates oxygen, immune response and drug diffusion
"""

import numpy as np


class TumorMicroenvironment:

    def __init__(self,
                 tumor_cells,
                 oxygen_level=1.0,
                 immune_cells=1e5,
                 nutrient_level=1.0):

        self.tumor_cells = tumor_cells
        self.oxygen = oxygen_level
        self.immune = immune_cells
        self.nutrients = nutrient_level

        self.history_tumor = []
        self.history_oxygen = []
        self.history_immune = []


    def step(self,
             drug_concentration):

        """
        simulate one microenvironment step
        """

        growth = self.tumor_cells * 0.03 * self.oxygen * self.nutrients

        immune_attack = self.immune * 0.00001

        drug_kill = drug_concentration * self.tumor_cells * 0.2

        self.tumor_cells = self.tumor_cells + growth - immune_attack - drug_kill

        if self.tumor_cells < 0:
            self.tumor_cells = 0

        oxygen_consumption = self.tumor_cells * 0.0000001

        self.oxygen = max(0, self.oxygen - oxygen_consumption)

        immune_response = self.tumor_cells * 0.000001

        self.immune += immune_response

        self.history_tumor.append(self.tumor_cells)
        self.history_oxygen.append(self.oxygen)
        self.history_immune.append(self.immune)


    def run_simulation(self,
                       drug_concentration,
                       steps=50):

        for _ in range(steps):

            self.step(drug_concentration)

        return {
            "tumor_cells": self.history_tumor,
            "oxygen": self.history_oxygen,
            "immune_cells": self.history_immune
        }
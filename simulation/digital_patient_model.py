"""
PharmaTab Whole Body Digital Patient Model
Simulates tumor, immune system and drug metabolism
"""

import numpy as np


class DigitalPatientModel:

    def __init__(self,
                 tumor_cells,
                 immune_cells,
                 drug_level=0.0):

        self.tumor = tumor_cells
        self.immune = immune_cells
        self.drug = drug_level

        # NEW
        self.resistance = 0.1
        self.history_tumor = []
        self.history_immune = []
        self.history_drug = []
        self.history_resistance = []


    def drug_metabolism(self):

        """
        simulate drug clearance by liver
        """

        clearance_rate = 0.1

        self.drug *= (1 - clearance_rate)


    def immune_response(self):

        """
        immune cells attack tumor
        """

        attack = self.immune * 0.00001

        self.tumor -= attack

        if self.tumor < 0:
            self.tumor = 0


    def tumor_growth(self):

        """
        tumor proliferation
        """

        growth = self.tumor * 0.03

        self.tumor += growth


    def drug_effect(self):

        """
        drug kills tumor cells
        """
        
        kill_rate = 0.03 * (1 -
        self.resistance)
        kill = self.drug * self.tumor * kill_rate

        self.tumor -= kill

        if self.tumor < 0:
            self.tumor = 0


    def step(self,
             drug_dose):

        """
        simulate one treatment step
        """

        self.drug += drug_dose

        self.drug_metabolism()

        self.evolve_resistance()

        self.drug_effect()

        self.immune_response()

        self.tumor_growth()

        immune_activation = self.tumor * 0.000001

        self.immune += immune_activation

        self.history_tumor.append(self.tumor)
        self.history_immune.append(self.immune)
        self.history_drug.append(self.drug)
        self.history_resistance.append(self.resistance)


    def run_simulation(self,
                       drug_dose,
                       steps=50):

        for _ in range(steps):

            self.step(drug_dose)

        return {
            "tumor": self.history_tumor,
            "immune": self.history_immune,
            "drug": self.history_drug
        }
    
    def evolve_resistance(self):
        mutation_rate = 0.002

        self.resistance += mutation_rate

        if self.resistance > 1:
            self.resistance = 1
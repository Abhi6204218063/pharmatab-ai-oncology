import numpy as np


class DigitalPatientTwin:

    def __init__(self, tumor_cells=1000000, immune_cells=500000):

        self.tumor_cells = tumor_cells
        self.immune_cells = immune_cells

        self.tumor_growth_rate = 0.05
        self.immune_kill_rate = 0.02
        self.therapy_effect = 0.03


    def simulate(self, weeks=52):

        tumor_history = []
        immune_history = []

        tumor = self.tumor_cells
        immune = self.immune_cells

        for week in range(weeks):

            tumor_growth = tumor * self.tumor_growth_rate

            immune_kill = immune * self.immune_kill_rate

            therapy_kill = tumor * self.therapy_effect

            tumor = tumor + tumor_growth - immune_kill - therapy_kill

            if tumor < 0:
                tumor = 0

            immune = immune + (tumor * 0.00001)

            tumor_history.append(tumor)
            immune_history.append(immune)

        return tumor_history, immune_history
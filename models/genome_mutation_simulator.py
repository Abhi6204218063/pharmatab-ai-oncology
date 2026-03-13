"""
PharmaTab Whole Genome Mutation Simulator
"""

import numpy as np


class GenomeMutationSimulator:

    def __init__(self,
                 tumor_cells=1e7,
                 mutation_rate=1e-6):

        self.tumor_cells = tumor_cells
        self.mutation_rate = mutation_rate

        self.driver_mutations = 0
        self.passenger_mutations = 0

        self.history = {
            "tumor": [],
            "driver": [],
            "passenger": []
        }


    def mutate(self):

        mutations = int(self.tumor_cells * self.mutation_rate)

        for _ in range(mutations):

            if np.random.rand() < 0.01:

                self.driver_mutations += 1

            else:

                self.passenger_mutations += 1


    def tumor_growth(self):

        growth_rate = 0.03 + (self.driver_mutations * 0.002)

        self.tumor_cells += self.tumor_cells * growth_rate


    def step(self):

        self.mutate()

        self.tumor_growth()

        self.history["tumor"].append(self.tumor_cells)
        self.history["driver"].append(self.driver_mutations)
        self.history["passenger"].append(self.passenger_mutations)


    def run(self, steps=50):

        for _ in range(steps):

            self.step()

        return self.history  
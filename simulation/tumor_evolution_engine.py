import numpy as np
import matplotlib.pyplot as plt


class TumorEvolutionEngine:

    def __init__(self):

        # model parameters

        self.initial_cells = 1e6        # initial tumor cells
        self.growth_rate = 0.03         # tumor growth rate
        self.carrying_capacity = 1e9    # max tumor size
        self.therapy_kill = 0.02        # therapy kill rate


    def simulate(self, weeks=52):

        """
        Logistic tumor growth with therapy effect
        """

        time = np.arange(0, weeks)

        tumor_cells = []

        N = self.initial_cells

        for t in time:

            # logistic growth

            growth = self.growth_rate * N * (1 - N/self.carrying_capacity)

            # therapy killing

            therapy = self.therapy_kill * N

            # update tumor size

            N = N + growth - therapy

            if N < 0:
                N = 0

            tumor_cells.append(N)

        return time, tumor_cells


    def plot(self, time, tumor_cells):

        plt.figure(figsize=(8,5))

        plt.plot(time, tumor_cells)

        plt.title("Tumor Evolution Simulation")

        plt.xlabel("Weeks")

        plt.ylabel("Tumor Cell Count")

        plt.grid(True)

        plt.savefig("tumor_simulation.png")

        plt.close()


    def run(self):

        time, tumor = self.simulate()

        self.plot(time, tumor)

        return time, tumor
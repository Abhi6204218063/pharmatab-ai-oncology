import numpy as np
import matplotlib.pyplot as plt


class VirtualCohortSimulator:

    def __init__(self):

        # number of virtual patients

        self.n_patients = 200

        # tumor parameters

        self.initial_cells = 1e6

        self.base_growth = 0.03

        self.carrying_capacity = 1e9

        self.therapy_kill = 0.02


    def simulate_patient(self, weeks=52):

        time = np.arange(weeks)

        N = self.initial_cells

        tumor = []

        # random variability

        growth_rate = np.random.normal(self.base_growth, 0.005)

        for t in time:

            growth = growth_rate * N * (1 - N/self.carrying_capacity)

            therapy = self.therapy_kill * N

            N = N + growth - therapy

            if N < 0:
                N = 0

            tumor.append(N)

        return tumor


    def run(self):

        weeks = 52

        cohort = []

        for i in range(self.n_patients):

            tumor = self.simulate_patient(weeks)

            cohort.append(tumor)

        cohort = np.array(cohort)

        time = np.arange(weeks)

        mean_growth = cohort.mean(axis=0)

        self.plot(time, cohort, mean_growth)

        return time, cohort, mean_growth


    def plot(self, time, cohort, mean_growth):

        plt.figure(figsize=(8,5))

        # individual patients

        for i in range(20):

            plt.plot(time, cohort[i], alpha=0.2)

        # average

        plt.plot(time, mean_growth, linewidth=3, label="Average Tumor Growth")

        plt.title("Virtual Patient Cohort Simulation")

        plt.xlabel("Weeks")

        plt.ylabel("Tumor Cell Count")

        plt.legend()

        plt.grid(True)

        plt.savefig("cohort_simulation.png")

        plt.close()
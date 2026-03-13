import numpy as np
import matplotlib.pyplot as plt


class TumorResistanceEngine:

    def __init__(self):

        # initial populations

        self.sensitive_cells = 9e5
        self.resistant_cells = 1e5

        # growth rates

        self.sensitive_growth = 0.025
        self.resistant_growth = 0.03

        # therapy killing effect

        self.therapy_kill = 0.04


    def simulate(self, weeks=52):

        time = np.arange(0, weeks)

        sensitive = []
        resistant = []

        S = self.sensitive_cells
        R = self.resistant_cells

        for t in time:

            # sensitive cells growth
            S_growth = self.sensitive_growth * S

            # therapy killing sensitive cells
            S_kill = self.therapy_kill * S

            S = S + S_growth - S_kill

            if S < 0:
                S = 0


            # resistant cells growth
            R_growth = self.resistant_growth * R

            R = R + R_growth


            sensitive.append(S)
            resistant.append(R)


        return time, sensitive, resistant


    def plot(self, time, sensitive, resistant):

        plt.figure(figsize=(8,5))

        plt.plot(time, sensitive, label="Drug Sensitive Cells")

        plt.plot(time, resistant, label="Drug Resistant Cells")

        plt.title("Tumor Resistance Evolution")

        plt.xlabel("Weeks")

        plt.ylabel("Cell Count")

        plt.legend()

        plt.grid(True)

        plt.savefig("tumor_resistance.png")

        plt.close()


    def run(self):

        time, S, R = self.simulate()

        self.plot(time, S, R)

        return time, S, R
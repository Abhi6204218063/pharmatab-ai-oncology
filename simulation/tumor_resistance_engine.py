import numpy as np
import matplotlib.pyplot as plt


class TumorResistanceEngine:

    def simulate(self):

        weeks = np.arange(0, 52)

        # sensitive tumor cells
        sensitive = 1e6 * np.exp(-0.01 * weeks)

        # resistant tumor cells
        resistant = 1e4 * np.exp(0.03 * weeks)

        total = sensitive + resistant

        plt.figure(figsize=(8,5))

        plt.plot(weeks, sensitive, label="Drug Sensitive Cells")

        plt.plot(weeks, resistant, label="Resistant Cells")

        plt.plot(weeks, total, label="Total Tumor Cells")

        plt.title("Tumor Resistance Evolution")

        plt.xlabel("Weeks")

        plt.ylabel("Cell Count")

        plt.legend()

        plt.grid(True)

        plt.savefig("tumor_resistance.png")

        plt.close()

        return sensitive, resistant, total


    def resistance_risk(self, resistant_cells):

        final_resistance = resistant_cells[-1]

        if final_resistance > 5e5:
            return "High probability of drug resistance"

        elif final_resistance > 1e5:
            return "Moderate resistance risk"

        else:
            return "Low resistance risk"
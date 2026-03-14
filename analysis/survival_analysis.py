import numpy as np
import matplotlib.pyplot as plt


class SurvivalAnalysis:

    def simulate(self):

        time = np.arange(0, 60)

        therapyA = np.exp(-0.03 * time)
        therapyB = np.exp(-0.05 * time)

        fig, ax = plt.subplots()

        ax.plot(time, therapyA, label="Therapy A")

        ax.plot(time, therapyB, label="Therapy B")

        ax.set_xlabel("Time (months)")

        ax.set_ylabel("Survival Probability")

        ax.set_title("Kaplan–Meier Survival Curve")

        ax.legend()

        return fig
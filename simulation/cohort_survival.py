import numpy as np
import matplotlib.pyplot as plt

class CohortSurvival:

    def simulate(self):

        time = np.arange(0,24)

        therapyA = np.exp(-0.05*time)
        therapyB = np.exp(-0.08*time)

        fig, ax = plt.subplots()

        ax.plot(time, therapyA, label="Therapy A")
        ax.plot(time, therapyB, label="Therapy B")

        ax.set_xlabel("Months")
        ax.set_ylabel("Survival Probability")

        ax.set_title("Cohort Survival Comparison")

        ax.legend()

        return fig
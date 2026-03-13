import numpy as np
import matplotlib.pyplot as plt


class KaplanMeierSurvival:

    def __init__(self):

        # number of patients

        self.n_patients = 200

        # baseline hazard

        self.base_hazard = 0.03


    def simulate_survival_times(self):

        """
        Generate survival times using exponential distribution
        """

        survival_times = np.random.exponential(
            scale=1/self.base_hazard,
            size=self.n_patients
        )

        # convert to weeks

        survival_times = survival_times * 10

        return survival_times


    def compute_km_curve(self, survival_times):

        """
        Compute Kaplan-Meier survival curve
        """

        times = np.sort(survival_times)

        n = len(times)

        survival_prob = []

        prob = 1

        for i in range(n):

            prob = prob * (1 - 1/(n-i))

            survival_prob.append(prob)

        return times, survival_prob


    def plot(self, times, survival_prob):

        plt.figure(figsize=(8,5))

        plt.step(times, survival_prob, where="post")

        plt.title("Kaplan-Meier Survival Curve")

        plt.xlabel("Time (weeks)")

        plt.ylabel("Survival Probability")

        plt.grid(True)

        plt.savefig("survival_curve.png")

        plt.close()


    def run(self):

        survival_times = self.simulate_survival_times()

        times, survival_prob = self.compute_km_curve(survival_times)

        self.plot(times, survival_prob)

        return times, survival_prob
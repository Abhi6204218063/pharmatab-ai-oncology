"""
PharmaTab
Model Layer - Tumor Growth Model

Purpose:
Simulate tumor growth using logistic growth dynamics.

Scientific Model:
dN/dt = rN(1 - N/K)

Where:
N = tumor population
r = growth rate
K = carrying capacity
"""

import numpy as np


class TumorGrowthModel:

    def __init__(self, growth_rate=0.03, carrying_capacity=1e9):

        """
        Parameters
        ----------
        growth_rate : float
            intrinsic tumor growth rate

        carrying_capacity : float
            maximum tumor size environment can sustain
        """

        self.r = growth_rate
        self.K = carrying_capacity


    def logistic_growth(self, population):

        """
        Logistic growth equation
        """

        growth = self.r * population * (1 - population / self.K)

        return growth


    def simulate(self, initial_population, time_steps):

        """
        Simulate tumor growth over time
        """

        population = initial_population

        population_history = []

        for t in range(time_steps):

            growth = self.logistic_growth(population)

            population = population + growth

            population_history.append(population)

        return population_history


    def simulate_with_noise(self, initial_population, time_steps, noise_level=0.01):

        """
        Simulate tumor growth with biological noise
        """

        population = initial_population

        history = []

        for t in range(time_steps):

            growth = self.logistic_growth(population)

            noise = np.random.normal(0, noise_level * population)

            population = population + growth + noise

            if population < 0:
                population = 0

            history.append(population)

        return history


    def estimate_growth_rate(self, population_series):

        """
        Estimate growth rate from observed data
        """

        population_series = np.array(population_series)

        diffs = np.diff(population_series)

        rates = diffs / population_series[:-1]

        return np.mean(rates)
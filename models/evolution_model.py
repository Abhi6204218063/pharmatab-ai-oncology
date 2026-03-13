"""
PharmaTab
Model Layer - Tumor Evolution Model

Purpose:
Simulate tumor evolution by combining:

1. Tumor growth dynamics
2. Mutation emergence
3. Resistant clone expansion
"""

import numpy as np

from models.tumor_growth_model import TumorGrowthModel
from models.mutation_model import MutationModel


class EvolutionModel:

    def __init__(
        self,
        growth_rate_sensitive=0.03,
        growth_rate_resistant=0.02,
        carrying_capacity=1e9,
        mutation_rate=1e-7
    ):

        self.growth_sensitive = TumorGrowthModel(
            growth_rate=growth_rate_sensitive,
            carrying_capacity=carrying_capacity
        )

        self.growth_resistant = TumorGrowthModel(
            growth_rate=growth_rate_resistant,
            carrying_capacity=carrying_capacity
        )

        self.mutation_model = MutationModel(mutation_rate)


    def simulate(
        self,
        sensitive_initial,
        resistant_initial,
        steps
    ):

        sensitive = sensitive_initial
        resistant = resistant_initial

        sensitive_history = []
        resistant_history = []
        total_history = []

        for t in range(steps):

            # tumor growth
            growth_s = self.growth_sensitive.logistic_growth(sensitive)
            growth_r = self.growth_resistant.logistic_growth(resistant)

            sensitive = sensitive + growth_s
            resistant = resistant + growth_r

            # mutation event
            sensitive, resistant = self.mutation_model.update_population(
                sensitive,
                resistant
            )

            total_population = sensitive + resistant

            sensitive_history.append(sensitive)
            resistant_history.append(resistant)
            total_history.append(total_population)

        return {
            "sensitive_cells": sensitive_history,
            "resistant_cells": resistant_history,
            "total_cells": total_history
        }


    def simulate_with_environment_noise(
        self,
        sensitive_initial,
        resistant_initial,
        steps,
        noise_level=0.02
    ):

        sensitive = sensitive_initial
        resistant = resistant_initial

        sensitive_history = []
        resistant_history = []

        for t in range(steps):

            growth_s = self.growth_sensitive.logistic_growth(sensitive)
            growth_r = self.growth_resistant.logistic_growth(resistant)

            noise_s = np.random.normal(0, noise_level * sensitive)
            noise_r = np.random.normal(0, noise_level * resistant)

            sensitive = sensitive + growth_s + noise_s
            resistant = resistant + growth_r + noise_r

            if sensitive < 0:
                sensitive = 0

            if resistant < 0:
                resistant = 0

            sensitive, resistant = self.mutation_model.update_population(
                sensitive,
                resistant
            )

            sensitive_history.append(sensitive)
            resistant_history.append(resistant)

        return {
            "sensitive_cells": sensitive_history,
            "resistant_cells": resistant_history
        }
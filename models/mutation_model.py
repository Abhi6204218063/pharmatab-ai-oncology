"""
PharmaTab
Model Layer - Mutation Model

Purpose:
Simulate mutation emergence in tumor cell populations.

Concept:
Sensitive tumor cells can mutate and become resistant cells.

Equation:
mutated_cells = mutation_rate * sensitive_cells
"""

import numpy as np


class MutationModel:

    def __init__(self, mutation_rate=1e-7):

        """
        Parameters
        ----------
        mutation_rate : float
            probability of mutation per cell division
        """

        self.mutation_rate = mutation_rate


    def compute_mutations(self, sensitive_cells):

        """
        Calculate number of cells that mutate
        """

        mutated_cells = sensitive_cells * self.mutation_rate

        return mutated_cells


    def update_population(self, sensitive_cells, resistant_cells):

        """
        Update populations after mutation
        """

        mutations = self.compute_mutations(sensitive_cells)

        new_sensitive = sensitive_cells - mutations

        new_resistant = resistant_cells + mutations

        return new_sensitive, new_resistant


    def stochastic_mutation(self, sensitive_cells):

        """
        Stochastic mutation using binomial distribution
        """

        mutated_cells = np.random.binomial(
            int(sensitive_cells),
            self.mutation_rate
        )

        return mutated_cells


    def simulate_mutation_step(self, sensitive_cells, resistant_cells):

        """
        Simulate one mutation step
        """

        mutated = self.stochastic_mutation(sensitive_cells)

        sensitive_cells = sensitive_cells - mutated

        resistant_cells = resistant_cells + mutated

        return sensitive_cells, resistant_cells
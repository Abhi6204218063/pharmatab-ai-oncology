"""
PharmaTab Spatial Tumor Simulator
2D tumor growth with drug diffusion
"""

import numpy as np


class SpatialTumorSimulator:

    def __init__(self,
                 grid_size=50,
                 initial_cells=100):

        self.grid_size = grid_size

        self.grid = np.zeros((grid_size, grid_size))

        # seed tumor cells in center
        center = grid_size // 2

        for _ in range(initial_cells):

            x = center + np.random.randint(-2, 2)
            y = center + np.random.randint(-2, 2)

            self.grid[x, y] = 1

        self.history = []


    def diffuse_drug(self,
                     drug_strength):

        """
        simulate drug diffusion
        """

        diffusion = drug_strength * np.random.rand(
            self.grid_size,
            self.grid_size
        )

        return diffusion


    def step(self,
             drug_strength):

        """
        simulate single time step
        """

        drug_field = self.diffuse_drug(drug_strength)

        new_grid = self.grid.copy()

        for i in range(1, self.grid_size - 1):

            for j in range(1, self.grid_size - 1):

                if self.grid[i, j] == 1:

                    # drug kill probability
                    if drug_field[i, j] > 0.7:

                        new_grid[i, j] = 0

                    else:

                        # tumor growth
                        if np.random.rand() < 0.2:

                            dx = np.random.randint(-1, 2)
                            dy = np.random.randint(-1, 2)

                            new_grid[i + dx, j + dy] = 1

        self.grid = new_grid

        self.history.append(np.sum(self.grid))


    def run_simulation(self,
                       drug_strength=0.3,
                       steps=50):

        for _ in range(steps):

            self.step(drug_strength)

        return {
            "tumor_size": self.history,
            "final_grid": self.grid
        }
"""
PharmaTab AI Guided Therapy Planner
Selects optimal therapy schedule
"""

import numpy as np


class TherapyPlanner:

    def __init__(self,
                 drugs=["DrugA", "DrugB", "Combo"]):

        self.drugs = drugs

        self.strategy_history = []


    def evaluate_state(self,
                       tumor_size,
                       resistant_fraction):

        """
        classify tumor state
        """

        if tumor_size < 1e6:
            return "small"

        elif resistant_fraction > 0.5:
            return "resistant"

        else:
            return "growing"


    def choose_therapy(self,
                       state):

        """
        select therapy based on tumor state
        """

        if state == "small":

            therapy = "DrugA"

        elif state == "resistant":

            therapy = "Combo"

        else:

            therapy = "DrugB"

        self.strategy_history.append(therapy)

        return therapy


    def simulate_response(self,
                          tumor_size,
                          therapy):

        """
        simple tumor response model
        """

        if therapy == "DrugA":

            tumor_size *= 0.8

        elif therapy == "DrugB":

            tumor_size *= 0.75

        elif therapy == "Combo":

            tumor_size *= 0.6

        tumor_size += tumor_size * 0.02

        return tumor_size


    def run_planner(self,
                    tumor_size,
                    resistant_fraction,
                    steps=30):

        history = []

        for _ in range(steps):

            state = self.evaluate_state(
                tumor_size,
                resistant_fraction
            )

            therapy = self.choose_therapy(state)

            tumor_size = self.simulate_response(
                tumor_size,
                therapy
            )

            history.append({
                "therapy": therapy,
                "tumor_size": tumor_size
            })

        return history
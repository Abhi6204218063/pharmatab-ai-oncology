"""
PharmaTab
Simulation Layer - Patient Simulator

Purpose:
Simulate tumor evolution and treatment response
for a virtual patient.

Pipeline:
Tumor Evolution → Resistance Prediction → Therapy Optimization
"""

from models.evolution_model import EvolutionModel
from ai.resistance_predictor import ResistancePredictor
from ai.therapy_optimizer import TherapyOptimizer


class PatientSimulator:

    def __init__(self):

        self.evolution_model = EvolutionModel()

        self.resistance_predictor = ResistancePredictor()

        self.therapy_optimizer = TherapyOptimizer()


    def simulate_patient(
        self,
        sensitive_initial=1e6,
        resistant_initial=100,
        steps=100
    ):

        """
        Run full tumor evolution simulation
        """

        evolution_result = self.evolution_model.simulate(
            sensitive_initial,
            resistant_initial,
            steps
        )

        sensitive_history = evolution_result["sensitive_cells"]
        resistant_history = evolution_result["resistant_cells"]
        total_history = evolution_result["total_cells"]


        # Train resistance predictor
        self.resistance_predictor.train(
            sensitive_history,
            resistant_history
        )


        resistance_info = self.resistance_predictor.detect_resistance_time(
            sensitive_history,
            resistant_history
        )


        therapy_schedule = self.therapy_optimizer.adaptive_strategy(
            sensitive_history,
            resistant_history
        )


        result = {
            "tumor_history": total_history,
            "sensitive_cells": sensitive_history,
            "resistant_cells": resistant_history,
            "resistance_prediction": resistance_info,
            "therapy_schedule": therapy_schedule
        }

        return result


    def simulate_multiple_patients(
        self,
        patient_count=10,
        steps=100
    ):

        """
        Generate virtual patient population
        """

        simulations = []

        for i in range(patient_count):

            result = self.simulate_patient(
                sensitive_initial=1e6,
                resistant_initial=100,
                steps=steps
            )

            simulations.append(result)

        return simulations
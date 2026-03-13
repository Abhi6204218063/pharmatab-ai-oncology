"""
PharmaTab Cloud Simulation Engine
Runs large scale virtual patient simulations
"""

import numpy as np
from multiprocessing import Pool

from simulation.digital_patient_model import DigitalPatientModel


def simulate_single_patient(params):

    tumor = params["tumor"]
    immune = params["immune"]
    drug = params["drug"]

    patient = DigitalPatientModel(
        tumor_cells=tumor,
        immune_cells=immune
    )

    result = patient.run_simulation(
        drug_dose=drug,
        steps=50
    )

    final_tumor = result["tumor"][-1]

    return final_tumor


class CloudSimulationEngine:

    def __init__(self,
                 patient_count=100):

        self.patient_count = patient_count


    def generate_population(self):

        patients = []

        for _ in range(self.patient_count):

            tumor = np.random.uniform(1e6, 1e8)
            immune = np.random.uniform(1e5, 1e7)
            drug = np.random.uniform(0.2, 0.6)

            patients.append({
                "tumor": tumor,
                "immune": immune,
                "drug": drug
            })

        return patients


    def run_parallel_simulation(self):

        patients = self.generate_population()

        with Pool() as pool:

            results = pool.map(
                simulate_single_patient,
                patients
            )

        return results


    def summarize_results(self,
                          results):

        return {
            "average_final_tumor": float(np.mean(results)),
            "min_tumor": float(np.min(results)),
            "max_tumor": float(np.max(results))
        }
"""
PharmaTab Distributed Simulation Platform
"""

import numpy as np
from multiprocessing import Pool


def simulate_patient(params):

    tumor = params["tumor"]
    immune = params["immune"]
    drug = params["drug"]

    # simple tumor update
    for _ in range(50):

        growth = tumor * 0.03

        drug_kill = drug * tumor * 0.02

        immune_kill = immune * 0.00001

        tumor = tumor + growth - drug_kill - immune_kill

        if tumor < 0:
            tumor = 0

    return tumor


class DistributedSimulation:

    def __init__(self, patient_count=1000):

        self.patient_count = patient_count


    def generate_patients(self):

        patients = []

        for _ in range(self.patient_count):

            patients.append({
                "tumor": np.random.uniform(1e6, 1e8),
                "immune": np.random.uniform(1e5, 1e7),
                "drug": np.random.uniform(0.2, 0.6)
            })

        return patients


    def run(self):

        patients = self.generate_patients()

        with Pool() as pool:

            results = pool.map(simulate_patient, patients)

        return results


    def summarize(self, results):

        return {
            "average_tumor": float(np.mean(results)),
            "min_tumor": float(np.min(results)),
            "max_tumor": float(np.max(results))
        }
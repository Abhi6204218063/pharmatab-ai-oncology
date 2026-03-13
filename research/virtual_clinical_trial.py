"""
PharmaTab Research Module
Virtual Clinical Trial Simulator
"""

import numpy as np

from research.digital_twin import DigitalTumorTwin


class VirtualClinicalTrial:

    def __init__(self,
                 patient_count=100):

        self.patient_count = patient_count


    def generate_patients(self):

        """
        Generate virtual patient population
        """

        patients = []

        for i in range(self.patient_count):

            growth_rate = np.random.uniform(0.02, 0.05)

            mutation_rate = np.random.uniform(1e-8, 1e-6)

            drug_sensitivity = np.random.uniform(0.1, 0.4)

            twin = DigitalTumorTwin(
                growth_rate,
                mutation_rate,
                drug_sensitivity
            )

            patients.append(twin)

        return patients


    def run_trial(self,
                  drug_dose,
                  steps=50):

        patients = self.generate_patients()

        responses = []

        for patient in patients:

            result = patient.simulate_therapy(
                initial_size=1e6,
                drug_dose=drug_dose,
                steps=steps
            )

            final_tumor = result[-1]

            responses.append(final_tumor)

        return responses


    def trial_summary(self,
                      drug_dose):

        results = self.run_trial(drug_dose)

        avg_tumor = np.mean(results)

        responders = [r for r in results if r < 1e6]

        response_rate = len(responders) / len(results)

        return {
            "average_final_tumor": float(avg_tumor),
            "response_rate": float(response_rate),
            "patients": len(results)
        }
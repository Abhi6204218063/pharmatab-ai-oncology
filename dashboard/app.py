"""
PharmaTab Research Dashboard
"""

import sys
import os
import streamlit as st

sys.path.append(os.path.obspath(os.path.join(os.path.dirname(__file__), '..')))

from research.digital_twin import DigitalTumorTwin
from research.virtual_clinical_trial import VirtualClinicalTrial
from research.therapy_simulator import TherapySimulator
from research.mutation_predictor import MutationPredictor
from research.evolution_forecast import EvolutionForecast


st.title("PharmaTab Oncology Simulation Platform")


st.sidebar.header("Simulation Parameters")

growth_rate = st.sidebar.slider(
    "Tumor Growth Rate",
    0.01, 0.1, 0.03
)

mutation_rate = st.sidebar.slider(
    "Mutation Rate",
    0.00000001,
    0.000001,
    0.0000001
)

drug_dose = st.sidebar.slider(
    "Drug Dose",
    0.1,
    0.8,
    0.3
)


if st.button("Run Tumor Simulation"):

    twin = DigitalTumorTwin(
        growth_rate=growth_rate,
        mutation_rate=mutation_rate,
        drug_sensitivity=drug_dose
    )

    tumor_history = twin.simulate_growth(
        tumor_size=1e6,
        steps=50
    )

    st.subheader("Tumor Growth")

    st.line_chart(tumor_history)



if st.button("Run Virtual Clinical Trial"):

    trial = VirtualClinicalTrial(
        patient_count=100
    )

    summary = trial.trial_summary(
        drug_dose=drug_dose
    )

    st.subheader("Trial Results")

    st.json(summary)



if st.button("Compare Therapies"):

    sim = TherapySimulator()

    result = sim.compare_therapies(
        drug_a=0.3,
        drug_b=0.5
    )

    st.subheader("Therapy Comparison")

    st.json(result)



if st.button("Predict Mutation Risk"):

    predictor = MutationPredictor()

    predictor.train()

    result = predictor.predict_resistance(
        tumor_size=1e7,
        mutation_rate=mutation_rate,
        growth_rate=growth_rate
    )

    st.subheader("Mutation Prediction")

    st.json(result)



if st.button("Forecast Tumor Evolution"):

    forecast = EvolutionForecast()

    tumor_history = [
        1000000,
        1200000,
        1400000,
        1700000
    ]

    forecast.train(tumor_history)

    future = forecast.forecast(
        current_tumor=1700000,
        steps=10
    )

    st.subheader("Future Tumor Prediction")

    st.line_chart(future)
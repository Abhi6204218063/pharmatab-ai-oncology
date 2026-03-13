"""
PharmaTab Integrated Simulation Control Center
"""

import sys
import os
import streamlit as st
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulation.digital_patient_model import DigitalPatientModel
from simulation.cloud_simulation_engine import CloudSimulationEngine
from ai.meta_learning_engine import MetaLearningEngine
from simulation.multiclone_tumor_model import MultiCloneTumorModel
from ai.rl_therapy_optimizer import RLTherapyOptimizer
from models.genome_mutation_simulator import GenomeMutationSimulator
from ai.cancer_evolution_predictor import CancerEvolutionPredictor
from simulation.distributed_simulation import DistributedSimulation
from ai.drug_discovery_engine import DrugDiscoveryEngine
from data_layer.vcf_parser import VCFParser
from ai.mutation_therapy_mapper import MutationTherapyMapper
from ai.treatment_plan_generator import TreatmentPlanGenerator
from utils.pdf_exporter import PDFExporter
from ai.clinical_reasoning_engine import ClinicalReasoningEngine
from simulation.digital_patient_twin import DigitalPatientTwin

st.title("PharmaTab Simulation Control Center")


st.sidebar.header("Patient Parameters")

uploaded_file = st.sidebar.file_uploader(
    "Upload Patient Dataset",
    type=["csv", "xlsx", "json"]
)
import pandas as pd

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".xlsx"):
        data = pd.read_excel(uploaded_file)

    else:
        data = pd.read_json(uploaded_file)

    st.subheader("Uploaded Dataset")

    st.write(data.head())
    
vcf_file = st.sidebar.file_uploader(
    "Upload Genomic Mutation File (VCF)",
    type=["vcf"]
)

initial_tumor = st.sidebar.slider(
    "Initial Tumor Cells",
    100000,
    10000000,
    1000000
)

immune_cells = st.sidebar.slider(
    "Immune Cells",
    100000,
    10000000,
    500000
)

tumor_size = st.sidebar.slider(
    "Initial Tumor Cells",
    1_000_000,
    100_000_000,
    10_000_000
)

immune_cells = st.sidebar.slider(
    "Immune Cells",
    100_000,
    10_000_000,
    1_000_000
)

drug_dose = st.sidebar.slider(
    "Drug Dose",
    0.0,
    1.0,
    0.4
)


if st.button("Run Single Patient Simulation"):

    patient = DigitalPatientModel(
        tumor_cells=tumor_size,
        immune_cells=immune_cells
    )

    result = patient.run_simulation(
        drug_dose=drug_dose,
        steps=50
    )

    st.subheader("Tumor Evolution")

    st.line_chart(result["tumor"])

    st.subheader("Drug Resistance Evolution")

    st.line_chart(result["resistance"])


if st.button("Run Population Simulation"):

    engine = CloudSimulationEngine(
        patient_count=200
    )

    results = engine.run_parallel_simulation()

    avg = np.mean(results)

    st.subheader("Population Outcome")

    st.write("Average final tumor:", avg)


if st.button("AI Therapy Recommendation"):

    ai = MetaLearningEngine()

    ai.train()

    therapy = ai.predict_therapy(
        tumor_size=tumor_size,
        immune_level=immune_cells,
        resistance=0.3
    )

    st.subheader("AI Recommended Therapy")

    st.write(therapy)

if st.button("Run Multi-Clone Simulation"):

    model = MultiCloneTumorModel()

    result = model.run(drug_dose=drug_dose)

    st.subheader("Total Tumor")
    st.line_chart(result["total"])

    st.subheader("Clone Evolution")

    st.line_chart({
        "Sensitive": result["sensitive"],
        "Moderate": result["moderate"],
        "Resistant": result["resistant"]
    })

if st.button("RL Therapy Optimization"):

    agent = RLTherapyOptimizer()

    agent.train()

    therapy = agent.recommend(tumor_size)

    st.write("RL Recommended Therapy:", therapy)

if st.button("Run Genome Evolution Simulation"):

    sim = GenomeMutationSimulator()

    result = sim.run()

    st.subheader("Tumor Growth (Genomic Evolution)")
    st.line_chart(result["tumor"])

    st.subheader("Driver Mutations")
    st.line_chart(result["driver"])

    st.subheader("Passenger Mutations")
    st.line_chart(result["passenger"])

if st.button("Predict Tumor Evolution"):

    history = [1e6, 1.2e6, 1.5e6, 1.8e6, 2.2e6]

    predictor = CancerEvolutionPredictor()

    predictor.train(history)

    future = predictor.predict_future(
        current_tumor=2.2e6
    )

    st.subheader("Predicted Tumor Evolution")

    st.line_chart(future)

if st.button("Run Large Scale Simulation"):

    sim = DistributedSimulation(patient_count=500)

    results = sim.run()

    summary = sim.summarize(results)

    st.subheader("Distributed Simulation Results")

    st.json(summary)

if st.button("Run AI Analysis"):

    tumor_size = data["tumor_size"].values
    immune = data["immune_cells"].values

    st.write("Dataset Loaded Successfully")

if vcf_file is not None:

    with open("temp.vcf", "wb") as f:
        f.write(vcf_file.read())

    parser = VCFParser("temp.vcf")

    mutations = parser.parse()

    st.subheader("Detected Mutations")

    st.write(mutations[:10])

if st.button("Analyze Mutations for Therapy"):

    mapper = MutationTherapyMapper()

    therapy = mapper.recommend_therapy(mutations)

    st.subheader("Recommended Therapies")

    st.write(therapy)

if st.button("Generate Treatment Plan"):

    mutations = ["EGFR", "PI3K"]

    therapies = ["Erlotinib", "Alpelisib"]

    generator = TreatmentPlanGenerator()

    plan = generator.generate_plan(mutations, therapies)

    st.subheader("AI Generated Treatment Plan")

    st.text(plan)

    exporter = PDFExporter()

    filename = exporter.export_plan(plan)

    with open(filename, "rb") as f:

        st.download_button(
            "Download PDF Treatment Plan",
            f,
            file_name="PharmaTab_Treatment_Plan.pdf"
        )

if st.button("Generate Clinical Reasoning Report"):

    engine = ClinicalReasoningEngine()

    report = engine.generate_reasoning(
        mutations=["EGFR","PI3K"],
        tumor_stage=2,
        immune_level=600000
    )

    st.subheader("AI Clinical Reasoning")

    st.text(report)

if st.button("Run Digital Twin Simulation"):

    patient = DigitalPatientTwin(
        tumor_cells=initial_tumor,
        immune_cells=immune_cells
    )

    result = patient.simulate()

    st.subheader("Digital Patient Twin Simulation")

    st.line_chart(result)                                             
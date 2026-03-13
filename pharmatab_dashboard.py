import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from ai.mutation_detector import MutationDetector
from ai.therapy_mapper import MutationTherapyMapper
from ai.therapy_optimizer import TherapyOptimizer

from simulation.tumor_evolution_engine import TumorEvolutionEngine
from simulation.resistance_engine import TumorResistanceEngine
from simulation.cohort_simulator import VirtualCohortSimulator
from simulation.kalpan_meier_survival import KaplanMeierSurvival

from utils.pdf_exporter import PDFExporter


st.set_page_config(
    page_title="PharmaTab AI Oncology Platform",
    layout="wide"
)

st.title("PharmaTab AI Oncology Platform")

st.write(
"""
AI-driven oncology simulation platform for mutation analysis,
therapy optimization, tumor evolution modeling and survival prediction.
"""
)

# ---------------------------------------------------
# Upload Dataset
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload mutation dataset (CSV, TSV or TXT)",
    type=["csv", "tsv", "txt"]
)

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file, sep="\t", comment="#")
    except:
        df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # ---------------------------------------------------
    # Mutation Detection
    # ---------------------------------------------------

    st.subheader("Mutation Detection")

    detector = MutationDetector()
    mutations = detector.detect_mutations(df)

    st.write("Detected Mutations")
    st.write(mutations)

    # ---------------------------------------------------
    # Therapy Mapping
    # ---------------------------------------------------

    st.subheader("Therapy Mapping")

    mapper = MutationTherapyMapper()
    therapies = mapper.map_therapies(mutations)

    st.write("Candidate Therapies")
    st.write(therapies)

    # ---------------------------------------------------
    # Therapy Optimization
    # ---------------------------------------------------

    st.subheader("Therapy Optimization")

    optimizer = TherapyOptimizer()
    best_plan = optimizer.optimize(therapies)

    st.write("Optimized Treatment Plan")
    st.write(best_plan)

    # ---------------------------------------------------
    # Tumor Evolution Simulation
    # ---------------------------------------------------

    st.subheader("Tumor Evolution Simulation")

    tumor_engine = TumorEvolutionEngine()
    tumor_result = tumor_engine.simulate(best_plan)

    fig1, ax1 = plt.subplots()

    ax1.plot(tumor_result)
    ax1.set_title("Tumor Evolution Over Time")

    st.pyplot(fig1)

    # ---------------------------------------------------
    # Resistance Prediction
    # ---------------------------------------------------

    st.subheader("Resistance Evolution Prediction")

    resistance_engine = TumorResistanceEngine()
    resistance = resistance_engine.predict(best_plan)

    fig2, ax2 = plt.subplots()

    ax2.plot(resistance)
    ax2.set_title("Drug Resistance Evolution")

    st.pyplot(fig2)

    # ---------------------------------------------------
    # Virtual Cohort Simulation
    # ---------------------------------------------------

    st.subheader("Virtual Clinical Trial Simulation")

    cohort_sim = VirtualCohortSimulator()
    cohort_results = cohort_sim.run_simulation(best_plan)

    st.write("Virtual Patient Cohort Outcomes")
    st.write(cohort_results.head())

    # ---------------------------------------------------
    # Kaplan-Meier Survival
    # ---------------------------------------------------

    st.subheader("Kaplan-Meier Survival Analysis")

    km = KaplanMeierSurvival()
    survival_curve = km.run_analysis(cohort_results)

    st.pyplot(survival_curve)

    # ---------------------------------------------------
    # PDF Clinical Report
    # ---------------------------------------------------

    st.subheader("Clinical Report")

    pdf = PDFExporter()

    report_path = pdf.generate(
        mutations,
        therapies,
        best_plan
    )

    with open(report_path, "rb") as f:
        st.download_button(
            "Download Clinical Report",
            f,
            file_name="pharmatab_report.pdf"
        )
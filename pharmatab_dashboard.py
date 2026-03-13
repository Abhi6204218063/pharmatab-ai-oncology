import streamlit as st
import pandas as pd
import os
import io
import matplotlib.pyplot as plt

from ai.mutation_detector import MutationDetector
from ai.therapy_mapper import MutationTherapyMapper
from ai.therapy_optimizer import TherapyOptimizer

from simulation.tumor_evolution_engine import TumorEvolutionEngine
from simulation.resistance_engine import TumorResistanceEngine
from simulation.cohort_simulator import VirtualCohortSimulator
from simulation.kalpan_meier_survival import KaplanMeierSurvival

from utils.pdf_exporter import PDFExporter


st.set_page_config(page_title="PharmaTab AI Oncology Platform", layout="wide")

st.title("PharmaTab AI Oncology Platform")

# ---------- SIDEBAR ----------

menu = st.sidebar.selectbox(

    "Navigation",

    [

        "Home",
        "Upload Patient Data",
        "Mutation Analysis",
        "Therapy Recommendation",
        "Run Simulation",
        "Results",
        "Generate Clinical Report",
        "About"

    ]

)

# ---------- HOME ----------

if menu == "Home":

    st.header("Welcome to PharmaTab")

    st.write("""
AI-driven oncology simulation platform integrating
genomic mutation analysis, therapy optimization,
tumor evolution modeling and survival prediction.
""")


# ---------- UPLOAD DATA ----------

elif menu == "Upload Patient Data":

    st.header("Upload Mutation Dataset")

    uploaded_file = st.file_uploader(
    "Upload mutation dataset (CSV or TSV)",
    type=["csv", "tsv"]
    )

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file, sep=None, engine="python")
        except:
            df = pd.read_csv(uploaded_file)

    st.write("Preview of dataset")
    st.dataframe(df.head())

    st.write("Preview of dataset")
    st.dataframe(df.head())

    detector = MutationDetector()

    genes = detector.detect_mutations(df)

    st.success("Detected mutations:")
    st.write(genes)


# ---------- MUTATION ANALYSIS ----------

elif menu == "Mutation Analysis":

    st.header("Mutation Detection")

    if "patient_data" in st.session_state:

        detector = MutationDetector()

        df = st.session_state["patient_data"]

        genes = detector.detect_mutations(df)

        drivers = detector.detect_driver_mutations(genes)

        st.write("Detected genes")

        st.write(genes)

        st.write("Driver mutations")

        st.write(drivers)

        st.session_state["drivers"] = drivers

    else:

        st.warning("Upload dataset first")


# ---------- THERAPY RECOMMENDATION ----------

elif menu == "Therapy Recommendation":

    st.header("Therapy Mapping")

    if "drivers" in st.session_state:

        mapper = MutationTherapyMapper()

        therapies = mapper.map_therapies(st.session_state["drivers"])

        st.write("Recommended therapies")

        st.write(therapies)

        st.session_state["therapies"] = therapies

    else:

        st.warning("Run mutation analysis first")


# ---------- RUN SIMULATION ----------

elif menu == "Run Simulation":

    st.header("Run Oncology Simulations")

    if st.button("Start Simulation"):

        # tumor evolution

        tumor_engine = TumorEvolutionEngine()

        tumor_engine.run()

        # resistance

        res_engine = TumorResistanceEngine()

        res_engine.run()

        # cohort

        cohort = VirtualCohortSimulator()

        cohort.run()

        # survival

        surv = KaplanMeierSurvival()

        surv.run()

        st.success("Simulation completed")


# ---------- RESULTS ----------

elif menu == "Results":

    st.header("Simulation Results")

    if os.path.exists("tumor_simulation.png"):

        st.subheader("Tumor Evolution")

        st.image("tumor_simulation.png")

    if os.path.exists("tumor_resistance.png"):

        st.subheader("Resistance Evolution")

        st.image("tumor_resistance.png")

    if os.path.exists("cohort_simulation.png"):

        st.subheader("Virtual Cohort")

        st.image("cohort_simulation.png")

    if os.path.exists("survival_curve.png"):

        st.subheader("Kaplan-Meier Survival")

        st.image("survival_curve.png")


# ---------- REPORT ----------

elif menu == "Generate Clinical Report":

    st.header("Generate Oncology Report")

    if "drivers" in st.session_state and "therapies" in st.session_state:

        report_text = f"""
PharmaTab AI Oncology Report

Detected Driver Mutations
{st.session_state['drivers']}

Recommended Therapies
{st.session_state['therapies']}
"""

        pdf = PDFExporter()

        pdf.export(report_text)

        st.success("Report generated")

        with open("treatment_plan.pdf","rb") as f:

            st.download_button(

                "Download Report",
                f,
                file_name="treatment_plan.pdf"

            )

    else:

        st.warning("Run mutation and therapy analysis first")


# ---------- ABOUT ----------

elif menu == "About":

    st.header("About PharmaTab")

    st.write("""
PharmaTab is a computational oncology platform for
precision cancer therapy simulation combining genomic
mutation analysis, therapy optimization and tumor evolution modeling.
""")
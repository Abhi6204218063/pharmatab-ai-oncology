import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from ai.mutation_detector import MutationDetector
from ai.therapy_mapper import MutationTherapyMapper
from ai.therapy_optimizer import TherapyOptimizer
from ai.survival_predictor import SurvivalPredictor

from simulation.tumor_evolution_engine import TumorEvolutionEngine
from simulation.resistance_engine import TumorResistanceEngine
from simulation.cohort_simulator import VirtualCohortSimulator
from simulation.kalpan_meier_survival import KaplanMeierSurvival
from simulation.cohort_survival import CohortSurvival

from visualization.oncoprint import OncoPrint
from visualization.mutation_heatmap import MutationHeatmap

from data_sources.cbioportal_api import CBioPortalAPI
from data_sources.clinical_trials_api import ClinicalTrialsAPI

from explorer.gene_explorer import GeneExplorer
from clinical_trials.trial_matcher import TrialMatcher

from utils.pdf_exporter import PDFExporter

# --------------------------------------------------------
# Page config
# --------------------------------------------------------

st.set_page_config(
    page_title="PharmaTab AI Oncology Platform",
    layout="wide"
)

# --------------------------------------------------------
# Tempus-style UI
# --------------------------------------------------------

st.markdown("""
<style>

.stApp {
background: radial-gradient(circle at 20% 20%, #0b132b, #000000);
background-size: 400% 400%;
animation: gradientMove 15s ease infinite;
}

@keyframes gradientMove {
0% {background-position:0% 50%;}
50% {background-position:100% 50%;}
100% {background-position:0% 50%;}
}

h1,h2,h3{
color:#6dd3ff;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# Title
# --------------------------------------------------------

st.title("PharmaTab AI Oncology Platform")
st.caption("Precision Oncology Simulation System")

# --------------------------------------------------------
# Sidebar navigation
# --------------------------------------------------------
st.sidebar.title("PharmaTab AI")

menu = st.sidebar.radio(
"Navigation",
[
"About Platform",
"Load Public Dataset",
"Upload Patient Data",
"Mutation Explorer",
"Therapy Recommendation",
"Survival Prediction",
"Clinical Trials"
]
)

# --------------------------------------------------------
# session state
# --------------------------------------------------------

if "dataset" not in st.session_state:
    st.session_state.dataset=None

if "mutations" not in st.session_state:
    st.session_state.mutations=None

if "therapy" not in st.session_state:
    st.session_state.therapy=None

# --------------------------------------------------------
# HOME
# --------------------------------------------------------

if menu=="Home":

    st.header("Precision Oncology Research Platform")

    st.write("""
PharmaTab is an AI-driven oncology simulation platform designed to analyze
cancer genomic mutations and model therapeutic responses.

The platform integrates multiple computational modules including:

• Mutation detection  
• Therapy mapping  
• Therapy optimization  
• Tumor evolution simulation  
• Drug resistance modeling  
• Virtual cohort simulation  
• Survival outcome modeling  

These modules are connected through a unified pipeline to simulate
personalized treatment strategies based on genomic data.

PharmaTab enables researchers to explore how genomic alterations influence
therapy response and patient survival outcomes.

The system supports integration with public cancer datasets such as
TCGA and cBioPortal and can simulate therapy responses under different
treatment strategies.

This platform is designed for computational oncology research and
precision medicine modeling.
""")

# --------------------------------------------------------
# PUBLIC DATASET LOADER
# --------------------------------------------------------

if menu=="Load Public Dataset":

    st.header("Load TCGA Mutation Dataset")

    if st.button("Load Data From cBioPortal"):

        api=CBioPortalAPI()

        df=api.get_mutations()

        if df is None or df.empty:
            st.error("No data returned from cBioPortal")

        else:
            st.session_state.dataset=df

            st.success("Dataset Loaded")

            st.dataframe(df.head())

# --------------------------------------------------------
# UPLOAD DATA
# --------------------------------------------------------

if menu=="Upload Patient Data":

    st.header("Upload Mutation Dataset")

    uploaded_file=st.file_uploader(
    "Upload CSV / TSV / TXT mutation dataset",
    type=["csv","tsv","txt"]
    )

    if uploaded_file:

        try:

            if uploaded_file.name.endswith(".tsv"):

                df=pd.read_csv(uploaded_file,sep="\t")

            else:

                df=pd.read_csv(uploaded_file)

            st.session_state.dataset=df

            st.success("Dataset Loaded")

            st.dataframe(df.head())

        except:

            st.error("Dataset loading failed")

    if menu=="Mutation Explorer":

        st.header("Mutation Gene Explorer")

    if "dataset" in st.session_state:

        explorer = GeneExplorer()

        genes = explorer.top_genes(st.session_state.dataset)

        st.dataframe(genes)

    else:
        st.warning("Load dataset first")        

# --------------------------------------------------------
# MUTATION ANALYSIS
# --------------------------------------------------------

if menu=="Mutation Analysis":

    if st.session_state.dataset is None:

        st.warning("Load dataset first")

    else:

        st.header("Mutation Detection")

        detector=MutationDetector()

        mutations=detector.detect_mutations(
        st.session_state.dataset
        )

        st.session_state.mutations=mutations

        st.subheader("Detected Mutations")

        st.dataframe(mutations)

        st.subheader("Mutation Visualization")

        onco=OncoPrint()

        fig=onco.plot(mutations)

        if fig:
            st.pyplot(fig)

        heat = MutationHeatmap()
        fig = heat.plot(mutations)

        if fig:
            st.pyplot(fig)    

    if menu=="Clinical Trials":

        st.header("Clinical Trial Finder")

        gene = st.text_input("Enter Gene")

    if gene:

        matcher = TrialMatcher()

        trials = matcher.search_trials(gene)

        st.dataframe(trials)       

# --------------------------------------------------------
# THERAPY RECOMMENDATION
# --------------------------------------------------------

if menu=="Therapy Recommendation":

    if st.session_state.mutations is None:

        st.warning("Run mutation analysis first")

    else:

        st.header("Therapy Mapping")

        mapper=MutationTherapyMapper()

        therapy_options=mapper.map_therapies(
        st.session_state.mutations
        )

        st.write("Therapy Options")

        st.dataframe(therapy_options)

        st.header("Therapy Optimization")

        optimizer=TherapyOptimizer()

        best_plan=optimizer.optimize(
        therapy_options
        )

        st.session_state.therapy=best_plan

        st.write("Recommended Therapy")

        st.write(best_plan)

# --------------------------------------------------------
# TUMOR SIMULATION
# --------------------------------------------------------

if menu=="Tumor Simulation":

    if st.session_state.therapy is None:

        st.warning("Generate therapy recommendation first")

    else:

        st.header("Tumor Evolution Simulation")
        import io

        tumor_engine=TumorEvolutionEngine()

        sim=tumor_engine.simulate(
        st.session_state.therapy
        )
        fig, ax = plt.subplots()
        ax.plot(sim)
        ax.set_title("Tumor Evolution Simulation")
        st.pyplot(fig)

        tumor_buffer = io.BytesI0()
        fig.savefig(tumor_buffer, format="png")
        tumor_buffer.seek(0)
        st.session_state.tumor_plot = tumor_buffer

        st.header("Drug Resistance Prediction")

        res_engine=TumorResistanceEngine()

        resistance=res_engine.predict(
        st.session_state.therapy
        )

        st.write(resistance)

        st.header("Virtual Cohort Simulation")

        cohort=VirtualCohortSimulator()

        cohort_results=cohort.run_simulation(
        st.session_state.therapy
        )

        st.dataframe(cohort_results.head())

# --------------------------------------------------------
# SURVIVAL ANALYSIS
# --------------------------------------------------------

if menu=="Survival Analysis":

    if st.session_state.dataset is None:

        st.warning("Load dataset first")

    else:

        st.header("Kaplan-Meier Survival Analysis")
        import io

        km=KaplanMeierSurvival()

        fig=km.run_analysis(
        st.session_state.dataset
        )
        st.pyplot(fig)
        survival_buffer = io.BytesI0()
        fig.savefig(survival_buffer, format="png")
        survival_buffer.seek(0)

        st.session_state.survival_plot = survival_buffer

        cohort = CohortSurvival()
        fig = cohort.simulate()
        st.pyplot(fig)

# --------------------------------------------------------
# CLINICAL TRIALS
# --------------------------------------------------------

if menu == "Clinical Trials":

    st.header("Clinical Trials Search")

    condition = st.text_input("Enter cancer type")

    if st.button("Search Trials"):

        api = ClinicalTrialsAPI()

        trials = api.search_trials(condition)

        if trials.empty:

            st.warning("No trials found")

        else:

            st.dataframe(trials)

            st.success(f"{len(trials)} trials found")   

# --------------------------------------------------------
# CLINICAL REPORT
# --------------------------------------------------------

if menu=="Clinical Report":

    st.header("Generate Clinical Report")

    if "dataset" in st.session_state:

        pdf = PDFExporter()

        report = pdf.generate_report(
            st.session_state.dataset
        )

        st.download_button(
            "Download Report",
            report,
            "pharmatab_report.pdf"
        )

# --------------------------------------------------------
# ABOUT
# --------------------------------------------------------

if menu=="About":

    st.title("About PharmaTab")

    st.markdown("""
PharmaTab is a computational precision oncology platform designed
to simulate cancer treatment strategies using genomic mutation data.

The system integrates multiple AI-driven modules to model the
interaction between tumor genomics and therapeutic interventions.

Core components include:

Mutation Detection Engine  
Therapy Mapping Engine  
Therapy Optimization Engine  
Tumor Evolution Simulator  
Resistance Prediction Model  
Virtual Cohort Simulation  
Kaplan-Meier Survival Analysis  

These modules work together to simulate how different therapies
may influence tumor progression and survival outcomes.

The platform supports integration with public cancer genomics
resources including TCGA and cBioPortal and can be extended
to include drug response prediction and clinical trial matching.

PharmaTab provides a research environment for computational
oncology and precision medicine modeling.
""")
    
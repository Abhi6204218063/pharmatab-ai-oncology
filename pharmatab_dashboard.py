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
"Clinical Trials",
"Clinical Report"
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

if "trials" not in st.session_state:
    st.session_state.trials=None    

# --------------------------------------------------------
# HOME
# --------------------------------------------------------

if menu=="Home":

    st.header("Precision Oncology Research Platform")

    st.markdown("""
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

        st.header("Mutation Explorer")

    if st.session_state.dataset is None:
        st.warning("Load dataset first")

    else:

        df=st.session_state.dataset

        gene_counts=df["geneSymbol"].value_counts().head(20)

        st.bar_chart(gene_counts)

        selected_gene=st.selectbox(
            "Select gene",
            gene_counts.index
        )

        st.session_state.selected_gene=selected_gene     

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

    st.header("Targeted Therapy Suggestions")

    if "selected_gene" not in st.session_state:

        st.warning("Select gene in Mutation Explorer")

    else:

        gene=st.session_state.selected_gene

        therapy_map={
            "BRCA1":"PARP inhibitors",
            "BRCA2":"PARP inhibitors",
            "EGFR":"EGFR inhibitors",
            "KRAS":"MEK inhibitors",
            "PIK3CA":"PI3K inhibitors",
        }

        therapy=therapy_map.get(gene,"Standard chemotherapy")

        st.session_state.therapy=therapy

        st.success(f"Recommended therapy: {therapy}")

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

# -------------------------------------------------------
# SURVIVAL PREDICTION
# -------------------------------------------------------

if menu=="Survival Prediction":

    st.header("Survival Prediction")

    age=st.slider("Patient Age",20,90)

    stage=st.selectbox(
        "Cancer Stage",
        ["Stage I","Stage II","Stage III","Stage IV"]
    )

    if st.button("Predict Survival"):

        score=100-age

        if stage=="Stage IV":
            score-=40

        survival=max(score,10)

        st.metric(
            "Estimated Survival Probability",
            f"{survival}%"
        )        

# --------------------------------------------------------
# CLINICAL TRIALS
# --------------------------------------------------------

if menu=="Clinical Trials":

    st.header("Clinical Trial Finder")

    condition=st.text_input("Enter cancer type")

    if st.button("Search Trials"):

        matcher=TrialMatcher()

        trials=matcher.search_trials(condition)

        st.session_state.trials=trials

        st.dataframe(trials)   

# --------------------------------------------------------
# CLINICAL REPORT
# --------------------------------------------------------

if menu=="Clinical Report":

    st.header("Clinical Oncology Report")

    if st.session_state.dataset is None:

        st.warning("Load dataset first")

    else:

        df=st.session_state.dataset

        st.subheader("Mutation Summary")

        st.dataframe(df.head())

        if "selected_gene" in st.session_state:

            st.subheader("Selected Gene")

            st.write(st.session_state.selected_gene)

        if st.session_state.therapy:

            st.subheader("Recommended Therapy")

            st.write(st.session_state.therapy)

        if st.session_state.trials is not None:

            st.subheader("Relevant Clinical Trials")

            st.dataframe(st.session_state.trials.head())

# --------------------------------------------------------
# ABOUT
# --------------------------------------------------------

if menu=="About Platform":

    st.title("PharmaTab AI Oncology Platform")

    st.markdown("""
### Precision Oncology Simulation Platform

PharmaTab is an AI-assisted computational oncology platform designed to help researchers
and clinicians analyze cancer genomic mutations and translate them into therapeutic insights.

The system integrates multiple modules used in modern precision oncology pipelines.

### Core Capabilities

**1️⃣ Genomic Mutation Analysis**

Analyze tumor mutation datasets from TCGA and other public repositories.
Identify frequently mutated genes and visualize mutation patterns.

**2️⃣ Therapy Recommendation Engine**

Map detected mutations to known targeted therapies using curated drug-gene relationships.

**3️⃣ Clinical Trial Discovery**

Automatically search ClinicalTrials.gov to identify ongoing trials relevant to a patient’s
cancer type or molecular profile.

**4️⃣ Survival Prediction Modeling**

Machine learning models estimate survival probabilities based on clinical variables.

**5️⃣ Automated Clinical Reporting**

Generate structured oncology reports summarizing mutations, potential therapies,
and relevant clinical trials.

### Intended Use

PharmaTab is designed for **research and hypothesis generation** in computational oncology,
supporting translational cancer research workflows.

""")
    
if menu=="Clinical Report":

    st.header("Clinical Oncology Report")

    st.markdown("""
        Generate a structured report summarizing genomic findings and therapeutic insights.
    """)

    if "dataset" not in st.session_state:

        st.warning("Load dataset first")

    else:

        df=st.session_state.dataset

        st.subheader("Mutation Summary")

        st.write(df.head())

        st.subheader("Mutation Frequency")

        gene_counts=df["geneSymbol"].value_counts().head(10)

        st.bar_chart(gene_counts)

        st.subheader("Therapy Recommendation")

        st.markdown("""
        Based on detected mutations, targeted therapies and relevant clinical trials
        can be explored for research purposes.
        """)

        st.success("Report Ready for Export")    
    
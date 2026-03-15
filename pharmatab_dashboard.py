import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import networkx as nx
from io import BytesIO


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
from clinical.therapy_engine import TherapyEngine
from analysis.survival_analysis import SurvivalAnalysis
from analysis.gene_drug_network import GeneDrugNetwork
from analysis.mutation_heatmap import MutationHeatmap

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from utils.pdf_exporter import PDFExporter

# -------------------------------------------------------
# GENE DRUG PATHWAY
# ------------------------------------------------------
gene_network_data = {

    "TP53": {
        "drug": "APR-246",
        "pathway": "p53 signaling"
    },

    "EGFR": {
        "drug": "Gefitinib",
        "pathway": "RTK/RAS/MAPK"
    },

    "KRAS": {
        "drug": "Sotorasib",
        "pathway": "RAS/MAPK"
    },

    "PIK3CA": {
        "drug": "Alpelisib",
        "pathway": "PI3K/AKT"
    },

    "BRCA1": {
        "drug": "Olaparib",
        "pathway": "DNA repair"
    },

    "BRCA2": {
        "drug": "Olaparib",
        "pathway": "DNA repair"
    }

}

def build_gene_drug_network(mutations):

        G = nx.Graph()

        for gene in mutations:

         if gene in gene_network_data:

            drug = gene_network_data[gene]["drug"]
            pathway = gene_network_data[gene]["pathway"]

            G.add_node(gene)
            G.add_node(drug)
            G.add_node(pathway, type="pathway")

            G.add_edge(gene, drug)
            G.add_edge(gene, pathway)
            
            return G
    
        fig, ax = plt.subplots()
        pos = nx.spring_layout(G)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=3000,
            node_color="lightblue",
            font_size=10,
            ax=ax
        )       
        st.pyplot(fig)

        network_buffer = BytesIO()
        fig.savefig(network_buffer, format="png")
        network_buffer.seek(0)
        st.session_state.network_plot = network_buffer

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
background-color: #f5f7fb;
}

h1,h2,h3{
color:#111111;
}

section[data-testid="stSidebar"]{
background-color:#ffffff;
}

.block-container{
background-color:#ffffff;
padding:2rem;
border-radius:10px;
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
st.sidebar.title("PharmaTab Navigation")

page = st.sidebar.radio(
    "Navigation",
    [
        "About Platform",
        "Load Public Dataset",
        "Upload Patient Data",
        "Mutation Explorer",
        "Mutation Heatmap + Drug Gene Network",
        "Therapy Recommendation",
        "Survival Prediction",
        "Clinical Trials",
        "Survival Analysis",
        "Clinical Report",
        "Export Report"
    ]
)

# --------------------------------------------------------
# ABOUT
# --------------------------------------------------------

if page == "About Platform":

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

if page=="Home":

    st.header("Precision Oncology Research Platform")

    st.markdown("""
    # 🧬 PharmaTab AI Oncology Platform

    ### Computational Platform for Mutation-Driven Therapy Discovery
    """)

    st.markdown("""
    PharmaTab integrates genomic mutation analysis, therapy mapping,
    clinical trial discovery and survival modeling into a unified
    precision oncology research platform.
    """)

# -------------------------------
# DATASET LOADER
# -------------------------------

if page == "Load Public Dataset":

    st.header("Load Cancer Mutation Dataset")

    option = st.radio(
        "Choose dataset source",
        [
            "Upload TCGA Dataset",
            "Fetch From cBioPortal"
        ]
    )

    # --------------------------------
    # OPTION 1: Upload TCGA dataset
    # --------------------------------

    if option == "Upload TCGA Dataset":

        uploaded_file = st.file_uploader(
            "Upload TCGA mutation dataset (CSV / TSV)",
            type=["csv", "tsv"]
        )

        if uploaded_file is not None:

            try:

                df = pd.read_csv(uploaded_file, sep="\t")

                if "Hugo_Symbol" in df.columns:
                    df["geneSymbol"] = df["Hugo_Symbol"]
                    mutated_genes = df["geneSymbol"].unique()
                    G = build_gene_drug_network(mutated_genes)  

                st.session_state.dataset = df

                st.success("Dataset uploaded successfully")

                st.dataframe(df.head())

            except:

                st.error("Dataset format not supported")
    

    # --------------------------------
    # OPTION 2: Fetch from cBioPortal
    # --------------------------------

    if option == "Fetch From cBioPortal":

        if st.button("Load Data From cBioPortal"):

            try:

                url = "https://www.cbioportal.org/api/mutations"

                params = {
                    "molecularProfileId": "brca_tcga_mutations",
                    "sampleListId": "brca_tcga_all",
                    "projection": "DETAILED"
                }

                headers = {
                    "Accept": "application/json"
                }

                response = requests.get(url, params=params, headers=headers)

                if response.status_code != 200:

                    st.error("cBioPortal API failed")

                else:

                    data = response.json()

                    df = pd.DataFrame(data)

                    if df.empty:

                        st.error("No data returned from cBioPortal")

                    else:

                        st.session_state.dataset = df

                        st.success("Dataset loaded from cBioPortal")

                        st.dataframe(df.head())

            except Exception as e:

                st.error("Failed to fetch data")

                st.info(
                    "Mutation datasets can be uploaded directly or retrieved from cBioPortal."
                )

# --------------------------------------------------------
# UPLOAD DATA
# --------------------------------------------------------

if page=="Upload Patient Data":

    st.header("Upload Mutation Dataset")

uploaded_file = st.file_uploader(
    "Upload CSV / TSV / TXT mutation dataset",
    type=["csv","tsv","txt"]
)

if uploaded_file is not None:

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_csv(uploaded_file, sep="\t")

        # TCGA column fix
        if "Hugo_Symbol" in df.columns:
            df["geneSymbol"] = df["Hugo_Symbol"]
            mutated_genes = df["geneSymbol"].unique()

            G = build_gene_drug_network(mutated_genes)

        st.session_state.dataset = df

        st.success("Dataset loaded successfully")

        st.dataframe(df.head())

    except Exception as e:

        st.error("Dataset loading failed")

        st.write(e)


    if page == "Mutation Explorer":

        st.header("Mutation Explorer")

    df = st.session_state.get("dataset")

    if df is None:

        st.warning("Load dataset first")

    else:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Dataset Preview")

            st.dataframe(df.head())

        with col2:

            st.subheader("Mutation Frequency")

            gene_counts = df["geneSymbol"].value_counts().head(10)

            st.bar_chart(gene_counts) 


# --------------------------------------------------------
# MUTATION ANALYSIS
# --------------------------------------------------------

if page=="Mutation Analysis":

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

    if page=="Clinical Trials":

        st.header("Clinical Trial Finder")

        gene = st.text_input("Enter Gene")

    if gene:

        matcher = TrialMatcher()

        trials = matcher.search_trials(gene)

        st.dataframe(trials)  

# ----------------------------
# MUTATION HEATMAP + GENE NETWORK
# ----------------------------

if page == "Mutation Heatmap":

    st.header("Genomic Mutation Analysis")

    df = st.session_state.get("dataset")

    if df is None:

        st.warning("Load dataset first")

    else:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Mutation Heatmap")

            heat = MutationHeatmap()

            fig = heat.plot(df)

            st.pyplot(fig)

        with col2:

            st.subheader("Gene–Drug Network")

            network = GeneDrugNetwork()

            fig2 = network.build()

            st.pyplot(fig2)

    mutation_buffer = BytesIO()

    fig.savefig(mutation_buffer, format="png")

    mutation_buffer.seek(0)

    st.session_state.mutation_plot = mutation_buffer

    network_buffer = BytesIO()

    fig.savefig(network_buffer, format="png")

    network_buffer.seek(0)

    st.session_state.network_plot = network_buffer        


# -----------------------------
# THERAPY RECOMMENDATION
# -----------------------------

if page == "Therapy Recommendation":

    st.header("AI Therapy Recommendation")

    df = st.session_state.get("dataset")

    if df is None:

        st.warning("Load dataset first")

    else:

        engine = TherapyEngine()

        therapy_df = engine.recommend(df)

        if therapy_df is None:

            st.info("No known therapy matches found")

        else:

            st.success("Therapy recommendations generated")

            st.dataframe(therapy_df)

            st.subheader("Clinical Interpretation")

            for _, row in therapy_df.iterrows():

                st.markdown(
                    f"""
                    **Gene:** {row['Gene']}  
                    **Recommended Therapy:** {row['Recommended Therapy']}  
                    **Mechanism:** {row['Therapy Type']}
                    """
                )

# --------------------------------------------------------
# TUMOR SIMULATION
# --------------------------------------------------------

if page=="Tumor Simulation":

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

        tumor_buffer = BytesIO()
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
        st.session_state.therapy_table = therapy_df
        st.dataframe(cohort_results.head())

# --------------------------------------------------------
# SURVIVAL ANALYSIS
# --------------------------------------------------------

if page=="Survival Analysis":

    if st.session_state.dataset is None:

        st.warning("Load dataset first")

    else:

        st.header("Kaplan-Meier Survival Analysis")
        import io

        km=KaplanMeierSurvival()

        km_fig=km.run_analysis(
        st.session_state.dataset
        )
        
        st. pyplot(km_fig)

        survival_buffer = BytesIO()

        km_fig.savefig(survival_buffer, format="png")

        survival_buffer.seek(0)

        st.session_state.survival_plot = survival_buffer       

# -------------------------------------------------------
# SURVIVAL PREDICTION
# -------------------------------------------------------

if page=="Survival Prediction":

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

if page=="Clinical Trials":

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

if page == "Clinical Report":

    st.header("Clinical Oncology Report")

    df = st.session_state.get("dataset")

    if df is None:

        st.warning("Load dataset first")

    else:

        st.subheader("Mutation Summary")

        st.dataframe(df.head())

        st.subheader("Top Mutated Genes")

        gene_counts = df["geneSymbol"].value_counts().head(10)

        st.bar_chart(gene_counts)

        st.subheader("Clinical Interpretation")

        st.markdown("""
        Detected mutations indicate potential activation of oncogenic pathways.
        Targeted therapies and ongoing clinical trials should be evaluated
        to determine optimal treatment strategies.
        """)

# -----------------------------------
# PDF REPORT GENERATOR
# -----------------------------------

def generate_pdf_report():

    buffer = BytesIO()

    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(
        Paragraph(
            "PharmaTab AI Oncology Analysis Report",
            styles['Title']
        )
    )

    elements.append(Spacer(1,20))

    # Intro paragraph
    intro = """
    PharmaTab AI Oncology Platform performs genomic mutation analysis,
    therapy recommendation mapping, and survival prediction modeling.
    This report summarizes the computational analysis performed on the
    uploaded patient mutation dataset.
    """

    elements.append(Paragraph(intro, styles['BodyText']))
    elements.append(Spacer(1,20))

    # ----------------------------
    # Mutation Plot
    # ----------------------------

    if "mutation_plot" in st.session_state:

        elements.append(
            Paragraph("Mutation Frequency Analysis", styles['Heading2'])
        )

        img = Image(
            st.session_state.mutation_plot,
            width=5*inch,
            height=3*inch
        )

        elements.append(img)
        elements.append(Spacer(1,20))

    # ----------------------------
    # Survival Plot
    # ----------------------------

    if "survival_plot" in st.session_state:

        elements.append(
            Paragraph("Patient Survival Prediction", styles['Heading2'])
        )

        img = Image(
            st.session_state.survival_plot,
            width=5*inch,
            height=3*inch
        )

        elements.append(img)
        elements.append(Spacer(1,20))

    # ----------------------------
    # Gene Drug Network
    # ----------------------------

    if "network_plot" in st.session_state:

        elements.append(
            Paragraph("Gene Drug Interaction Network", styles['Heading2'])
        )

        img = Image(
            st.session_state.network_plot,
            width=5*inch,
            height=4*inch
        )

        elements.append(img)
        elements.append(Spacer(1,20))

    # ----------------------------
    # Therapy Table
    # ----------------------------

    if "therapy_table" in st.session_state:

        elements.append(
            Paragraph("Therapy Recommendations", styles['Heading2'])
        )

        data = st.session_state.therapy_table

        table_data = [data.columns.tolist()] + data.values.tolist()

        table = Table(table_data)

        elements.append(table)

    # ----------------------------
    # Build PDF
    # ----------------------------

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    doc.build(elements)

    buffer.seek(0)

    return buffer




# -------------------------------
# EXPORT REPORT
# -------------------------------

if page == "Export Report":

    st.header("Export Oncology Analysis Report")

    if st.button("Generate PDF Report"):

        pdf = generate_pdf_report()

        st.download_button(
            label="Download PDF",
            data=pdf,
            file_name="pharmatab_report.pdf",
            mime="application/pdf"
        )
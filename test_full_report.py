from ai.treatment_plan_generator import TreatmentPlanGenerator
from utils.pdf_exporter import PDFExporter
from simulation.tumor_evolution_engine import TumorEvolutionEngine


mutations = ["BRAF", "NRAS", "HRAS"]

therapies = [

    ("Dabrafenib + Trametinib", "BRAF / MEK", "FDA Approved"),
    ("MEK inhibitors", "NRAS pathway", "Clinical Evidence"),
    ("Tipifarnib", "HRAS", "Clinical Trial")
]


engine = TumorEvolutionEngine()

simulation = engine.simulate()

risk = engine.risk_prediction(simulation)


generator = TreatmentPlanGenerator()

plan = generator.generate_plan(

    mutations,
    therapies,

    cancer_type="Thyroid Papillary Carcinoma",
    patient_id="TCGA-THCA-001",

    age=52,
    sex="Female",
    stage="Stage II"
)


plan = plan + f"""

AI Tumor Evolution Result
--------------------------------------------------

Predicted Risk: {risk}
"""


pdf = PDFExporter()

pdf.export(plan, "tumor_simulation.png")
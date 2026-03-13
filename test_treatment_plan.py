from ai.treatment_plan_generator import TreatmentPlanGenerator
from utils.pdf_exporter import PDFExporter


mutations = [
    "BRAF V600E",
    "NRAS Q61R",
    "HRAS G13R"
]


therapies = [

    ("Dabrafenib + Trametinib", "BRAF / MEK", "FDA Approved"),

    ("MEK inhibitors", "NRAS pathway", "Clinical Evidence"),

    ("Tipifarnib", "HRAS", "Clinical Trial")
]


generator = TreatmentPlanGenerator()

plan = generator.generate_plan(

    mutations=mutations,
    therapies=therapies,

    cancer_type="Thyroid Papillary Carcinoma",
    patient_id="TCGA-THCA-001",

    age=52,
    sex="Female",
    stage="Stage II"
)


pdf = PDFExporter()

pdf.export(plan)
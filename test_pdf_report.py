from ai.treatment_plan_generator import TreatmentPlanGenerator
from utils.pdf_exporter import PDFExporter

mutations = ["BRAF", "NRAS", "HRAS"]

therapies = [
    "Dabrafenib + Trametinib",
    "MEK inhibitors",
    "Tipifarnib"
]

generator = TreatmentPlanGenerator()

plan = generator.generate_plan(mutations, therapies)

pdf = PDFExporter()

pdf.export(plan)
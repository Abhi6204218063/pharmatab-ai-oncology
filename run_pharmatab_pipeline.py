from ai.mutation_therapy_mapper import MutationTherapyMapper
from ai.treatment_plan_generator import TreatmentPlanGenerator
from ai.therapy_optimizer import TherapyOptimizer

from simulation.tumor_evolution_engine import TumorEvolutionEngine
from simulation.digital_patient_twin import DigitalPatientTwin
from simulation.tumor_resistance_engine import TumorResistanceEngine
from simulation.cohort_simulator import DigitalCohortSimulator
from simulation.kalpan_meier_survival import KaplanMeierSurvival
from data_loader.tcga_mutation_loader import TCGAMutationLoader

from utils.pdf_exporter import PDFExporter


print("\nPharmaTab AI Oncology Pipeline Starting...\n")


# =============================
# Step 1 — Load TCGA Mutations
# =============================

loader = TCGAMutationLoader()

mutations = loader.load_mutations(

    file_path="data/data_mutations.txt",

    patient_id="TCGA-DJ-A2PX"

)

print("\nDetected Mutations:", mutations[:10])


# =============================
# Step 2 — Therapy Mapping
# =============================

mapper = MutationTherapyMapper()

therapies = mapper.map_therapies(mutations)

print("\nMapped Therapies:")
print(therapies)


# =============================
# Step 3 — Tumor Evolution
# =============================

tumor_engine = TumorEvolutionEngine()

tumor_result = tumor_engine.simulate()

tumor_risk = tumor_engine.risk_prediction(tumor_result)

print("\nTumor Evolution Risk:", tumor_risk)

#==============================
# Step 4 - Resistance simulation
# =============================

res_engine = TumorResistanceEngine()

sensitive, resistant, total = res_engine.simulate()

resistance_status = res_engine.resistance_risk(resistant)

print("\nResistance Evolution:", resistance_status)

# =============================
# Step 5 - Virtual patient cohort simulation
# =============================

cohort = DigitalCohortSimulator()

mean_growth = cohort.simulate(patients=200)

cohort_risk = cohort.cohort_risk(mean_growth)

print("\nVirtual Cohort Risk:", cohort_risk)

# ===============================
# step 6 - Kaplan-Meier survival simulation
# ===============================

survival = KaplanMeierSurvival()

survival_curve = survival.simulate(patients=200)

survival_status = survival.survival_risk(survival_curve)

print("\nPredicted Survival:", survival_status)


# =============================
# Step 7 — Digital Patient Twin
# =============================

patient = DigitalPatientTwin()

tumor, immune = patient.simulate()

print("\nDigital Patient Twin Simulation Complete")


# =============================
# Step 8 — AI Therapy Optimization
# =============================

optimizer = TherapyOptimizer()

strategy, reduction, resistance = optimizer.find_best_strategy()

print("\nAI Optimized Therapy Strategy:", strategy)


# =============================
# Step 9 — Generate Clinical Plan
# =============================

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

plan += f"""

Resistance Evolution Analysis
--------------------------------------------------

{resistance_status}

Tumor resistance simulation predicts emergence
of drug-resistant clones during therapy.
"""

plan += f"""

Virtual Patient Cohort Simulation
--------------------------------------------------

Cohort Size: 200 virtual patients

Risk Assessment: {cohort_risk}

Population-level tumor evolution simulation
suggests heterogeneous therapy response.
"""

plan += f"""

Kaplan-Meier Survival Prediction
--------------------------------------------------

Predicted Survival Outcome: {survival_status}

AI survival model predicts therapy response
and long-term survival probability.
"""


plan += f"""

AI Therapy Optimization
--------------------------------------------------

Recommended Strategy: {strategy}

Expected Tumor Reduction: {round(reduction*100,2)} %

Resistance Risk: {round(resistance*100,2)} %


Tumor Evolution Risk
--------------------------------------------------

{tumor_risk}
"""


# =============================
# Step 10 — Export PDF
# =============================

pdf = PDFExporter()

pdf.export(plan)

print("\nPharmaTab AI Report Generated: treatment_plan.pdf\n")
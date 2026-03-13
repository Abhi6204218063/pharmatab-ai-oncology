from ai.therapy_mapper import TherapyMapper

driver_genes = [
    "BRAF",
    "NRAS",
    "HRAS"
]

engine = TherapyMapper()

therapy = engine.recommend(driver_genes)

print("\n===== Therapy Recommendations =====")

for gene, drug in therapy.items():
    print(gene, "→", drug)
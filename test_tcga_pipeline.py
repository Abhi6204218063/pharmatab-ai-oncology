import pandas as pd

# -------- Mutation Data --------

mutation_file = "data/data_mutations.txt"

mutations = pd.read_csv(
    mutation_file,
    sep="\t",
    comment="#",
    low_memory=False
)

print("\n===== Mutation Data =====")
print(mutations.head())

print("\nTotal mutation records:", len(mutations))


# -------- Clinical Data --------

clinical_file = "data/thca_tcga_pan_can_atlas_2018_clinical_data.tsv"

clinical = pd.read_csv(
    clinical_file,
    sep="\t",
    comment="#",
    low_memory=False
)

print("\n===== Clinical Data =====")
print(clinical.head())

print("\nTotal clinical records:", len(clinical))
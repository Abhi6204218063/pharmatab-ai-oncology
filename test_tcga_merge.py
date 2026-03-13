import pandas as pd

# load mutation data
mutations = pd.read_csv(
    "data/data_mutations.txt",
    sep="\t",
    comment="#",
    low_memory=False
)

# extract patient ID from tumor barcode
mutations["Patient_ID"] = mutations["Tumor_Sample_Barcode"].str[:12]

# load clinical data
clinical = pd.read_csv(
    "data/thca_tcga_pan_can_atlas_2018_clinical_data.tsv",
    sep="\t",
    comment="#",
    low_memory=False
)

# merge datasets
merged = pd.merge(
    mutations,
    clinical,
    left_on="Patient_ID",
    right_on="Patient ID",
    how="inner"
)

print("\n===== Merged Dataset =====")

print(merged.head())

print("\nTotal merged records:", len(merged))
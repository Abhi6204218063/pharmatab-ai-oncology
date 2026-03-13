import pandas as pd


class TCGAMutationLoader:

    def load_mutations(self, file_path, patient_id):

        df = pd.read_csv(file_path, sep="\t", low_memory=False)

        # filter patient
        patient_df = df[df["Tumor_Sample_Barcode"].str.contains(patient_id)]

        # extract gene symbols
        genes = patient_df["Hugo_Symbol"].dropna().unique()

        return list(genes)
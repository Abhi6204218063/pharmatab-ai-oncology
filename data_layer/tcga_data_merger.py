import pandas as pd


class TCGADataMerger:

    def merge(self, mutations, clinical):

        merged = pd.merge(
            mutations,
            clinical,
            left_on="Tumor_Sample_Barcode",
            right_on="PATIENT_ID",
            how="inner"
        )

        return merged
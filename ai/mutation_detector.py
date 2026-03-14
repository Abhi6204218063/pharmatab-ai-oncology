import pandas as pd


class MutationDetector:

    def detect_mutations(self, df):

        required_cols = [
            "Hugo_Symbol",
            "Variant_Classification",
            "Tumor_Sample_Barcode"
        ]

        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        driver_classes = [
            "Missense_Mutation",
            "Nonsense_Mutation",
            "Frame_Shift_Del",
            "Frame_Shift_Ins"
        ]

        mutations = df[df["Variant_Classification"].isin(driver_classes)]

        return mutations
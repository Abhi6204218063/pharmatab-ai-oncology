"""
PharmaTab Genomic Data Pipeline
Extracts mutation features from cancer datasets
"""

import pandas as pd
import numpy as np


class GenomicPipeline:

    def __init__(self, filepath):

        self.filepath = filepath


    def load_dataset(self):

        data = pd.read_csv(self.filepath)

        return data


    def extract_mutation_features(self, data):

        features = {}

        if "mutation_count" in data.columns:
            features["mutation_count"] = data["mutation_count"]

        if "tumor_stage" in data.columns:
            features["tumor_stage"] = data["tumor_stage"]

        if "gene_expression" in data.columns:
            features["gene_expression"] = data["gene_expression"]

        return pd.DataFrame(features)


    def normalize_features(self, df):

        return (df - df.min()) / (df.max() - df.min())


    def run_pipeline(self):

        data = self.load_dataset()

        features = self.extract_mutation_features(data)

        features = self.normalize_features(features)

        return features
"""
PharmaTab Research Module
Genomic Data Loader

Purpose:
Load and process real cancer genomic datasets
such as TCGA, GEO, or other mutation datasets.
"""

import pandas as pd
import numpy as np


class GenomicDataLoader:

    def __init__(self, dataset_path):

        self.dataset_path = dataset_path


    def load_dataset(self):

        """
        Load genomic dataset
        """

        data = pd.read_csv(self.dataset_path)

        return data


    def extract_mutation_features(self, dataframe):

        """
        Extract useful mutation related features
        """

        features = {}

        if "mutation_count" in dataframe.columns:

            features["mutation_count"] = dataframe["mutation_count"].values

        if "tumor_stage" in dataframe.columns:

            features["tumor_stage"] = dataframe["tumor_stage"].values

        if "gene_expression" in dataframe.columns:

            features["gene_expression"] = dataframe["gene_expression"].values

        return features


    def summarize_dataset(self, dataframe):

        """
        Provide dataset summary statistics
        """

        summary = {

            "samples": len(dataframe),

            "columns": list(dataframe.columns),

            "missing_values": dataframe.isnull().sum().sum()

        }

        return summary


    def normalize_expression(self, expression_values):

        """
        Normalize gene expression data
        """

        expression_values = np.array(expression_values)

        norm = (expression_values - np.min(expression_values)) / \
               (np.max(expression_values) - np.min(expression_values))

        return norm
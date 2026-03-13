"""
PharmaTab
Data Layer - Dataset Loader

Purpose:
Load biological and clinical datasets used in simulation.

Supported formats:
- CSV
- JSON
- Excel
"""

import pandas as pd
import os


class DatasetLoader:

    def __init__(self, data_path: str):

        """
        Parameters
        ----------
        data_path : str
            Path to dataset file
        """

        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Dataset not found: {data_path}")

        self.data_path = data_path

    def load_csv(self):

        """
        Load CSV dataset
        """

        data = pd.read_csv(self.data_path)

        return data

    def load_json(self):

        """
        Load JSON dataset
        """

        data = pd.read_json(self.data_path)

        return data

    def load_excel(self):

        """
        Load Excel dataset
        """

        data = pd.read_excel(self.data_path)

        return data

    def dataset_summary(self, dataframe):

        """
        Basic dataset statistics
        """

        summary = {
            "rows": dataframe.shape[0],
            "columns": dataframe.shape[1],
            "column_names": list(dataframe.columns)
        }

        return summary

    def validate_dataset(self, dataframe):

        """
        Validate dataset integrity
        """

        missing_values = dataframe.isnull().sum().sum()

        return {
            "missing_values": int(missing_values),
            "is_valid": missing_values == 0
        }
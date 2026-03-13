"""
PharmaTab
Data Layer - Data Preprocessing

Purpose:
Prepare biological datasets for simulation and AI models.

Main Tasks:
- missing data handling
- normalization
- feature extraction
- dataset validation
"""

import numpy as np
import pandas as pd


class DataPreprocessor:

    def __init__(self):
        pass


    def remove_missing_rows(self, dataframe):

        """
        Remove rows containing missing values
        """

        cleaned = dataframe.dropna()

        return cleaned


    def fill_missing_values(self, dataframe, method="mean"):

        """
        Fill missing values

        method options:
        - mean
        - median
        - zero
        """

        df = dataframe.copy()

        for column in df.columns:

            if df[column].dtype != "object":

                if method == "mean":
                    df[column].fillna(df[column].mean(), inplace=True)

                elif method == "median":
                    df[column].fillna(df[column].median(), inplace=True)

                elif method == "zero":
                    df[column].fillna(0, inplace=True)

        return df


    def normalize_minmax(self, data):

        """
        Min-Max normalization
        """

        data = np.array(data)

        normalized = (data - np.min(data)) / (np.max(data) - np.min(data))

        return normalized


    def standardize(self, data):

        """
        Standardization (Z-score)
        """

        data = np.array(data)

        standardized = (data - np.mean(data)) / np.std(data)

        return standardized


    def extract_features(self, dataframe, feature_columns):

        """
        Extract specific features from dataset
        """

        return dataframe[feature_columns]


    def create_feature_matrix(self, dataframe):

        """
        Convert dataframe into feature matrix for ML models
        """

        numeric_df = dataframe.select_dtypes(include=["float64", "int64"])

        return numeric_df.values


    def dataset_statistics(self, dataframe):

        """
        Return descriptive statistics
        """

        stats = dataframe.describe()

        return stats


    def detect_outliers(self, dataframe, threshold=3):

        """
        Detect outliers using Z-score
        """

        numeric_df = dataframe.select_dtypes(include=["float64", "int64"])

        z_scores = np.abs((numeric_df - numeric_df.mean()) / numeric_df.std())

        outliers = (z_scores > threshold)

        return outliers
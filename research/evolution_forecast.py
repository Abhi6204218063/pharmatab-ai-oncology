"""
PharmaTab Research Module
Tumor Evolution Forecast Engine
"""

import numpy as np

from sklearn.linear_model import LinearRegression


class EvolutionForecast:

    def __init__(self):

        self.model = LinearRegression()


    def prepare_training_data(self,
                              tumor_history):

        """
        Convert tumor history into training dataset
        """

        X = []
        y = []

        for i in range(len(tumor_history) - 1):

            X.append([tumor_history[i]])

            y.append(tumor_history[i + 1])

        return np.array(X), np.array(y)


    def train(self,
              tumor_history):

        """
        Train forecasting model
        """

        X, y = self.prepare_training_data(tumor_history)

        self.model.fit(X, y)


    def forecast(self,
                 current_tumor,
                 steps=10):

        """
        Predict future tumor size
        """

        predictions = []

        tumor = current_tumor

        for i in range(steps):

            pred = self.model.predict([[tumor]])[0]

            tumor = pred

            predictions.append(tumor)

        return predictions


    def therapy_failure_time(self,
                             tumor_predictions,
                             threshold=1e9):

        """
        Estimate therapy failure time
        """

        for t, size in enumerate(tumor_predictions):

            if size > threshold:

                return {
                    "failure": True,
                    "time_step": t
                }

        return {
            "failure": False
        }
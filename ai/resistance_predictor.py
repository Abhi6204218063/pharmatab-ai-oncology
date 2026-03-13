"""
PharmaTab
AI Layer - Resistance Predictor

Purpose:
Predict emergence of drug resistant tumor populations.

Approach:
Use simple machine learning classification to detect
when resistant population becomes dominant.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression


class ResistancePredictor:

    def __init__(self):

        self.model = LogisticRegression()


    def prepare_training_data(self, sensitive_history, resistant_history):

        """
        Convert simulation history into ML training dataset
        """

        X = []
        y = []

        for s, r in zip(sensitive_history, resistant_history):

            total = s + r

            if total == 0:
                continue

            resistant_fraction = r / total

            X.append([s, r, resistant_fraction])

            if resistant_fraction > 0.5:
                y.append(1)   # resistance dominant
            else:
                y.append(0)

        return np.array(X), np.array(y)


    def train(self, sensitive_history, resistant_history):

        """
        Train ML model
        """

        X, y = self.prepare_training_data(
            sensitive_history,
            resistant_history
        )
        # ensure at least 2 classes exist
        if len(X) > 5 and len(set(y)) > 1:
            self.model.fit(X, y)


    def predict_resistance(self, sensitive, resistant):

        """
        Predict if resistance is dominant
        """

        total = sensitive + resistant

        if total == 0:
            return 0

        resistant_fraction = resistant / total

        X = np.array([[sensitive, resistant, resistant_fraction]])

        prediction = self.model.predict(X)

        return prediction[0]


    def detect_resistance_time(self, sensitive_history, resistant_history):

        """
        Detect time step when resistance becomes dominant
        """

        for t, (s, r) in enumerate(zip(sensitive_history, resistant_history)):

            total = s + r

            if total == 0:
                continue

            if r / total > 0.5:

                return {
                    "resistance_detected": True,
                    "time_step": t,
                    "resistant_fraction": r / total
                }

        return {
            "resistance_detected": False
        }
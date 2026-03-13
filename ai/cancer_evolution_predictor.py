"""
PharmaTab Cancer Evolution AI Predictor
"""

import numpy as np
from sklearn.linear_model import LinearRegression


class CancerEvolutionPredictor:

    def __init__(self):

        self.model = LinearRegression()


    def prepare_training_data(self, tumor_history):

        X = []
        y = []

        for i in range(len(tumor_history) - 1):

            X.append([tumor_history[i]])
            y.append(tumor_history[i + 1])

        return np.array(X), np.array(y)


    def train(self, tumor_history):

        X, y = self.prepare_training_data(tumor_history)

        self.model.fit(X, y)


    def predict_future(self, current_tumor, steps=10):

        predictions = []

        tumor = current_tumor

        for _ in range(steps):

            tumor = self.model.predict([[tumor]])[0]

            predictions.append(tumor)

        return predictions
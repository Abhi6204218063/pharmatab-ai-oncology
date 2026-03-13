"""
PharmaTab Meta Learning Engine
Learns therapy strategies from many simulations
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier


class MetaLearningEngine:

    def __init__(self):

        self.model = RandomForestClassifier(
            n_estimators=100
        )


    def generate_training_data(self,
                               simulations=500):

        """
        create synthetic training data from simulations
        """

        X = []
        y = []

        for _ in range(simulations):

            tumor_size = np.random.uniform(1e6, 1e8)
            immune_level = np.random.uniform(1e5, 1e7)
            resistance = np.random.uniform(0, 1)

            # therapy label
            if resistance > 0.6:
                therapy = 2
            elif tumor_size > 5e7:
                therapy = 1
            else:
                therapy = 0

            X.append([
                tumor_size,
                immune_level,
                resistance
            ])

            y.append(therapy)

        return np.array(X), np.array(y)


    def train(self):

        """
        train meta-learning model
        """

        X, y = self.generate_training_data()

        self.model.fit(X, y)


    def predict_therapy(self,
                        tumor_size,
                        immune_level,
                        resistance):

        """
        predict best therapy option
        """

        X = [[
            tumor_size,
            immune_level,
            resistance
        ]]

        prediction = self.model.predict(X)[0]

        if prediction == 0:
            return "DrugA"

        elif prediction == 1:
            return "DrugB"

        else:
            return "Combination"
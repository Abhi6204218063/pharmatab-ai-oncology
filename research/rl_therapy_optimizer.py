"""
PharmaTab Research Module
Reinforcement Learning Therapy Optimizer
"""

import numpy as np


class RLAgent:

    def __init__(self,
                 learning_rate=0.1,
                 discount_factor=0.9,
                 epsilon=0.1):

        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon

        self.actions = ["LOW_DOSE", "MEDIUM_DOSE", "HIGH_DOSE"]

        self.q_table = {}


    def get_state(self, tumor_size):

        """
        Convert tumor size to discrete state
        """

        if tumor_size < 1e6:
            return "small"

        elif tumor_size < 1e8:
            return "medium"

        else:
            return "large"


    def choose_action(self, state):

        """
        Epsilon-greedy action selection
        """

        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))

        if np.random.rand() < self.epsilon:

            return np.random.choice(self.actions)

        else:

            return self.actions[np.argmax(self.q_table[state])]


    def update_q_table(self,
                       state,
                       action,
                       reward,
                       next_state):

        action_index = self.actions.index(action)

        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(len(self.actions))

        best_next = np.max(self.q_table[next_state])

        current = self.q_table[state][action_index]

        new_value = current + self.lr * (
            reward + self.gamma * best_next - current
        )

        self.q_table[state][action_index] = new_value


class TherapyEnvironment:

    def __init__(self,
                 growth_rate=0.03):

        self.growth_rate = growth_rate


    def step(self,
             tumor_size,
             action):

        """
        Apply therapy dose
        """

        if action == "LOW_DOSE":
            effect = 0.1

        elif action == "MEDIUM_DOSE":
            effect = 0.25

        else:
            effect = 0.4

        tumor_size = tumor_size * (1 - effect)

        tumor_size = tumor_size + self.growth_rate * tumor_size

        reward = -tumor_size

        return tumor_size, reward
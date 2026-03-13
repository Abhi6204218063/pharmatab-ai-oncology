"""
PharmaTab Reinforcement Learning Therapy Optimizer
"""

import numpy as np


class RLTherapyOptimizer:

    def __init__(self):

        # actions = therapy options
        self.actions = ["low_dose", "medium_dose", "high_dose"]

        # Q-table
        self.q_table = {}

        self.learning_rate = 0.1
        self.discount = 0.9
        self.epsilon = 0.2


    def get_state(self, tumor_size):

        if tumor_size < 1e6:
            return "small"

        elif tumor_size < 1e7:
            return "medium"

        else:
            return "large"


    def choose_action(self, state):

        if np.random.rand() < self.epsilon:

            return np.random.choice(self.actions)

        if state not in self.q_table:

            self.q_table[state] = np.zeros(len(self.actions))

        action_index = np.argmax(self.q_table[state])

        return self.actions[action_index]


    def update_q(self, state, action, reward, next_state):

        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))

        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(len(self.actions))

        action_index = self.actions.index(action)

        old_value = self.q_table[state][action_index]

        next_max = np.max(self.q_table[next_state])

        new_value = old_value + self.learning_rate * (
            reward + self.discount * next_max - old_value
        )

        self.q_table[state][action_index] = new_value


    def simulate_environment(self, tumor_size, action):

        # therapy effects
        if action == "low_dose":
            tumor_size *= 0.95

        elif action == "medium_dose":
            tumor_size *= 0.85

        else:
            tumor_size *= 0.70

        tumor_size += tumor_size * 0.03

        reward = -tumor_size

        return tumor_size, reward


    def train(self, episodes=100):

        tumor = 1e7

        for _ in range(episodes):

            state = self.get_state(tumor)

            action = self.choose_action(state)

            next_tumor, reward = self.simulate_environment(tumor, action)

            next_state = self.get_state(next_tumor)

            self.update_q(state, action, reward, next_state)

            tumor = next_tumor


    def recommend(self, tumor_size):

        state = self.get_state(tumor_size)

        if state not in self.q_table:

            return "medium_dose"

        action_index = np.argmax(self.q_table[state])

        return self.actions[action_index]
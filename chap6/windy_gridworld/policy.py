import numpy as np


def epsilon_greedy(Q, state, epsilon):
    row, col = state

    if np.random.rand() < epsilon:
        return np.random.choice(4)
    else:
        values = Q[row, col]
        max_value = max(values)
        greedy_actions = np.where(values == max_value)[0]
        return np.random.choice(greedy_actions)

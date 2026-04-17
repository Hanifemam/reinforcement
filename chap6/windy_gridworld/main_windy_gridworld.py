import matplotlib.pyplot as plt
import numpy as np

from env import WindyGridworldEnv
from control import sarsa
from utils import print_policy

env = WindyGridworldEnv()
Q, steps_per_episode = sarsa(env)

plt.plot(np.cumsum(steps_per_episode), np.arange(1, len(steps_per_episode) + 1))
plt.xlabel("Time steps")
plt.ylabel("Episodes")
plt.title("Windy Gridworld with SARSA")
plt.show()

print_policy(Q, env)

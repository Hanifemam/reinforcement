from collections import defaultdict
from typing import List, Tuple
import random

from env import BlackjackEnv, BlackjackState
from episods import EpisodeGenerator, simple_policy


class OffPolicy:
    def __init__(self) -> None:
        self.ACTIONS = [0, 1]

    def behavior_policy(self, state):
        return random.choice([0, 1])

    def behavior_prob(state, action) -> float:
        return 0.5

    def greedy_action(self, state, Q):
        return 0 if Q[(state, 0)] >= Q[(state, 1)] else 1

    def generate_episode_behavior(self, env, behavior_policy_fn):
        episode = []
        state = env.reset()
        done = False

        while not done:
            action = behavior_policy_fn(state, env.rng)
            next_state, reward, done = env.step(action)
            episode.append((state, action, reward))
            state = next_state

        return episode

    def mc_off_policy_control(self, env, num_episodes: int):
        Q = defaultdict(float)
        C = defaultdict(float)
        target_policy = {}

        for _ in range(num_episodes):
            episode = self.generate_episode_behavior(env, behavior_policy)

            G = 0.0
            W = 1.0

            for t in reversed(range(len(episode))):
                state, action, reward = episode[t]
                G += reward

                sa = (state, action)
                C[sa] += W
                Q[sa] += (W / C[sa]) * (G - Q[sa])

                # improve target policy greedily
                target_policy[state] = self.greedy_action(state, Q)

                # if behavior action differs from greedy target action, stop
                if action != target_policy[state]:
                    break

                W *= 1.0 / self.behavior_prob(state, action)

        return Q, target_policy

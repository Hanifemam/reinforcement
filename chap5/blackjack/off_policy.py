"""Off-policy Monte Carlo control for the Blackjack toy environment.

The original version in this repo had a few bugs:
- actions used integers while the environment expects strings ("hit"/"stick"),
- the behaviour policy signature did not match the generator,
- env.reset()/step return tuples that were unpacked incorrectly,
- and the behaviour policy function was referenced without ``self``.

This file now runs a working off-policy control loop and includes a
lightweight self-test when executed directly.
"""

from collections import defaultdict
from typing import Callable, List, Tuple
import random

from env import BlackjackEnv, BlackjackState


Action = str  # "hit" or "stick"


class OffPolicy:
    def __init__(self) -> None:
        # Keep the action vocabulary in one place; order is stick (0), hit (1)
        self.ACTIONS: List[Action] = ["stick", "hit"]

    def behavior_policy(self, state: BlackjackState, rng) -> Action:
        """Exploring behavior policy: choose uniformly at random."""
        if hasattr(rng, "integers"):
            idx = int(rng.integers(0, 2))
        elif hasattr(rng, "randint"):
            idx = rng.randint(0, 1)
        else:
            idx = random.randint(0, 1)
        return self.ACTIONS[idx]

    def behavior_prob(self, state: BlackjackState, action: Action) -> float:
        # Uniform over two actions
        return 0.5

    def greedy_action(self, state: BlackjackState, Q) -> Action:
        # Prefer "stick" on ties to keep behaviour deterministic.
        q_stick = Q[(state, "stick")]
        q_hit = Q[(state, "hit")]
        return "stick" if q_stick >= q_hit else "hit"

    def generate_episode_behavior(
        self, env: BlackjackEnv, behavior_policy_fn: Callable[[BlackjackState, random.Random], Action]
    ) -> List[Tuple[BlackjackState, Action, int]]:
        episode = []
        state, _ = env.reset()
        done = False

        while not done:
            action = behavior_policy_fn(state, env.rng)
            next_state, reward, done, _ = env.step(action)
            episode.append((state, action, reward))
            state = next_state if next_state is not None else state

        return episode

    def mc_off_policy_control(self, env: BlackjackEnv, num_episodes: int):
        Q = defaultdict(float)
        C = defaultdict(float)
        target_policy = {}

        for _ in range(num_episodes):
            episode = self.generate_episode_behavior(env, self.behavior_policy)

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


if __name__ == "__main__":
    # Quick smoke test so running `python off_policy.py` exercises the code.
    env = BlackjackEnv(seed=0)
    agent = OffPolicy()
    Q, policy = agent.mc_off_policy_control(env, num_episodes=200)

    # Report how many state-action values we touched and show one example.
    print(f"Learned {len(Q)} state-action values over 200 episodes.")
    sample_sa = next(iter(Q.keys()))
    print("Example entry:")
    print(f"  state={sample_sa[0]} | action={sample_sa[1]} | Q={Q[sample_sa]:.3f}")

from collections import defaultdict
from typing import List, Tuple

from env import BlackjackEnv, BlackjackState
from episods import EpisodeGenerator, simple_policy

class MonteCarloPredictor:
    def __init__(self, gamma: float = 1.0):
        self.gamma = gamma
        self.returns_sum = defaultdict(float)
        self.returns_count = defaultdict(int)
        self.V = defaultdict(float)

    def first_visit_update(self, episode: List[Tuple[BlackjackState, str, int]]) -> None:
        pass

    def train(self, episode_generator: EpisodeGenerator, num_episodes: int) -> dict:
        for _ in range(num_episodes):
            episode = episode_generator.generate_episode()
            states_in_episode = [step[0] for step in episode]
            rewards_in_episode = [step[2] for step in episode]
            G = 0
            visited_states = set()
            for t in reversed(range(len(episode))):
                state = states_in_episode[t]
                reward = rewards_in_episode[t]
                G += reward
                if state not in visited_states:
                    visited_states.add(state)
                    self.returns_sum[state] += G
                    self.returns_count[state] += 1
                    self.V[state] = self.returns_sum[state] / self.returns_count[state]
                    
        return self.V


if __name__ == "__main__":
    # Debuggy smoke test: run a handful of episodes and log each MC update.
    env = BlackjackEnv(seed=0)
    generator = EpisodeGenerator(env, simple_policy)
    mc = MonteCarloPredictor(gamma=1.0)

    num_episodes = 5
    for i in range(num_episodes):
        episode = generator.generate_episode()
        print(f"\nEpisode {i + 1}")
        for t, (state, action, reward) in enumerate(episode):
            print(f"  t={t} state={state} action={action} reward={reward}")

        G = 0.0
        visited_states = set()
        for t in reversed(range(len(episode))):
            state, _, reward = episode[t]
            G += reward  # gamma=1.0
            if state not in visited_states:
                visited_states.add(state)
                mc.returns_sum[state] += G
                mc.returns_count[state] += 1
                mc.V[state] = mc.returns_sum[state] / mc.returns_count[state]
                print(
                    f"    update state={state} "
                    f"G={G:.2f} count={mc.returns_count[state]} "
                    f"V={mc.V[state]:.3f}"
                )

    sample_states = [
        BlackjackState(20, 10, False),
        BlackjackState(13, 2, False),
        BlackjackState(18, 7, True),
    ]
    for s in sample_states:
        print(f"\nFinal estimate V({s}) = {mc.V.get(s, 0):.3f}")

from typing import Callable, List, Tuple

from env import BlackjackEnv, BlackjackState


# A policy maps a state to an action string understood by the env: "hit" or "stick".
PlayerPolicy = Callable[[BlackjackState], str]


class EpisodeGenerator:
    def __init__(self, env: BlackjackEnv, policy: PlayerPolicy):
        self.env = env
        self.policy = policy

    def generate_episode(self) -> List[Tuple[BlackjackState, str, int]]:
        """
        Returns a sequence of (state, action, reward).
        Since reward is terminal in blackjack, most rewards will be 0 until the final step.
        """
        episode: List[Tuple[BlackjackState, str, int]] = []
        state, _ = self.env.reset()
        done = False

        while not done:
            action = self.policy(state)
            next_state, reward, done, _ = self.env.step(action)
            episode.append((state, action, reward))
            state = next_state if next_state is not None else state

        return episode


def simple_policy(state: BlackjackState) -> str:
    return "hit" if state.player_sum < 20 else "stick"


env = BlackjackEnv(seed=42)
episode_generator = EpisodeGenerator(env, simple_policy)
if __name__ == "__main__":
    for _ in range(3):
        ep = episode_generator.generate_episode()
        print("Episode:")
        for step in ep:
            print(step)
        print()

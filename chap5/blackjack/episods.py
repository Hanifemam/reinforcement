class EpisodeGenerator:
    def __init__(self, env: BlackjackEnv, policy: PlayerPolicy):
        self.env = env
        self.policy = policy

    def generate_episode(self) -> list[tuple[BlackjackState, str, int]]:
        """
        Returns a sequence of (state, action, reward).
        Since reward is terminal in blackjack, most rewards will be 0
        until the final step.
        """
        pass
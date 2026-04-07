from collections import defaultdict

class MonteCarloPredictor:
    def __init__(self, gamma: float = 1.0):
        self.gamma = gamma
        self.returns_sum = defaultdict(float)
        self.returns_count = defaultdict(int)
        self.V = defaultdict(float)

    def first_visit_update(self, episode: list[tuple[BlackjackState, str, int]]) -> None:
        pass

    def train(self, episode_generator: EpisodeGenerator, num_episodes: int) -> dict:
        pass
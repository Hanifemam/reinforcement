class RandomWalkMRP:
    def __init__(self, n_states=100):
        self.n_states = n_states
        self.states = list(range(self.n_states))
        self.state = None

    def reset(self):
        self.state = self.n_states // 2
        return self.state

    def step(self):
        pass

import random


class RandomWalkMRP:
    def __init__(self, n_states=100):
        self.n_states = n_states
        self.states = list(range(self.n_states))
        self.state = None
        self.ACTIONS = ["l", "r"]

    def reset(self):
        self.state = self.n_states // 2
        return self.state

    def step(self):
        action = random.choice(self.ACTIONS)

        if action == "l":
            self.state -= 1
        else:
            self.state += 1

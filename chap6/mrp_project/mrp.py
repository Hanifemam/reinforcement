import random


class RandomWalkMRP:
    def __init__(self, n_states=100):
        self.n_states = n_states
        self.states = list(range(n_states))
        self.state = None

    def reset(self):
        self.state = self.n_states // 2
        return self.state

    def step(self):
        move = random.choice([-1, 1])
        next_state = self.state + move

        if next_state < 0:
            reward = 0
            done = True
            next_state = "left_terminal"
        elif next_state >= self.n_states:
            reward = 1
            done = True
            next_state = "right_terminal"
        else:
            reward = 0
            done = False

        self.state = next_state if not done else self.state
        return next_state, reward, done

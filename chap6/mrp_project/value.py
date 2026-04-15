from mrp import RandomWalkMRP


class StateValueFunction:
    def __init__(self, states):
        self.V = {s: 0.0 for s in states}

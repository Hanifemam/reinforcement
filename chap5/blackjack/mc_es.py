from collections import defaultdict
from typing import List, Tuple

from env import BlackjackEnv, BlackjackState
from episods import EpisodeGenerator, simple_policy

class MS_ES:
    def __init__(self, gamma: float = 1.0):
        self.ACTIONS = [0, 1]
    
    def init_mc_es(self):
        Q = defaultdict(float)
        returns_sum = defaultdict(float)
        returns_count = defaultdict(float)
        policy = {}
        return Q, returns_sum, returns_count, policy
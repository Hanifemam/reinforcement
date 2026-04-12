from collections import defaultdict
from typing import List, Tuple

from env import BlackjackEnv, BlackjackState
from episods import EpisodeGenerator, simple_policy

class MC_ES:
    def __init__(self, gamma: float = 1.0):
        self.gamma = gamma
        self.ACTIONS = [0, 1]
    
    def init_mc_es(self):
        Q = defaultdict(float)
        returns_sum = defaultdict(float)
        returns_count = defaultdict(int)
        policy = {}
        return Q, returns_sum, returns_count, policy
    
    def greedy_action(self, state, Q):
        q_stick = Q[(state, 0)]
        q_hit = Q[(state, 1)]
        return 0 if q_stick >= q_hit else 1
    
    def policy_action(self, state, policy):
        return policy.get(state, 1 if state.player_sum < 20 else 0)
    
    def update_q_from_episode(self, episode, Q, returns_sum, returns_count):
        G = 0
        visited_pairs = set()

        for t in reversed(range(len(episode))):
            state, action, reward = episode[t]
            G += reward
            sa = (state, action)

            if sa not in visited_pairs:
                visited_pairs.add(sa)
                returns_sum[sa] += G
                returns_count[sa] += 1
                Q[sa] = returns_sum[sa] / returns_count[sa]
                
    def improve_policy_from_episode(self, episode, policy, Q):
        states_in_episode = {state for state, _, _ in episode}

        for state in states_in_episode:
            policy[state] = self.greedy_action(state, Q)
            
            
    def mc_control_es(self, env: BlackjackEnv, num_episodes: int):
        Q = defaultdict(float)
        returns_sum = defaultdict(float)
        returns_count = defaultdict(int)
        policy = {}

        for _ in range(num_episodes):
            episode = generate_episode_es(env, policy)
            self.update_q_from_episode(episode, Q, returns_sum, returns_count)
            self.improve_policy_from_episode(episode, policy, Q)

        return Q, policy


if __name__ == "__main__":
    # Minimal demonstration of how MS_ES updates Q and policy from an episode.
    agent = MC_ES(gamma=1.0)
    Q, returns_sum, returns_count, policy = agent.init_mc_es()

    # Fabricated one-step episode: state, action (0=stick,1=hit), reward
    demo_state = BlackjackState(player_sum=20, dealer_showing=10, usable_ace=False)
    demo_episode = [(demo_state, 1, 1)]  # chose hit, got +1 reward

    agent.update_q_from_episode(demo_episode, Q, returns_sum, returns_count)
    agent.improve_policy_from_episode(demo_episode, policy, Q)

    print("After one demo episode:")
    print(f"Q[(state, hit)] = {Q[(demo_state, 1)]:.3f}")
    print(f"Visit count = {returns_count[(demo_state, 1)]}")
    print(f"Greedy policy for state -> action {policy[demo_state]} (0=stick, 1=hit)")

from env import BlackjackEnv

class EpisodeGenerator:
    def __init__(self, env: BlackjackEnv, policy: PlayerPolicy):
        self.env = env
        self.policy = policy
        self.STICK = 1
        HIT = 0

    def generate_episode(self) -> list[tuple[BlackjackState, str, int]]:
        """
        Returns a sequence of (state, action, reward).
        Since reward is terminal in blackjack, most rewards will be 0
        until the final step.
        """
        episode = []
        state = self.env.rest()
        done = False
        
        while not done:
            action = self.policy(state)
            next_state, reward, done = self.env.step(action)
            episode.append((state, action, reward))
            state = next_state
            
        return episode

        
    
def simple_policy(state: BlackjackState) -> int:
    return 1 if state.player_sum < 20 else 0

env = BlackjackEnv(seed=42)
episode_generator = EpisodeGenerator(env, simple_policy)
for _ in range(3):
    ep = episode_generator.generate_episode(env, simple_policy)
    print("Episode:")
    for step in ep:
        print(step)
    print()
def main():
    env = BlackjackEnv(seed=42)
    policy = FixedPolicy()
    generator = EpisodeGenerator(env, policy)
    mc = MonteCarloPredictor(gamma=1.0)

    V = mc.train(generator, num_episodes=500000)

    # plot usable ace
    # plot no usable ace
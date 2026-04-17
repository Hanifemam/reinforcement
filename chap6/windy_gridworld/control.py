import numpy as np
from policy import epsilon_greedy


def sarsa(env, num_episodes, alpha, epsilon, gamma):
    Q = np.zeros((env.height, env.width, 4))
    steps_per_episode = []
    for episode in range(num_episodes):
        state = env.reset()
        action = epsilon_greedy(Q, state, epsilon)

        done = False
        steps = 0

        while not done:
            next_state, reward, done = env.step(action)
            steps += 1

            if done:
                td_target = reward
                Q[state[0], state[1], action] += alpha * (
                    td_target - Q[state[0], state[1], action]
                )
            else:
                next_action = epsilon_greedy(Q, next_state, epsilon)
                td_target = (
                    reward + gamma * Q[next_state[0], next_state[1], next_action]
                )
                Q[state[0], state[1], action] += alpha * (
                    td_target - Q[state[0], state[1], action]
                )

                state = next_state
                action = next_action

        steps_per_episode.append(steps)

    return Q, steps_per_episode

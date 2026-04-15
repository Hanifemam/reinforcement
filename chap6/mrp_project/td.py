def td_zero_prediction(mrp, value_function, alpha, gamma, num_episodes):
    V = value_function.V
    for _ in range(num_episodes):
        state = mrp.reset()
        done = False
        while not done:
            next_state, reward, done = mrp.step()

            target = reward
            if not done:
                target += gamma * V[next_state]

            V[state] += alpha * (target - V[state])

            state = next_state

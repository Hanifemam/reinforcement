class WindyGridworldEnv:
    def __init__(self):
        self.height = 7
        self.width = 10
        self.start = (3, 0)
        self.goal = (3, 7)
        self.wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

        self.actions = {
            0: (-1, 0),  # up
            1: (0, 1),  # right
            2: (1, 0),  # down
            3: (0, -1),  # left
        }

        self.state = None

    def restart(self):
        self.state = self.start
        return self.start

    def reset(self):
        return self.restart()

    def step(self, action):
        row, col = self.state
        dr, dc = self.actions[action]

        new_row = row + dr
        new_col = col + dc

        new_row = max(0, min(self.height - 1, new_row))
        new_col = max(0, min(self.width - 1, new_col))

        new_row -= self.wind[new_col]
        new_row = max(0, min(self.height - 1, new_row))

        next_state = (new_row, new_col)
        self.state = next_state

        reward = -1
        done = next_state == self.goal

        return next_state, reward, done

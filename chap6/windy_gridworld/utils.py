def print_policy(policy, env):
    symbols = {0: "U", 1: "R", 2: "D", 3: "L"}

    for r in range(env.height):
        row_symbols = []
        for c in range(env.width):
            if (r, c) == env.start:
                row_symbols.append("S")
            elif (r, c) == env.goal:
                row_symbols.append("G")
            else:
                row_symbols.append(symbols[policy[r, c]])
        print(" ".join(row_symbols))

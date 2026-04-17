from mrp import RandomWalkMRP
from value import StateValueFunction
from td import td_zero_prediction
from utils import (
    compute_true_values_random_walk,
    plot_estimated_vs_true,
    plot_rmse_curve,
    rmse,
)

mrp = RandomWalkMRP(n_states=100)  # assuming this means 5 non-terminal states
value_function = StateValueFunction(mrp.states)

true_values = compute_true_values_random_walk(n_non_terminal_states=mrp.n_states)

rmses = []

for _ in range(100):
    td_zero_prediction(
        mrp=mrp,
        value_function=value_function,
        alpha=0.1,
        gamma=1.0,
        num_episodes=1,
    )

    current_rmse = rmse(
        estimated_values=value_function.V,
        true_values=true_values,
        states=mrp.states,
    )
    rmses.append(current_rmse)

plot_estimated_vs_true(
    estimated_values=value_function.V,
    true_values=true_values,
    states=mrp.states,
    title="Random Walk: Estimated vs True Values",
)

plot_rmse_curve(
    rmses,
    title="Random Walk: TD(0) RMSE",
)

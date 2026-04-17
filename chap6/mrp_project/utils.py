import math
from typing import Dict, Iterable, List, Optional

import matplotlib.pyplot as plt


def _sorted_non_terminal_states(
    states: Iterable[int],
    terminal_states: Optional[Iterable[int]] = None,
) -> List[int]:
    terminal_states = set(terminal_states or [])
    return sorted([s for s in states if s not in terminal_states])


def extract_values_in_state_order(
    value_dict: Dict[int, float],
    states: Iterable[int],
    terminal_states: Optional[Iterable[int]] = None,
) -> List[float]:
    ordered_states = _sorted_non_terminal_states(states, terminal_states)
    return [value_dict[s] for s in ordered_states]


def compute_true_values_random_walk(
    n_non_terminal_states: int,
) -> Dict[int, float]:
    """
    True values for the standard random walk:
    left terminal reward = 0, right terminal reward = 1, gamma = 1.

    This project's `RandomWalkMRP` indexes only non-terminal states:
        0..n_non_terminal_states - 1

    The implicit terminal states live one step outside that range, so the
    standard random-walk true values are linearly spaced as:
        V(s) = (s + 1) / (n_non_terminal_states + 1)
    for s in 0..n_non_terminal_states - 1.
    """
    if n_non_terminal_states <= 0:
        raise ValueError("n_non_terminal_states must be positive")

    scale = n_non_terminal_states + 1
    return {s: (s + 1) / scale for s in range(n_non_terminal_states)}


def rmse(
    estimated_values: Dict[int, float],
    true_values: Dict[int, float],
    states: Iterable[int],
    terminal_states: Optional[Iterable[int]] = None,
) -> float:
    ordered_states = _sorted_non_terminal_states(states, terminal_states)
    errors = [(estimated_values[s] - true_values[s]) ** 2 for s in ordered_states]
    return math.sqrt(sum(errors) / len(errors))


def plot_value_estimates(
    value_dict: Dict[int, float],
    states: Iterable[int],
    terminal_states: Optional[Iterable[int]] = None,
    title: str = "Estimated Value Function",
    xlabel: str = "State",
    ylabel: str = "Estimated value",
    save_path: Optional[str] = None,
    show: bool = True,
):
    ordered_states = _sorted_non_terminal_states(states, terminal_states)
    y = [value_dict[s] for s in ordered_states]

    plt.figure(figsize=(8, 5))
    plt.plot(ordered_states, y, marker="o")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)

    if save_path is not None:
        plt.savefig(save_path, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


def plot_estimated_vs_true(
    estimated_values: Dict[int, float],
    true_values: Dict[int, float],
    states: Iterable[int],
    terminal_states: Optional[Iterable[int]] = None,
    title: str = "Estimated vs True Values",
    xlabel: str = "State",
    ylabel: str = "Value",
    estimated_label: str = "Estimated",
    true_label: str = "True",
    save_path: Optional[str] = None,
    show: bool = True,
):
    ordered_states = _sorted_non_terminal_states(states, terminal_states)
    y_est = [estimated_values[s] for s in ordered_states]
    y_true = [true_values[s] for s in ordered_states]

    plt.figure(figsize=(8, 5))
    plt.plot(ordered_states, y_est, marker="o", label=estimated_label)
    plt.plot(ordered_states, y_true, linestyle="--", marker="x", label=true_label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path is not None:
        plt.savefig(save_path, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


def plot_value_snapshots(
    snapshots: Dict[str, Dict[int, float]],
    states: Iterable[int],
    terminal_states: Optional[Iterable[int]] = None,
    true_values: Optional[Dict[int, float]] = None,
    title: str = "Value Estimates Over Time",
    xlabel: str = "State",
    ylabel: str = "Estimated value",
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    snapshots example:
        {
            "0 episodes": {...},
            "1 episode": {...},
            "10 episodes": {...},
            "100 episodes": {...},
        }
    """
    ordered_states = _sorted_non_terminal_states(states, terminal_states)

    plt.figure(figsize=(8, 5))

    for label, value_dict in snapshots.items():
        y = [value_dict[s] for s in ordered_states]
        plt.plot(ordered_states, y, marker="o", label=label)

    if true_values is not None:
        y_true = [true_values[s] for s in ordered_states]
        plt.plot(
            ordered_states, y_true, linestyle="--", marker="x", label="True values"
        )

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path is not None:
        plt.savefig(save_path, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


def plot_rmse_curve(
    rmses: List[float],
    title: str = "RMSE over Episodes",
    xlabel: str = "Episode",
    ylabel: str = "RMSE",
    label: Optional[str] = None,
    save_path: Optional[str] = None,
    show: bool = True,
):
    x = list(range(1, len(rmses) + 1))

    plt.figure(figsize=(8, 5))
    plt.plot(x, rmses, label=label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if label is not None:
        plt.legend()

    plt.grid(True, alpha=0.3)

    if save_path is not None:
        plt.savefig(save_path, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


def plot_multiple_rmse_curves(
    curves: Dict[str, List[float]],
    title: str = "RMSE Comparison",
    xlabel: str = "Episode",
    ylabel: str = "RMSE",
    save_path: Optional[str] = None,
    show: bool = True,
):
    """
    curves example:
        {
            "TD, alpha=0.1": [...],
            "TD, alpha=0.05": [...],
            "MC, alpha=0.01": [...],
        }
    """
    plt.figure(figsize=(8, 5))

    for label, rmses in curves.items():
        x = list(range(1, len(rmses) + 1))
        plt.plot(x, rmses, label=label)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path is not None:
        plt.savefig(save_path, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()

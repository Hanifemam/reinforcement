from dataclasses import dataclass

@dataclass(frozen=True)
class BlackjackState:
    player_sum: int
    dealer_showing: int
    usable_ace: bool
    
class BlackjackEnv:
    def __init__(self, natural: bool = False, seed: int | None = None):
        pass

    def draw_card(self) -> int:
        pass

    def draw_hand(self) -> list[int]:
        pass

    def usable_ace(self, hand: list[int]) -> bool:
        pass

    def sum_hand(self, hand: list[int]) -> int:
        pass

    def is_bust(self, hand: list[int]) -> bool:
        pass

    def score(self, hand: list[int]) -> int:
        pass

    def dealer_policy(self, dealer_hand: list[int]) -> str:
        pass

    def get_state(self, player_hand: list[int], dealer_hand: list[int]) -> BlackjackState:
        pass

    def reset(self) -> tuple[BlackjackState, dict]:
        """
        Start a new game.
        Return initial state and optional raw info.
        """
        pass

    def step(self, action: str) -> tuple[BlackjackState | None, int, bool, dict]:
        """
        action in {"hit", "stick"}
        Return: next_state, reward, done, info
        """
        pass
from dataclasses import dataclass
import random

# numpy is optional; fall back to Python's random when unavailable.
try:
    import numpy as np  # type: ignore
except ImportError:  # pragma: no cover - allows running without numpy installed
    np = None

@dataclass(frozen=True)
class BlackjackState:
    player_sum: int
    dealer_showing: int
    usable_ace: bool
    

class BlackjackEnv:
    def __init__(self, seed: int, natural: bool = False):
        if np is not None:
            self.rng = np.random.default_rng(seed)
        else:
            self.rng = random.Random(seed)
        self.player_hand = None
        self.dealer_hand = None
        self.natural = natural
        self.seed = seed

    def draw_card(self) -> int:
        possible_cards_dict = {
            "ace": 1, "2": 2, "3": 3,
            "4": 4, "5": 5, "6": 6,
            "7": 7, "8": 8, "9": 9,
            "10": 10, "J": 10, "Q": 10,
            "K": 10
        }
        keys = list(possible_cards_dict.keys())
        if hasattr(self.rng, "choice"):
            card = self.rng.choice(keys)
        else:  # Random objects before 3.11 lack choice; use module-level
            card = random.choice(keys)
        return possible_cards_dict[card]

    def draw_hand(self) -> list[int]:
        hand = []
        hand.append(self.draw_card())
        hand.append(self.draw_card())
        return hand

    def usable_ace(self, hand: list[int]) -> bool:
        usable = (1 in hand) and (sum(hand) + 10 <= 21)
        return usable

    def sum_hand(self, hand: list[int]) -> int:
        if self.usable_ace(hand):
            return sum(hand) + 10
        return sum(hand)

    def is_bust(self, hand: list[int]) -> bool:
        return self.sum_hand(hand) > 21

    def score(self, hand: list[int]) -> int:
        if self.is_bust(hand):
            return 0
        else:
            return self.sum_hand(hand)

    def dealer_policy(self, dealer_hand: list[int]) -> str:
        if self.sum_hand(dealer_hand) < 17:
            return "hit"
        else:
            return "stick"

    def get_state(self, player_hand: list[int], dealer_hand: list[int]) -> BlackjackState:
        return BlackjackState(
            self.sum_hand(player_hand),
            dealer_hand[0],
            self.usable_ace(player_hand)
        )

    def reset(self) -> tuple[BlackjackState, dict]:
        """
        Start a new game.
        Return initial state and optional raw info.
        """
        self.player_hand = self.draw_hand()
        self.dealer_hand = self.draw_hand()

        while self.sum_hand(self.player_hand) < 12:
            self.player_hand.append(self.draw_card())

        return self.get_state(self.player_hand, self.dealer_hand), {}

    def step(self, action: str) -> tuple[BlackjackState | None, int, bool, dict]:
        """
        action in {"hit", "stick"}
        Return: next_state, reward, done, info
        """
        if action == "hit":
            self.player_hand.append(self.draw_card())

            if self.is_bust(self.player_hand):
                return None, -1, True, {}
            else:
                return self.get_state(self.player_hand, self.dealer_hand), 0, False, {}

        elif action == "stick":
            while self.dealer_policy(self.dealer_hand) == "hit":
                self.dealer_hand.append(self.draw_card())

            player_score = self.score(self.player_hand)
            dealer_score = self.score(self.dealer_hand)

            if dealer_score > 21 or player_score > dealer_score:
                return None, 1, True, {}
            elif player_score < dealer_score:
                return None, -1, True, {}
            else:
                return None, 0, True, {}

        else:
            raise ValueError("Action must be 'hit' or 'stick'")
    def set_state(self, state: BlackjackState):
        self.dealer_hand = [state.dealer_showing, self.draw_card()]
        if state.usable_ace:
            other = state.player_sum - 11
            self.player_hand = [1, other]
        else:
            found = False
            for c1 in range(1, 11):
                for c2 in range(1, 11):
                    hand = [c1, c2]
                    if self.sum_hand(hand) == state.player_sum and self.usable_ace(hand) == state.usable_ace:
                        self.player_hand = hand
                        found = True
                        break
                if found:
                    break

            if not found:
                raise ValueError(f"Cannot construct hand for state {state}")
            
    import random

    def random_start_state(self):
        return BlackjackState(
            player_sum=random.randint(12, 21),
            dealer_showing=random.randint(1, 10),
            usable_ace=random.choice([False, True])
        )
        
    def random_start_action(rng):
        if hasattr(rng, "integers"):
            return int(rng.integers(0, 2))
        if hasattr(rng, "randint"):
            return rng.randint(0, 1)
        return random.randint(0, 1)
    
    

from dataclasses import dataclass

@dataclass(frozen=True)
class BlackjackState:
    player_sum: int
    dealer_showing: int
    usable_ace: bool
    

class PlayerPolicy:
    def action(self, state: BlackjackState) -> str:
        raise NotImplementedError
    
class FixedPolicy(PlayerPolicy):
    def action(self, state: BlackjackState) -> str:
        if state.player_sum >= 20:
            return "stick"
        return "hit"
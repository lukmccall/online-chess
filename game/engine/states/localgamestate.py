from piceces import Team

from .basegamestate import BaseGameState
from ..gamemanagers import GameManagerInterface
from ..gamecontrollers import GameController


class LocalGameState(BaseGameState):
    def __init__(self, game_manager: GameManagerInterface):
        super().__init__(game_manager)

        self.white_controller = None
        self.black_controller = None

    def on_state_start(self):
        super().on_state_start()
        self.white_controller = GameController(self.board, Team.WHITE)
        self.black_controller = GameController(self.board, Team.BLACK)

    def get_game_controller(self) -> GameController:
        if self.board.turn() == Team.WHITE:
            return self.white_controller
        return self.black_controller

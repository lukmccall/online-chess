"""
A module containing LocalGameState
"""
from constants import Team

from .basegamestate import BaseGameState
from ..gamemanagers import GameManagerInterface
from ..gamecontrollers import GameController


class LocalGameState(BaseGameState):
    """
    A state where user is playing the local game
    """
    def __init__(self, game_manager: GameManagerInterface):
        super().__init__(game_manager)

        self.white_controller = None
        self.black_controller = None

    def on_state_start(self) -> None:
        super().on_state_start()
        self.white_controller = GameController(self._board, Team.WHITE)
        self.black_controller = GameController(self._board, Team.BLACK)

    def get_game_controller(self) -> GameController:
        if self._board.turn() == Team.WHITE:
            return self.white_controller
        return self.black_controller

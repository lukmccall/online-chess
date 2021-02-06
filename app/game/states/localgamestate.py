"""
A module containing LocalGameState
"""
from typing import Optional, cast
from constants import Team

from .basegamestate import BaseGameState
from ..gamemanagers import GameManagerInterface
from ..gamecontrollers import GameController


class LocalGameState(BaseGameState):
    """
    A state where user is playing the local game
    """
    def __init__(self, game_manager: GameManagerInterface) -> None:
        super().__init__(game_manager)

        self.white_controller: Optional[GameController] = None
        self.black_controller: Optional[GameController] = None

    def on_state_start(self) -> None:
        super().on_state_start()
        self.white_controller = GameController(self.get_board(), Team.WHITE)
        self.black_controller = GameController(self.get_board(), Team.BLACK)

    def get_game_controller(self) -> GameController:
        assert self.white_controller
        assert self.black_controller

        white_controller = cast(GameController, self.white_controller)
        black_controller = cast(GameController, self.black_controller)

        if self.get_board().turn() == Team.WHITE:
            return white_controller
        return black_controller

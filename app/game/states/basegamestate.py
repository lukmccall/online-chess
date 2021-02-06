"""
A module containing base game state
"""
from typing import List
import pygame

from .basestate import BaseState
from .resultstate import ResultState
from ..gamecontrollers import GameController
from ..gamemanagers import GameManagerInterface
from ..boards import Board


class BaseGameState(BaseState):
    """
    A base game state implementation
    """
    def __init__(self, game_manager: GameManagerInterface):
        super().__init__(game_manager)
        self._board = None

    def on_state_exit(self) -> None:
        pass

    def on_state_start(self) -> None:
        self._board = Board(
            self.get_display(),
            self.get_pieces_factory()
        )

    def get_game_controller(self) -> GameController:
        """Gets the instance of the game controller

        Note: this method need to be implemented by all the derived classes

        :returns An GameController instance
        """
        raise NotImplementedError()

    def on_game_loop(self, events: List[pygame.event.Event]) -> None:
        game_controller = self.get_game_controller()

        game_controller.prepare()

        self._board.draw()

        if self._board.is_game_over():
            self._game_manager.change_state(
                ResultState(self._game_manager, self._board)
            )
            return

        game_controller.pipe_events(events)
        game_controller.action()

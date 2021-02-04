from typing import List
import pygame

from .basestate import BaseState
from ..gamecontrollers import GameController
from ..gamemanagers import GameManagerInterface
from ..boards import Board


class BaseGameState(BaseState):
    def __init__(self, game_manager: GameManagerInterface):
        super().__init__(game_manager)
        self.board = None

    def on_state_exit(self):
        pass

    def on_state_start(self):
        self.board = Board(
            self.get_display(),
            self.get_pieces_factory()
        )

    def get_game_controller(self) -> GameController:
        raise NotImplementedError()

    def on_game_loop(self, events: List[pygame.event.Event]):
        game_controller = self.get_game_controller()

        game_controller.prepare()

        self.board.draw()

        if self.board.is_game_over():
            self.game_manager.go_to_main_state()
            return

        game_controller.pipe_events(events)
        game_controller.action()

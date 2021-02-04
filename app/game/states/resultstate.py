import pygame
import chess

from settings import Settings

from .basestate import BaseState
from ..boards import GameBoardInterface
from ..gamemanagers import GameManagerInterface


class ResultState(BaseState):
    def __init__(
            self,
            game_manager:
            GameManagerInterface,
            board: GameBoardInterface
    ):
        super().__init__(game_manager)

        self.board = board
        self.font = pygame.font.Font(pygame.font.get_default_font(), 70)

        self.result = self._get_result()

    def _get_result(self):
        color = self.board.winner()

        if color is None:
            text = "Draw"
        elif color == chess.WHITE:
            text = "White win"
        else:
            text = "Black win"

        return text

    def on_state_exit(self):
        pass

    def on_state_start(self):
        pass

    def draw_game_result(self):
        text = self.font.render(self.result, True, Settings().get_text_color())

        text_position = (
            self.game_manager.window.width / 2 - text.get_width() / 2,
            self.game_manager.window.height / 2 - text.get_height() / 2
        )
        pygame.draw.rect(
            self.get_display(),
            (0, 0, 0),
            pygame.Rect(
                text_position[0] - 20, text_position[1] - 10,
                text.get_width() + 40, text.get_height() + 15
            )
        )
        self.get_display().blit(text, text_position)

    def on_game_loop(self, events: [pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.game_manager.go_to_main_state()
                return

        self.board.draw()
        self.draw_game_result()

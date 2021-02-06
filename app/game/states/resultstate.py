"""
A module containing ResultState
"""
from typing import List
import pygame
import chess

from settings import Settings

from .basestate import BaseState
from ..boards import GameBoardInterface
from ..gamemanagers import GameManagerInterface


class ResultState(BaseState):
    """
    State when the user finish local or multiplayer game with score.
    """
    def __init__(
        self,
        game_manager: GameManagerInterface,
        board: GameBoardInterface
    ) -> None:
        super().__init__(game_manager)

        self._board = board
        self._font = pygame.font.Font(pygame.font.get_default_font(), 70)

        self._result: str = self._get_result()

    def _get_result(self) -> str:
        """Gets string representing game result

        :return: Game result
        """
        color = self._board.winner()

        if color is None:
            text = "Draw"
        elif color == chess.WHITE:  # pyre-ignore[16]
            text = "White win"
        else:
            text = "Black win"

        return text

    def on_state_exit(self) -> None:
        pass

    def on_state_start(self) -> None:
        pass

    def _draw_game_result(self) -> None:
        """Draws message after the game
        """
        text = self._font.render(self._result, True, Settings().get_text_color())

        text_position = (
            self.get_display().get_width() / 2 - text.get_width() / 2,
            self.get_display().get_height() / 2 - text.get_height() / 2
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

    def on_game_loop(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._game_manager.go_to_main_state()
                return

        self._board.draw()
        self._draw_game_result()

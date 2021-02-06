"""
A module that contains the piece sprite implementation
"""
from typing import Tuple
import pygame

from constants import Team


class ChessPieceSprite(pygame.sprite.Sprite):  # pylint: disable=R0903
    """
    Class containing state and image of piece.
    ChessPieceSprite implementing the Sprite class from pygame
    """
    def __init__(
            self,
            image: pygame.Surface,
            position: Tuple[int, int],
            team: Team,
            cell_size: Tuple[int, int]
    ):
        super().__init__()

        self._cell_size = cell_size
        self.image = pygame.transform.smoothscale(image, cell_size)
        self._team = team
        self.rect = self.image.get_rect()

        self._recalculate_rect(position)

    def move_to(self, new_position: Tuple[int, int]) -> None:
        """Moves piece sprite to the new position

        :param new_position: New position
        """
        self._recalculate_rect(new_position)

    def _recalculate_rect(self, position: Tuple[int, int]) -> None:
        """Recalculates the sprite rect according to given position

        :param position: New position
        """
        width, height = self._cell_size

        row, col = position
        top_y = row * height
        top_x = col * width

        # noinspection SpellCheckingInspection
        self.rect.topleft = (top_x, top_y)

    @property
    def team(self) -> Team:
        """Gets piece team

        :return: Team
        """
        return self._team

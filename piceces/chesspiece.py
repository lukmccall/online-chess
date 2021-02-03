import pygame

from enum import Enum


class Team(Enum):
    WHITE = 0
    BLACK = 1


class ChessPiece(pygame.sprite.Sprite):

    def __init__(self, image: pygame.Surface, position, team: Team, cell_size):
        super().__init__()

        self.cell_size = cell_size
        self.image = pygame.transform.smoothscale(image, cell_size)
        self.team = team
        self.rect = self.image.get_rect()

        self._set_rect_according_to_position(position)

    def move_to(self, new_position):
        self._set_rect_according_to_position(new_position)

    def _set_rect_according_to_position(self, position):
        width, height = self.cell_size

        row, col = position
        top_y = row * height
        top_x = col * width

        self.rect.topleft = (top_x, top_y)

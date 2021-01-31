import pygame

from settings import Settings
from enum import Enum


class Team(Enum):
    WHITE = 0
    BLACK = 1


class ChessPiece(pygame.sprite.Sprite):

    def __init__(self, image: pygame.Surface, position, team: Team):
        pygame.sprite.Sprite.__init__(self)
        width, height = Settings().get_cell_size()

        self.image = pygame.transform.smoothscale(image, (width, height))
        self.team = team
        self.position = position
        self.rect = self.image.get_rect()

        self._set_rect_according_to_position()

    def move_to(self, new_position):
        self.position = new_position
        self._set_rect_according_to_position()

    def _set_rect_according_to_position(self):
        width, height = Settings().get_cell_size()

        row, col = self.position
        top_y = row * height
        top_x = col * width

        self.rect.topleft = (top_x, top_y)

    def belongs_to_team(self, team: Team):
        return self.team == team

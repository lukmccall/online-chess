import pygame

from settings import Settings


class ChessPiece(pygame.sprite.Sprite):

    def __init__(self, image: pygame.Surface, position, team):
        pygame.sprite.Sprite.__init__(self)

        width, height = Settings().get_window_size()
        width, height = width // 8, height // 8

        self.image = pygame.transform.smoothscale(image, (width, height))
        self.team = team

        row, col = position
        top_y = row * height
        top_x = col * width

        self.rect = self.image.get_rect()
        self.rect.topleft = (top_x, top_y)

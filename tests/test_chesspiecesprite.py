from unittest import TestCase, mock
import pygame

from constants import Team
from game.piceces import ChessPieceSprite

surface = pygame.surface.Surface((1, 1))
surface.set_at((0, 0), (99, 99, 99))


class TestChessPieceSprite(TestCase):
    def test_if_position_is_set_up_correctly_should_not_change(self):
        piece = ChessPieceSprite(surface, (0, 0), Team.WHITE, (1, 1))

        rect = piece.rect
        x, y = rect.topleft

        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(rect.width, 1)
        self.assertEqual(rect.height, 1)

    def test_if_position_is_set_up_correctly_should_change(self):
        piece = ChessPieceSprite(surface, (2, 3), Team.WHITE, (1, 1))

        rect = piece.rect
        x, y = rect.topleft

        self.assertEqual(x, 3)
        self.assertEqual(y, 2)
        self.assertEqual(rect.width, 1)
        self.assertEqual(rect.height, 1)

    def test_if_position_is_set_up_correctly_should_change_and_scale(self):
        piece = ChessPieceSprite(surface, (2, 3), Team.WHITE, (2, 2))

        rect = piece.rect
        x, y = rect.topleft

        self.assertEqual(x, 6)
        self.assertEqual(y, 4)
        self.assertEqual(rect.width, 2)
        self.assertEqual(rect.height, 2)

    def test_move_to(self):
        piece = ChessPieceSprite(surface, (0, 0), Team.WHITE, (1, 1))

        piece.move_to((2, 3))
        rect = piece.rect
        x, y = rect.topleft

        self.assertEqual(x, 3)
        self.assertEqual(y, 2)
        self.assertEqual(rect.width, 1)
        self.assertEqual(rect.height, 1)

    def test_move_to_same_position(self):
        piece = ChessPieceSprite(surface, (2, 3), Team.WHITE, (1, 1))

        piece.move_to((2, 3))
        rect = piece.rect
        x, y = rect.topleft

        self.assertEqual(x, 3)
        self.assertEqual(y, 2)
        self.assertEqual(rect.width, 1)
        self.assertEqual(rect.height, 1)

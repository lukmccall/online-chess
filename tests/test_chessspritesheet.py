from unittest import TestCase, mock
import pygame

from game.piceces import ChessPieceEnum
from constants import Team
from game.assets import ChessSpriteSheet

pygame.display.init()
pygame.display.set_mode((1, 1))

surface = pygame.surface.Surface((6, 2))
counter = 0
for y in range(2):
    for x in range(6):
        surface.set_at((x, y), (counter, counter, counter))
        counter += 1
        if counter == 6:
            counter = 10


@mock.patch("pygame.image.load", return_value=surface)
class TestChessSpriteSheet(TestCase):
    def test_get_piece_image(self, mocked_pygame_load):
        ss = ChessSpriteSheet("test path")

        mocked_pygame_load.asser_called_with("test path")

        white_king = ss.get_piece_image(ChessPieceEnum.KING, Team.WHITE)
        self.assertEqual(white_king.get_at((0, 0))[0], 0)

        black_king = ss.get_piece_image(ChessPieceEnum.KING, Team.BLACK)
        self.assertEqual(black_king.get_at((0, 0))[0], 10)

        white_knight = ss.get_piece_image(ChessPieceEnum.KNIGHT, Team.WHITE)
        self.assertEqual(white_knight.get_at((0, 0))[0], 3)

        black_knight = ss.get_piece_image(ChessPieceEnum.KNIGHT, Team.BLACK)
        self.assertEqual(black_knight.get_at((0, 0))[0], 13)

    def test_get_all_images(self, mocked_pygame_load):
        ss = ChessSpriteSheet("test path")

        images = ss.get_all_images()

        mocked_pygame_load.asser_called_with("test path")
        self.assertEqual(len(images), 6 * 2)
        pieces = []
        for image in images:
            self.assertEqual(image.get_width(), 1)
            self.assertEqual(image.get_height(), 1)
            pieces.append(image.get_at((0, 0))[0])
        self.assertListEqual(pieces, list(range(6)) + list(range(10, 16)))


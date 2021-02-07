from unittest import TestCase, mock
import pygame

from game.assets import AssetsProvider
from settings import Settings

pygame.display.init()
pygame.display.set_mode((1, 1))

surface = pygame.surface.Surface((1, 1))


class TestAssetsProvider(TestCase):
    @mock.patch("pygame.image.load", return_value=surface)
    def test_check_if_piece_factory_is_created_correctly(self, mocked_pygame_load):
        assets_provider = AssetsProvider()
        factory = assets_provider.get_pieces_factory()

        ss = factory._chess_sprite_sheet

        self.assertIsNotNone(ss)
        mocked_pygame_load.asser_called_once()
        mocked_pygame_load.asser_called_with(Settings().get_chess_assets_path())



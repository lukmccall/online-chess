from unittest import TestCase, mock
from os import path

from settings import Settings


class TestSettings(TestCase):

    def _test_color(self, color):
        self.assertEqual(len(color), 3)
        for c in color:
            self.assertGreaterEqual(c, 0)
            self.assertLessEqual(c, 255)

    def test_get_window_size(self):
        window_size = Settings().get_window_size()
        self.assertEqual(len(window_size), 2)
        for s in window_size:
            self.assertGreater(s, 0)

    def test_get_chess_assets_path(self):
        asset_path = Settings().get_chess_assets_path()
        self.assertTrue(path.exists(asset_path))

    def test_get_light_squares_color(self):
        color = Settings().get_light_squares_color()
        self._test_color(color)

    def test_get_dark_squares_color(self):
        color = Settings().get_dark_squares_color()
        self._test_color(color)

    def test_get_highlights_moves_color(self):
        color = Settings().get_highlights_moves_color()
        self._test_color(color)

    def test_get_highlights_moves_size(self):
        size = Settings().get_highlights_moves_size()
        self.assertGreater(size, 0)

    def test_get_text_color(self):
        color = Settings().get_text_color()
        self._test_color(color)

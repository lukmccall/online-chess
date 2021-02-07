from unittest import TestCase, mock
import pygame

from game.assets import SpriteSheet

pygame.display.init()
pygame.display.set_mode((1, 1))

surface = pygame.surface.Surface((8, 2))
counter = 0
for y in range(2):
    for x in range(8):
        surface.set_at((x, y), (counter, counter, counter))
        counter += 1


@mock.patch("pygame.image.load", return_value=surface)
class TestSpriteSheet(TestCase):
    def test_image_at(self, mocked_pygame_load):
        ss = SpriteSheet("test path")

        image = ss.image_at(pygame.rect.Rect(0, 0, 8, 1))

        mocked_pygame_load.asser_called_with("test path")
        i = 0
        for x_pixel in range(8):
            pixel = image.get_at((x_pixel, 0))
            self.assertEqual(pixel, (i, i, i, 255))
            i += 1

    def test_images(self, mocked_pygame_load):
        ss = SpriteSheet("test path")

        images = ss.images(2, 8)

        mocked_pygame_load.asser_called_with("test path")
        self.assertTrue(len(images) == 8 * 2)

        pixel_colors = []
        for image in images:
            self.assertEqual(image.get_width(), 1)
            self.assertEqual(image.get_height(), 1)
            pixel_colors.append(image.get_at((0, 0))[0])

        pixel_colors.sort()
        self.assertListEqual(pixel_colors, list(range(8 * 2)))

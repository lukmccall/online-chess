"""
This module contains a simple sprite sheet base class.
"""
from typing import List
import pygame


class SpriteSheet:
    """
    A base class which loads and cuts a sprite sheet.
    It's also responsible for converting an image to the proper format.
    """
    def __init__(self, filename: str):
        """Basic constructor, which loads a sprite sheet to the memory

        :param filename: Path to the sprite sheet
        """
        self._img = pygame.image.load(filename)

    def image_at(self, rectangle: pygame.Rect) -> pygame.Surface:
        """Gets image from loaded sprite sheet
        at the provided position

        :param rectangle: The location of wanted image
        :return: A surface with cut image
        """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self._img, (0, 0), rect)
        return image

    def images(self, rows: int, cols: int) -> List[pygame.Surface]:
        """Gets all images

        :param rows: An number of rows
        :param cols: An number of cols
        :return: A list with all images.
        """
        height = self._img.get_height() // rows
        width = self._img.get_width() // cols
        result = []
        for row in range(rows):
            for col in range(cols):
                top_x = col * width
                top_y = row * height

                result.append(self.image_at(pygame.Rect(top_x, top_y, width, height)))

        return result

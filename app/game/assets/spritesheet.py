import pygame


class SpriteSheet:
    def __init__(self, filename):
        self.img = pygame.image.load(filename)

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.img, (0, 0), rect)
        return image

    def images(self, rows, cols):
        height = self.img.get_height() // rows
        width = self.img.get_width() // cols
        result = []
        for row in range(rows):
            for col in range(cols):
                top_x = col * width
                top_y = row * height

                result.append(self.image_at((top_x, top_y, width, height)))

        return result

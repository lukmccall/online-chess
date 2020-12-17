import pygame


class Window:

    def __init__(self, width, height, *, fps=30):
        self.width = width
        self.height = height

        pygame.time.Clock().tick(fps)

        self.game_display = pygame.display.set_mode((width, height))
        self.is_running = False

    def loop(self, fn):
        self.is_running = True

        while self.is_running:
            self.game_display.fill((255, 255, 255))
            fn(self.game_display, pygame.event.get())

            pygame.display.flip()
import pygame


class Window:
    def __init__(self, width, height, *, fps=60):
        self.width = width
        self.height = height

        pygame.time.Clock().tick(fps)
        pygame.init()
        self.game_display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess Online")
        self.is_running = False

    def loop(self, fun):
        self.is_running = True

        while self.is_running:
            self.game_display.fill((255, 255, 255))
            fun(pygame.event.get())

            pygame.display.flip()

    def stop(self):
        self.is_running = False

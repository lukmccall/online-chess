"""
A module which contains the Window class
"""
from typing import List, Callable
import pygame


class Window:
    """
    A abstract representation of the system window.
    Wrapper for the pygame display.
    """

    def __init__(self, width: int, height: int, *, fps: int = 60):
        self._width = width
        self._height = height

        pygame.time.Clock().tick(fps)
        pygame.init()
        self.game_display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Chess Online")
        self._is_running = False

    def loop(self, fun: Callable[[List[pygame.event.Event]], None]) -> None:
        """Game loop

        :param fun: Function which will be called on every frame
        """
        self._is_running = True

        while self._is_running:
            self.game_display.fill((255, 255, 255))
            fun(pygame.event.get())

            pygame.display.flip()

    def stop(self) -> None:
        """Stops the game loop function
        """
        self._is_running = False

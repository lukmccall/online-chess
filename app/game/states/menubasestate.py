"""
A module containing MenuBaseState
"""
from typing import List
import pygame
import pygame_menu

from .basestate import BaseState
from ..gamemanagers import GameManagerInterface


class MenuBaseState(BaseState):
    """
    A base state for all menu related states
    """
    def __init__(self, game_manager: GameManagerInterface) -> None:
        super().__init__(game_manager)
        # pyre-ignore[16]:
        self._menu = pygame_menu.Menu(
            game_manager.get_window().game_display.get_height(),
            game_manager.get_window().game_display.get_width(),
            "Online Chess",
            theme=pygame_menu.themes.THEME_DARK,
            enabled=False
        )

    def on_state_exit(self) -> None:
        self._menu.disable()

    def on_state_start(self) -> None:
        self._menu.enable()

    def on_game_loop(self, events: List[pygame.event.Event]) -> None:
        if self._menu.is_enabled():
            self._menu.update(events)
            if not self._menu.is_enabled():
                return
            self._menu.draw(self.get_display())

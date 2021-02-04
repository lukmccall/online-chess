import pygame

from .basestate import BaseState
from ..gamemanagers import GameManagerInterface


class MenuBaseState(BaseState):
    def __init__(self, game_manger: GameManagerInterface):
        super().__init__(game_manger)
        self.menu = None

    def on_state_exit(self):
        self.menu.disable()

    def on_state_start(self):
        self.menu.enable()

    def on_game_loop(self, events: [pygame.event.Event]):
        if self.menu.is_enabled():
            self.menu.update(events)
            if not self.menu.is_enabled():
                return
            self.menu.draw(self.get_display())
